"""
Basic Financial Agent with LangChain and Gemini 2.5
A simple chat interface for financial literacy questions.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from finlit_agent.literacy_assessment import FinancialLiteracyAssessment

# Load environment variables
load_dotenv()

# Constants
SEPARATOR_LENGTH = 60
EXIT_COMMANDS = ['quit', 'exit', 'bye', 'έξοδος', 'τέλος']
BASE_SYSTEM_PROMPT = """Είσαι ένας χρήσιμος βοηθός οικονομικού αλφαβητισμού που ειδικεύεται στα 
προσωπικά οικονομικά για ελληνικά νοικοκυριά. Παρέχεις σαφείς και πρακτικές συμβουλές 
για προϋπολογισμό, αποταμίευση, επενδύσεις, διαχείριση χρέους και γενικό οικονομικό 
σχεδιασμό. Εξηγείς τις έννοιες με απλούς όρους και δίνεις παραδείγματα σχετικά με 
το ελληνικό πλαίσιο όταν είναι κατάλληλο. Απαντάς πάντα στα ελληνικά.

"""


def create_financial_agent():
    """Initialize the Gemini chat model with financial expertise."""
    
    # Check if API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("Το GOOGLE_API_KEY δεν βρέθηκε. Παρακαλώ ορίστε το στο αρχείο .env")
    
    # Initialize Gemini 2.5 (using gemini-2.0-flash-exp for latest features)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0.7,
        google_api_key=api_key
    )
    
    return llm


def chat_loop():
    """Simple chat loop for interacting with the financial agent."""
    
    print(f"{'='*SEPARATOR_LENGTH}")
    print("Ελληνικός Βοηθός Οικονομικού Εγγραμματισμού")
    print(f"{'='*SEPARATOR_LENGTH}")
    print("Καλώς ήρθες! Είμαι εδώ για να σε βοηθήσω με τα οικονομικά σου.")
    print(f"{'='*SEPARATOR_LENGTH}")
    print()
    
    # Run Big 3 financial literacy assessment
    print("Πριν ξεκινήσουμε, θα κάνουμε μια γρήγορη αξιολόγηση...")
    print()
    
    assessment = FinancialLiteracyAssessment()
    score, literacy_level, details = assessment.assess_user()
    
    # Show results
    print(f"{'='*SEPARATOR_LENGTH}")
    print("✅ Ολοκληρώθηκε!")
    print(f"{'='*SEPARATOR_LENGTH}")
    print(f"📊 {assessment.get_short_summary()}")
    
    # Show explanations
    assessment.show_results()
    
    print("\nΤώρα μπορούμε να ξεκινήσουμε! Οι απαντήσεις μου θα είναι")
    print("προσαρμοσμένες στο επίπεδό σου.")
    print("\nΠληκτρολογήστε 'quit' ή 'exit' για να τερματίσετε τη συζήτηση.")
    print(f"{'='*SEPARATOR_LENGTH}")
    print()
    
    # Initialize the agent
    agent = create_financial_agent()
    
    # System message with literacy context
    system_prompt = BASE_SYSTEM_PROMPT + assessment.get_context_summary()
    system_message = SystemMessage(content=system_prompt)
    
    # Chat history (including system message)
    chat_history = [system_message]
    
    while True:
        # Get user input
        user_input = input("Εσείς: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in EXIT_COMMANDS:
            print("\nΣας ευχαριστώ που χρησιμοποιήσατε τον Βοηθό Οικονομικού Εγγραμματισμού. Αντίο!")
            break
        
        # Add user message to history
        chat_history.append(HumanMessage(content=user_input))
        
        try:
            # Get response from agent
            response = agent.invoke(chat_history)
            
            # Add AI response to history
            chat_history.append(AIMessage(content=response.content))
            
            # Display response
            print(f"\nΒοηθός: {response.content}\n")
            
        except Exception as e:
            print(f"\nΣφάλμα: {str(e)}\n")
            # Remove the last user message if there was an error
            chat_history.pop()


def main():
    """Main entry point."""
    try:
        chat_loop()
    except KeyboardInterrupt:
        print("\n\nΗ συνεδρία διακόπηκε. Αντίο!")
    except Exception as e:
        print(f"\nΠαρουσιάστηκε σφάλμα: {str(e)}")


if __name__ == "__main__":
    main()
