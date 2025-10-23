"""
Configuration settings for the Streamlit UI.
"""

# Page configuration
PAGE_CONFIG = {
    "page_title": "Ελληνικός Βοηθός Οικονομικού Εγγραμματισμού",
    "page_icon": "💰",
    "layout": "centered"
}

# App title
APP_TITLE = "💰 Ελληνικός Βοηθός Οικονομικού Εγγραμματισμού"

# Assessment UI strings
ASSESSMENT_TITLE = "### 📊 Αξιολόγηση Οικονομικού Εγγραμματισμού (Big 3)"
ASSESSMENT_COMPLETE = "✅ Αξιολόγηση ολοκληρώθηκε!"
RESULTS_EXPANDER = "📋 Δες τα αποτελέσματα"
START_CHAT_BUTTON = "🚀 Ξεκίνα τη Συζήτηση"
NEXT_BUTTON = "Επόμενο"
QUESTION_PROMPT = "Επίλεξε την απάντησή σου:"
LEVEL_METRIC_LABEL = "Επίπεδο"

# Path selection UI strings
PATH_SELECTION_TITLE = "### 🛣️ Επιλέξτε Διαδρομή"
GENERAL_CHAT_PATH = "💬 Βοηθός Χρηματοοικονομικής παιδείας"
RESPONSIBLE_BORROWING_PATH = "🏠 Υπεύθυνος Δανεισμός"
SELECT_PATH_BUTTON = "Επιλογή Διαδρομής"

# Responsible borrowing UI strings
RESPONSIBLE_BORROWING_TITLE = "### 🏠 Υπεύθυνος Δανεισμός"
RESPONSIBLE_BORROWING_DESCRIPTION = "Θα σε καθοδηγήσουμε βήμα-βήμα για να κατανοήσεις αν ένα δάνειο είναι κατάλληλο για εσένα."

# Responsible borrowing step strings
RB_STEP1_TITLE = "### Βήμα 1: Τι χρειάζεσαι;"
RB_STEP1_PROMPT = "Πες μας τι θέλεις να κάνεις με το δάνειο:"
RB_STEP1_PLACEHOLDER = "π.χ. Θέλω να αγοράσω το πρώτο μου σπίτι, Χρειάζομαι χρήματα για επιδιόρθωση αυτοκινήτου..."
RB_STEP1_BUTTON = "🔍 Ανάλυση Αίτησης"
RB_CLASSIFYING = "🔍 Αναλύω την αίτησή σου..."
RB_NEXT_STEP = "Συνέχεια στο Βήμα {step} →"
RB_PREV_STEP = "← Πίσω στο Βήμα {step}"
RB_BACK_TO_PATH = "⬅️ Πίσω στην Επιλογή Διαδρομής"

# Sidebar strings
SIDEBAR_NAV_TITLE = "### Πλοήγηση"

# Chat UI strings
CHAT_INPUT_PLACEHOLDER = "Γράψε την ερώτησή σου..."
THINKING_SPINNER = "Σκέφτομαι..."
ERROR_PREFIX = "Σφάλμα"

# Session state keys
SESSION_ASSESSMENT_DONE = "assessment_done"
SESSION_CURRENT_QUESTION = "current_question"
SESSION_ASSESSMENT = "assessment"
SESSION_MESSAGES = "messages"
SESSION_AGENT = "agent"
SESSION_PATH_SELECTED = "path_selected"
SESSION_SELECTED_PATH = "selected_path"

# Responsible borrowing workflow session keys
SESSION_RB_WORKFLOW = "rb_workflow"
SESSION_RB_STATE = "rb_state"
