"""
Amortization Service

Calculates detailed payment schedules and breakdowns for loans.
Shows how principal and interest change over the life of the loan.
"""

from dataclasses import dataclass
from typing import List, Literal


@dataclass
class PaymentPeriod:
    """Represents a single payment period in an amortization schedule."""
    period: int  # Month number (1-based)
    payment: float  # Total monthly payment
    principal: float  # Principal portion of payment
    interest: float  # Interest portion of payment
    remaining_balance: float  # Balance after this payment
    cumulative_interest: float  # Total interest paid so far


@dataclass
class AmortizationSchedule:
    """Complete amortization schedule for a loan."""
    loan_amount: float
    interest_rate: float
    term_months: int
    monthly_payment: float
    periods: List[PaymentPeriod]
    total_interest: float
    total_payments: float


@dataclass
class SchedulePoint:
    """Aggregated schedule point for visualization."""
    label: str  # e.g., "Year 1", "Q1 2024"
    period_end: int  # Last month of this period
    principal_paid: float  # Principal paid in this period
    interest_paid: float  # Interest paid in this period
    remaining_balance: float  # Balance at end of period
    cumulative_interest: float  # Total interest paid up to this point


class AmortizationService:
    """Service for calculating loan amortization schedules."""
    
    def calculate_amortization_schedule(
        self,
        loan_amount: float,
        annual_interest_rate: float,
        term_years: int
    ) -> AmortizationSchedule:
        """
        Calculate complete month-by-month amortization schedule.
        
        Args:
            loan_amount: Principal loan amount
            annual_interest_rate: Annual interest rate as decimal (e.g., 0.05 for 5%)
            term_years: Loan term in years
            
        Returns:
            AmortizationSchedule with all payment periods
        """
        if loan_amount <= 0 or term_years <= 0:
            return AmortizationSchedule(
                loan_amount=loan_amount,
                interest_rate=annual_interest_rate,
                term_months=0,
                monthly_payment=0,
                periods=[],
                total_interest=0,
                total_payments=0
            )
        
        monthly_rate = annual_interest_rate / 12
        term_months = term_years * 12
        
        # Calculate monthly payment
        if monthly_rate == 0:
            monthly_payment = loan_amount / term_months
        else:
            monthly_payment = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** term_months
            ) / (
                (1 + monthly_rate) ** term_months - 1
            )
        
        # Calculate each period
        periods: List[PaymentPeriod] = []
        remaining_balance = loan_amount
        cumulative_interest = 0.0
        
        for month in range(1, term_months + 1):
            # Interest for this month
            interest_payment = remaining_balance * monthly_rate
            
            # Principal for this month
            principal_payment = monthly_payment - interest_payment
            
            # Update cumulative interest
            cumulative_interest += interest_payment
            
            # Update remaining balance
            remaining_balance -= principal_payment
            
            # Handle last payment (may be slightly different due to rounding)
            if month == term_months:
                principal_payment += remaining_balance  # Add any remaining balance
                remaining_balance = 0.0
            
            periods.append(PaymentPeriod(
                period=month,
                payment=monthly_payment,
                principal=principal_payment,
                interest=interest_payment,
                remaining_balance=max(0, remaining_balance),
                cumulative_interest=cumulative_interest
            ))
        
        total_payments = monthly_payment * term_months
        total_interest = total_payments - loan_amount
        
        return AmortizationSchedule(
            loan_amount=loan_amount,
            interest_rate=annual_interest_rate,
            term_months=term_months,
            monthly_payment=monthly_payment,
            periods=periods,
            total_interest=total_interest,
            total_payments=total_payments
        )
    
    def get_schedule_summary(
        self,
        schedule: AmortizationSchedule,
        interval: Literal['monthly', 'quarterly', 'yearly'] = 'yearly'
    ) -> List[SchedulePoint]:
        """
        Aggregate amortization schedule into larger intervals for visualization.
        
        Args:
            schedule: Complete amortization schedule
            interval: Aggregation interval ('monthly', 'quarterly', 'yearly')
            
        Returns:
            List of aggregated schedule points
        """
        if not schedule.periods:
            return []
        
        # Determine grouping size
        if interval == 'monthly':
            group_size = 1
        elif interval == 'quarterly':
            group_size = 3
        else:  # yearly
            group_size = 12
        
        summary_points: List[SchedulePoint] = []
        
        for i in range(0, len(schedule.periods), group_size):
            group = schedule.periods[i:i + group_size]
            
            # Calculate aggregates for this period
            principal_paid = sum(p.principal for p in group)
            interest_paid = sum(p.interest for p in group)
            
            # Use last period in group for balance and cumulative
            last_period = group[-1]
            
            # Generate label
            if interval == 'monthly':
                label = f"Month {last_period.period}"
            elif interval == 'quarterly':
                quarter = (last_period.period - 1) // 3 + 1
                label = f"Q{quarter}"
            else:  # yearly
                year = (last_period.period - 1) // 12 + 1
                label = f"Year {year}"
            
            summary_points.append(SchedulePoint(
                label=label,
                period_end=last_period.period,
                principal_paid=principal_paid,
                interest_paid=interest_paid,
                remaining_balance=last_period.remaining_balance,
                cumulative_interest=last_period.cumulative_interest
            ))
        
        return summary_points
    
    def get_payment_breakdown(
        self,
        schedule: AmortizationSchedule,
        period: int = 1
    ) -> dict:
        """
        Get detailed breakdown of a specific payment period.
        
        Args:
            schedule: Amortization schedule
            period: Period number (1-based, default first payment)
            
        Returns:
            Dictionary with payment breakdown details
        """
        if not schedule.periods or period < 1 or period > len(schedule.periods):
            return {
                "period": period,
                "payment": 0,
                "principal": 0,
                "interest": 0,
                "principal_percentage": 0,
                "interest_percentage": 0
            }
        
        payment_period = schedule.periods[period - 1]
        
        principal_pct = (payment_period.principal / payment_period.payment * 100) if payment_period.payment > 0 else 0
        interest_pct = (payment_period.interest / payment_period.payment * 100) if payment_period.payment > 0 else 0
        
        return {
            "period": period,
            "payment": payment_period.payment,
            "principal": payment_period.principal,
            "interest": payment_period.interest,
            "principal_percentage": principal_pct,
            "interest_percentage": interest_pct,
            "remaining_balance": payment_period.remaining_balance
        }

