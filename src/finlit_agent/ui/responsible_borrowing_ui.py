"""
Responsible borrowing workflow - Presentation layer.

This module handles only the Streamlit UI rendering.
All business logic is delegated to service classes.

Workflow:
1. User describes what they need
2. Classify loan type using AI agent
3. Show educational content about that loan type
4. Collect financial information
5. Analyze affordability and provide recommendations
"""

import streamlit as st
from finlit_agent.agents.loan_classifier import create_loan_classifier_agent, classify_loan_request
from finlit_agent.services import (
    LoanInformationService,
    FinancialCalculatorService,
    AffordabilityService
)
from .config import (
    RESPONSIBLE_BORROWING_TITLE,
    SESSION_PATH_SELECTED,
    SESSION_SELECTED_PATH,
)

# Initialize services
loan_info_service = LoanInformationService()
calculator_service = FinancialCalculatorService()
affordability_service = AffordabilityService()


def render_responsible_borrowing() -> None:
    """Κύρια συνάρτηση - απλή ροή."""
    st.markdown(RESPONSIBLE_BORROWING_TITLE)
    st.write("Θα σε βοηθήσουμε να καταλάβεις αν ένα δάνειο είναι κατάλληλο για εσένα.")
    
    # If we don't have a loan type yet, ask the user
    if "rb_loan_type" not in st.session_state:
        _ask_user_need()
    else:
        _explain_loan_basics()
    
    # Πίσω button
    st.markdown("---")
    if st.button("⬅️ Πίσω στην Επιλογή Διαδρομής"):
        _reset()


def _ask_user_need():
    """Βήμα 1: Ρωτάμε τι θέλει."""
    st.markdown("### Βήμα 1: Τι θέλεις να κάνεις;")
    
    user_input = st.text_area(
        "Πες μας τι σκέφτεσαι:",
        placeholder="π.χ. Θέλω να αγοράσω σπίτι, Χρειάζομαι λεφτά για το αυτοκίνητο...",
        height=100
    )
    
    if st.button("🔍 Ανάλυση", type="primary", disabled=not user_input.strip()):
        with st.spinner("Αναλύω..."):
            _classify_and_save(user_input)


def _classify_and_save(user_input: str):
    """Καλούμε το classifier και σώζουμε στο session state."""
    try:
        agent = create_loan_classifier_agent()
        result = classify_loan_request(agent, user_input)
        
        if result["success"]:
            st.session_state["rb_loan_type"] = result["loan_type"]
            st.session_state["rb_confidence"] = result["confidence"]
            st.session_state["rb_reasoning"] = result["reasoning"]
            st.session_state["rb_user_input"] = user_input
            st.rerun()
        else:
            st.error(f"❌ Κάτι πήγε στραβά: {result['error']}")
    except Exception as e:
        st.error(f"❌ Σφάλμα: {str(e)}")


def _explain_loan_basics():
    """Βήμα 2: Εξηγούμε τι σημαίνει το δάνειο και ζητάμε οικονομικά στοιχεία."""
    loan_type = st.session_state["rb_loan_type"]
    confidence = st.session_state["rb_confidence"]
    
    # Get loan name from service
    loan_type_gr = loan_info_service.get_loan_name(loan_type)
    
    # We show the found loan type
    st.success(f"✅ Κατάλαβα! Ενδιαφέρεσαι για: **{loan_type_gr}**")
    st.caption(f"Βεβαιότητα: {confidence*100:.0f}%")
    
    st.markdown("---")
    st.markdown("### 📚 Ας μάθουμε τα βασικά")
    
    # Εξήγηση με απλά λόγια
    _show_simple_explanation(loan_type)
    
    st.markdown("---")
    
    # Φόρμα οικονομικών στοιχείων
    if "rb_financial_data" not in st.session_state:
        _show_financial_form()
    else:
        _show_financial_summary()
        
        # Button για reset
        if st.button("🔄 Ξανά από την αρχή"):
            _reset()


