"""
Tests for Amortization Service.
"""

import pytest
from finlit_agent.services import AmortizationService, PaymentPeriod


@pytest.fixture
def service():
    """Create an AmortizationService instance."""
    return AmortizationService()


def test_calculate_amortization_schedule_basic(service):
    """Test basic amortization schedule calculation."""
    schedule = service.calculate_amortization_schedule(100000, 0.05, 20)
    
    assert schedule.loan_amount == 100000
    assert schedule.interest_rate == 0.05
    assert schedule.term_months == 240
    assert 659 < schedule.monthly_payment < 660
    assert len(schedule.periods) == 240
    assert schedule.total_interest > 0


def test_calculate_amortization_schedule_zero_interest(service):
    """Test amortization with zero interest rate."""
    schedule = service.calculate_amortization_schedule(12000, 0.0, 5)
    
    assert schedule.monthly_payment == 200.0
    assert schedule.total_interest == 0.0


def test_calculate_amortization_schedule_zero_amount(service):
    """Test amortization with zero loan amount."""
    schedule = service.calculate_amortization_schedule(0, 0.05, 20)
    
    assert schedule.monthly_payment == 0.0
    assert len(schedule.periods) == 0


def test_calculate_amortization_schedule_zero_term(service):
    """Test amortization with zero term."""
    schedule = service.calculate_amortization_schedule(100000, 0.05, 0)
    
    assert schedule.monthly_payment == 0.0
    assert len(schedule.periods) == 0


def test_amortization_periods_structure(service):
    """Test that payment periods have correct structure."""
    schedule = service.calculate_amortization_schedule(10000, 0.05, 5)
    
    assert len(schedule.periods) == 60
    
    # Check first period
    first = schedule.periods[0]
    assert first.period == 1
    assert first.payment > 0
    assert first.principal > 0
    assert first.interest > 0
    assert first.remaining_balance > 0


def test_amortization_last_period_zero_balance(service):
    """Test that last period has zero remaining balance."""
    schedule = service.calculate_amortization_schedule(10000, 0.05, 5)
    
    last = schedule.periods[-1]
    assert last.remaining_balance == 0.0


def test_amortization_cumulative_interest_increases(service):
    """Test that cumulative interest increases each period."""
    schedule = service.calculate_amortization_schedule(10000, 0.05, 5)
    
    for i in range(1, len(schedule.periods)):
        assert schedule.periods[i].cumulative_interest > schedule.periods[i-1].cumulative_interest


def test_get_schedule_summary_yearly(service):
    """Test yearly schedule summary."""
    schedule = service.calculate_amortization_schedule(100000, 0.05, 20)
    summary = service.get_schedule_summary(schedule, 'yearly')
    
    assert len(summary) == 20
    assert summary[0].label == "Year 1"
    assert summary[-1].label == "Year 20"


def test_get_schedule_summary_quarterly(service):
    """Test quarterly schedule summary."""
    schedule = service.calculate_amortization_schedule(10000, 0.05, 5)
    summary = service.get_schedule_summary(schedule, 'quarterly')
    
    assert len(summary) == 20  # 5 years * 4 quarters
    assert summary[0].label == "Q1"


def test_get_schedule_summary_monthly(service):
    """Test monthly schedule summary."""
    schedule = service.calculate_amortization_schedule(10000, 0.05, 5)
    summary = service.get_schedule_summary(schedule, 'monthly')
    
    assert len(summary) == 60
    assert summary[0].label == "Month 1"


def test_get_schedule_summary_empty(service):
    """Test schedule summary with empty schedule."""
    schedule = service.calculate_amortization_schedule(0, 0.05, 5)
    summary = service.get_schedule_summary(schedule, 'yearly')
    
    assert len(summary) == 0


def test_get_payment_breakdown_first_payment(service):
    """Test payment breakdown for first payment."""
    # Use longer term loan where first payment has more interest
    schedule = service.calculate_amortization_schedule(100000, 0.05, 30)
    breakdown = service.get_payment_breakdown(schedule, 1)
    
    assert breakdown["period"] == 1
    assert breakdown["payment"] > 0
    assert breakdown["principal"] > 0
    assert breakdown["interest"] > 0
    # First payment of long-term loan should have more interest than principal
    assert breakdown["interest"] > breakdown["principal"]


def test_get_payment_breakdown_last_payment(service):
    """Test payment breakdown for last payment."""
    schedule = service.calculate_amortization_schedule(10000, 0.05, 5)
    breakdown = service.get_payment_breakdown(schedule, 60)
    
    assert breakdown["period"] == 60
    assert breakdown["remaining_balance"] == 0.0
    # Last payment should have more principal than interest
    assert breakdown["principal"] > breakdown["interest"]


def test_get_payment_breakdown_invalid_period(service):
    """Test payment breakdown with invalid period."""
    schedule = service.calculate_amortization_schedule(10000, 0.05, 5)
    breakdown = service.get_payment_breakdown(schedule, 999)
    
    assert breakdown["payment"] == 0
    assert breakdown["principal"] == 0


def test_get_payment_breakdown_percentages(service):
    """Test that payment breakdown percentages sum to ~100."""
    schedule = service.calculate_amortization_schedule(10000, 0.05, 5)
    breakdown = service.get_payment_breakdown(schedule, 30)
    
    total_pct = breakdown["principal_percentage"] + breakdown["interest_percentage"]
    assert 99.9 < total_pct < 100.1

