"""Simple Streamlit UI for Greek Financial Literacy Agent."""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Import existing logic
from finlit_agent.literacy_assessment import FinancialLiteracyAssessment
from finlit_agent.main import BASE_SYSTEM_PROMPT, create_financial_agent

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Ελληνικός Βοηθός Οικονομικού Εγγραμματισμού",
    page_icon="💰",
    layout="centered"
)

# Initialize session state
if "assessment_done" not in st.session_state:
    st.session_state.assessment_done = False
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.messages = []
    st.session_state.agent = None

# Title
st.title("💰 Ελληνικός Βοηθός Οικονομικού Εγγραμματισμού")

# Assessment phase
if not st.session_state.assessment_done:
    st.markdown("### 📊 Αξιολόγηση Οικονομικού Εγγραμματισμού (Big 3)")
    
    assessment = FinancialLiteracyAssessment()
    questions = assessment.QUESTIONS
    
    if st.session_state.current_question < len(questions):
        q = questions[st.session_state.current_question]
        
        st.write(f"**Ερώτηση {st.session_state.current_question + 1}/3:**")
        st.write(q['question'])
        st.write("")
        
        # Radio buttons for answer
        option_labels = q['options']
        option_values = [opt[0] for opt in option_labels]
        
        answer = st.radio(
            "Επίλεξε την απάντησή σου:",
            options=option_values,
            format_func=lambda x: next(opt for opt in option_labels if opt.startswith(x)),
            key=f"q_{st.session_state.current_question}"
        )
        
        if st.button("Επόμενο", type="primary"):
            # Score answer
            is_correct = (answer == q['correct'])
            if is_correct:
                st.session_state.score += 1
            
            # Store answer
            st.session_state.answers[q['id']] = {
                'user_answer': answer,
                'correct_answer': q['correct'],
                'is_correct': is_correct,
                'explanation': q['explanation']
            }
            
            st.session_state.current_question += 1
            st.rerun()
    
    else:
        # Show results
        assessment.score = st.session_state.score
        assessment.answers = st.session_state.answers
        level = assessment._calculate_level(st.session_state.score)
        
        st.success("✅ Αξιολόγηση ολοκληρώθηκε!")
        st.metric("Επίπεδο", assessment.LEVEL_NAMES[level], f"{st.session_state.score}/3")
        
        with st.expander("📋 Δες τα αποτελέσματα"):
            for q_id, ans in st.session_state.answers.items():
                icon = "✅" if ans['is_correct'] else "❌"
                st.write(f"{icon} Ερώτηση {q_id}: {ans['explanation']}")
        
        if st.button("🚀 Ξεκίνα τη Συζήτηση", type="primary"):
            # Initialize agent with context
            st.session_state.agent = create_financial_agent()
            system_prompt = BASE_SYSTEM_PROMPT + assessment.get_context_summary()
            st.session_state.messages = [SystemMessage(content=system_prompt)]
            st.session_state.assessment_done = True
            st.rerun()

# Chat phase
else:
    # Display chat messages (skip system message)
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.write(msg.content)
    
    # Chat input
    if prompt := st.chat_input("Γράψε την ερώτησή σου..."):
        # Show user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add to history
        st.session_state.messages.append(HumanMessage(content=prompt))
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Σκέφτομαι..."):
                try:
                    response = st.session_state.agent.invoke(st.session_state.messages)
                    st.write(response.content)
                    st.session_state.messages.append(AIMessage(content=response.content))
                except Exception as e:
                    st.error(f"Σφάλμα: {str(e)}")

