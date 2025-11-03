import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from .services.affordability_service import AffordabilityService
from .services.loan_plan_generator_service import LoanPlanGeneratorService

# Base system prompt for the financial literacy agent
BASE_SYSTEM_PROMPT = """Είσαι ένας χρήσιμος βοηθός οικονομικού αλφαβητισμού που ειδικεύεται στα 
προσωπικά οικονομικά για ελληνικά νοικοκυριά. Παρέχεις σαφείς και πρακτικές συμβουλές 
για προϋπολογισμό, αποταμίευση, επενδύσεις, διαχείριση χρέους και γενικό οικονομικό 
σχεδιασμό. Εξηγείς τις έννοιες με απλούς όρους και δίνεις παραδείγματα σχετικά με 
το ελληνικό πλαίσιο όταν είναι κατάλληλο. Απαντάς πάντα στα ελληνικά.

"""

@tool
def analyze_affordability(financial_data: dict, metrics: dict) -> dict:
    """
    Analyze loan affordability based on financial data and metrics.
    
    Args:
        financial_data: Dictionary with loan_amount, savings, etc.
        metrics: Dictionary with payment_ratio, disposable_income, estimated_payment.
    
    Returns:
        Dictionary with status, recommendations, and metrics.
    """
    service = AffordabilityService()
    return service.analyze_affordability(financial_data, metrics)

@tool
def generate_loan_plans(total_amount: float, loan_type: str, monthly_income: float) -> list:
    """
    Generate multiple loan plan options with different terms and down payments.
    
    Args:
        total_amount: Total amount needed for the loan (before down payment).
        loan_type: Type of loan (mortgage, personal, auto, student, business).
        monthly_income: User's monthly income for affordability calculation.
    
    Returns:
        List of loan plan dictionaries with details like monthly payment, total cost, etc.
    """
    service = LoanPlanGeneratorService()
    plans = service.generate_loan_options(total_amount, loan_type, monthly_income)
    # Convert dataclass to dict for JSON serialization
    return [plan.__dict__ for plan in plans]

def create_financial_agent(system_prompt: str):
    """
    Initialize the Gemini chat agent with financial expertise and tools.
    
    Args:
        system_prompt: The system prompt for the agent.
    
    Returns:
        Agent: Configured LangChain agent
        
    Raises:
        ValueError: If GOOGLE_API_KEY is not found in environment
    """
    # Check if API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("Το GOOGLE_API_KEY δεν βρέθηκε. Παρακαλώ ορίστε το στο αρχείο .env")
    
    # Initialize Gemini 2.5 Flash
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        google_api_key=api_key
    )
    
    # Create agent with tools
    agent = create_agent(
        model=model,
        tools=[analyze_affordability, generate_loan_plans],
        system_prompt=system_prompt
    )
    
    return agent

