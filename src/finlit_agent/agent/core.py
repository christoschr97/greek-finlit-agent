"""
Core Agent Implementation

Contains the main FinancialAgent class and related functionality.
"""

import logging
from typing import Optional

from smolagents import CodeAgent, DuckDuckGoSearchTool, PythonInterpreterTool
from smolagents.models import LiteLLMModel

# Configure logging
logger = logging.getLogger(__name__)


class FinancialAgent:
    """A financial literacy agent for personal finance management."""
    
    def __init__(self, model_name: str = "ollama/gemma3:12b", ollama_base_url: str = "http://localhost:11434"):
        """
        Initialize the Financial Literacy Agent.
        
        Args:
            model_name: The Ollama model name (default: gemma3:12b)
            ollama_base_url: The Ollama server URL (default: http://localhost:11434)
        """
        self.model_name = model_name
        self.ollama_base_url = ollama_base_url
        self.agent = None
        self._setup_agent()
    
    def _setup_agent(self):
        """Setup the agent with the specified model and tools."""
        try:
            # Configure the LiteLLM model for Ollama
            model = LiteLLMModel(
                model_id=self.model_name,
                api_base=self.ollama_base_url
            )
            
            # Define tools for the agent
            tools = [
                DuckDuckGoSearchTool(),  # For searching financial information
                PythonInterpreterTool(),  # For financial calculations
            ]
            
            # Create the agent (CodeAgent doesn't take system_prompt directly)
            self.agent = CodeAgent(
                tools=tools,
                model=model
            )
            
            # Set up the system instructions as part of the agent's context
            self.system_instructions = """
            Είσαι ένας εξειδικευμένος σύμβουλος χρηματοοικονομικής παιδείας για ελληνικά νοικοκυριά. 
            Η αποστολή σου είναι να βοηθάς τους Έλληνες πολίτες να:

            1. Κατανοήσουν βασικές έννοιες χρηματοοικονομικής παιδείας
            2. Δημιουργήσουν και να διαχειρίζονται προϋπολογισμούς
            3. Λάβουν αποφάσεις για αποταμίευση και επένδυση
            4. Κατανοήσουν τα ελληνικά φορολογικά και ασφαλιστικά συστήματα
            5. Σχεδιάσουν τη συνταξιοδότησή τους
            6. Διαχειρίζονται χρέη και πιστώσεις

            Παρέχεις πρακτικές συμβουλές που λαμβάνουν υπόψη:
            - Την ελληνική οικονομική πραγματικότητα
            - Τους ελληνικούς μισθούς και το κόστος ζωής
            - Τις φορολογικές υποχρεώσεις στην Ελλάδα
            - Τις διαθέσιμες επενδυτικές επιλογές για Έλληνες πολίτες

            Απαντάς στα ελληνικά και χρησιμοποιείς απλή, κατανοητή γλώσσα. Όταν κάνεις υπολογισμούς,
            εξηγείς τη διαδικασία βήμα προς βήμα.
            """.strip()
            
            logger.info(f"Agent initialized successfully with model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise
    
    def chat(self, message: str) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            message: The user's message
            
        Returns:
            The agent's response
        """
        if not self.agent:
            raise RuntimeError("Agent not initialized")
        
        try:
            # Combine system instructions with user message
            full_message = f"{self.system_instructions}\n\nQuestion: {message}"
            response = self.agent.run(full_message)
            return response
        except Exception as e:
            logger.error(f"Error during chat: {e}")
            return f"Sorry, there was an error: {e}"
    
    def start_interactive_session(self):
        """Start an interactive chat session with the agent."""
        print("🏛️ Γεια σας! Είμαι ο ψηφιακός σας σύμβουλος χρηματοοικονομικής παιδείας.")
        print("Μπορώ να σας βοηθήσω με ερωτήσεις σχετικά με:")
        print("• Προϋπολογισμό και διαχείριση χρημάτων")
        print("• Αποταμίευση και επενδύσεις")
        print("• Φόρους και ασφάλειες")
        print("• Συνταξιοδότηση")
        print("• Δάνεια και πιστώσεις")
        print("\nΓράψτε 'exit' για έξοδο.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['exit', 'έξοδος', 'quit']:
                    print("Αντίο! Καλή επιτυχία με τα οικονομικά σας! 💰")
                    break
                
                if not user_input:
                    continue
                
                print("Agent: ", end="", flush=True)
                response = self.chat(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n\nΑντίο! Καλή επιτυχία με τα οικονομικά σας! 💰")
                break
            except Exception as e:
                print(f"Error: {e}")
