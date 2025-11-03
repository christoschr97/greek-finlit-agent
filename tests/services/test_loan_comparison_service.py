"""
Tests for Loan Comparison Service.
"""

import pytest
from finlit_agent.services import (
    LoanComparisonService,
    LoanPlanGeneratorService,
    LoanPlan
)


@pytest.fixture
def service():
    """Create a LoanComparisonService instance."""
    return LoanComparisonService()


@pytest.fixture
def sample_plans():
    """Create sample loan plans for testing."""
    generator = LoanPlanGeneratorService()
    return generator.generate_loan_options(100000, "mortgage", 3000)


def test_rank_loan_plans_basic(service, sample_plans):
    """Test basic ranking of loan plans."""
    financial_data = {"monthly_income": 3000}
    ranked = service.rank_loan_plans(sample_plans, financial_data)
    
    assert len(ranked) == len(sample_plans)
    # Should be sorted by score (highest first)
    for i in range(len(ranked) - 1):
        assert ranked[i].score >= ranked[i+1].score


def test_rank_loan_plans_empty_list(service):
    """Test ranking with empty plan list."""
    ranked = service.rank_loan_plans([], {})
    assert len(ranked) == 0


def test_rank_loan_plans_scores_in_range(service, sample_plans):
    """Test that scores are in valid range (0-100)."""
    ranked = service.rank_loan_plans(sample_plans, {})
    
    for rp in ranked:
        assert 0 <= rp.score <= 100
        assert 0 <= rp.affordability_score <= 100
        assert 0 <= rp.cost_score <= 100


def test_rank_loan_plans_has_reasons(service, sample_plans):
    """Test that ranked plans have recommendation reasons."""
    ranked = service.rank_loan_plans(sample_plans, {})
    
    for rp in ranked:
        assert rp.recommendation_reason is not None
        assert len(rp.recommendation_reason) > 0


def test_select_best_plans_returns_two(service, sample_plans):
    """Test selecting top 2 plans."""
    ranked = service.rank_loan_plans(sample_plans, {})
    selected = service.select_best_plans(ranked, count=2)
    
    assert len(selected) == 2


def test_select_best_plans_returns_top_ranked(service, sample_plans):
    """Test that top-ranked plan is always selected."""
    ranked = service.rank_loan_plans(sample_plans, {})
    selected = service.select_best_plans(ranked, count=2)
    
    # First selected should be the top-ranked
    assert selected[0].id == ranked[0].plan.id


def test_select_best_plans_empty_list(service):
    """Test selecting from empty list."""
    selected = service.select_best_plans([], count=2)
    assert len(selected) == 0


def test_select_best_plans_fewer_than_requested(service):
    """Test selecting when fewer plans available than requested."""
    generator = LoanPlanGeneratorService()
    plan = generator.create_loan_plan(10000, 0.0, 0.05, 5, 2000)
    ranked = service.rank_loan_plans([plan], {})
    
    selected = service.select_best_plans(ranked, count=5)
    assert len(selected) == 1


def test_compare_two_plans_basic(service):
    """Test basic comparison between two plans."""
    generator = LoanPlanGeneratorService()
    plan_a = generator.create_loan_plan(100000, 0.20, 0.05, 20, 3000)
    plan_b = generator.create_loan_plan(100000, 0.20, 0.05, 10, 3000)
    
    comparison = service.compare_two_plans(plan_a, plan_b)
    
    assert comparison.plan_a == plan_a
    assert comparison.plan_b == plan_b
    assert comparison.winner in ['a', 'b', 'tie']


def test_compare_two_plans_calculates_differences(service):
    """Test that comparison calculates correct differences."""
    generator = LoanPlanGeneratorService()
    plan_a = generator.create_loan_plan(100000, 0.20, 0.05, 20, 3000)
    plan_b = generator.create_loan_plan(100000, 0.20, 0.05, 10, 3000)
    
    comparison = service.compare_two_plans(plan_a, plan_b)
    
    expected_monthly_diff = plan_b.monthly_payment - plan_a.monthly_payment
    assert abs(comparison.monthly_payment_diff - expected_monthly_diff) < 1.0
    
    assert comparison.term_diff == (plan_b.term_years - plan_a.term_years)


def test_compare_two_plans_has_pros(service):
    """Test that comparison includes pros for each plan."""
    generator = LoanPlanGeneratorService()
    plan_a = generator.create_loan_plan(100000, 0.20, 0.05, 20, 3000)
    plan_b = generator.create_loan_plan(100000, 0.20, 0.05, 10, 3000)
    
    comparison = service.compare_two_plans(plan_a, plan_b)
    
    assert isinstance(comparison.pros_plan_a, list)
    assert isinstance(comparison.pros_plan_b, list)
    assert len(comparison.pros_plan_a) > 0
    assert len(comparison.pros_plan_b) > 0


def test_compare_two_plans_has_recommendation(service):
    """Test that comparison includes overall recommendation."""
    generator = LoanPlanGeneratorService()
    plan_a = generator.create_loan_plan(100000, 0.20, 0.05, 20, 3000)
    plan_b = generator.create_loan_plan(100000, 0.20, 0.05, 10, 3000)
    
    comparison = service.compare_two_plans(plan_a, plan_b)
    
    assert comparison.recommendation is not None
    assert len(comparison.recommendation) > 0


def test_score_affordability_excellent(service):
    """Test affordability scoring for excellent ratio."""
    generator = LoanPlanGeneratorService()
    # Create plan with low payment ratio
    plan = generator.create_loan_plan(50000, 0.20, 0.03, 30, 5000)
    
    score = service._score_affordability(plan)
    assert score > 80  # Should be high score


def test_score_affordability_poor(service):
    """Test affordability scoring for poor ratio."""
    generator = LoanPlanGeneratorService()
    # Create plan with high payment ratio
    plan = generator.create_loan_plan(150000, 0.0, 0.06, 10, 2000)
    
    score = service._score_affordability(plan)
    assert score < 50  # Should be low score


def test_rank_plans_with_preferences_short_term(service, sample_plans):
    """Test ranking with preference for short-term loans."""
    preferences = {"prefer_short_term": True}
    ranked = service.rank_loan_plans(sample_plans, {}, preferences)
    
    # Top ranked should have relatively short term
    assert ranked[0].plan.term_years <= 20


def test_select_best_plans_diversity(service):
    """Test that selected plans offer diversity."""
    generator = LoanPlanGeneratorService()
    plans = generator.generate_loan_options(100000, "mortgage", 3000)
    ranked = service.rank_loan_plans(plans, {})
    
    selected = service.select_best_plans(ranked, count=2)
    
    # Selected plans should have different terms
    if len(selected) == 2:
        assert abs(selected[0].term_years - selected[1].term_years) >= 5


def test_affordability_thresholds_defined(service):
    """Test that affordability thresholds are properly defined."""
    assert service.SAFE_PAYMENT_RATIO == 30.0
    assert service.WARNING_PAYMENT_RATIO == 40.0


def test_scoring_weights_sum_to_one(service):
    """Test that scoring weights sum to approximately 1.0."""
    total_weight = (
        service.AFFORDABILITY_WEIGHT +
        service.COST_WEIGHT +
        service.PAYMENT_WEIGHT +
        service.TERM_WEIGHT +
        service.FLEXIBILITY_WEIGHT
    )
    
    assert 0.99 < total_weight < 1.01

