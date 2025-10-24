"""
Tests for Visualization Data Service.
"""

import pytest
from finlit_agent.services import (
    VisualizationDataService,
    AmortizationService,
    LoanPlanGeneratorService
)


@pytest.fixture
def service():
    """Create a VisualizationDataService instance."""
    return VisualizationDataService()


@pytest.fixture
def sample_schedule():
    """Create a sample amortization schedule."""
    amort = AmortizationService()
    return amort.calculate_amortization_schedule(100000, 0.05, 20)


@pytest.fixture
def sample_plans():
    """Create sample loan plans."""
    generator = LoanPlanGeneratorService()
    return generator.generate_loan_options(100000, "mortgage", 3000)[:2]


def test_prepare_amortization_chart_data_yearly(service, sample_schedule):
    """Test preparing amortization chart data with yearly interval."""
    chart_data = service.prepare_amortization_chart_data(sample_schedule, 'yearly')
    
    assert chart_data.chart_type == "area"
    assert len(chart_data.labels) == 20  # 20 years
    assert len(chart_data.datasets) == 2  # Principal and Interest
    assert chart_data.datasets[0].label == "Κεφάλαιο"
    assert chart_data.datasets[1].label == "Τόκοι"


def test_prepare_amortization_chart_data_quarterly(service, sample_schedule):
    """Test preparing amortization chart data with quarterly interval."""
    chart_data = service.prepare_amortization_chart_data(sample_schedule, 'quarterly')
    
    assert len(chart_data.labels) == 80  # 20 years * 4 quarters
    assert chart_data.chart_type == "area"


def test_prepare_amortization_chart_data_monthly(service, sample_schedule):
    """Test preparing amortization chart data with monthly interval."""
    chart_data = service.prepare_amortization_chart_data(sample_schedule, 'monthly')
    
    assert len(chart_data.labels) == 240  # 20 years * 12 months
    assert chart_data.chart_type == "area"


def test_prepare_balance_chart_data(service, sample_schedule):
    """Test preparing balance over time chart data."""
    chart_data = service.prepare_balance_chart_data(sample_schedule, 'yearly')
    
    assert chart_data.chart_type == "line"
    assert len(chart_data.datasets) == 1
    assert chart_data.datasets[0].label == "Υπόλοιπο"
    assert len(chart_data.labels) == 20


def test_prepare_comparison_chart_data(service, sample_plans):
    """Test preparing plan comparison chart data."""
    chart_data = service.prepare_comparison_chart_data(sample_plans)
    
    assert chart_data.chart_type == "bar"
    assert len(chart_data.labels) == len(sample_plans)
    assert len(chart_data.datasets) == 3  # Monthly, Interest, Total


def test_prepare_comparison_chart_data_empty(service):
    """Test preparing comparison chart with no plans."""
    chart_data = service.prepare_comparison_chart_data([])
    
    assert len(chart_data.labels) == 0
    assert len(chart_data.datasets) == 0


def test_prepare_payment_breakdown_data(service, sample_schedule):
    """Test preparing payment breakdown pie chart data."""
    chart_data = service.prepare_payment_breakdown_data(sample_schedule, 1)
    
    assert chart_data.chart_type == "pie"
    assert len(chart_data.labels) == 2  # Principal and Interest
    assert chart_data.labels == ["Κεφάλαιο", "Τόκοι"]


def test_prepare_cumulative_interest_chart_data(service, sample_schedule):
    """Test preparing cumulative interest chart data."""
    chart_data = service.prepare_cumulative_interest_chart_data(sample_schedule, 'yearly')
    
    assert chart_data.chart_type == "area"
    assert len(chart_data.datasets) == 1
    assert chart_data.datasets[0].label == "Αθροιστικοί Τόκοι"
    
    # Cumulative interest should be monotonically increasing
    data = chart_data.datasets[0].data
    for i in range(len(data) - 1):
        assert data[i+1] >= data[i]


def test_prepare_multi_plan_comparison_data(service):
    """Test preparing multi-plan comparison chart data."""
    generator = LoanPlanGeneratorService()
    plans = generator.generate_loan_options(100000, "mortgage", 3000)[:2]
    
    amort = AmortizationService()
    schedules = {
        plan.id: amort.calculate_amortization_schedule(
            plan.amount, plan.interest_rate, plan.term_years
        ) 
        for plan in plans
    }
    
    chart_data = service.prepare_multi_plan_comparison_data(plans, schedules, 'yearly')
    
    assert chart_data.chart_type == "line"
    assert len(chart_data.datasets) == len(plans)


def test_chart_data_has_colors(service, sample_schedule):
    """Test that datasets have color assignments."""
    chart_data = service.prepare_amortization_chart_data(sample_schedule, 'yearly')
    
    for dataset in chart_data.datasets:
        assert dataset.color is not None
        assert len(dataset.color) > 0


def test_chart_data_has_titles(service, sample_schedule):
    """Test that chart data includes titles and labels."""
    chart_data = service.prepare_amortization_chart_data(sample_schedule, 'yearly')
    
    assert chart_data.title is not None
    assert len(chart_data.title) > 0
    assert chart_data.x_label is not None
    assert chart_data.y_label is not None


def test_dataset_data_lengths_match_labels(service, sample_schedule):
    """Test that dataset data lengths match label count."""
    chart_data = service.prepare_amortization_chart_data(sample_schedule, 'yearly')
    
    for dataset in chart_data.datasets:
        assert len(dataset.data) == len(chart_data.labels)


def test_color_scheme_defined(service):
    """Test that color scheme is properly defined."""
    assert "principal" in service.COLORS
    assert "interest" in service.COLORS
    assert "balance" in service.COLORS


def test_empty_chart_data_structure(service):
    """Test empty chart data has correct structure."""
    empty = service._empty_chart_data("Test")
    
    assert empty.title == "Test"
    assert empty.labels == []
    assert empty.datasets == []

