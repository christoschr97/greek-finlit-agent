# Greek Financial Literacy Agent

A basic financial agent built with LangChain and Google Gemini 2.5 to help with personal finance questions for Greek households.

## Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 3. Test the Big 3 Assessment (Optional)

See how the assessment works without needing API keys:
```bash
python3 test_big3.py
```

### 4. Run the Agent

**Local:**
```bash
streamlit run app.py
```

**Docker:**
```bash
docker-compose up
```

Access at: http://localhost:8501

See [DOCKER.md](DOCKER.md) for Docker details.

## Usage

Once running, you can ask the agent any questions (in Greek) about:
- Personal finance basics
- Budgeting and expense tracking
- Savings strategies
- Investment concepts
- Debt management
- Financial planning

### Example Questions (Παραδείγματα Ερωτήσεων)

- "Πώς μπορώ να δημιουργήσω έναν μηνιαίο προϋπολογισμό;"
- "Ποια είναι η διαφορά μεταξύ αποταμίευσης και επένδυσης;"
- "Πώς μπορώ να μειώσω τα μηνιαία έξοδά μου;"
- "Τι πρέπει να γνωρίζω για τις πιστωτικές κάρτες;"

Type `quit`, `exit`, `έξοδος`, or `τέλος` to end the conversation.

## Features

- ✅ **Big 3 Financial Literacy Assessment** - Lusardi-Mitchell validated questions (1 minute)
- ✅ **Adaptive Responses** - Agent adapts to your literacy level
- ✅ **Deterministic Scoring** - Clear, algorithmic assessment (no LLM guessing)
- ✅ **Basic chat interface** with Gemini 2.5
- ✅ **Conversation history** - Maintains context throughout the chat
- ✅ **Greek language** - Full Greek interface and responses
- ✅ **Greek context-aware** - Financial advice tailored to Greek households

### 📊 The Big 3 Assessment

When you start the app, it runs the **Lusardi-Mitchell Big 3** - the most widely-used financial literacy test globally (validated in 20+ countries):

**3 Questions (1 minute):**
1. 💰 **Compound Interest** - Understanding how money grows
2. 📉 **Inflation** - Impact on purchasing power  
3. 📊 **Risk Diversification** - Investment safety principles

**Deterministic Scoring:**
- **3/3 correct** → Προχωρημένο (Advanced) - Technical explanations, in-depth analysis
- **2/3 correct** → Μέτριο (Intermediate) - Moderate complexity, some technical terms
- **0-1/3 correct** → Αρχάριο (Beginner) - Simple language, explains all basic concepts

The agent uses your score to adapt its responses to your level!

## Testing

### Testing Framework

We use a simple but effective testing setup:

- **pytest** - Python testing framework for writing and running tests
- **pytest-cov** - Coverage plugin to measure test coverage
- **unittest.mock** - Python's built-in mocking library for isolating components

All tests mock Streamlit components, so they run fast without requiring a browser or UI rendering.

### Running Tests

#### Install dev dependencies
```bash
uv sync --extra dev
```

#### Run all tests
```bash
uv run pytest tests/ -v
```

#### Run with coverage report
```bash
uv run pytest tests/ --cov=src/finlit_agent/ui --cov-report=term-missing
```

#### Run specific test file
```bash
uv run pytest tests/ui/test_config.py
```

#### Run specific test
```bash
uv run pytest tests/ui/test_config.py::test_page_config_exists
```

### Test Coverage

Current coverage: **75%** ✅

**Core Modules:**
- `agent.py`: 100%
- `literacy_assessment.py`: 60%

**UI Modules:**
- `config.py`: 100%
- `session_state.py`: 100%
- `assessment_ui.py`: 95%
- `chat_ui.py`: 55%

**Total: 51 tests**

### What We Test

Our tests validate:
- ✅ **Agent creation** - API key handling, model configuration
- ✅ **Assessment logic** - Big 3 questions, scoring, level calculation
- ✅ **Configuration** - Constants are properly defined
- ✅ **Session state** - Initialization works correctly
- ✅ **Assessment UI** - Renders questions and results
- ✅ **Chat UI** - Handles messages and user input

Tests are kept **simple and focused** - each test validates one specific behavior.


## Next Steps

This is a basic starting point. You can progressively add:
- Custom tools for financial calculations
- RAG for Greek financial regulations
- Memory persistence across sessions
- Structured output for financial plans
- Multi-agent workflows
