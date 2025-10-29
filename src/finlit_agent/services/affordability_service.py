"""
Affordability Service

Analyzes loan affordability based on financial metrics and generates recommendations.
"""

from typing import Dict, List, Literal


AffordabilityStatus = Literal["safe", "warning", "danger"]


class AffordabilityService:
    """Service for analyzing loan affordability and generating recommendations."""
    
    # Thresholds for affordability assessment
    SAFE_PAYMENT_RATIO = 30.0  # Payment should be <= 30% of income
    WARNING_PAYMENT_RATIO = 40.0  # Payment between 30-40% is risky
    MINIMUM_SAVINGS_RATIO = 0.1  # Should have at least 10% of loan amount saved
    
    def get_affordability_status(
        self,
        payment_ratio: float,
        disposable_income: float,
        estimated_payment: float
    ) -> AffordabilityStatus:
        """
        Determine affordability status based on financial metrics.
        
        Args:
            payment_ratio: Payment as percentage of income
            disposable_income: Monthly income minus expenses
            estimated_payment: Estimated monthly loan payment
            
        Returns:
            Status: "safe", "warning", or "danger"
        """
        # Danger: No disposable income or payment ratio too high
        if disposable_income <= 0 or payment_ratio > self.WARNING_PAYMENT_RATIO:
            return "danger"
        
        # Danger: Payment exceeds disposable income
        if disposable_income < estimated_payment:
            return "danger"
        
        # Warning: Payment ratio in risky zone
        if payment_ratio > self.SAFE_PAYMENT_RATIO:
            return "warning"
        
        # Safe: All metrics look good
        return "safe"
    
    def generate_recommendations(
        self,
        financial_data: Dict[str, float],
        metrics: Dict[str, float],
        status: AffordabilityStatus
    ) -> List[str]:
        """
        Generate personalized recommendations based on financial situation.
        
        Args:
            financial_data: User's financial data
            metrics: Calculated financial metrics
            status: Affordability status
            
        Returns:
            List of recommendation strings in Greek
        """
        recommendations = []
        
        disposable_income = metrics["disposable_income"]
        payment_ratio = metrics["payment_ratio"]
        estimated_payment = metrics["estimated_payment"]
        loan_amount = financial_data.get("loan_amount", 0)
        savings = financial_data.get("savings", 0)
        
        # Recommendations based on status
        if status == "danger":
            if disposable_income <= 0:
                recommendations.append(
                    "**Προσοχή!** Τα έξοδά σου ξεπερνούν το εισόδημά σου.\n\n"
                    "Πριν πάρεις δάνειο, καλό θα ήταν:\n"
                    "- Να μειώσεις τα έξοδά σου\n"
                    "- Να αυξήσεις το εισόδημά σου\n"
                    "- Να ξεπληρώσεις υπάρχοντα δάνεια"
                )
            elif payment_ratio > 35:
                recommendations.append(
                    "**Προσοχή!** Η δόση είναι υψηλή σε σχέση με το εισόδημά σου.\n\n"
                    "Σκέψου:\n"
                    "- Μικρότερο ποσό δανείου\n"
                    "- Μεγαλύτερη διάρκεια (χαμηλότερη δόση, αλλά περισσότεροι τόκοι)\n"
                    "- Να περιμένεις να βελτιώσεις την οικονομική σου κατάσταση"
                )
            elif disposable_income < estimated_payment:
                recommendations.append(
                    "**Προσοχή!** Η εκτιμώμενη δόση είναι πάνω από το διαθέσιμο εισόδημά σου.\n\n"
                    "Αυτό σημαίνει ότι μπορεί να δυσκολευτείς να την πληρώνεις."
                )
        
        elif status == "warning":
            recommendations.append(
                "**Προσοχή!** Η δόση είναι στο όριο του ασφαλούς.\n\n"
                "Σκέψου:\n"
                "- Μικρότερο ποσό δανείου\n"
                "- Μεγαλύτερη διάρκεια (χαμηλότερη δόση, αλλά περισσότεροι τόκοι)\n"
                "- Να περιμένεις να βελτιώσεις την οικονομική σου κατάσταση"
            )
        
        else:  # safe
            recommendations.append(
                "**Καλά νέα!** Φαίνεται ότι έχεις περιθώριο για αυτό το δάνειο.\n\n"
                "Θυμήσου:\n"
                "- Αυτή είναι μια εκτίμηση - μίλησε με τράπεζα για ακριβή ποσά\n"
                "- Κράτα πάντα ένα buffer για έκτακτα έξοδα\n"
                "- Σύγκρινε προσφορές από διάφορες τράπεζες"
            )
        
        # Additional recommendation about savings
        if savings < loan_amount * self.MINIMUM_SAVINGS_RATIO:
            recommendations.append(
                "💡 **Tip:** Καλό θα ήταν να έχεις αποταμιεύσεις τουλάχιστον 10% του ποσού του δανείου "
                "για προκαταβολή και έκτακτα έξοδα."
            )
        
        return recommendations
    
    def analyze_affordability(
        self,
        financial_data: Dict[str, float],
        metrics: Dict[str, float]
    ) -> Dict:
        """
        Perform complete affordability analysis.
        
        Args:
            financial_data: User's financial data
            metrics: Calculated financial metrics
            
        Returns:
            Dictionary with:
                - status: AffordabilityStatus
                - recommendations: List of recommendation strings
                - metrics: The financial metrics (passed through)
        """
        status = self.get_affordability_status(
            payment_ratio=metrics["payment_ratio"],
            disposable_income=metrics["disposable_income"],
            estimated_payment=metrics["estimated_payment"]
        )
        
        recommendations = self.generate_recommendations(
            financial_data=financial_data,
            metrics=metrics,
            status=status
        )
        
        return {
            "status": status,
            "recommendations": recommendations,
            "metrics": metrics
        }

