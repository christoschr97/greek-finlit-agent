from dataclasses import dataclass

@dataclass
class LoanClassificationResponse:
    """Structured response for loan classification."""
    
    loan_type: str  # mortgage, personal, auto, student, business, unknown
    confidence: float  # 0.0 to 1.0
    reasoning: str  # Brief explanation of classification
    next_question: str | None = None  # Optional clarifying question if confidence is low