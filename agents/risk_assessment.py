from orchestrator import ApplicationData, AgentResponse

class RiskAssessmentAgent:
    def assess(self, app: ApplicationData, credit_data: dict) -> AgentResponse:
        risk_score = 0.0
        flags = []

        if app.loan_amount > app.monthly_income * 40:
            risk_score += 25
            flags.append("High loan-to-income ratio")

        if app.age < 21:
            risk_score += 30
            flags.append("Age below 21")
        elif app.age > 60:
            risk_score += 20
            flags.append("Age above 60")

        if app.has_previous_default:
            risk_score += 40
            flags.append("History of previous default or settlement")

        if app.city_tier == "Tier 3/Other":
            risk_score += 10
            flags.append("Higher geographic risk (Tier 3/Other)")

        credit_decision = credit_data.get("credit_decision")
        if credit_decision == "review":
            risk_score += 15
            flags.append("Borderline credit profile from credit scoring agent")
        elif credit_decision == "approve_with_caution":
            risk_score += 5
            flags.append("Moderate credit risk")

        if risk_score <= 20:
            risk_level = "Low"
        elif risk_score <= 45:
            risk_level = "Medium"
        else:
            risk_level = "High"

        msg = f"Overall risk assessed as {risk_level} with score {int(risk_score)}."
        if flags:
            msg += " Key factors: " + ", ".join(flags) + "."

        return AgentResponse(
            status="ok",
            message=msg,
            data={"risk_score": float(risk_score), "risk_level": risk_level, "risk_flags": flags},
        )
