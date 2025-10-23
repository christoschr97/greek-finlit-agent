"""
Responsible borrowing workflow - Simplified version.

Απλή ροή: 
1. Ρωτάμε τι θέλει ο χρήστης
2. Εξηγούμε βασικές έννοιες με απλά λόγια
"""

import streamlit as st
from finlit_agent.agents.loan_classifier import create_loan_classifier_agent, classify_loan_request
from .config import (
    RESPONSIBLE_BORROWING_TITLE,
    SESSION_PATH_SELECTED,
    SESSION_SELECTED_PATH,
)

# Loan types in Greek
LOAN_TYPES_GR = {
    "mortgage": "Στεγαστικό Δάνειο",
    "personal": "Προσωπικό Δάνειο",
    "auto": "Δάνειο Αυτοκινήτου",
    "student": "Φοιτητικό Δάνειο",
    "business": "Επιχειρηματικό Δάνειο",
    "unknown": "Άγνωστο"
}


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
    
    loan_type_gr = LOAN_TYPES_GR.get(loan_type, loan_type)
    
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
    """Εξήγηση με πολύ απλά λόγια - όχι περίπλοκα."""
    
    if loan_type == "mortgage":
        st.markdown("#### Στεγαστικό Δάνειο")
        st.write("""
        **Τι είναι;** Δανείζεσαι χρήματα για να αγοράσεις σπίτι.
        
        **Βασικά που πρέπει να ξέρεις:**
        - 📅 **Διάρκεια:** Συνήθως 15-30 χρόνια
        - 💰 **Προκαταβολή:** Χρειάζεσαι 10-20% από την αξία του σπιτιού
        - 🏦 **Τόκος:** Το επιπλέον ποσό που πληρώνεις στην τράπεζα
        - 📊 **Δόση:** Το ποσό που πληρώνεις κάθε μήνα
        """)
        
        st.info("💡 **Tip:** Μην ξεπερνάς το 30-35% του μηνιαίου εισοδήματός σου σε δόση!")
        
        # Απλό παράδειγμα
        with st.expander("📊 Δες ένα απλό παράδειγμα"):
            st.write("""
            **Σενάριο:** Θέλεις σπίτι 100,000€
            - Προκαταβολή (20%): 20,000€
            - Δάνειο: 80,000€
            - Επιτόκιο: 3% ετησίως
            - Διάρκεια: 20 χρόνια
            - **Μηνιαία δόση: ~444€**
            """)
    
    elif loan_type == "personal":
        st.markdown("#### Προσωπικό Δάνειο")
        st.write("""
        **Τι είναι;** Δανείζεσαι χρήματα για προσωπική χρήση (έπιπλα, διακοπές, κλπ).
        
        **Βασικά που πρέπει να ξέρεις:**
        - 📅 **Διάρκεια:** Συνήθως 1-7 χρόνια
        - 💰 **Ποσά:** Από 1,000€ έως 50,000€
        - 🏦 **Τόκος:** Συνήθως ψηλότερος από στεγαστικό
        - ⚡ **Ταχύτητα:** Εγκρίνεται γρήγορα
        """)
        
        st.warning("⚠️ **Προσοχή:** Μόνο για πραγματικές ανάγκες, όχι για καταναλωτισμό!")
    
    elif loan_type == "auto":
        st.markdown("#### Δάνειο Αυτοκινήτου")
        st.write("""
        **Τι είναι;** Δανείζεσαι για να αγοράσεις όχημα.
        
        **Βασικά που πρέπει να ξέρεις:**
        - 📅 **Διάρκεια:** Συνήθως 3-7 χρόνια
        - 💰 **Προκαταβολή:** Συνήθως 10-30%
        - 🚗 **Εξασφάλιση:** Το αυτοκίνητο είναι εγγύηση
        - 📊 **Αξία:** Το αυτοκίνητο χάνει αξία με τον καιρό!
        """)
        
        st.info("💡 **Tip:** Υπολόγισε και τα έξοδα (ασφάλεια, συντήρηση, καύσιμα)!")
    
    elif loan_type == "student":
        st.markdown("#### Φοιτητικό Δάνειο")
        st.write("""
        **Τι είναι;** Δανείζεσαι για σπουδές.
        
        **Βασικά που πρέπει να ξέρεις:**
        - 📅 **Αποπληρωμή:** Ξεκινάει μετά τις σπουδές
        - 💰 **Επιτόκιο:** Συνήθως πιο χαμηλό
        - 🎓 **Χρήση:** Μόνο για εκπαίδευση
        - ⏰ **Χάρις περίοδος:** Μήνες πριν αρχίσεις να πληρώνεις
        """)
    
    elif loan_type == "business":
        st.markdown("#### Επιχειρηματικό Δάνειο")
        st.write("""
        **Τι είναι;** Δανείζεσαι για την επιχείρησή σου.
        
        **Βασικά που πρέπει να ξέρεις:**
        - 📊 **Business Plan:** Χρειάζεσαι σχέδιο επιχείρησης
        - 💰 **Εξασφάλιση:** Συχνά χρειάζονται εγγυήσεις
        - 📈 **Ρίσκο:** Υψηλότερο από προσωπικό
        - 🏦 **Τόκος:** Εξαρτάται από την επιχείρηση
        """)
    
    else:
        st.info("Δεν κατάλαβα ακριβώς τι ψάχνεις. Μπορείς να διευκρινίσεις;")
    
    # Common terms for all loan types
    st.markdown("---")
    st.markdown("### 🎯 Βασικοί Όροι που πρέπει να ξέρεις")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Επιτόκιο (Interest Rate)**  
        Το ποσοστό που πληρώνεις επιπλέον. Όσο πιο χαμηλό, τόσο καλύτερα!
        
        **Δόση (Installment)**  
        Το ποσό που πληρώνεις κάθε μήνα.
        """)
    
    with col2:
        st.markdown("""
        **Διάρκεια (Term)**  
        Πόσα χρόνια θα πληρώνεις. Περισσότερα χρόνια = μικρότερη δόση αλλά περισσότεροι τόκοι!
        
        **ΤΑΕ (APR)**  
        Το πραγματικό κόστος με όλα τα έξοδα.
        """)


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
    
    # Calculations
    total_income = data["monthly_income"] + data["other_income"]
    total_expenses = data["monthly_expenses"] + data["existing_loans"]
    disposable_income = total_income - total_expenses
    
    # Δείχνουμε τα νούμερα
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💰 Συνολικό Εισόδημα", f"{total_income:,.0f}€")
    
    with col2:
        st.metric("💸 Συνολικά Έξοδα", f"{total_expenses:,.0f}€")
    
    with col3:
        delta_color = "normal" if disposable_income > 0 else "inverse"
        st.metric(
            "💵 Διαθέσιμο Ποσό", 
            f"{disposable_income:,.0f}€",
            delta=f"{(disposable_income/total_income*100):.1f}% του εισοδήματος" if total_income > 0 else None
        )
    
    st.markdown("---")
    
    # Simple analysis
    _analyze_affordability(data, disposable_income)
    
    # Button to change financial data
    if st.button("✏️ Αλλαγή Στοιχείων"):
        del st.session_state["rb_financial_data"]
        st.rerun()


def _analyze_affordability(data: dict, disposable_income: float):
    """Απλή ανάλυση αν μπορεί να ανταπεξέλθει στο δάνειο."""
    st.markdown("### 🎯 Τι σημαίνουν αυτά τα νούμερα;")
    
    loan_amount = data["loan_amount"]
    
    # We calculate an estimated payment (simplified)
    # We assume 5 years and 5% interest rate
    months = 60
    monthly_rate = 0.05 / 12
    estimated_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    
    # Ποσοστό εισοδήματος που θα πάει σε δόση
    if data["monthly_income"] > 0:
        payment_ratio = (estimated_payment / data["monthly_income"]) * 100
    else:
        payment_ratio = 0
    
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
    
    # Συμβουλές
    st.markdown("#### 💡 Συμβουλές")
    
    if disposable_income <= 0:
        st.error("""
        **Προσοχή!** Τα έξοδά σου ξεπερνούν το εισόδημά σου.
        
        Πριν πάρεις δάνειο, καλό θα ήταν:
        - Να μειώσεις τα έξοδά σου
        - Να αυξήσεις το εισόδημά σου
        - Να ξεπληρώσεις υπάρχοντα δάνεια
        """)
    elif payment_ratio > 35:
        st.warning("""
        **Προσοχή!** Η δόση είναι υψηλή σε σχέση με το εισόδημά σου.
        
        Σκέψου:
        - Μικρότερο ποσό δανείου
        - Μεγαλύτερη διάρκεια (χαμηλότερη δόση, αλλά περισσότεροι τόκοι)
        - Να περιμένεις να βελτιώσεις την οικονομική σου κατάσταση
        """)
    elif disposable_income < estimated_payment:
        st.warning("""
        **Προσοχή!** Η εκτιμώμενη δόση είναι πάνω από το διαθέσιμο εισόδημά σου.
        
        Αυτό σημαίνει ότι μπορεί να δυσκολευτείς να την πληρώνεις.
        """)
    else:
        st.success("""
        **Καλά νέα!** Φαίνεται ότι έχεις περιθώριο για αυτό το δάνειο.
        
        Θυμήσου:
        - Αυτή είναι μια εκτίμηση - μίλησε με τράπεζα για ακριβή ποσά
        - Κράτα πάντα ένα buffer για έκτακτα έξοδα
        - Σύγκρινε προσφορές από διάφορες τράπεζες
        """)
    
    # Αποταμιεύσεις
    if data["savings"] < data["loan_amount"] * 0.1:
        st.info("""
        💡 **Tip:** Καλό θα ήταν να έχεις αποταμιεύσεις τουλάχιστον 10% του ποσού του δανείου 
        για προκαταβολή και έκτακτα έξοδα.
        """)


def _reset():
    """Καθαρίζουμε το session state."""
    keys_to_delete = [
        "rb_loan_type", 
        "rb_confidence", 
        "rb_reasoning", 
        "rb_user_input",
        "rb_financial_data"
    ]
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]
    
    st.session_state[SESSION_PATH_SELECTED] = False
    st.session_state[SESSION_SELECTED_PATH] = None
    st.rerun()
