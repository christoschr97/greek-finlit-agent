# Greek Financial Literacy Agent - Architecture Documentation

**Version:** 0.1.0  
**Last Updated:** October 22, 2025

## Table of Contents

1. [Overview](#overview)
2. [Architecture Principles](#architecture-principles)
3. [Project Structure](#project-structure)
4. [Technology Stack](#technology-stack)
5. [User Flow](#user-flow)
6. [Data Flow](#data-flow)
7. [Core Components](#core-components)
8. [Session State Management](#session-state-management)
9. [Database Layer](#database-layer)
10. [Testing Strategy](#testing-strategy)
11. [Deployment](#deployment)
12. [Extension Points](#extension-points)

---

## Overview

The Greek Financial Literacy Agent is a Streamlit-based conversational AI application designed to provide personalized financial education to Greek households. The system adapts its communication style based on the user's assessed financial literacy level using the internationally validated Lusardi-Mitchell "Big 3" assessment.

### Key Features

- **Validated Assessment**: Uses the Lusardi-Mitchell Big 3 questions (validated in 20+ countries)
- **Adaptive Responses**: LLM responses tailored to user's literacy level
- **Dual Pathways**: General financial literacy chat + Responsible borrowing workflow
- **Greek Context**: All content in Greek with culturally relevant examples
- **PostgreSQL Backend**: Persistent data storage for user information
- **Modular Architecture**: Clean separation of concerns for easy extension

---

## Architecture Principles

### 1. **Separation of Concerns**
- UI components are isolated from business logic
- Assessment logic is independent of the LLM
- Database operations are abstracted

### 2. **Session-Based State**
- Streamlit session state manages user journey
- No authentication required (single-session app)
- State persists within a browser session

### 3. **Deterministic Assessment**
- Financial literacy scoring uses rule-based logic
- No LLM involvement in assessment scoring
- Predictable and transparent results

### 4. **Modular UI Components**
- Each screen is a separate module
- Reusable configuration constants
- Easy to add new workflows

---

## Project Structure

```
greek-finlit-agent/
├── app.py                          # Main entry point & routing
├── docker-compose.yml              # Multi-container orchestration
├── Dockerfile                      # Application container
├── pyproject.toml                  # Dependencies & project config
├── README.md                       # User-facing documentation
├── ARCHITECTURE.md                 # This file
│
├── src/finlit_agent/              # Main package
│   ├── __init__.py
│   ├── agent.py                   # LLM initialization & base prompt
│   ├── database.py                # PostgreSQL connection utilities
│   ├── literacy_assessment.py     # Big 3 assessment logic
│   │
│   ├── agents/                    # Specialized agent modules
│   │   └── loan_classifier.py    # Loan type classification agent
│   │
│   ├── prompts/                   # LLM prompt templates
│   │   └── templates.py          # System prompts for agents
│   │
│   ├── schemas/                   # Data structures
│   │   └── responses.py          # Structured output schemas
│   │
│   └── ui/                        # Streamlit UI components
│       ├── __init__.py           # Public UI exports
│       ├── assessment_ui.py      # Big 3 assessment screens
│       ├── chat_ui.py            # General chat interface
│       ├── config.py             # UI constants & strings
│       ├── path_selection_ui.py  # Workflow selection (currently bypassed)
│       ├── responsible_borrowing_ui.py  # Borrowing workflow (placeholder)
│       └── session_state.py      # Session initialization
│
└── tests/                         # Test suite
    ├── conftest.py               # Pytest configuration
    ├── test_agent.py             # Agent tests
    ├── test_literacy_assessment.py  # Assessment tests
    └── ui/                       # UI component tests
        ├── test_assessment_ui.py
        ├── test_chat_ui.py
        ├── test_config.py
        └── test_session_state.py
```

---

## Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Frontend** | Streamlit | 1.39+ | Web UI framework |
| **LLM Framework** | LangChain | 1.0+ | LLM orchestration |
| **LLM Provider** | Google Gemini | 2.5 Flash | Language model |
| **Database** | PostgreSQL | 15 | Data persistence |
| **DB Driver** | psycopg2 | 2.9+ | PostgreSQL adapter |
| **Package Manager** | uv | Latest | Fast Python package management |
| **Testing** | pytest | 8.0+ | Test framework |
| **Containerization** | Docker | Latest | Deployment |

### Key Dependencies

```toml
langchain>=1.0.0              # LLM framework
langchain-google-genai>=2.0.10 # Gemini integration
langgraph>=1.0.0              # Multi-agent workflows
streamlit>=1.39.0             # Web UI
psycopg2-binary>=2.9.0        # PostgreSQL
python-dotenv>=1.0.0          # Environment management
```

---

## User Flow

### Complete User Journey

```
┌─────────────────────────────────────────────────────────────┐
│                    1. App Initialization                     │
│  - Load environment variables                               │
│  - Check database connection                                │
│  - Initialize session state                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              2. Big 3 Assessment (3 Questions)              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Q1: Compound Interest (100€ at 2% for 5 years)     │   │
│  │ Q2: Inflation (1% interest vs 2% inflation)        │   │
│  │ Q3: Risk Diversification (single stock vs fund)    │   │
│  └─────────────────────────────────────────────────────┘   │
│  - User answers each question                               │
│  - Deterministic scoring (0-3 correct)                     │
│  - Level calculated: Beginner/Intermediate/Advanced        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  3. Results & Path Selection                 │
│  - Display score and literacy level                         │
│  - Show explanations for each question                      │
│  - Present two path buttons:                                │
│    ┌──────────────────────┐  ┌──────────────────────┐      │
│    │ 💬 General Chat      │  │ 🏠 Responsible      │      │
│    │    (Financial        │  │    Borrowing        │      │
│    │     Education)       │  │    (Workflow)       │      │
│    └──────────────────────┘  └──────────────────────┘      │
└────────────────┬───────────────────┬────────────────────────┘
                 │                   │
        ┌────────┘                   └────────┐
        │                                     │
        ▼                                     ▼
┌─────────────────────┐            ┌──────────────────────────┐
│  4a. General Chat   │            │ 4b. Responsible Borrowing│
│                     │            │                          │
│ - Initialize agent  │            │ - Loan classification    │
│   with assessment   │            │ - Risk assessment        │
│   context          │            │ - Budget analysis        │
│ - Adaptive system   │            │ - Recommendation engine  │
│   prompt           │            │   (Coming soon)          │
│ - Conversational    │            │                          │
│   Q&A interface    │            │                          │
│                     │            │                          │
│ Sidebar Navigation: │            │ Sidebar Navigation:      │
│ ┌─────────────────┐ │            │ ┌─────────────────────┐ │
│ │ 💬 General Chat │ │            │ │ 💬 General Chat     │ │
│ │ 🏠 Responsible  │ │            │ │ 🏠 Responsible      │ │
│ │    Borrowing    │ │            │ │    Borrowing        │ │
│ └─────────────────┘ │            │ └─────────────────────┘ │
└─────────────────────┘            └──────────────────────────┘
```

### Screen Flow Details

#### Screen 1: Assessment Questions (assessment_ui.py)
- **Trigger**: App starts, `SESSION_ASSESSMENT_DONE = False`
- **Display**: One question at a time with radio buttons
- **Interaction**: User selects answer → clicks "Επόμενο" → next question
- **State Changes**: 
  - `SESSION_CURRENT_QUESTION` increments
  - `assessment.record_answer()` stores result
  - `assessment.score` updates

#### Screen 2: Results & Path Selection (assessment_ui.py)
- **Trigger**: All 3 questions answered
- **Display**: 
  - Success message
  - Score metric (e.g., "Προχωρημένο 3/3")
  - Expandable results with explanations
  - Two pathway buttons side-by-side
- **Interaction**: User clicks path button
- **State Changes**:
  - `SESSION_ASSESSMENT_DONE = True`
  - `SESSION_SELECTED_PATH = "general_chat" | "responsible_borrowing"`
  - `SESSION_PATH_SELECTED = True`

#### Screen 3a: General Chat (chat_ui.py)
- **Trigger**: User selects General Chat path
- **Initialization** (app.py):
  ```python
  agent = create_financial_agent()
  system_prompt = BASE_SYSTEM_PROMPT + assessment.get_context_summary()
  SESSION_AGENT = agent
  SESSION_MESSAGES = [SystemMessage(content=system_prompt)]
  ```
- **Display**:
  - Chat history (user/assistant messages)
  - Chat input box at bottom
- **Interaction**: 
  - User types message → submits
  - Agent processes → responds
  - Message appended to history

#### Screen 3b: Responsible Borrowing (responsible_borrowing_ui.py)
- **Trigger**: User selects Responsible Borrowing path
- **Display**: 
  - Title and description
  - "Under development" message
  - Back button to return to path selection
- **State**: Placeholder for future workflow

---

## Data Flow

### Assessment Flow

```
User Input → Assessment UI → FinancialLiteracyAssessment
                                      │
                                      ├─ record_answer()
                                      ├─ calculate score (deterministic)
                                      ├─ determine level (Beginner/Intermediate/Advanced)
                                      └─ generate context_summary()
                                             │
                                             ▼
                              System Prompt Enhancement
                                             │
                                             ▼
                                   LLM Agent Initialization
```

### Chat Interaction Flow

```
User Message → chat_ui.py
                   │
                   ├─ Append HumanMessage to SESSION_MESSAGES
                   │
                   ▼
            agent.invoke(messages)
                   │
                   ├─ LLM processes with context:
                   │  - Base system prompt
                   │  - Assessment context
                   │  - Conversation history
                   │
                   ▼
            AI Response
                   │
                   ├─ Append AIMessage to SESSION_MESSAGES
                   │
                   ▼
            Display in UI
```

### Session State Flow

```
App Start
    │
    ▼
initialize_session_state()
    │
    ├─ SESSION_ASSESSMENT_DONE = False
    ├─ SESSION_CURRENT_QUESTION = 0
    ├─ SESSION_ASSESSMENT = FinancialLiteracyAssessment()
    ├─ SESSION_MESSAGES = []
    ├─ SESSION_AGENT = None
    ├─ SESSION_PATH_SELECTED = False
    └─ SESSION_SELECTED_PATH = None
    │
    ▼
User Completes Assessment
    │
    ├─ SESSION_ASSESSMENT_DONE = True
    ├─ assessment.score = 0-3
    └─ assessment.answers = {1: {...}, 2: {...}, 3: {...}}
    │
    ▼
User Selects Path
    │
    ├─ SESSION_PATH_SELECTED = True
    └─ SESSION_SELECTED_PATH = "general_chat" or "responsible_borrowing"
    │
    ▼
Initialize Agent (if general_chat)
    │
    ├─ SESSION_AGENT = ChatGoogleGenerativeAI(...)
    └─ SESSION_MESSAGES = [SystemMessage(...)]
    │
    ▼
Conversation Loop
    │
    └─ SESSION_MESSAGES appends HumanMessage/AIMessage pairs
```

---

## Core Components

### 1. Main Application (app.py)

**Responsibilities:**
- Application entry point
- Route management based on session state
- Sidebar navigation rendering
- Agent initialization for general chat

**Key Functions:**

```python
def _render_sidebar_navigation():
    """
    Renders navigation buttons in sidebar after assessment.
    Allows switching between General Chat and Responsible Borrowing.
    """
    
# Routing logic:
if not SESSION_ASSESSMENT_DONE:
    render_assessment()
elif not SESSION_PATH_SELECTED:
    render_path_selection()  # Currently bypassed
elif SESSION_SELECTED_PATH == "general_chat":
    # Initialize agent if needed
    render_chat()
elif SESSION_SELECTED_PATH == "responsible_borrowing":
    render_responsible_borrowing()
```

### 2. Financial Literacy Assessment (literacy_assessment.py)

**Class: `FinancialLiteracyAssessment`**

**Core Data:**
```python
QUESTIONS = [
    {
        "id": 1,
        "dimension": "compound_interest",
        "question": "Υπόθεσε ότι έχεις 100€...",
        "options": ["a) ...", "b) ...", "c) ...", "d) ..."],
        "correct": "a",
        "explanation": "Με ανατοκισμό..."
    },
    # ... 2 more questions
]
```

**Key Methods:**

```python
def record_answer(question_id: int, user_answer: str) -> bool:
    """
    Records user's answer and updates score.
    Returns True if correct, False otherwise.
    Deterministic - no LLM involved.
    """

def get_level() -> LiteracyLevel:
    """
    Returns current literacy level based on score:
    - 0-1: BEGINNER
    - 2: INTERMEDIATE  
    - 3: ADVANCED
    """

def get_context_summary() -> str:
    """
    Generates rich context for LLM system prompt:
    - User's level
    - Correct/incorrect dimensions
    - Specific instructions for LLM adaptation
    """
```

**Example Context Summary:**
```
ΕΠΙΠΕΔΟ ΟΙΚΟΝΟΜΙΚΟΥ ΕΓΓΡΑΜΜΑΤΙΣΜΟΥ: Αρχάριο (1/3)

Αποτελέσματα Big 3 Assessment:
• Σκορ: 1/3 σωστές απαντήσεις
• Κατανοεί: Ανατοκισμός
• Χρειάζεται βοήθεια: Πληθωρισμός, Διαφοροποίηση Κινδύνου

ΟΔΗΓΙΕΣ ΠΡΟΣΑΡΜΟΓΗΣ:
- Χρησιμοποίησε ΠΟΛΥ απλή γλώσσα
- Εξήγησε ΟΛΕΣ τις βασικές έννοιες
- Δώσε συγκεκριμένα παραδείγματα με αριθμούς
- Αποφυγε εντελώς τεχνικούς όρους
```

### 3. LLM Agent (agent.py)

**Function: `create_financial_agent()`**

```python
def create_financial_agent():
    """
    Initializes Gemini 2.5 Flash model.
    
    Returns:
        ChatGoogleGenerativeAI instance configured for:
        - Model: gemini-2.5-flash
        - Temperature: 0.7 (balanced creativity/consistency)
        - API Key: from GOOGLE_API_KEY env var
    """
```

**Base System Prompt:**
```python
BASE_SYSTEM_PROMPT = """
Είσαι ένας χρήσιμος βοηθός οικονομικού αλφαβητισμού που 
ειδικεύεται στα προσωπικά οικονομικά για ελληνικά νοικοκυριά.
Παρέχεις σαφείς και πρακτικές συμβουλές για προϋπολογισμό, 
αποταμίευση, επενδύσεις, διαχείριση χρέους και γενικό 
οικονομικό σχεδιασμό...
"""
```

**Actual System Prompt = BASE + Assessment Context**

### 4. UI Components

#### a. Assessment UI (assessment_ui.py)

**render_assessment()**: Main entry point
- Checks current question index
- Calls `_render_question()` or `_render_results()`

**_render_question()**: Single question display
- Shows question text
- Radio buttons for options
- "Επόμενο" button to submit

**_render_results()**: Results + path selection
- Success message
- Score metric
- Expandable explanations
- **Two path buttons** (General Chat / Responsible Borrowing)

#### b. Chat UI (chat_ui.py)

**render_chat()**: Main chat interface
- Calls `_display_chat_history()` and `_handle_chat_input()`

**_display_chat_history()**: Renders message history
- Skips SystemMessage (internal context)
- Displays HumanMessage and AIMessage
- Uses Streamlit's `st.chat_message()`

**_handle_chat_input()**: Input handling
- `st.chat_input()` for user input
- Calls `_process_user_message()`

**_generate_agent_response()**: LLM invocation
```python
response = agent.invoke(messages)
messages.append(AIMessage(content=response.content))
```

#### c. Path Selection UI (path_selection_ui.py)

**Status**: Currently bypassed in normal flow
- Path selection happens directly in assessment results
- This component kept for potential future use

**render_path_selection()**: Two-button layout
- General Chat button (primary)
- Responsible Borrowing button

#### d. Responsible Borrowing UI (responsible_borrowing_ui.py)

**Status**: Placeholder implementation

**render_responsible_borrowing()**: Placeholder screen
- Title and description
- "Under development" message
- Back button to return to path selection

#### e. Configuration (config.py)

**Categories:**
- Page config (title, icon, layout)
- UI strings (Greek text for all components)
- Session state keys (constants for dict access)

**Example:**
```python
SESSION_ASSESSMENT_DONE = "assessment_done"
SESSION_SELECTED_PATH = "selected_path"
GENERAL_CHAT_PATH = "💬 Γενικές Ερωτήσεις Οικονομικού Εγγραμματισμού"
```

#### f. Session State (session_state.py)

**initialize_session_state()**: One-time initialization
- Only runs if `SESSION_ASSESSMENT_DONE` not in state
- Sets all default values

---

## Session State Management

### Session State Keys

| Key | Type | Initial Value | Purpose |
|-----|------|---------------|---------|
| `assessment_done` | bool | `False` | Assessment completion flag |
| `current_question` | int | `0` | Current question index (0-2) |
| `assessment` | Object | `FinancialLiteracyAssessment()` | Assessment instance |
| `messages` | List | `[]` | Chat message history |
| `agent` | Object | `None` | LLM agent instance |
| `path_selected` | bool | `False` | Path selection completion flag |
| `selected_path` | str | `None` | Selected path: "general_chat" or "responsible_borrowing" |

### State Transitions

```
INITIAL STATE
├─ assessment_done: False
├─ current_question: 0
├─ path_selected: False
└─ selected_path: None

↓ User answers question 1

MID-ASSESSMENT STATE
├─ assessment_done: False
├─ current_question: 1
├─ assessment.score: 1
└─ assessment.answers: {1: {...}}

↓ User completes all questions

ASSESSMENT COMPLETE STATE
├─ assessment_done: True (set when path button clicked)
├─ current_question: 3
├─ assessment.score: 0-3
└─ assessment.answers: {1: {...}, 2: {...}, 3: {...}}

↓ User selects General Chat

GENERAL CHAT STATE
├─ assessment_done: True
├─ path_selected: True
├─ selected_path: "general_chat"
├─ agent: ChatGoogleGenerativeAI(...)
└─ messages: [SystemMessage(...)]

↓ User asks question

CONVERSATION STATE
├─ messages: [
│    SystemMessage(...),
│    HumanMessage("Πώς..."),
│    AIMessage("Για να...")
│  ]
└─ [conversation continues]
```

### State Persistence

- **Within Session**: State persists as long as browser tab is open
- **Across Sessions**: No persistence (refresh resets to initial state)
- **Future Enhancement**: Database-backed session persistence

---

## Database Layer

### Configuration (database.py)

**Connection Parameters:**
```python
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")
database = os.getenv("DB_NAME", "finlit_db")
user = os.getenv("DB_USER", "finlit_user")
password = os.getenv("DB_PASSWORD", "finlit_password")
```

**Key Functions:**

```python
def get_db_connection():
    """Returns psycopg2 connection with RealDictCursor."""

def check_db_connection() -> bool:
    """Health check - returns True if DB is accessible."""

def init_db():
    """Creates tables if they don't exist."""
```

### Current Schema

```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Note**: This is a placeholder. Future schemas will include:
- User sessions
- Assessment results
- Conversation history
- Responsible borrowing workflow data

### Docker Setup

**docker-compose.yml** defines three services:

```yaml
services:
  app:          # Streamlit application
  postgres:     # PostgreSQL database
  pgadmin:      # Database management UI
```

**Access Points:**
- App: http://localhost:8501
- PgAdmin: http://localhost:5050
  - Email: admin@admin.com
  - Password: admin

---

## Testing Strategy

### Test Structure

```
tests/
├── conftest.py                    # Shared fixtures
├── test_agent.py                  # Agent initialization tests
├── test_literacy_assessment.py    # Assessment logic tests
└── ui/
    ├── test_assessment_ui.py      # Assessment UI tests
    ├── test_chat_ui.py            # Chat UI tests
    ├── test_config.py             # Config constants tests
    └── test_session_state.py      # Session state tests
```

### Test Coverage: 75%

| Module | Coverage | Key Tests |
|--------|----------|-----------|
| `agent.py` | 100% | API key handling, model config |
| `literacy_assessment.py` | 60% | Scoring, level calculation, context generation |
| `config.py` | 100% | Constants exist and are strings |
| `session_state.py` | 100% | Initialization logic |
| `assessment_ui.py` | 95% | Question rendering, results display |
| `chat_ui.py` | 55% | Message handling, error handling |

### Running Tests

```bash
# All tests
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ --cov=src/finlit_agent/ui --cov-report=term-missing

# Specific test file
uv run pytest tests/test_agent.py

# Specific test
uv run pytest tests/ui/test_config.py::test_page_config_exists
```

### Mocking Strategy

**Streamlit Mocking:**
```python
@pytest.fixture
def mock_streamlit(monkeypatch):
    mock_st = MagicMock()
    monkeypatch.setattr("streamlit.session_state", {})
    return mock_st
```

**Why Mock Streamlit?**
- Tests run without browser
- Fast execution
- Isolated component testing
- No UI rendering overhead

---

## Deployment

### Local Development

```bash
# 1. Install dependencies
uv sync

# 2. Set up environment
cp env.example .env
# Edit .env with your GOOGLE_API_KEY

# 3. Run locally
streamlit run app.py
```

### Docker Deployment

```bash
# Build and start all services
docker-compose up

# Access
# - App: http://localhost:8501
# - PgAdmin: http://localhost:5050
```

### Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `GOOGLE_API_KEY` | Yes | - | Gemini API authentication |
| `DB_HOST` | No | localhost | PostgreSQL host |
| `DB_PORT` | No | 5432 | PostgreSQL port |
| `DB_NAME` | No | finlit_db | Database name |
| `DB_USER` | No | finlit_user | Database user |
| `DB_PASSWORD` | No | finlit_password | Database password |

### Dockerfile Structure

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync
COPY . .
CMD ["uv", "run", "streamlit", "run", "app.py"]
```

---

## Extension Points

### 1. Adding New Workflows

**Steps:**
1. Create new UI component in `src/finlit_agent/ui/new_workflow_ui.py`
2. Add constants to `config.py`
3. Update `session_state.py` with new state keys
4. Add routing in `app.py`
5. Add sidebar button
6. Export from `ui/__init__.py`

**Example:**
```python
# config.py
BUDGET_PLANNING_PATH = "📊 Προϋπολογισμός"
SESSION_BUDGET_DATA = "budget_data"

# new_workflow_ui.py
def render_budget_planning():
    st.markdown("### 📊 Σχεδιασμός Προϋπολογισμού")
    # ... implementation

# app.py
elif st.session_state[config.SESSION_SELECTED_PATH] == "budget_planning":
    render_budget_planning()
```

### 2. Adding Custom Tools (LangChain)

**Use Case**: Financial calculators, data retrieval

```python
from langchain.tools import tool

@tool
def calculate_loan_payment(principal: float, rate: float, years: int) -> float:
    """Calculate monthly loan payment."""
    monthly_rate = rate / 12
    num_payments = years * 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
              ((1 + monthly_rate)**num_payments - 1)
    return payment

# Add to agent
agent = create_agent(
    model=llm,
    tools=[calculate_loan_payment],
    system_prompt=system_prompt
)
```

### 3. Adding RAG (Retrieval Augmented Generation)

**Use Case**: Greek financial regulations, tax law

```python
from langchain.vectorstores import FAISS
from langchain.embeddings import GoogleGenerativeAIEmbeddings

# 1. Create vector store from Greek financial docs
embeddings = GoogleGenerativeAIEmbeddings()
vectorstore = FAISS.from_documents(greek_fin_docs, embeddings)

# 2. Add retrieval tool
retriever = vectorstore.as_retriever()

# 3. Integrate with agent
from langchain.chains import RetrievalQA
qa_chain = RetrievalQA.from_chain_type(
    llm=agent,
    retriever=retriever
)
```

### 4. Multi-Agent Workflows (LangGraph)

**Use Case**: Complex responsible borrowing workflow

```python
from langgraph.graph import StateGraph

# Define workflow states
workflow = StateGraph()

workflow.add_node("classify_loan", loan_classifier_agent)
workflow.add_node("assess_risk", risk_assessment_agent)
workflow.add_node("analyze_budget", budget_analyzer_agent)
workflow.add_node("generate_recommendation", recommendation_agent)

workflow.add_edge("classify_loan", "assess_risk")
workflow.add_edge("assess_risk", "analyze_budget")
workflow.add_edge("analyze_budget", "generate_recommendation")

app = workflow.compile()
```

### 5. Persistent User Profiles

**Database Schema:**
```sql
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE,
    literacy_level VARCHAR(50),
    assessment_score INT,
    assessment_date TIMESTAMP,
    preferences JSONB
);

CREATE TABLE conversation_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES user_profiles(id),
    message_type VARCHAR(20),  -- 'human' or 'ai'
    content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Implementation:**
```python
def save_assessment_result(session_id: str, assessment: FinancialLiteracyAssessment):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO user_profiles (session_id, literacy_level, assessment_score)
                VALUES (%s, %s, %s)
            """, (session_id, assessment.get_level_name(), assessment.score))
```

### 6. Analytics & Monitoring

**Metrics to Track:**
- Assessment completion rates
- Score distributions
- Most common questions
- Average conversation length
- Path selection preferences

**Implementation Ideas:**
- Integrate with Google Analytics
- Log to database
- Export to CSV for analysis

---

## Development Guidelines

### Code Style

- **Python**: Follow PEP 8
- **Line Length**: 100 characters max
- **Imports**: Grouped (stdlib, third-party, local)
- **Type Hints**: Use where beneficial
- **Docstrings**: Google style for functions/classes

### Git Workflow

**Branch Naming:**
- `feature/` - New features
- `bugfix/` - Bug fixes
- `refactor/` - Code improvements
- `docs/` - Documentation updates

**Example:**
```bash
git checkout -b feature/add_budget_calculator
# Make changes
git commit -m "Add budget calculator tool"
git push origin feature/add_budget_calculator
```

### Testing Requirements

- All new features must have tests
- Maintain > 70% coverage
- Mock external dependencies (Streamlit, LLM calls)
- Test both happy path and error cases

### Documentation Requirements

- Update ARCHITECTURE.md for structural changes
- Update README.md for user-facing changes
- Add docstrings to new functions
- Comment complex logic

---

## Troubleshooting

### Common Issues

**1. "GOOGLE_API_KEY not found"**
- Ensure `.env` file exists with `GOOGLE_API_KEY=your_key`
- Restart Streamlit after adding key

**2. Database Connection Failed**
- Check docker-compose services are running: `docker-compose ps`
- Verify DB credentials in `.env` match `docker-compose.yml`
- Check PostgreSQL logs: `docker-compose logs postgres`

**3. Streamlit Session State Errors**
- Clear browser cache
- Restart Streamlit app
- Check `initialize_session_state()` is called before any state access

**4. LLM Response Errors**
- Verify API key is valid
- Check internet connection
- Review Gemini API quotas/limits
- Increase timeout in `init_chat_model()`

### Debug Mode

```bash
# Run with verbose logging
streamlit run app.py --logger.level=debug

# Python debugging
import pdb; pdb.set_trace()  # Add breakpoint
```

---

## Future Roadmap

### Phase 1: Responsible Borrowing (Current Branch)
- [ ] Implement loan classifier integration
- [ ] Build risk assessment workflow
- [ ] Add budget analysis tools
- [ ] Create recommendation engine

### Phase 2: Enhanced Assessment
- [ ] Add more literacy questions
- [ ] Track progress over time
- [ ] Personalized learning paths

### Phase 3: RAG Integration
- [ ] Greek tax law knowledge base
- [ ] Bank product comparisons
- [ ] Regulatory updates

### Phase 4: Multi-User Support
- [ ] User authentication
- [ ] Profile management
- [ ] Conversation history persistence

### Phase 5: Advanced Features
- [ ] Financial calculators (mortgage, retirement, savings)
- [ ] Document upload & analysis
- [ ] Personalized financial plans
- [ ] Export recommendations as PDF

---

## Glossary

| Term | Definition |
|------|------------|
| **Big 3** | Lusardi-Mitchell 3-question financial literacy assessment |
| **LiteracyLevel** | Enum: BEGINNER, INTERMEDIATE, or ADVANCED |
| **Session State** | Streamlit's per-session data storage |
| **System Prompt** | Initial instructions given to the LLM |
| **Context Summary** | Assessment results formatted for LLM |
| **RAG** | Retrieval Augmented Generation - LLM + knowledge base |
| **LangGraph** | Framework for multi-agent workflows |

---

## Contact & Support

- **Repository**: [github.com/yourorg/greek-finlit-agent]
- **Issues**: Use GitHub Issues for bug reports
- **Contributions**: PRs welcome! Follow development guidelines above

---

**Last Updated**: October 22, 2025  
**Version**: 0.1.0  
**Authors**: Development Team

