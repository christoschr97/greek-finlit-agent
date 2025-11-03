"""
Business logic services for the Greek Financial Literacy Agent.

This package contains service classes that handle business logic,
separated from the presentation layer (UI) and data access layer.
"""

from .loan_information_service import LoanInformationService
from .financial_calculator_service import FinancialCalculatorService
from .affordability_service import AffordabilityService
from .amortization_service import (
    AmortizationService,
    AmortizationSchedule,
    PaymentPeriod,
    SchedulePoint
)
from .loan_plan_generator_service import (
    LoanPlanGeneratorService,
    LoanPlan
)
from .loan_comparison_service import (
    LoanComparisonService,
    RankedPlan,
    ComparisonResult
)
from .visualization_data_service import (
    VisualizationDataService,
    ChartData,
    Dataset
)

__all__ = [
    # Original services
    "LoanInformationService",
    "FinancialCalculatorService",
    "AffordabilityService",
    # Amortization
    "AmortizationService",
    "AmortizationSchedule",
    "PaymentPeriod",
    "SchedulePoint",
    # Loan Planning
    "LoanPlanGeneratorService",
    "LoanPlan",
    # Loan Comparison
    "LoanComparisonService",
    "RankedPlan",
    "ComparisonResult",
    # Visualization
    "VisualizationDataService",
    "ChartData",
    "Dataset",
]

