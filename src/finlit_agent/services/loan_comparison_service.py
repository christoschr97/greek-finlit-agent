"""
Loan Comparison Service

Compares, ranks, and selects the best loan options based on multiple factors.
Ensures diversity in recommendations.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from .loan_plan_generator_service import LoanPlan


@dataclass
class RankedPlan:
    """Loan plan with ranking score and breakdown."""
    plan: LoanPlan
    score: float  # Overall score (0-100)
    affordability_score: float  # Score for affordability (0-100)
    cost_score: float  # Score for total cost (0-100)
    payment_score: float  # Score for monthly payment (0-100)
    term_score: float  # Score for term length (0-100)
    recommendation_reason: str  # Why this plan is recommended


@dataclass
class ComparisonResult:
    """Detailed comparison between two loan plans."""
    plan_a: LoanPlan
    plan_b: LoanPlan
    winner: str  # 'a', 'b', or 'tie'
    monthly_payment_diff: float  # Difference in monthly payment
    total_cost_diff: float  # Difference in total cost
    interest_diff: float  # Difference in total interest
    term_diff: int  # Difference in term (years)
    pros_plan_a: List[str]  # Advantages of plan A
    pros_plan_b: List[str]  # Advantages of plan B
    recommendation: str  # Overall recommendation


class LoanComparisonService:
    """Service for comparing and ranking loan plans."""
    
    # Scoring weights
    AFFORDABILITY_WEIGHT = 0.30  # 30%
    COST_WEIGHT = 0.25  # 25%
    PAYMENT_WEIGHT = 0.20  # 20%
    TERM_WEIGHT = 0.15  # 15%
    FLEXIBILITY_WEIGHT = 0.10  # 10%
    
    # Safe affordability thresholds
    SAFE_PAYMENT_RATIO = 30.0
    WARNING_PAYMENT_RATIO = 40.0
    
    def rank_loan_plans(
        self,
        plans: List[LoanPlan],
        financial_data: Dict[str, float],
        preferences: Optional[Dict[str, any]] = None
    ) -> List[RankedPlan]:
        """
        Rank all loan plans based on multiple factors.
        
        Args:
            plans: List of loan plans to rank
            financial_data: User's financial information
            preferences: Optional user preferences (e.g., prefer_short_term)
            
        Returns:
            List of ranked plans, sorted by score (highest first)
        """
        if not plans:
            return []
        
        preferences = preferences or {}
        ranked_plans: List[RankedPlan] = []
        
        for plan in plans:
            # Calculate individual scores
            affordability_score = self._score_affordability(plan)
            cost_score = self._score_cost(plan, plans)
            payment_score = self._score_monthly_payment(plan, plans)
            term_score = self._score_term(plan, preferences)
            
            # Calculate overall score
            overall_score = (
                affordability_score * self.AFFORDABILITY_WEIGHT +
                cost_score * self.COST_WEIGHT +
                payment_score * self.PAYMENT_WEIGHT +
                term_score * self.TERM_WEIGHT +
                self._score_flexibility(plan) * self.FLEXIBILITY_WEIGHT
            )
            
            # Generate recommendation reason
            reason = self._generate_recommendation_reason(
                plan,
                affordability_score,
                cost_score,
                payment_score,
                term_score
            )
            
            ranked_plans.append(RankedPlan(
                plan=plan,
                score=overall_score,
                affordability_score=affordability_score,
                cost_score=cost_score,
                payment_score=payment_score,
                term_score=term_score,
                recommendation_reason=reason
            ))
        
        # Sort by score (highest first)
        ranked_plans.sort(key=lambda x: x.score, reverse=True)
        
        return ranked_plans
    
    def select_best_plans(
        self,
        ranked_plans: List[RankedPlan],
        count: int = 2
    ) -> List[LoanPlan]:
        """
        Select the best N plans, ensuring diversity.
        
        Args:
            ranked_plans: List of ranked plans
            count: Number of plans to select (default 2)
            
        Returns:
            List of selected loan plans
        """
        if not ranked_plans or count <= 0:
            return []
        
        if len(ranked_plans) <= count:
            return [rp.plan for rp in ranked_plans]
        
        selected: List[LoanPlan] = []
        
        # Always include the top-ranked plan
        selected.append(ranked_plans[0].plan)
        
        # For remaining selections, prefer diversity
        for rp in ranked_plans[1:]:
            if len(selected) >= count:
                break
            
            # Check if this plan offers diversity
            is_diverse = self._is_diverse_from_selected(rp.plan, selected)
            
            if is_diverse or len(selected) < count:
                selected.append(rp.plan)
        
        return selected[:count]
    
    def compare_two_plans(
        self,
        plan_a: LoanPlan,
        plan_b: LoanPlan
    ) -> ComparisonResult:
        """
        Detailed comparison between two specific plans.
        
        Args:
            plan_a: First loan plan
            plan_b: Second loan plan
            
        Returns:
            ComparisonResult with detailed analysis
        """
        # Calculate differences
        monthly_diff = plan_b.monthly_payment - plan_a.monthly_payment
        total_diff = plan_b.total_cost - plan_a.total_cost
        interest_diff = plan_b.total_interest - plan_a.total_interest
        term_diff = plan_b.term_years - plan_a.term_years
        
        # Determine winner
        winner = self._determine_winner(plan_a, plan_b)
        
        # Generate pros for each plan
        pros_a = self._generate_pros(plan_a, plan_b)
        pros_b = self._generate_pros(plan_b, plan_a)
        
        # Generate overall recommendation
        recommendation = self._generate_comparison_recommendation(
            plan_a,
            plan_b,
            winner
        )
        
        return ComparisonResult(
            plan_a=plan_a,
            plan_b=plan_b,
            winner=winner,
            monthly_payment_diff=monthly_diff,
            total_cost_diff=total_diff,
            interest_diff=interest_diff,
            term_diff=term_diff,
            pros_plan_a=pros_a,
            pros_plan_b=pros_b,
            recommendation=recommendation
        )
    
    def _score_affordability(self, plan: LoanPlan) -> float:
        """Score based on payment-to-income ratio (0-100)."""
        ratio = plan.payment_to_income_ratio
        
        if ratio <= self.SAFE_PAYMENT_RATIO:
            # Excellent affordability
            return 100.0
        elif ratio <= self.WARNING_PAYMENT_RATIO:
            # Acceptable but risky
            # Linear scale from 100 to 50
            return 100 - ((ratio - self.SAFE_PAYMENT_RATIO) / 
                         (self.WARNING_PAYMENT_RATIO - self.SAFE_PAYMENT_RATIO) * 50)
        else:
            # Too expensive
            # Exponentially decreasing from 50 to 0
            excess = ratio - self.WARNING_PAYMENT_RATIO
            return max(0, 50 - (excess * 2))
    
    def _score_cost(self, plan: LoanPlan, all_plans: List[LoanPlan]) -> float:
        """Score based on total cost relative to other options (0-100)."""
        if not all_plans:
            return 50.0
        
        costs = [p.total_cost for p in all_plans]
        min_cost = min(costs)
        max_cost = max(costs)
        
        if max_cost == min_cost:
            return 100.0
        
        # Lower cost = higher score
        score = 100 - ((plan.total_cost - min_cost) / (max_cost - min_cost) * 100)
        return max(0, min(100, score))
    
    def _score_monthly_payment(self, plan: LoanPlan, all_plans: List[LoanPlan]) -> float:
        """Score based on monthly payment relative to other options (0-100)."""
        if not all_plans:
            return 50.0
        
        payments = [p.monthly_payment for p in all_plans]
        min_payment = min(payments)
        max_payment = max(payments)
        
        if max_payment == min_payment:
            return 100.0
        
        # Lower payment = higher score
        score = 100 - ((plan.monthly_payment - min_payment) / (max_payment - min_payment) * 100)
        return max(0, min(100, score))
    
    def _score_term(self, plan: LoanPlan, preferences: Dict) -> float:
        """Score based on loan term (0-100)."""
        prefer_short = preferences.get('prefer_short_term', False)
        prefer_long = preferences.get('prefer_long_term', False)
        
        if prefer_short:
            # Prefer shorter terms (10 years = 100, 30 years = 0)
            return max(0, 100 - (plan.term_years - 10) * 5)
        elif prefer_long:
            # Prefer longer terms (30 years = 100, 10 years = 0)
            return max(0, min(100, (plan.term_years - 10) * 5))
        else:
            # Moderate preference (15-20 years is optimal)
            if 15 <= plan.term_years <= 20:
                return 100.0
            elif plan.term_years < 15:
                return 70 + (plan.term_years - 10) * 6
            else:
                return 100 - (plan.term_years - 20) * 3
    
    def _score_flexibility(self, plan: LoanPlan) -> float:
        """Score based on flexibility (0-100)."""
        # Shorter terms and lower payment ratios offer more flexibility
        term_factor = max(0, 100 - (plan.term_years - 5) * 3)
        ratio_factor = max(0, 100 - plan.payment_to_income_ratio * 2)
        
        return (term_factor + ratio_factor) / 2
    
    def _generate_recommendation_reason(
        self,
        plan: LoanPlan,
        affordability: float,
        cost: float,
        payment: float,
        term: float
    ) -> str:
        """Generate a Greek language recommendation reason."""
        reasons = []
        
        if affordability >= 80:
            reasons.append("Πολύ προσιτό")
        elif affordability >= 60:
            reasons.append("Αξιόπιστο")
        
        if cost >= 80:
            reasons.append("Χαμηλό συνολικό κόστος")
        
        if payment >= 80:
            reasons.append("Χαμηλή μηνιαία δόση")
        
        if plan.term_years <= 15:
            reasons.append("Γρήγορη αποπληρωμή")
        elif plan.term_years >= 25:
            reasons.append("Μικρή μηνιαία επιβάρυνση")
        
        return ", ".join(reasons) if reasons else "Ισορροπημένη επιλογή"
    
    def _is_diverse_from_selected(
        self,
        plan: LoanPlan,
        selected: List[LoanPlan]
    ) -> bool:
        """Check if plan offers diversity from already selected plans."""
        for selected_plan in selected:
            # Check term diversity (at least 5 years difference)
            if abs(plan.term_years - selected_plan.term_years) < 5:
                return False
            
            # Check payment diversity (at least 15% difference)
            payment_diff_pct = abs(
                plan.monthly_payment - selected_plan.monthly_payment
            ) / selected_plan.monthly_payment * 100
            
            if payment_diff_pct < 15:
                return False
        
        return True
    
    def _determine_winner(self, plan_a: LoanPlan, plan_b: LoanPlan) -> str:
        """Determine which plan is better overall."""
        # Simple scoring: lower total cost + better affordability
        score_a = (100 - plan_a.payment_to_income_ratio) + (1 / plan_a.total_cost * 100000)
        score_b = (100 - plan_b.payment_to_income_ratio) + (1 / plan_b.total_cost * 100000)
        
        if abs(score_a - score_b) < 0.1:
            return "tie"
        elif score_a > score_b:
            return "a"
        else:
            return "b"
    
    def _generate_pros(self, plan: LoanPlan, other: LoanPlan) -> List[str]:
        """Generate list of advantages for a plan compared to another."""
        pros = []
        
        if plan.monthly_payment < other.monthly_payment:
            diff = other.monthly_payment - plan.monthly_payment
            pros.append(f"Χαμηλότερη μηνιαία δόση κατά €{diff:.0f}")
        
        if plan.total_cost < other.total_cost:
            diff = other.total_cost - plan.total_cost
            pros.append(f"Λιγότερο συνολικό κόστος κατά €{diff:.0f}")
        
        if plan.total_interest < other.total_interest:
            diff = other.total_interest - plan.total_interest
            pros.append(f"Εξοικονόμηση €{diff:.0f} σε τόκους")
        
        if plan.term_years < other.term_years:
            diff = other.term_years - plan.term_years
            pros.append(f"Γρηγορότερη αποπληρωμή κατά {diff} έτη")
        
        if plan.payment_to_income_ratio < other.payment_to_income_ratio:
            pros.append("Καλύτερη αναλογία δόσης/εισοδήματος")
        
        return pros if pros else ["Εναλλακτική επιλογή"]
    
    def _generate_comparison_recommendation(
        self,
        plan_a: LoanPlan,
        plan_b: LoanPlan,
        winner: str
    ) -> str:
        """Generate overall comparison recommendation in Greek."""
        if winner == "a":
            return f"Το {plan_a.name} είναι η καλύτερη επιλογή συνολικά."
        elif winner == "b":
            return f"Το {plan_b.name} είναι η καλύτερη επιλογή συνολικά."
        else:
            return "Και τα δύο σχέδια είναι εξίσου καλές επιλογές. Διάλεξε βάσει των προτιμήσεών σου."

