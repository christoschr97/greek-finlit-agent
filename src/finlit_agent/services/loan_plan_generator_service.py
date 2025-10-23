"""
Loan Plan Generator Service

Generates multiple loan plan options with different parameters.
Creates variations of terms, down payments, and calculates all metrics.
"""

from dataclasses import dataclass
from typing import List, Dict
import uuid


@dataclass
class LoanPlan:
    """Represents a complete loan plan with all details."""
    id: str
    name: str  # Human-readable name (e.g., "Conservative 20-year")
    amount: float  # Loan amount (after down payment)
    term_years: int
    interest_rate: float  # Annual rate as decimal
    down_payment: float  # Down payment amount
    down_payment_percentage: float  # Down payment as percentage
    monthly_payment: float
    total_interest: float
    total_cost: float  # Total amount paid over life of loan
    payment_to_income_ratio: float  # As percentage


class LoanPlanGeneratorService:
    """Service for generating loan plan options."""
    
    # Default interest rates by loan type (annual, as decimal)
    DEFAULT_RATES = {
        "mortgage": 0.035,  # 3.5%
        "personal": 0.07,   # 7%
        "auto": 0.05,       # 5%
        "student": 0.04,    # 4%
        "business": 0.06,   # 6%
        "unknown": 0.06     # 6%
    }
    
    # Standard term options by loan type (in years)
    TERM_OPTIONS = {
        "mortgage": [15, 20, 25, 30],
        "personal": [3, 5, 7],
        "auto": [3, 5, 7],
        "student": [10, 15, 20],
        "business": [5, 10, 15],
        "unknown": [5, 10, 15]
    }
    
    # Down payment options (as percentages)
    DOWN_PAYMENT_OPTIONS = [0.10, 0.15, 0.20]  # 10%, 15%, 20%
    
    def generate_loan_options(
        self,
        total_amount: float,
        loan_type: str,
        monthly_income: float,
        custom_rate: float = None
    ) -> List[LoanPlan]:
        """
        Generate multiple loan plan options with different parameters.
        
        Args:
            total_amount: Total amount needed (before down payment)
            loan_type: Type of loan (mortgage, personal, auto, etc.)
            monthly_income: User's monthly income (for ratio calculation)
            custom_rate: Optional custom interest rate (overrides default)
            
        Returns:
            List of viable loan plans (5-7 options)
        """
        plans: List[LoanPlan] = []
        
        # Get interest rate
        interest_rate = custom_rate if custom_rate is not None else self.DEFAULT_RATES.get(
            loan_type, 
            self.DEFAULT_RATES["unknown"]
        )
        
        # Get term options for this loan type
        term_options = self.TERM_OPTIONS.get(loan_type, self.TERM_OPTIONS["unknown"])
        
        # Generate plans with different term lengths
        for term in term_options:
            # For mortgage and high-value loans, include down payment variations
            if loan_type == "mortgage" and total_amount > 50000:
                for down_pct in self.DOWN_PAYMENT_OPTIONS:
                    plan = self.create_loan_plan(
                        total_amount=total_amount,
                        down_payment_percentage=down_pct,
                        interest_rate=interest_rate,
                        term_years=term,
                        monthly_income=monthly_income
                    )
                    if plan:
                        plans.append(plan)
            else:
                # For other loans, use minimal/no down payment
                plan = self.create_loan_plan(
                    total_amount=total_amount,
                    down_payment_percentage=0.0,
                    interest_rate=interest_rate,
                    term_years=term,
                    monthly_income=monthly_income
                )
                if plan:
                    plans.append(plan)
        
        return plans
    
    def create_loan_plan(
        self,
        total_amount: float,
        down_payment_percentage: float,
        interest_rate: float,
        term_years: int,
        monthly_income: float
    ) -> LoanPlan:
        """
        Create a single loan plan with all calculated details.
        
        Args:
            total_amount: Total amount needed
            down_payment_percentage: Down payment as decimal (e.g., 0.20 for 20%)
            interest_rate: Annual interest rate as decimal
            term_years: Loan term in years
            monthly_income: Monthly income for ratio calculation
            
        Returns:
            Complete LoanPlan object
        """
        # Calculate down payment and loan amount
        down_payment = total_amount * down_payment_percentage
        loan_amount = total_amount - down_payment
        
        if loan_amount <= 0 or term_years <= 0:
            return None
        
        # Calculate monthly payment
        monthly_payment = self._calculate_monthly_payment(
            loan_amount, 
            interest_rate, 
            term_years
        )
        
        # Calculate totals
        total_payments = monthly_payment * term_years * 12
        total_interest = total_payments - loan_amount
        total_cost = total_payments + down_payment
        
        # Calculate payment-to-income ratio
        payment_ratio = (monthly_payment / monthly_income * 100) if monthly_income > 0 else 0
        
        # Generate descriptive name
        name = self._generate_plan_name(term_years, down_payment_percentage, payment_ratio)
        
        return LoanPlan(
            id=str(uuid.uuid4())[:8],
            name=name,
            amount=loan_amount,
            term_years=term_years,
            interest_rate=interest_rate,
            down_payment=down_payment,
            down_payment_percentage=down_payment_percentage * 100,
            monthly_payment=monthly_payment,
            total_interest=total_interest,
            total_cost=total_cost,
            payment_to_income_ratio=payment_ratio
        )
    
    def _calculate_monthly_payment(
        self,
        principal: float,
        annual_rate: float,
        years: int
    ) -> float:
        """Calculate monthly payment using amortization formula."""
        if principal <= 0 or years <= 0:
            return 0.0
        
        if annual_rate == 0:
            return principal / (years * 12)
        
        monthly_rate = annual_rate / 12
        num_payments = years * 12
        
        payment = principal * (
            monthly_rate * (1 + monthly_rate) ** num_payments
        ) / (
            (1 + monthly_rate) ** num_payments - 1
        )
        
        return payment
    
    def _generate_plan_name(
        self,
        term_years: int,
        down_payment_pct: float,
        payment_ratio: float
    ) -> str:
        """
        Generate a descriptive name for the loan plan.
        
        Args:
            term_years: Loan term
            down_payment_pct: Down payment percentage
            payment_ratio: Payment to income ratio
            
        Returns:
            Greek descriptive name
        """
        # Classify by term length
        if term_years <= 10:
            term_desc = "Γρήγορη Αποπληρωμή"
        elif term_years <= 20:
            term_desc = "Ισορροπημένο"
        else:
            term_desc = "Μακροπρόθεσμο"
        
        # Classify by affordability
        if payment_ratio <= 25:
            affordability = "Άνετο"
        elif payment_ratio <= 35:
            affordability = "Μέτριο"
        else:
            affordability = "Απαιτητικό"
        
        # Add down payment info if significant
        if down_payment_pct >= 0.15:
            return f"{term_desc} ({term_years} έτη) - {affordability}"
        else:
            return f"{term_desc} ({term_years} έτη) - {affordability}"
    
    def get_interest_rate(self, loan_type: str) -> float:
        """
        Get default interest rate for a loan type.
        
        Args:
            loan_type: Type of loan
            
        Returns:
            Annual interest rate as decimal
        """
        return self.DEFAULT_RATES.get(loan_type, self.DEFAULT_RATES["unknown"])

