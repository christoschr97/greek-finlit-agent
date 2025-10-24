"""
Visualization Data Service

Prepares data structures for charts and visualizations.
Transforms service data into format suitable for plotting libraries (Plotly, Altair).
"""

from dataclasses import dataclass
from typing import List, Dict, Literal
from .amortization_service import AmortizationSchedule, SchedulePoint
from .loan_plan_generator_service import LoanPlan


@dataclass
class Dataset:
    """Dataset for a single series in a chart."""
    label: str  # Series name
    data: List[float]  # Data points
    color: str  # Color for this series


@dataclass
class ChartData:
    """Complete data structure for a chart."""
    labels: List[str]  # X-axis labels
    datasets: List[Dataset]  # One or more data series
    chart_type: str  # 'line', 'bar', 'pie', 'area'
    title: str  # Chart title
    x_label: str  # X-axis label
    y_label: str  # Y-axis label


class VisualizationDataService:
    """Service for preparing chart data from financial calculations."""
    
    # Color scheme for charts
    COLORS = {
        "principal": "#2E86AB",  # Blue
        "interest": "#A23B72",   # Purple/Pink
        "balance": "#F18F01",    # Orange
        "plan_a": "#06A77D",     # Green
        "plan_b": "#D4AF37",     # Gold
        "total_cost": "#C73E1D", # Red
        "monthly": "#6C757D"     # Gray
    }
    
    def prepare_amortization_chart_data(
        self,
        schedule: AmortizationSchedule,
        interval: Literal['monthly', 'quarterly', 'yearly'] = 'yearly'
    ) -> ChartData:
        """
        Prepare data for amortization schedule chart (principal vs interest over time).
        
        Args:
            schedule: Amortization schedule
            interval: Time interval for grouping
            
        Returns:
            ChartData for line/area chart
        """
        from .amortization_service import AmortizationService
        
        # Get aggregated schedule
        amort_service = AmortizationService()
        summary = amort_service.get_schedule_summary(schedule, interval)
        
        if not summary:
            return self._empty_chart_data("Αποσβεση Δανείου")
        
        # Extract labels and data
        labels = [point.label for point in summary]
        principal_data = [point.principal_paid for point in summary]
        interest_data = [point.interest_paid for point in summary]
        
        return ChartData(
            labels=labels,
            datasets=[
                Dataset(
                    label="Κεφάλαιο",
                    data=principal_data,
                    color=self.COLORS["principal"]
                ),
                Dataset(
                    label="Τόκοι",
                    data=interest_data,
                    color=self.COLORS["interest"]
                )
            ],
            chart_type="area",
            title="Αποσβεση Δανείου με την Πάροδο του Χρόνου",
            x_label="Περίοδος",
            y_label="Ποσό (€)"
        )
    
    def prepare_balance_chart_data(
        self,
        schedule: AmortizationSchedule,
        interval: Literal['monthly', 'quarterly', 'yearly'] = 'yearly'
    ) -> ChartData:
        """
        Prepare data for remaining balance over time chart.
        
        Args:
            schedule: Amortization schedule
            interval: Time interval for grouping
            
        Returns:
            ChartData for line chart
        """
        from .amortization_service import AmortizationService
        
        amort_service = AmortizationService()
        summary = amort_service.get_schedule_summary(schedule, interval)
        
        if not summary:
            return self._empty_chart_data("Υπόλοιπο Δανείου")
        
        labels = [point.label for point in summary]
        balance_data = [point.remaining_balance for point in summary]
        
        return ChartData(
            labels=labels,
            datasets=[
                Dataset(
                    label="Υπόλοιπο",
                    data=balance_data,
                    color=self.COLORS["balance"]
                )
            ],
            chart_type="line",
            title="Υπόλοιπο Δανείου με την Πάροδο του Χρόνου",
            x_label="Περίοδος",
            y_label="Υπόλοιπο (€)"
        )
    
    def prepare_comparison_chart_data(
        self,
        plans: List[LoanPlan]
    ) -> ChartData:
        """
        Prepare data for side-by-side plan comparison (bar chart).
        
        Args:
            plans: List of loan plans to compare (typically 2)
            
        Returns:
            ChartData for grouped bar chart
        """
        if not plans:
            return self._empty_chart_data("Σύγκριση Σχεδίων")
        
        labels = [plan.name for plan in plans]
        
        # Monthly payments
        monthly_payments = [plan.monthly_payment for plan in plans]
        
        # Total interest
        total_interest = [plan.total_interest for plan in plans]
        
        # Total cost
        total_costs = [plan.total_cost for plan in plans]
        
        return ChartData(
            labels=labels,
            datasets=[
                Dataset(
                    label="Μηνιαία Δόση (€)",
                    data=monthly_payments,
                    color=self.COLORS["monthly"]
                ),
                Dataset(
                    label="Συνολικοί Τόκοι (€)",
                    data=total_interest,
                    color=self.COLORS["interest"]
                ),
                Dataset(
                    label="Συνολικό Κόστος (€)",
                    data=total_costs,
                    color=self.COLORS["total_cost"]
                )
            ],
            chart_type="bar",
            title="Σύγκριση Σχεδίων Δανείου",
            x_label="Σχέδιο",
            y_label="Ποσό (€)"
        )
    
    def prepare_payment_breakdown_data(
        self,
        schedule: AmortizationSchedule,
        period: int = 1
    ) -> ChartData:
        """
        Prepare data for payment breakdown pie chart (principal vs interest).
        
        Args:
            schedule: Amortization schedule
            period: Which payment period to show (default first)
            
        Returns:
            ChartData for pie chart
        """
        from .amortization_service import AmortizationService
        
        amort_service = AmortizationService()
        breakdown = amort_service.get_payment_breakdown(schedule, period)
        
        if not breakdown or breakdown["payment"] == 0:
            return self._empty_chart_data("Ανάλυση Δόσης")
        
        return ChartData(
            labels=["Κεφάλαιο", "Τόκοι"],
            datasets=[
                Dataset(
                    label="Ανάλυση Δόσης",
                    data=[breakdown["principal"], breakdown["interest"]],
                    color=""  # Pie charts use multiple colors
                )
            ],
            chart_type="pie",
            title=f"Ανάλυση Δόσης - {breakdown['period']}η Πληρωμή",
            x_label="",
            y_label=""
        )
    
    def prepare_cumulative_interest_chart_data(
        self,
        schedule: AmortizationSchedule,
        interval: Literal['monthly', 'quarterly', 'yearly'] = 'yearly'
    ) -> ChartData:
        """
        Prepare data for cumulative interest paid over time.
        
        Args:
            schedule: Amortization schedule
            interval: Time interval for grouping
            
        Returns:
            ChartData for area chart
        """
        from .amortization_service import AmortizationService
        
        amort_service = AmortizationService()
        summary = amort_service.get_schedule_summary(schedule, interval)
        
        if not summary:
            return self._empty_chart_data("Αθροιστικοί Τόκοι")
        
        labels = [point.label for point in summary]
        cumulative_interest = [point.cumulative_interest for point in summary]
        
        return ChartData(
            labels=labels,
            datasets=[
                Dataset(
                    label="Αθροιστικοί Τόκοι",
                    data=cumulative_interest,
                    color=self.COLORS["interest"]
                )
            ],
            chart_type="area",
            title="Αθροιστικοί Τόκοι με την Πάροδο του Χρόνου",
            x_label="Περίοδος",
            y_label="Συνολικοί Τόκοι (€)"
        )
    
    def prepare_multi_plan_comparison_data(
        self,
        plans: List[LoanPlan],
        schedules: Dict[str, AmortizationSchedule],
        interval: Literal['monthly', 'quarterly', 'yearly'] = 'yearly'
    ) -> ChartData:
        """
        Prepare data for comparing multiple plans' balances over time.
        
        Args:
            plans: List of loan plans
            schedules: Dict mapping plan IDs to their amortization schedules
            interval: Time interval for grouping
            
        Returns:
            ChartData for multi-line chart
        """
        if not plans or not schedules:
            return self._empty_chart_data("Σύγκριση Πολλαπλών Σχεδίων")
        
        from .amortization_service import AmortizationService
        amort_service = AmortizationService()
        
        # Get the longest term to determine labels
        max_periods = max(
            len(schedules[plan.id].periods) 
            for plan in plans 
            if plan.id in schedules
        )
        
        # Generate common labels based on longest plan
        if interval == 'yearly':
            labels = [f"Year {i+1}" for i in range(max_periods // 12 + 1)]
        elif interval == 'quarterly':
            labels = [f"Q{i+1}" for i in range(max_periods // 3 + 1)]
        else:
            labels = [f"Month {i+1}" for i in range(max_periods)]
        
        # Prepare dataset for each plan
        datasets = []
        colors = [self.COLORS["plan_a"], self.COLORS["plan_b"], self.COLORS["balance"]]
        
        for idx, plan in enumerate(plans[:3]):  # Limit to 3 plans for clarity
            if plan.id not in schedules:
                continue
            
            summary = amort_service.get_schedule_summary(
                schedules[plan.id], 
                interval
            )
            
            balance_data = [point.remaining_balance for point in summary]
            
            datasets.append(Dataset(
                label=plan.name,
                data=balance_data,
                color=colors[idx % len(colors)]
            ))
        
        return ChartData(
            labels=labels[:len(datasets[0].data)] if datasets else labels,
            datasets=datasets,
            chart_type="line",
            title="Σύγκριση Υπολοίπου Δανείων",
            x_label="Περίοδος",
            y_label="Υπόλοιπο (€)"
        )
    
    def _empty_chart_data(self, title: str) -> ChartData:
        """Return empty chart data structure."""
        return ChartData(
            labels=[],
            datasets=[],
            chart_type="line",
            title=title,
            x_label="",
            y_label=""
        )

