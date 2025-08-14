"""
Example usage of the Financial Literacy Agent.
"""

import sys
import os

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from finlit_agent.agent.core import FinancialAgent


def example_conversations():
    """Demonstrate the agent with example conversations."""
    
    # Initialize the agent
    print("Initializing Financial Literacy Agent...")
    agent = FinancialAgent()
    
    # Example questions in English
    example_questions = [
        "What is a budget and how do I create one?",
        "How much money should I save each month?",
        "What are the best investment options for someone starting out?",
        "How does the tax system work for employees?",
        "What do I need to get a mortgage loan?"
    ]
    
    print("\n" + "="*60)
    print("EXAMPLE CONVERSATIONS")
    print("="*60)
    
    for i, question in enumerate(example_questions, 1):
        print(f"\n{i}. Question: {question}")
        print("-" * 50)
        
        try:
            response = agent.chat(question)
            print(f"Answer: {response}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "-" * 50)


if __name__ == "__main__":
    example_conversations()
