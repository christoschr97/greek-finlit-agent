"""
Tests for Loan Plan Generator Service.
"""

import pytest
from finlit_agent.services import LoanPlanGeneratorService, LoanPlan


@pytest.fixture
def service():
    """Create a LoanPlanGeneratorService instance."""
    return LoanPlanGeneratorService()


def test_generate_loan_options_mortgage(service):
    """Test generating mortgage loan options."""
    plans = service.generate_loan_options(
        total_amount=100000,
        loan_type="mortgage",
        monthly_income=3000
    )
    
    assert len(plans) > 0
    assert all(isinstance(p, LoanPlan) for p in plans)
    assert all(p.interest_rate > 0 for p in plans)


def test_generate_loan_options_personal(service):
    """Test generating personal loan options."""
    plans = service.generate_loan_options(
        total_amount=10000,
        loan_type="personal",
        monthly_income=2000
    )
    
    assert len(plans) > 0
    # Personal loans should have shorter terms
    assert all(p.term_years <= 7 for p in plans)


def test_generate_loan_options_auto(service):
    """Test generating auto loan options."""
    plans = service.generate_loan_options(
        total_amount=25000,
        loan_type="auto",
        monthly_income=2500
    )
    
    assert len(plans) > 0
    # Auto loans should have medium terms
    assert all(p.term_years <= 7 for p in plans)


def test_generate_loan_options_custom_rate(service):
    """Test generating options with custom interest rate."""
    custom_rate = 0.04
    plans = service.generate_loan_options(
        total_amount=50000,
        loan_type="mortgage",
        monthly_income=3000,
        custom_rate=custom_rate
    )
    
    assert all(p.interest_rate == custom_rate for p in plans)


def test_generate_loan_options_different_down_payments(service):
    """Test that mortgage options include different down payments."""
    plans = service.generate_loan_options(
        total_amount=100000,
        loan_type="mortgage",
        monthly_income=3000
    )
    
    down_payments = set(p.down_payment_percentage for p in plans)
    assert len(down_payments) > 1  # Should have multiple down payment options


def test_create_loan_plan_basic(service):
    """Test creating a single loan plan."""
    plan = service.create_loan_plan(
        total_amount=100000,
        down_payment_percentage=0.20,
        interest_rate=0.05,
        term_years=20,
        monthly_income=3000
    )
    
    assert plan is not None
    assert plan.amount == 80000  # 100k - 20% down
    assert plan.down_payment == 20000
    assert plan.term_years == 20
    assert plan.monthly_payment > 0
    assert plan.total_interest > 0


def test_create_loan_plan_zero_down_payment(service):
    """Test creating plan with no down payment."""
    plan = service.create_loan_plan(
        total_amount=10000,
        down_payment_percentage=0.0,
        interest_rate=0.07,
        term_years=5,
        monthly_income=2000
    )
    
    assert plan.amount == 10000
    assert plan.down_payment == 0


def test_create_loan_plan_zero_amount_returns_none(service):
    """Test that zero amount returns None."""
    plan = service.create_loan_plan(
        total_amount=0,
        down_payment_percentage=0.0,
        interest_rate=0.05,
        term_years=10,
        monthly_income=2000
    )
    
    assert plan is None


def test_create_loan_plan_zero_term_returns_none(service):
    """Test that zero term returns None."""
    plan = service.create_loan_plan(
        total_amount=10000,
        down_payment_percentage=0.0,
        interest_rate=0.05,
        term_years=0,
        monthly_income=2000
    )
    
    assert plan is None


def test_create_loan_plan_payment_ratio_calculated(service):
    """Test that payment-to-income ratio is calculated."""
    plan = service.create_loan_plan(
        total_amount=100000,
        down_payment_percentage=0.20,
        interest_rate=0.05,
        term_years=20,
        monthly_income=2000
    )
    
    assert plan.payment_to_income_ratio > 0
    assert plan.payment_to_income_ratio == (plan.monthly_payment / 2000 * 100)


def test_create_loan_plan_total_cost_calculated(service):
    """Test that total cost includes down payment."""
    plan = service.create_loan_plan(
        total_amount=100000,
        down_payment_percentage=0.20,
        interest_rate=0.05,
        term_years=20,
        monthly_income=3000
    )
    
    total_payments = plan.monthly_payment * 20 * 12
    expected_total_cost = total_payments + plan.down_payment
    assert abs(plan.total_cost - expected_total_cost) < 1.0


def test_create_loan_plan_has_unique_id(service):
    """Test that each plan has a unique ID."""
    plan1 = service.create_loan_plan(10000, 0.0, 0.05, 5, 2000)
    plan2 = service.create_loan_plan(10000, 0.0, 0.05, 5, 2000)
    
    assert plan1.id != plan2.id


def test_create_loan_plan_has_name(service):
    """Test that plan has a descriptive name."""
    plan = service.create_loan_plan(10000, 0.0, 0.05, 5, 2000)
    
    assert plan.name is not None
    assert len(plan.name) > 0
    assert "έτη" in plan.name  # Should contain "έτη" (years in Greek)


def test_get_interest_rate_mortgage(service):
    """Test getting default mortgage rate."""
    rate = service.get_interest_rate("mortgage")
    assert rate == service.DEFAULT_RATES["mortgage"]


def test_get_interest_rate_unknown_type(service):
    """Test getting rate for unknown loan type."""
    rate = service.get_interest_rate("unknown_type")
    assert rate == service.DEFAULT_RATES["unknown"]


def test_generate_loan_options_variety_of_terms(service):
    """Test that generated plans have variety of terms."""
    plans = service.generate_loan_options(50000, "mortgage", 3000)
    
    terms = set(p.term_years for p in plans)
    assert len(terms) > 1  # Should have multiple term options


def test_loan_plan_calculations_consistent(service):
    """Test that loan calculations are internally consistent."""
    plan = service.create_loan_plan(50000, 0.15, 0.06, 15, 2500)
    
    # Total interest + loan amount should equal total payments
    expected_total_payments = plan.monthly_payment * 15 * 12
    actual_total_payments = plan.amount + plan.total_interest
    
    assert abs(expected_total_payments - actual_total_payments) < 1.0