def _show_simple_explanation(loan_type: str):
    """Εξήγηση με πολύ απλά λόγια - Delegates to service."""
    # Get explanation from service
    explanation = loan_info_service.get_loan_explanation(loan_type)
    
    if explanation:
        # Render loan type explanation
        st.markdown(f"#### {explanation['title']}")
        st.write(explanation['description'])
        st.write(explanation['key_points'])
        
        # Show tip/warning based on loan type
        if 'tip' in explanation:
            if loan_type == "personal":
                st.warning(explanation['tip'])
            else:
                st.info(explanation['tip'])
        
        # Show example if available
        if 'example' in explanation:
            with st.expander("📊 Δες ένα απλό παράδειγμα"):
                st.write(explanation['example'])
    else:
        st.info("Δεν κατάλαβα ακριβώς τι ψάχνεις. Μπορείς να διευκρινίσεις;")
    
    # Common terms for all loan types
    st.markdown("---")
    st.markdown("### 🎯 Βασικοί Όροι που πρέπει να ξέρεις")
    
    # Get common terms from service
    common_terms = loan_info_service.get_common_terms()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(common_terms["col1"]["interest_rate"])
    
    with col2:
        st.markdown(common_terms["col2"]["term_and_apr"])


def _show_financial_form():
    """Φόρμα για συλλογή οικονομικών στοιχείων."""
    st.markdown("### 💰 Η Οικονομική σου Κατάσταση")
    st.write("Για να σε βοηθήσουμε καλύτερα, πες μας λίγα για την οικονομική σου κατάσταση:")
    
    with st.form("financial_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Εισοδήματα")
            monthly_income = st.number_input(
                "Μηνιαίο καθαρό εισόδημα (€)",
                min_value=0,
                value=1000,
                step=100,
                help="Το ποσό που παίρνεις στο χέρι κάθε μήνα"
            )
            
            other_income = st.number_input(
                "Άλλα εισοδήματα (€)",
                min_value=0,
                value=0,
                step=50,
                help="Ενοίκια, μερίσματα, κλπ"
            )
        
        with col2:
            st.markdown("#### 📉 Έξοδα")
            monthly_expenses = st.number_input(
                "Μηνιαία έξοδα διαβίωσης (€)",
                min_value=0,
                value=600,
                step=50,
                help="Ενοίκιο, σούπερ μάρκετ, λογαριασμοί, κλπ"
            )
            
            existing_loans = st.number_input(
                "Υπάρχουσες δόσεις δανείων (€)",
                min_value=0,
                value=0,
                step=50,
                help="Δόσεις από άλλα δάνεια που πληρώνεις"
            )
        
        st.markdown("#### 💳 Επιπλέον Πληροφορίες")
        
        col3, col4 = st.columns(2)
        
        with col3:
            savings = st.number_input(
                "Αποταμιεύσεις (€)",
                min_value=0,
                value=0,
                step=500,
                help="Χρήματα που έχεις στην άκρη"
            )
        
        with col4:
            loan_amount = st.number_input(
                "Ποσό δανείου που σκέφτεσαι (€)",
                min_value=0,
                value=10000,
                step=1000,
                help="Πόσα χρήματα θέλεις να δανειστείς"
            )
        
        submitted = st.form_submit_button("📊 Ανάλυση της Κατάστασής μου", type="primary")
        
        if submitted:
            # save the financial data
            st.session_state["rb_financial_data"] = {
                "monthly_income": monthly_income,
                "other_income": other_income,
                "monthly_expenses": monthly_expenses,
                "existing_loans": existing_loans,
                "savings": savings,
                "loan_amount": loan_amount
            }
            st.rerun()


