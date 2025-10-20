"""
Financial Literacy Assessment - Lusardi-Mitchell "Big 3"

The most widely-used short financial literacy test globally.
Used in 20+ countries, validated across diverse populations.

Reference: Lusardi, A., & Mitchell, O. S. (2011). 
Financial literacy around the world: An overview.
"""

from typing import Tuple
from enum import Enum


class LiteracyLevel(Enum):
    """Financial literacy levels based on Big 3 score."""
    BEGINNER = 1      # 0-1 correct (Αρχάριο)
    INTERMEDIATE = 2  # 2 correct (Μέτριο)
    ADVANCED = 3      # 3 correct (Προχωρημένο)


class FinancialLiteracyAssessment:
    """
    Lusardi-Mitchell Big 3 Financial Literacy Questions.
    
    These 3 questions predict ~80% of financial literacy variance
    and have been validated in over 20 countries.
    
    Questions assess:
    1. Compound Interest (numeracy + interest understanding)
    2. Inflation (purchasing power)
    3. Risk Diversification (investment principle)
    """
    
    # Constants
    LEVEL_NAMES = {
        LiteracyLevel.BEGINNER: "Αρχάριο",
        LiteracyLevel.INTERMEDIATE: "Μέτριο",
        LiteracyLevel.ADVANCED: "Προχωρημένο"
    }
    
    DIMENSION_NAMES = {
        'compound_interest': 'Ανατοκισμός',
        'inflation': 'Πληθωρισμός',
        'risk_diversification': 'Διαφοροποίηση Κινδύνου'
    }
    
    SEPARATOR_LENGTH = 70
    
    # The Big 3 Questions (Greek adaptation)
    QUESTIONS = [
        {
            "id": 1,
            "dimension": "compound_interest",
            "question": "Υπόθεσε ότι έχεις 100€ σε λογαριασμό ταμιευτηρίου με επιτόκιο 2% το χρόνο. Μετά από 5 χρόνια, πόσα χρήματα θα έχεις στον λογαριασμό αν τα αφήσεις εκεί;",
            "options": [
                "a) Περισσότερα από 102€",
                "b) Ακριβώς 102€",
                "c) Λιγότερα από 102€",
                "d) Δεν ξέρω"
            ],
            "correct": "a",
            "explanation": "Με ανατοκισμό, τα χρήματα θα είναι περισσότερα από 102€ (περίπου 110,40€)."
        },
        {
            "id": 2,
            "dimension": "inflation",
            "question": "Φαντάσου ότι το επιτόκιο στον λογαριασμό ταμιευτηρίου σου είναι 1% το χρόνο και ο πληθωρισμός είναι 2% το χρόνο. Μετά από 1 χρόνο, με τα χρήματα σε αυτόν τον λογαριασμό θα μπορείς να αγοράσεις:",
            "options": [
                "a) Περισσότερα από ό,τι σήμερα",
                "b) Ακριβώς τα ίδια",
                "c) Λιγότερα από ό,τι σήμερα",
                "d) Δεν ξέρω"
            ],
            "correct": "c",
            "explanation": "Με πληθωρισμό 2% και επιτόκιο 1%, η αγοραστική δύναμη μειώνεται."
        },
        {
            "id": 3,
            "dimension": "risk_diversification",
            "question": "Η παρακάτω πρόταση είναι αληθής ή ψευδής; 'Η αγορά μετοχών μιας μόνο εταιρείας συνήθως παρέχει πιο ασφαλή απόδοση από ένα αμοιβαίο κεφάλαιο μετοχών'",
            "options": [
                "a) Αληθής",
                "b) Ψευδής",
                "c) Δεν ξέρω"
            ],
            "correct": "b",
            "explanation": "Η διαφοροποίηση (πολλές μετοχές) μειώνει τον κίνδυνο - άρα η πρόταση είναι ψευδής."
        }
    ]
    
    def __init__(self):
        """Initialize assessment."""
        self.score = 0
        self.answers = {}
    
    def record_answer(self, question_id: int, user_answer: str) -> bool:
        """
        Record a user's answer to a question.
        
        Args:
            question_id: The ID of the question (1-3)
            user_answer: The user's answer (a, b, c, or d)
            
        Returns:
            bool: True if answer was correct, False otherwise
        """
        # Find the question
        question = next((q for q in self.QUESTIONS if q['id'] == question_id), None)
        if not question:
            raise ValueError(f"Invalid question_id: {question_id}")
        
        # Score the answer
        is_correct = (user_answer == question['correct'])
        if is_correct:
            self.score += 1
        
        # Store the answer
        self.answers[question_id] = {
            'question': question['question'],
            'user_answer': user_answer,
            'correct_answer': question['correct'],
            'is_correct': is_correct,
            'explanation': question['explanation']
        }
        
        return is_correct
    
    def get_level(self) -> LiteracyLevel:
        """
        Get the user's literacy level based on current score.
        
        Returns:
            LiteracyLevel: The calculated literacy level
        """
        return self._calculate_level(self.score)
    
    def get_level_name(self) -> str:
        """
        Get the user's literacy level name in Greek.
        
        Returns:
            str: The Greek name of the literacy level
        """
        level = self.get_level()
        return self.LEVEL_NAMES[level]
    
    def assess_user(self) -> Tuple[int, LiteracyLevel, dict]:
        """
        Run the Big 3 assessment.
        
        Returns:
            - score (0-3)
            - literacy_level (Enum)
            - details (dict with answers and explanations)
        """
        print(f"\n{'='*self.SEPARATOR_LENGTH}")
        print("📊 ΑΞΙΟΛΟΓΗΣΗ ΟΙΚΟΝΟΜΙΚΟΥ ΕΓΓΡΑΜΜΑΤΙΣΜΟΥ")
        print(f"{'='*self.SEPARATOR_LENGTH}")
        print("Θα απαντήσεις σε 3 γρήγορες ερωτήσεις (1 λεπτό)")
        print("Βασισμένο στο Lusardi-Mitchell Big 3 - διεθνές πρότυπο")
        print(f"{'='*self.SEPARATOR_LENGTH}\n")
        
        for i, q in enumerate(self.QUESTIONS, 1):
            print(f"Ερώτηση {i}/3:")
            print(f"{q['question']}\n")
            
            for option in q['options']:
                print(f"  {option}")
            
            # Get answer with validation
            while True:
                answer = input("\nΑπάντηση (a, b, c ή d): ").strip().lower()
                valid_options = [opt[0] for opt in q['options']]
                if answer in valid_options:
                    break
                print(f"❌ Μη έγκυρη επιλογή. Διάλεξε {', '.join(valid_options)}")
            
            # Score the answer (deterministic)
            is_correct = (answer == q['correct'])
            if is_correct:
                self.score += 1
            
            self.answers[q['id']] = {
                'question': q['question'],
                'user_answer': answer,
                'correct_answer': q['correct'],
                'is_correct': is_correct,
                'explanation': q['explanation']
            }
            
            print()  # Empty line
        
        # Determine literacy level
        literacy_level = self._calculate_level(self.score)
        
        return self.score, literacy_level, self.answers
    
    def _calculate_level(self, score: int) -> LiteracyLevel:
        """Determine literacy level from score (0-3)."""
        if score >= 3:
            return LiteracyLevel.ADVANCED
        elif score >= 2:
            return LiteracyLevel.INTERMEDIATE
        else:
            return LiteracyLevel.BEGINNER
    
    def get_context_summary(self) -> str:
        """Generate context summary for LLM system prompt."""
        level = self._calculate_level(self.score)
        
        correct_dims = []
        incorrect_dims = []
        
        for q in self.QUESTIONS:
            if self.answers[q['id']]['is_correct']:
                correct_dims.append(self.DIMENSION_NAMES[q['dimension']])
            else:
                incorrect_dims.append(self.DIMENSION_NAMES[q['dimension']])
        
        summary = f"""
ΕΠΙΠΕΔΟ ΟΙΚΟΝΟΜΙΚΟΥ ΕΓΓΡΑΜΜΑΤΙΣΜΟΥ: {self.LEVEL_NAMES[level]} ({self.score}/3)

Αποτελέσματα Big 3 Assessment (Lusardi-Mitchell):
• Σκορ: {self.score}/3 σωστές απαντήσεις
• Κατανοεί: {', '.join(correct_dims) if correct_dims else 'Καμία περιοχή ακόμα'}
• Χρειάζεται βοήθεια: {', '.join(incorrect_dims) if incorrect_dims else 'Εξαιρετική κατανόηση'}

ΟΔΗΓΙΕΣ ΠΡΟΣΑΡΜΟΓΗΣ:
{self._get_instructions(level)}

Προσάρμοσε τις απαντήσεις σου στο επίπεδο {self.LEVEL_NAMES[level]} του χρήστη.
"""
        return summary.strip()
    
    def _get_instructions(self, level: LiteracyLevel) -> str:
        """Get LLM instructions based on literacy level."""
        instructions = {
            LiteracyLevel.BEGINNER: (
                "- Χρησιμοποίησε ΠΟΛΥ απλή γλώσσα\n"
                "- Εξήγησε ΟΛΕΣ τις βασικές έννοιες (επιτόκιο, πληθωρισμό, κίνδυνο)\n"
                "- Δώσε συγκεκριμένα παραδείγματα με αριθμούς\n"
                "- Αποφυγε εντελώς τεχνικούς όρους\n"
                "- Εστίασε στα θεμελιώδη"
            ),
            LiteracyLevel.INTERMEDIATE: (
                "- Χρησιμοποίησε απλή γλώσσα\n"
                "- Εξήγησε νέες έννοιες όταν τις εισάγεις\n"
                "- Δώσε πρακτικά παραδείγματα\n"
                "- Μπορείς να χρησιμοποιήσεις βασικούς οικονομικούς όρους με εξηγήσεις\n"
                "- Χτίσε πάνω στην υπάρχουσα γνώση"
            ),
            LiteracyLevel.ADVANCED: (
                "- Μπορείς να χρησιμοποιήσεις οικονομικούς όρους\n"
                "- Πήγαινε σε βάθος στην ανάλυση\n"
                "- Υπόθεσε καλή κατανόηση βασικών εννοιών\n"
                "- Εστίασε σε προχωρημένα θέματα και βελτιστοποίηση\n"
                "- Προσφέρε εξειδικευμένες συμβουλές"
            )
        }
        return instructions[level]
    
    def get_short_summary(self) -> str:
        """Get short one-line summary."""
        level = self._calculate_level(self.score)
        return f"Επίπεδο: {self.LEVEL_NAMES[level]} ({self.score}/3 σωστές απαντήσεις)"
    
    def show_results(self):
        """Display detailed results with explanations."""
        print(f"\n{'='*self.SEPARATOR_LENGTH}")
        print("📋 ΑΠΟΤΕΛΕΣΜΑΤΑ & ΕΞΗΓΗΣΕΙΣ")
        print(f"{'='*self.SEPARATOR_LENGTH}\n")
        
        for q_id, answer_data in self.answers.items():
            status = "✅ Σωστό" if answer_data['is_correct'] else "❌ Λάθος"
            print(f"Ερώτηση {q_id}: {status}")
            
            if not answer_data['is_correct']:
                print(f"  Η σωστή απάντηση είναι: {answer_data['correct_answer']}")
            
            print(f"  💡 {answer_data['explanation']}\n")
        
        print(f"{'='*self.SEPARATOR_LENGTH}")

