"""
Tests for Loan Information Service.
"""

import pytest
from finlit_agent.services import LoanInformationService


@pytest.fixture
def service():
    """Create a LoanInformationService instance."""
    return LoanInformationService()


def test_get_loan_name_mortgage(service):
    """Test getting loan name for mortgage."""
    assert service.get_loan_name("mortgage") == "Στεγαστικό Δάνειο"


def test_get_loan_name_personal(service):
    """Test getting loan name for personal loan."""
    assert service.get_loan_name("personal") == "Προσωπικό Δάνειο"


def test_get_loan_name_auto(service):
    """Test getting loan name for auto loan."""
    assert service.get_loan_name("auto") == "Δάνειο Αυτοκινήτου"


def test_get_loan_name_student(service):
    """Test getting loan name for student loan."""
    assert service.get_loan_name("student") == "Φοιτητικό Δάνειο"


def test_get_loan_name_business(service):
    """Test getting loan name for business loan."""
    assert service.get_loan_name("business") == "Επιχειρηματικό Δάνειο"


def test_get_loan_name_unknown(service):
    """Test getting loan name for unknown type."""
    assert service.get_loan_name("unknown") == "Άγνωστο"


def test_get_loan_name_invalid_returns_input(service):
    """Test that invalid loan type returns the input."""
    assert service.get_loan_name("invalid_type") == "invalid_type"


def test_get_loan_explanation_mortgage(service):
    """Test getting explanation for mortgage."""
    explanation = service.get_loan_explanation("mortgage")
    
    assert explanation is not None
    assert explanation["title"] == "Στεγαστικό Δάνειο"
    assert "description" in explanation
    assert "key_points" in explanation
    assert "tip" in explanation
    assert "example" in explanation


def test_get_loan_explanation_personal(service):
    """Test getting explanation for personal loan."""
    explanation = service.get_loan_explanation("personal")
    
    assert explanation is not None
    assert explanation["title"] == "Προσωπικό Δάνειο"
    assert "description" in explanation
    assert "key_points" in explanation
    assert "tip" in explanation


def test_get_loan_explanation_auto(service):
    """Test getting explanation for auto loan."""
    explanation = service.get_loan_explanation("auto")
    
    assert explanation is not None
    assert explanation["title"] == "Δάνειο Αυτοκινήτου"


def test_get_loan_explanation_student(service):
    """Test getting explanation for student loan."""
    explanation = service.get_loan_explanation("student")
    
    assert explanation is not None
    assert explanation["title"] == "Φοιτητικό Δάνειο"


def test_get_loan_explanation_business(service):
    """Test getting explanation for business loan."""
    explanation = service.get_loan_explanation("business")
    
    assert explanation is not None
    assert explanation["title"] == "Επιχειρηματικό Δάνειο"


def test_get_loan_explanation_invalid_returns_none(service):
    """Test that invalid loan type returns None."""
    explanation = service.get_loan_explanation("invalid_type")
    assert explanation is None


def test_get_common_terms(service):
    """Test getting common financial terms."""
    terms = service.get_common_terms()
    
    assert "col1" in terms
    assert "col2" in terms
    assert "interest_rate" in terms["col1"]
    assert "term_and_apr" in terms["col2"]
    
    # Check that terms contain Greek text
    assert "Επιτόκιο" in terms["col1"]["interest_rate"]
    assert "Διάρκεια" in terms["col2"]["term_and_apr"]

