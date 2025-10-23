"""
Tests for Affordability Service.
"""

import pytest
from finlit_agent.services import AffordabilityService


@pytest.fixture
def service():
    """Create an AffordabilityService instance."""
    return AffordabilityService()


def test_get_affordability_status_safe(service):
    """Test affordability status for safe scenario."""
    status = service.get_affordability_status(
        payment_ratio=25.0,
        disposable_income=1000,
        estimated_payment=500
    )
    
    assert status == "safe"


def test_get_affordability_status_warning_high_ratio(service):
    """Test affordability status with high payment ratio."""
    status = service.get_affordability_status(
        payment_ratio=35.0,
        disposable_income=1000,
        estimated_payment=700
    )
    
    assert status == "warning"


def test_get_affordability_status_danger_no_disposable_income(service):
    """Test affordability status with no disposable income."""
    status = service.get_affordability_status(
        payment_ratio=25.0,
        disposable_income=0,
        estimated_payment=500
    )
    
    assert status == "danger"


def test_get_affordability_status_danger_negative_disposable_income(service):
    """Test affordability status with negative disposable income."""
    status = service.get_affordability_status(
        payment_ratio=25.0,
        disposable_income=-500,
        estimated_payment=500
    )
    
    assert status == "danger"


def test_get_affordability_status_danger_payment_exceeds_disposable(service):
    """Test affordability status when payment exceeds disposable income."""
    status = service.get_affordability_status(
        payment_ratio=25.0,
        disposable_income=400,
        estimated_payment=500
    )
    
    assert status == "danger"


def test_get_affordability_status_danger_very_high_ratio(service):
    """Test affordability status with very high payment ratio."""
    status = service.get_affordability_status(
        payment_ratio=50.0,
        disposable_income=1000,
        estimated_payment=500
    )
    
    assert status == "danger"


def test_generate_recommendations_danger_no_disposable(service):
    """Test recommendations for danger status with no disposable income."""
    financial_data = {
        "monthly_income": 2000,
        "other_income": 0,
        "monthly_expenses": 2500,
        "existing_loans": 0,
        "loan_amount": 10000,
        "savings": 500
    }
    
    metrics = {
        "total_income": 2000,
        "total_expenses": 2500,
        "disposable_income": -500,
        "estimated_payment": 188,
        "payment_ratio": 9.4
    }
    
    recommendations = service.generate_recommendations(financial_data, metrics, "danger")
    
    assert len(recommendations) > 0
    assert any("έξοδά σου ξεπερνούν" in rec for rec in recommendations)


def test_generate_recommendations_danger_high_ratio(service):
    """Test recommendations for danger status with high payment ratio."""
    financial_data = {
        "monthly_income": 1000,
        "other_income": 0,
        "monthly_expenses": 500,
        "existing_loans": 0,
        "loan_amount": 20000,
        "savings": 500
    }
    
    metrics = {
        "total_income": 1000,
        "total_expenses": 500,
        "disposable_income": 500,
        "estimated_payment": 377,
        "payment_ratio": 37.7
    }
    
    recommendations = service.generate_recommendations(financial_data, metrics, "danger")
    
    assert len(recommendations) > 0
    assert any("δόση είναι υψηλή" in rec for rec in recommendations)


def test_generate_recommendations_warning(service):
    """Test recommendations for warning status."""
    financial_data = {
        "monthly_income": 2000,
        "other_income": 0,
        "monthly_expenses": 1200,
        "existing_loans": 0,
        "loan_amount": 15000,
        "savings": 500
    }
    
    metrics = {
        "total_income": 2000,
        "total_expenses": 1200,
        "disposable_income": 800,
        "estimated_payment": 283,
        "payment_ratio": 14.15
    }
    
    recommendations = service.generate_recommendations(financial_data, metrics, "warning")
    
    assert len(recommendations) > 0
    # Should have a warning about being at the limit
    assert any("στο όριο" in rec.lower() for rec in recommendations)


def test_generate_recommendations_safe(service):
    """Test recommendations for safe status."""
    financial_data = {
        "monthly_income": 3000,
        "other_income": 500,
        "monthly_expenses": 1500,
        "existing_loans": 200,
        "loan_amount": 10000,
        "savings": 2000
    }
    
    metrics = {
        "total_income": 3500,
        "total_expenses": 1700,
        "disposable_income": 1800,
        "estimated_payment": 188,
        "payment_ratio": 6.3
    }
    
    recommendations = service.generate_recommendations(financial_data, metrics, "safe")
    
    assert len(recommendations) > 0
    # Should have a positive message
    assert any("Καλά νέα" in rec for rec in recommendations)


def test_generate_recommendations_low_savings(service):
    """Test that low savings generates a recommendation."""
    financial_data = {
        "monthly_income": 3000,
        "other_income": 0,
        "monthly_expenses": 1500,
        "existing_loans": 0,
        "loan_amount": 10000,
        "savings": 500  # Less than 10% of loan amount
    }
    
    metrics = {
        "total_income": 3000,
        "total_expenses": 1500,
        "disposable_income": 1500,
        "estimated_payment": 188,
        "payment_ratio": 6.3
    }
    
    recommendations = service.generate_recommendations(financial_data, metrics, "safe")
    
    # Should recommend having more savings
    assert any("αποταμιεύσεις" in rec for rec in recommendations)


def test_analyze_affordability_complete(service):
    """Test complete affordability analysis."""
    financial_data = {
        "monthly_income": 2500,
        "other_income": 500,
        "monthly_expenses": 1500,
        "existing_loans": 200,
        "loan_amount": 10000,
        "savings": 2000
    }
    
    metrics = {
        "total_income": 3000,
        "total_expenses": 1700,
        "disposable_income": 1300,
        "estimated_payment": 188,
        "payment_ratio": 7.5
    }
    
    analysis = service.analyze_affordability(financial_data, metrics)
    
    assert "status" in analysis
    assert "recommendations" in analysis
    assert "metrics" in analysis
    
    assert analysis["status"] in ["safe", "warning", "danger"]
    assert isinstance(analysis["recommendations"], list)
    assert len(analysis["recommendations"]) > 0
    assert analysis["metrics"] == metrics


def test_affordability_thresholds(service):
    """Test that thresholds are correctly defined."""
    assert service.SAFE_PAYMENT_RATIO == 30.0
    assert service.WARNING_PAYMENT_RATIO == 40.0
    assert service.MINIMUM_SAVINGS_RATIO == 0.1

