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

```bash
uv run finlit-agent
```

Or:
```bash
python3 -m finlit_agent.main
```

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

## Next Steps

This is a basic starting point. You can progressively add:
- Custom tools for financial calculations
- RAG for Greek financial regulations
- Memory persistence across sessions
- Structured output for financial plans
- Multi-agent workflows
