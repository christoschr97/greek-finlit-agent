"""
Financial Calculator Service

Provides financial calculations for loans, affordability, and budgeting.
Pure calculation logic without any UI dependencies.
"""

from typing import Dict, Optional


class FinancialCalculatorService:
    """Service for financial calculations."""
    
    def calculate_monthly_payment(
        self, 
        principal: float, 
        annual_rate: float, 
        years: int
    ) -> float:
        """
        Calculate monthly loan payment using the standard amortization formula.
        
        Formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
        Where:
        - M = Monthly payment
        - P = Principal (loan amount)
        - r = Monthly interest rate (annual rate / 12)
        - n = Total number of payments (years * 12)
        
        Args:
            principal: Loan amount in euros
            annual_rate: Annual interest rate as decimal (e.g., 0.05 for 5%)
            years: Loan term in years
            
        Returns:
            Monthly payment amount in euros
        """
        if principal <= 0 or years <= 0:
            return 0.0
        
        if annual_rate == 0:
            # No interest, just divide principal by months
            return principal / (years * 12)
        
        monthly_rate = annual_rate / 12
        num_payments = years * 12
        
        # Amortization formula
        payment = principal * (
            monthly_rate * (1 + monthly_rate) ** num_payments
        ) / (
            (1 + monthly_rate) ** num_payments - 1
        )
        
        return payment
    
    def calculate_total_income(self, monthly_income: float, other_income: float) -> float:
        """
        Calculate total monthly income.
        
        Args:
            monthly_income: Primary monthly income
            other_income: Additional monthly income (rent, dividends, etc.)
            
        Returns:
            Total monthly income
        """
        return monthly_income + other_income
    
    def calculate_total_expenses(
        self, 
        monthly_expenses: float, 
        existing_loans: float
    ) -> float:
        """
        Calculate total monthly expenses.
        
        Args:
            monthly_expenses: Regular living expenses
            existing_loans: Existing loan payments
            
        Returns:
            Total monthly expenses
        """
        return monthly_expenses + existing_loans
    
    def calculate_disposable_income(self, total_income: float, total_expenses: float) -> float:
        """
        Calculate disposable income (income minus expenses).
        
        Args:
            total_income: Total monthly income
            total_expenses: Total monthly expenses
            
        Returns:
            Disposable income (can be negative)
        """
        return total_income - total_expenses
    
    def calculate_payment_ratio(self, payment: float, income: float) -> float:
        """
        Calculate the payment-to-income ratio as a percentage.
        
        Args:
            payment: Monthly loan payment
            income: Monthly income
            
        Returns:
            Ratio as percentage (0-100+)
        """
        if income <= 0:
            return 0.0
        
        return (payment / income) * 100
    
    def calculate_financial_metrics(
        self, 
        financial_data: Dict[str, float],
        loan_type: str = "personal",
        term_years: Optional[int] = None
    ) -> Dict[str, float]:
        """
        Calculate all financial metrics from user's financial data.
        
        Args:
            financial_data: Dictionary with keys:
                - monthly_income: Primary income
                - other_income: Additional income
                - monthly_expenses: Living expenses
                - existing_loans: Current loan payments
                - loan_amount: Desired loan amount
                - savings: Current savings
            loan_type: Type of loan (mortgage, personal, auto, etc.)
            term_years: Loan term in years (if None, uses default for loan type)
                
        Returns:
            Dictionary with calculated metrics:
                - total_income: Sum of all income
                - total_expenses: Sum of all expenses
                - disposable_income: Income minus expenses
                - estimated_payment: Estimated monthly loan payment
                - payment_ratio: Payment as % of income
                - term_years: Loan term used for calculation
                - interest_rate: Interest rate used for calculation
        """
        # Import here to avoid circular dependency
        from finlit_agent.services.loan_information_service import LoanInformationService
        
        # Extract inputs
        monthly_income = financial_data.get("monthly_income", 0)
        other_income = financial_data.get("other_income", 0)
        monthly_expenses = financial_data.get("monthly_expenses", 0)
        existing_loans = financial_data.get("existing_loans", 0)
        loan_amount = financial_data.get("loan_amount", 0)
        
        # Get defaults from LoanInformationService
        loan_info_service = LoanInformationService()
        if term_years is None:
            term_years = loan_info_service.get_default_term(loan_type)
        interest_rate = loan_info_service.get_default_interest_rate(loan_type)
        
        # Calculate metrics
        total_income = self.calculate_total_income(monthly_income, other_income)
        total_expenses = self.calculate_total_expenses(monthly_expenses, existing_loans)
        disposable_income = self.calculate_disposable_income(total_income, total_expenses)
        
        # Estimate payment using loan-type specific defaults
        estimated_payment = self.calculate_monthly_payment(
            principal=loan_amount,
            annual_rate=interest_rate,
            years=term_years
        )
        
        payment_ratio = self.calculate_payment_ratio(estimated_payment, monthly_income)
        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "disposable_income": disposable_income,
            "estimated_payment": estimated_payment,
            "payment_ratio": payment_ratio,
            "term_years": term_years,
            "interest_rate": interest_rate
        }

