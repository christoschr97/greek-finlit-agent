"""
Tests for Financial Calculator Service.
"""

import pytest
from finlit_agent.services import FinancialCalculatorService


@pytest.fixture
def service():
    """Create a FinancialCalculatorService instance."""
    return FinancialCalculatorService()


def test_calculate_monthly_payment_basic(service):
    """Test basic monthly payment calculation."""
    # €10,000 at 5% for 5 years
    payment = service.calculate_monthly_payment(10000, 0.05, 5)
    
    # Expected payment should be around €188.71
    assert 188 < payment < 189


def test_calculate_monthly_payment_zero_interest(service):
    """Test monthly payment with zero interest."""
    # €12,000 at 0% for 5 years = €200/month
    payment = service.calculate_monthly_payment(12000, 0.0, 5)
    
    assert payment == 200.0


def test_calculate_monthly_payment_zero_principal(service):
    """Test monthly payment with zero principal."""
    payment = service.calculate_monthly_payment(0, 0.05, 5)
    
    assert payment == 0.0


def test_calculate_monthly_payment_zero_years(service):
    """Test monthly payment with zero years."""
    payment = service.calculate_monthly_payment(10000, 0.05, 0)
    
    assert payment == 0.0


def test_calculate_total_income(service):
    """Test total income calculation."""
    total = service.calculate_total_income(2000, 500)
    
    assert total == 2500


def test_calculate_total_income_no_other_income(service):
    """Test total income with no other income."""
    total = service.calculate_total_income(2000, 0)
    
    assert total == 2000


def test_calculate_total_expenses(service):
    """Test total expenses calculation."""
    total = service.calculate_total_expenses(1200, 300)
    
    assert total == 1500


def test_calculate_total_expenses_no_loans(service):
    """Test total expenses with no existing loans."""
    total = service.calculate_total_expenses(1200, 0)
    
    assert total == 1200


def test_calculate_disposable_income_positive(service):
    """Test disposable income calculation (positive)."""
    disposable = service.calculate_disposable_income(2500, 1500)
    
    assert disposable == 1000


def test_calculate_disposable_income_negative(service):
    """Test disposable income calculation (negative)."""
    disposable = service.calculate_disposable_income(1500, 2000)
    
    assert disposable == -500


def test_calculate_disposable_income_zero(service):
    """Test disposable income calculation (zero)."""
    disposable = service.calculate_disposable_income(2000, 2000)
    
    assert disposable == 0


def test_calculate_payment_ratio(service):
    """Test payment ratio calculation."""
    ratio = service.calculate_payment_ratio(500, 2000)
    
    assert ratio == 25.0


def test_calculate_payment_ratio_zero_income(service):
    """Test payment ratio with zero income."""
    ratio = service.calculate_payment_ratio(500, 0)
    
    assert ratio == 0.0


def test_calculate_financial_metrics_complete(service):
    """Test complete financial metrics calculation."""
    financial_data = {
        "monthly_income": 2000,
        "other_income": 500,
        "monthly_expenses": 1200,
        "existing_loans": 300,
        "loan_amount": 10000,
        "savings": 2000
    }
    
    metrics = service.calculate_financial_metrics(financial_data)
    
    assert metrics["total_income"] == 2500
    assert metrics["total_expenses"] == 1500
    assert metrics["disposable_income"] == 1000
    assert 188 < metrics["estimated_payment"] < 189
    assert 9 < metrics["payment_ratio"] < 10


def test_calculate_financial_metrics_missing_keys(service):
    """Test financial metrics calculation with missing keys."""
    # Should use 0 as default for missing keys
    financial_data = {
        "monthly_income": 2000,
        "loan_amount": 10000,
    }
    
    metrics = service.calculate_financial_metrics(financial_data)
    
    assert metrics["total_income"] == 2000
    assert metrics["total_expenses"] == 0
    assert metrics["disposable_income"] == 2000


def test_calculate_financial_metrics_empty_dict(service):
    """Test financial metrics calculation with empty dict."""
    metrics = service.calculate_financial_metrics({})
    
    assert metrics["total_income"] == 0
    assert metrics["total_expenses"] == 0
    assert metrics["disposable_income"] == 0
    assert metrics["estimated_payment"] == 0.0
    assert metrics["payment_ratio"] == 0.0