def _show_financial_summary():
    """Δείχνουμε σύνοψη και ανάλυση της οικονομικής κατάστασης."""
    data = st.session_state["rb_financial_data"]
    
    st.markdown("### 📊 Ανάλυση Οικονομικής Κατάστασης")
    
    # Calculate metrics using service
    metrics = calculator_service.calculate_financial_metrics(data)
    
    # Δείχνουμε τα νούμερα
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💰 Συνολικό Εισόδημα", f"{metrics['total_income']:,.0f}€")
    
    with col2:
        st.metric("💸 Συνολικά Έξοδα", f"{metrics['total_expenses']:,.0f}€")
    
    with col3:
        disposable_income = metrics['disposable_income']
        total_income = metrics['total_income']
        st.metric(
            "💵 Διαθέσιμο Ποσό", 
            f"{disposable_income:,.0f}€",
            delta=f"{(disposable_income/total_income*100):.1f}% του εισοδήματος" if total_income > 0 else None
        )
    
    st.markdown("---")
    
    # Affordability analysis using service
    analysis, status = _analyze_affordability(data, metrics)
    
    # NEW: Show visualization button if user can afford the loan
    if status in ["safe", "warning"]:
        st.markdown("---")
        st.markdown("### 📊 Θέλεις να δεις τις καλύτερες επιλογές δανείου;")
        st.write("Μπορούμε να σου δείξουμε διαφορετικές επιλογές δανείου και πώς θα εξελιχθεί το δάνειο στα επόμενα χρόνια.")
        
        if st.button("💡 Δες Προτάσεις & Οπτικοποιήσεις", type="primary", use_container_width=True):
            st.session_state["rb_show_visualizations"] = True
            st.rerun()
    
    # Show visualizations if user clicked the button
    if st.session_state.get("rb_show_visualizations", False):
        st.markdown("---")
        _show_loan_visualizations()
    
    # Button to change financial data
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✏️ Αλλαγή Στοιχείων", use_container_width=True):
            del st.session_state["rb_financial_data"]
            if "rb_show_visualizations" in st.session_state:
                del st.session_state["rb_show_visualizations"]
            st.rerun()


def _analyze_affordability(data: dict, metrics: dict):
    """Απλή ανάλυση αν μπορεί να ανταπεξέλθει στο δάνειο - Delegates to service."""
    st.markdown("### 🎯 Τι σημαίνουν αυτά τα νούμερα;")
    
    # Get analysis from service
    analysis = affordability_service.analyze_affordability(data, metrics)
    
    estimated_payment = metrics["estimated_payment"]
    payment_ratio = metrics["payment_ratio"]
    
    # Display payment and ratio metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📌 Εκτιμώμενη Μηνιαία Δόση")
        st.info(f"**~{estimated_payment:,.0f}€/μήνα**")
        st.caption("(Υποθέτοντας 5 χρόνια και 5% επιτόκιο)")
    
    with col2:
        st.markdown("#### 📊 Ποσοστό Εισοδήματος")
        if payment_ratio <= 30:
            st.success(f"**{payment_ratio:.1f}%** του εισοδήματός σου")
            st.caption("✅ Εντός ασφαλών ορίων!")
        elif payment_ratio <= 40:
            st.warning(f"**{payment_ratio:.1f}%** του εισοδήματός σου")
            st.caption("⚠️ Στο όριο - πρόσεχε!")
        else:
            st.error(f"**{payment_ratio:.1f}%** του εισοδήματός σου")
            st.caption("❌ Υπερβολικά υψηλό!")
    
    st.markdown("---")
    
    # Display recommendations from service
    st.markdown("#### 💡 Συμβουλές")
    
    status = analysis["status"]
    
    for recommendation in analysis["recommendations"]:
        if status == "danger":
            st.error(recommendation)
        elif status == "warning":
            st.warning(recommendation)
        else:
            if "Tip" in recommendation:
                st.info(recommendation)
            else:
                st.success(recommendation)
    
    # Return analysis for use in next step
    return analysis, status


def _show_loan_visualizations():
    """Δείχνουμε τις οπτικοποιήσεις των δανειακών επιλογών."""
    from .loan_visualization_ui import render_loan_visualization
    
    data = st.session_state["rb_financial_data"]
    loan_type = st.session_state["rb_loan_type"]
    loan_amount = data["loan_amount"]
    
    # Render the visualization
    render_loan_visualization(
        financial_data=data,
        loan_type=loan_type,
        loan_amount=loan_amount
    )


def _reset():
    """Καθαρίζουμε το session state."""
    keys_to_delete = [
        "rb_loan_type", 
        "rb_confidence", 
        "rb_reasoning", 
        "rb_user_input",
        "rb_financial_data",
        "rb_show_visualizations"
    ]
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]
    
    st.session_state[SESSION_PATH_SELECTED] = False
    st.session_state[SESSION_SELECTED_PATH] = None
    st.rerun()
