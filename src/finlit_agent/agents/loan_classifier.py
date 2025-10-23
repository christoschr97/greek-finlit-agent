import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from finlit_agent.schemas.responses import LoanClassificationResponse
from finlit_agent.prompts.templates import LOAN_CLASSIFIER_SYSTEM_PROMPT

def create_loan_classifier_agent(model_name: str = "google_genai:gemini-2.5-flash-lite"):
    """
    Create Agent 1: Loan Type Classifier
    
    Uses LangChain v1.0 create_agent API with structured output.
    
    Args:
        model_name: LLM model identifier
        
    Returns:
        Configured agent that classifies loan types
    """

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set")

    # Initialize model with appropriate settings
    model = init_chat_model(
        model_name,
        temperature=0.3,  # Low temperature for consistent classification
        timeout=10,
        max_tokens=500  # Short responses for classification
    )
    
    # Create agent with structured output
    agent = create_agent(
        model=model,
        system_prompt=LOAN_CLASSIFIER_SYSTEM_PROMPT,
        response_format=LoanClassificationResponse,
        tools=[]  # No tools needed for classification
    )
    
    return agent


def classify_loan_request(agent, user_input: str) -> dict:
    """
    Run the loan classifier agent on user input.
    
    Args:
        agent: The loan classifier agent
        user_input: User's description of what they need
        
    Returns:
        dict with classification results
    """
    try:
        response = agent.invoke({
            "messages": [{"role": "user", "content": user_input}]
        })
        
        # Extract structured response
        result = response.get('structured_response')
        
        return {
            "success": True,
            "loan_type": result.loan_type,
            "confidence": result.confidence,
            "reasoning": result.reasoning,
            "next_question": result.next_question,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "loan_type": "unknown",
            "confidence": 0.0,
            "reasoning": "",
            "next_question": None,
            "error": str(e)
        }