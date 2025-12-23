import math
from orchestrator import ApplicationData

class OfferGenerationAgent:
    def _calculate_emi(self, principal: float, annual_rate: float, tenure_months: int) -> float:
        if tenure_months <= 0:
            return 0.0
        r = annual_rate / 12.0
        n = tenure_months
        if r <= 0:
            return principal / n
        denom = (math.pow(1 + r, n) - 1)
        if denom <= 0:
            return 0.0
        return principal * r * math.pow(1 + r, n) / denom

    def propose_offer(
        self,
        app: ApplicationData,
        credit_data: dict,
        risk_data: dict,
        affordability_data: dict,
        compliance_data: dict
    ) -> dict:
        base_rate = 0.16
        credit_score = credit_data.get("credit_score", 700)
        risk_level = risk_data.get("risk_level", "Medium")

        if credit_score >= 780:
            base_rate -= 0.03
        elif credit_score >= 730:
            base_rate -= 0.015
        elif credit_score < 680:
            base_rate += 0.02

        if risk_level == "Low":
            base_rate -= 0.005
        elif risk_level == "High":
            base_rate += 0.015

        base_rate = max(0.11, min(0.22, base_rate))

        requested_emi = affordability_data.get("requested_emi", 0.0)
        max_allowed_emi = affordability_data.get("max_allowed_emi", 0.0)
        max_eligible_loan = affordability_data.get("max_eligible_loan", app.loan_amount)

        if requested_emi <= max_allowed_emi and app.loan_amount <= max_eligible_loan:
            recommended_loan = app.loan_amount
            recommended_emi = requested_emi
            adjustment_note = "Requested loan amount is within affordability limits."
        else:
            recommended_loan = min(app.loan_amount, max_eligible_loan)
            recommended_emi = self._calculate_emi(recommended_loan, base_rate, app.loan_tenure_months)
            adjustment_note = "Loan amount and EMI have been aligned to internal affordability constraints."

        final_decision = compliance_data.get("final_decision", "review")

        return {
            "suggested_interest_rate_percent": round(base_rate * 100, 2),
            "recommended_loan_amount": float(recommended_loan),
            "recommended_emi": float(recommended_emi),
            "max_eligible_loan_amount": float(max_eligible_loan),
            "max_affordable_emi": float(max_allowed_emi),
            "decision_from_compliance": final_decision,
            "adjustment_note": adjustment_note,
        }
