"""
Loan Information Service

Provides information about different loan types in Greek.
Handles loan names, explanations, examples, and common terminology.
"""

from typing import Dict, Optional


class LoanInformationService:
    """Service for retrieving loan type information and explanations."""
    
    # Loan types in Greek
    LOAN_TYPES_GR = {
        "mortgage": "Στεγαστικό Δάνειο",
        "personal": "Προσωπικό Δάνειο",
        "auto": "Δάνειο Αυτοκινήτου",
        "student": "Φοιτητικό Δάνειο",
        "business": "Επιχειρηματικό Δάνειο",
        "unknown": "Άγνωστο"
    }
    
    # Default loan terms by loan type (in years)
    DEFAULT_TERMS = {
        "mortgage": 20,
        "personal": 5,
        "auto": 5,
        "student": 10,
        "business": 5,
        "unknown": 5
    }
    
    # Default interest rates by loan type (annual, as decimal)
    DEFAULT_INTEREST_RATES = {
        "mortgage": 0.03,  # 3%
        "personal": 0.07,  # 7%
        "auto": 0.05,      # 5%
        "student": 0.04,   # 4%
        "business": 0.06,  # 6%
        "unknown": 0.05    # 5%
    }
    
    def get_loan_name(self, loan_type: str) -> str:
        """
        Get the Greek name for a loan type.
        
        Args:
            loan_type: Loan type identifier (e.g., "mortgage", "personal")
            
        Returns:
            Greek name of the loan type
        """
        return self.LOAN_TYPES_GR.get(loan_type, loan_type)
    
    def get_default_term(self, loan_type: str) -> int:
        """
        Get the default loan term (in years) for a loan type.
        
        Args:
            loan_type: Loan type identifier
            
        Returns:
            Default loan term in years
        """
        return self.DEFAULT_TERMS.get(loan_type, self.DEFAULT_TERMS["unknown"])
    
    def get_default_interest_rate(self, loan_type: str) -> float:
        """
        Get the default interest rate for a loan type.
        
        Args:
            loan_type: Loan type identifier
            
        Returns:
            Annual interest rate as decimal (e.g., 0.05 for 5%)
        """
        return self.DEFAULT_INTEREST_RATES.get(loan_type, self.DEFAULT_INTEREST_RATES["unknown"])
    
    def get_loan_explanation(self, loan_type: str) -> Optional[Dict[str, str]]:
        """
        Get detailed explanation for a loan type.
        
        Args:
            loan_type: Loan type identifier
            
        Returns:
            Dictionary with 'title', 'description', 'key_points', 'tip', and optional 'example'
        """
        explanations = {
            "mortgage": {
                "title": "Στεγαστικό Δάνειο",
                "description": "**Τι είναι;** Δανείζεσαι χρήματα για να αγοράσεις σπίτι.",
                "key_points": """
**Βασικά που πρέπει να ξέρεις:**
- 📅 **Διάρκεια:** Συνήθως 15-30 χρόνια
- 💰 **Προκαταβολή:** Χρειάζεσαι 10-20% από την αξία του σπιτιού
- 🏦 **Τόκος:** Το επιπλέον ποσό που πληρώνεις στην τράπεζα
- 📊 **Δόση:** Το ποσό που πληρώνεις κάθε μήνα
                """,
                "tip": "💡 **Tip:** Μην ξεπερνάς το 30-35% του μηνιαίου εισοδήματός σου σε δόση!",
                "example": """
**Σενάριο:** Θέλεις σπίτι 100,000€
- Προκαταβολή (20%): 20,000€
- Δάνειο: 80,000€
- Επιτόκιο: 3% ετησίως
- Διάρκεια: 20 χρόνια
- **Μηνιαία δόση: ~444€**
                """
            },
            "personal": {
                "title": "Προσωπικό Δάνειο",
                "description": "**Τι είναι;** Δανείζεσαι χρήματα για προσωπική χρήση (έπιπλα, διακοπές, κλπ).",
                "key_points": """
**Βασικά που πρέπει να ξέρεις:**
- 📅 **Διάρκεια:** Συνήθως 1-7 χρόνια
- 💰 **Ποσά:** Από 1,000€ έως 50,000€
- 🏦 **Τόκος:** Συνήθως ψηλότερος από στεγαστικό
- ⚡ **Ταχύτητα:** Εγκρίνεται γρήγορα
                """,
                "tip": "⚠️ **Προσοχή:** Μόνο για πραγματικές ανάγκες, όχι για καταναλωτισμό!"
            },
            "auto": {
                "title": "Δάνειο Αυτοκινήτου",
                "description": "**Τι είναι;** Δανείζεσαι για να αγοράσεις όχημα.",
                "key_points": """
**Βασικά που πρέπει να ξέρεις:**
- 📅 **Διάρκεια:** Συνήθως 3-7 χρόνια
- 💰 **Προκαταβολή:** Συνήθως 10-30%
- 🚗 **Εξασφάλιση:** Το αυτοκίνητο είναι εγγύηση
- 📊 **Αξία:** Το αυτοκίνητο χάνει αξία με τον καιρό!
                """,
                "tip": "💡 **Tip:** Υπολόγισε και τα έξοδα (ασφάλεια, συντήρηση, καύσιμα)!"
            },
            "student": {
                "title": "Φοιτητικό Δάνειο",
                "description": "**Τι είναι;** Δανείζεσαι για σπουδές.",
                "key_points": """
**Βασικά που πρέπει να ξέρεις:**
- 📅 **Αποπληρωμή:** Ξεκινάει μετά τις σπουδές
- 💰 **Επιτόκιο:** Συνήθως πιο χαμηλό
- 🎓 **Χρήση:** Μόνο για εκπαίδευση
- ⏰ **Χάρις περίοδος:** Μήνες πριν αρχίσεις να πληρώνεις
                """
            },
            "business": {
                "title": "Επιχειρηματικό Δάνειο",
                "description": "**Τι είναι;** Δανείζεσαι για την επιχείρησή σου.",
                "key_points": """
**Βασικά που πρέπει να ξέρεις:**
- 📊 **Business Plan:** Χρειάζεσαι σχέδιο επιχείρησης
- 💰 **Εξασφάλιση:** Συχνά χρειάζονται εγγυήσεις
- 📈 **Ρίσκο:** Υψηλότερο από προσωπικό
- 🏦 **Τόκος:** Εξαρτάται από την επιχείρηση
                """
            }
        }
        
        return explanations.get(loan_type)
    
    def get_common_terms(self) -> Dict[str, Dict[str, str]]:
        """
        Get common financial terms explanations.
        
        Returns:
            Dictionary with term categories and their explanations
        """
        return {
            "col1": {
                "interest_rate": """
**Επιτόκιο (Interest Rate)**  
Το ποσοστό που πληρώνεις επιπλέον. Όσο πιο χαμηλό, τόσο καλύτερα!

**Δόση (Installment)**  
Το ποσό που πληρώνεις κάθε μήνα.
                """,
            },
            "col2": {
                "term_and_apr": """
**Διάρκεια (Term)**  
Πόσα χρόνια θα πληρώνεις. Περισσότερα χρόνια = μικρότερη δόση αλλά περισσότεροι τόκοι!

**ΤΑΕ (APR)**  
Το πραγματικό κόστος με όλα τα έξοδα.
                """
            }
        }

