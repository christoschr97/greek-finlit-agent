"""
Shared agent configuration and initialization.
Used by both CLI (main.py) and Streamlit (app.py) interfaces.
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Base system prompt for the financial literacy agent
BASE_SYSTEM_PROMPT = """Είσαι ένας χρήσιμος βοηθός οικονομικού αλφαβητισμού που ειδικεύεται στα 
προσωπικά οικονομικά για ελληνικά νοικοκυριά. Παρέχεις σαφείς και πρακτικές συμβουλές 
για προϋπολογισμό, αποταμίευση, επενδύσεις, διαχείριση χρέους και γενικό οικονομικό 
σχεδιασμό. Εξηγείς τις έννοιες με απλούς όρους και δίνεις παραδείγματα σχετικά με 
το ελληνικό πλαίσιο όταν είναι κατάλληλο. Απαντάς πάντα στα ελληνικά.

"""

def create_financial_agent():
    """
    Initialize the Gemini chat model with financial expertise.
    
    Returns:
        ChatGoogleGenerativeAI: Configured language model
        
    Raises:
        ValueError: If GOOGLE_API_KEY is not found in environment
    """
    # Check if API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("Το GOOGLE_API_KEY δεν βρέθηκε. Παρακαλώ ορίστε το στο αρχείο .env")
    
    # Initialize Gemini 2.5 (using gemini-2.0-flash-exp for latest features)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        google_api_key=api_key
    )
    
    return llm

