"""
Loan Visualization UI

Displays interactive charts and comparisons for loan plans.
Shows amortization schedules, payment breakdowns, and plan comparisons.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict
from finlit_agent.services import (
    LoanPlan,
    LoanPlanGeneratorService,
    LoanComparisonService,
    AmortizationService,
    VisualizationDataService,
    RankedPlan
)


def render_loan_visualization(
    financial_data: Dict[str, float],
    loan_type: str,
    loan_amount: float
) -> None:
    """
    Main entry point for loan visualization.
    
    Args:
        financial_data: User's financial information
        loan_type: Type of loan (mortgage, personal, etc.)
        loan_amount: Desired loan amount
    """
    st.markdown("## 📊 Οι Καλύτερες Επιλογές Δανείου για Εσένα")
    st.write("Βάσει των οικονομικών σου στοιχείων, ετοιμάσαμε τις καλύτερες επιλογές δανείου.")
    
    # Generate and rank loan options
    with st.spinner("Υπολογίζουμε τις καλύτερες επιλογές..."):
        plans, ranked_plans = _generate_and_rank_plans(
            financial_data,
            loan_type,
            loan_amount
        )
    
    if not plans:
        st.error("Δεν μπορέσαμε να δημιουργήσουμε κατάλληλες επιλογές δανείου.")
        return
    
    # Select best 2 plans
    comparison_service = LoanComparisonService()
    best_plans = comparison_service.select_best_plans(ranked_plans, count=2)
    
    # Show plan comparison cards
    _render_plan_comparison_cards(best_plans, financial_data)
    
    st.markdown("---")
    
    # Show detailed amortization charts
    _render_amortization_section(best_plans)
    
    st.markdown("---")
    
    # Show comparison charts
    _render_comparison_charts(best_plans)


def _generate_and_rank_plans(
    financial_data: Dict[str, float],
    loan_type: str,
    loan_amount: float
) -> tuple[List[LoanPlan], List[RankedPlan]]:
    """Generate loan options and rank them."""
    generator = LoanPlanGeneratorService()
    comparison = LoanComparisonService()
    
    monthly_income = financial_data.get("monthly_income", 0)
    
    # Generate options
    plans = generator.generate_loan_options(
        total_amount=loan_amount,
        loan_type=loan_type,
        monthly_income=monthly_income
    )
    
    # Rank plans
    ranked = comparison.rank_loan_plans(plans, financial_data)
    
    return plans, ranked


def _render_plan_comparison_cards(plans: List[LoanPlan], financial_data: Dict) -> None:
    """Render side-by-side comparison cards for loan plans."""
    st.markdown("### 🎯 Οι 2 Καλύτερες Επιλογές")
    
    if len(plans) == 0:
        st.info("Δεν βρέθηκαν κατάλληλες επιλογές.")
        return
    
    # Create columns for side-by-side comparison
    cols = st.columns(len(plans))
    
    for idx, plan in enumerate(plans):
        with cols[idx]:
            _render_single_plan_card(plan, idx, financial_data)


def _render_single_plan_card(plan: LoanPlan, index: int, financial_data: Dict) -> None:
    """Render a single loan plan card."""
    # Card header with plan name
    label = f"**Σχέδιο {chr(65 + index)}**" if index < 26 else f"**Σχέδιο {index + 1}**"
    st.markdown(f"#### {label}")
    st.markdown(f"**{plan.name}**")
    
    # Color-coded affordability indicator
    if plan.payment_to_income_ratio <= 30:
        st.success("✅ Άνετο")
    elif plan.payment_to_income_ratio <= 40:
        st.warning("⚠️ Στο όριο")
    else:
        st.error("❌ Απαιτητικό")
    
    # Key metrics
    st.metric(
        "Μηνιαία Δόση",
        f"€{plan.monthly_payment:,.0f}",
        delta=f"{plan.payment_to_income_ratio:.1f}% του εισοδήματος"
    )
    
    st.metric(
        "Διάρκεια",
        f"{plan.term_years} έτη"
    )
    
    st.metric(
        "Συνολικό Κόστος",
        f"€{plan.total_cost:,.0f}"
    )
    
    st.metric(
        "Συνολικοί Τόκοι",
        f"€{plan.total_interest:,.0f}"
    )
    
    # Down payment if applicable
    if plan.down_payment > 0:
        st.caption(f"💰 Προκαταβολή: €{plan.down_payment:,.0f} ({plan.down_payment_percentage:.0f}%)")
    
    # Expand for more details
    with st.expander("📋 Περισσότερες Λεπτομέρειες"):
        st.write(f"**Ποσό Δανείου:** €{plan.amount:,.0f}")
        st.write(f"**Επιτόκιο:** {plan.interest_rate * 100:.2f}%")
        st.write(f"**Σύνολο Πληρωμών:** {plan.term_years * 12} μήνες")
        
        # Calculate some extra metrics
        total_paid = plan.monthly_payment * plan.term_years * 12
        st.write(f"**Σύνολο που θα Πληρώσεις:** €{total_paid:,.0f}")


def _render_amortization_section(plans: List[LoanPlan]) -> None:
    """Render amortization schedule visualizations."""
    st.markdown("### 📈 Πώς Εξελίσσεται το Δάνειο με τον Χρόνο")
    
    # Let user select which plan to visualize in detail
    if len(plans) > 1:
        plan_names = [f"Σχέδιο {chr(65 + i)}: {plan.name}" for i, plan in enumerate(plans)]
        selected_idx = st.selectbox(
            "Επέλεξε σχέδιο για λεπτομερή ανάλυση:",
            range(len(plans)),
            format_func=lambda i: plan_names[i]
        )
        selected_plan = plans[selected_idx]
    else:
        selected_plan = plans[0]
    
    # Calculate amortization schedule
    amort_service = AmortizationService()
    schedule = amort_service.calculate_amortization_schedule(
        selected_plan.amount,
        selected_plan.interest_rate,
        selected_plan.term_years
    )
    
    # Show charts in tabs
    tab1, tab2, tab3 = st.tabs([
        "💰 Κεφάλαιο vs Τόκοι",
        "📉 Υπόλοιπο Δανείου",
        "🥧 Ανάλυση Δόσεων"
    ])
    
    with tab1:
        _render_principal_vs_interest_chart(schedule)
    
    with tab2:
        _render_balance_chart(schedule)
    
    with tab3:
        _render_payment_breakdown_comparison(schedule)


def _render_principal_vs_interest_chart(schedule) -> None:
    """Render area chart showing principal vs interest over time."""
    viz_service = VisualizationDataService()
    chart_data = viz_service.prepare_amortization_chart_data(schedule, 'yearly')
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add principal area
    fig.add_trace(go.Scatter(
        x=chart_data.labels,
        y=chart_data.datasets[0].data,
        name=chart_data.datasets[0].label,
        fill='tozeroy',
        fillcolor='rgba(46, 134, 171, 0.5)',
        line=dict(color='rgb(46, 134, 171)', width=2)
    ))
    
    # Add interest area
    fig.add_trace(go.Scatter(
        x=chart_data.labels,
        y=chart_data.datasets[1].data,
        name=chart_data.datasets[1].label,
        fill='tozeroy',
        fillcolor='rgba(162, 59, 114, 0.5)',
        line=dict(color='rgb(162, 59, 114)', width=2)
    ))
    
    fig.update_layout(
        title=chart_data.title,
        xaxis_title=chart_data.x_label,
        yaxis_title=chart_data.y_label,
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    📊 **Τι δείχνει αυτό το γράφημα:**
    - Το **μπλε** δείχνει πόσο κεφάλαιο πληρώνεις κάθε χρόνο
    - Το **ροζ** δείχνει πόσους τόκους πληρώνεις κάθε χρόνο
    - Στην αρχή πληρώνεις περισσότερους τόκους
    - Με τον χρόνο, μεγαλύτερο μέρος της δόσης πηγαίνει στο κεφάλαιο
    """)


