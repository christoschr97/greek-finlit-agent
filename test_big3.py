"""
Demo: Lusardi-Mitchell Big 3 Financial Literacy Assessment

Shows the questions and scoring system without needing API keys.
"""

from src.finlit_agent.literacy_assessment import FinancialLiteracyAssessment, LiteracyLevel


def demo_big3():
    """Display the Big 3 questions and scoring logic."""
    
    assessment = FinancialLiteracyAssessment()
    sep = "="*assessment.SEPARATOR_LENGTH
    
    print(f"\n{sep}")
    print("📊 LUSARDI-MITCHELL BIG 3 - Demo")
    print(sep)
    print("\nThe most widely-used financial literacy test worldwide")
    print("Used in 20+ countries, validated across diverse populations\n")
    
    # Show the questions
    print("THE 3 QUESTIONS:")
    print(f"{'-'*assessment.SEPARATOR_LENGTH}")
    
    for i, q in enumerate(assessment.QUESTIONS, 1):
        print(f"\n{i}. {q['dimension'].replace('_', ' ').title()}")
        print(f"   {q['question']}\n")
        for opt in q['options']:
            marker = "✓" if opt[0] == q['correct'] else " "
            print(f"   [{marker}] {opt}")
        print(f"\n   💡 {q['explanation']}")
    
    # Show scoring
    print(f"\n{sep}")
    print("SCORING SYSTEM (100% Deterministic):")
    print(sep)
    
    scenarios = [
        (0, LiteracyLevel.BEGINNER),
        (1, LiteracyLevel.BEGINNER),
        (2, LiteracyLevel.INTERMEDIATE),
        (3, LiteracyLevel.ADVANCED)
    ]
    
    for score, expected_level in scenarios:
        level = assessment._calculate_level(score)
        greek_name = assessment.LEVEL_NAMES[level]
        print(f"\n{score}/3 correct → {greek_name} ({level.name})")
        print(f"  → Level: {level.name}")
    
    # Show what gets passed to LLM
    print(f"\n{sep}")
    print("CONTEXT PASSED TO LLM (Example for 2/3 score):")
    print(sep)
    
    # Simulate a 2/3 score
    assessment.score = 2
    assessment.answers = {
        1: {'is_correct': True, 'explanation': 'Correct'},
        2: {'is_correct': True, 'explanation': 'Correct'},
        3: {'is_correct': False, 'explanation': 'Wrong'}
    }
    
    print(f"\n{assessment.get_context_summary()}")
    
    print(f"\n{sep}")
    print("✅ Fast (1 minute), Deterministic, Research-Validated!")
    print(f"{sep}\n")


if __name__ == "__main__":
    demo_big3()