def _render_balance_chart(schedule) -> None:
    """Render line chart showing remaining balance over time."""
    viz_service = VisualizationDataService()
    chart_data = viz_service.prepare_balance_chart_data(schedule, 'yearly')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=chart_data.labels,
        y=chart_data.datasets[0].data,
        name=chart_data.datasets[0].label,
        fill='tozeroy',
        fillcolor='rgba(241, 143, 1, 0.3)',
        line=dict(color='rgb(241, 143, 1)', width=3)
    ))
    
    fig.update_layout(
        title=chart_data.title,
        xaxis_title=chart_data.x_label,
        yaxis_title=chart_data.y_label,
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    📉 **Τι δείχνει αυτό το γράφημα:**
    - Δείχνει πόσα χρήματα χρωστάς ακόμα στην τράπεζα
    - Το υπόλοιπο μειώνεται σταδιακά με τον χρόνο
    - Όσο περνάει ο καιρός, τόσο πιο γρήγορα μειώνεται
    """)


def _render_payment_breakdown_comparison(schedule) -> None:
    """Render pie charts comparing first and last payment breakdown."""
    amort_service = AmortizationService()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Πρώτη Δόση")
        first = amort_service.get_payment_breakdown(schedule, 1)
        
        fig = go.Figure(data=[go.Pie(
            labels=['Κεφάλαιο', 'Τόκοι'],
            values=[first['principal'], first['interest']],
            hole=.4,
            marker_colors=['#2E86AB', '#A23B72']
        )])
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption(f"Τόκοι: {first['interest_percentage']:.1f}%")
    
    with col2:
        st.markdown("#### Τελευταία Δόση")
        last = amort_service.get_payment_breakdown(schedule, schedule.term_months)
        
        fig = go.Figure(data=[go.Pie(
            labels=['Κεφάλαιο', 'Τόκοι'],
            values=[last['principal'], last['interest']],
            hole=.4,
            marker_colors=['#2E86AB', '#A23B72']
        )])
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption(f"Κεφάλαιο: {last['principal_percentage']:.1f}%")


def _render_comparison_charts(plans: List[LoanPlan]) -> None:
    """Render comparison charts between plans."""
    if len(plans) < 2:
        return
    
    st.markdown("### ⚖️ Σύγκριση Σχεδίων")
    
    viz_service = VisualizationDataService()
    chart_data = viz_service.prepare_comparison_chart_data(plans)
    
    # Create grouped bar chart
    fig = go.Figure()
    
    for dataset in chart_data.datasets:
        fig.add_trace(go.Bar(
            name=dataset.label,
            x=chart_data.labels,
            y=dataset.data,
            marker_color=dataset.color
        ))
    
    fig.update_layout(
        title=chart_data.title,
        xaxis_title=chart_data.x_label,
        yaxis_title=chart_data.y_label,
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show comparison insights
    _render_comparison_insights(plans)


def _render_comparison_insights(plans: List[LoanPlan]) -> None:
    """Render insights comparing the two plans."""
    if len(plans) < 2:
        return
    
    comparison_service = LoanComparisonService()
    comparison = comparison_service.compare_two_plans(plans[0], plans[1])
    
    st.markdown("#### 💡 Βασικές Διαφορές")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Σχέδιο A: {plans[0].name}**")
        for pro in comparison.pros_plan_a:
            st.write(f"✓ {pro}")
    
    with col2:
        st.markdown(f"**Σχέδιο B: {plans[1].name}**")
        for pro in comparison.pros_plan_b:
            st.write(f"✓ {pro}")
    
    # Show winner recommendation
    st.markdown("---")
    if comparison.winner == "a":
        st.success(f"🏆 **Συνιστάται:** {plans[0].name}")
    elif comparison.winner == "b":
        st.success(f"🏆 **Συνιστάται:** {plans[1].name}")
    else:
        st.info("⚖️ **Και τα δύο σχέδια είναι εξίσου καλές επιλογές**")
    
    st.write(comparison.recommendation)

