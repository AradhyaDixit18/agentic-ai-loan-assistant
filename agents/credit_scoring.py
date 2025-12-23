from orchestrator import ApplicationData, AgentResponse

class CreditScoringAgent:
    def evaluate(self, app: ApplicationData) -> AgentResponse:
        if app.credit_score > 0:
            base_score = app.credit_score
        else:
            if app.monthly_income <= 0:
                dti = 1.0
            else:
                dti = app.existing_emi / app.monthly_income

            if dti < 0.2:
                base_score = 780
            elif dti < 0.4:
                base_score = 730
            elif dti < 0.6:
                base_score = 690
            else:
                base_score = 650

        if app.employment_type == "Salaried":
            base_score += 10
        elif app.employment_type == "Self-employed":
            base_score -= 5
        else:
            base_score -= 10

        if app.years_in_current_job >= 3:
            base_score += 10
        elif app.years_in_current_job < 1:
            base_score -= 10

        if app.has_previous_default:
            base_score -= 40

        score = max(300, min(900, base_score))

        if score >= 780:
            decision = "approve"
            band = "Excellent"
        elif score >= 730:
            decision = "approve_with_caution"
            band = "Good"
        elif score >= 680:
            decision = "review"
            band = "Fair"
        else:
            decision = "review"
            band = "Weak"

        return AgentResponse(
            status="ok",
            message=f"Credit score evaluated as {int(score)} ({band}) with decision inclination: {decision}.",
            data={"credit_score": int(score), "credit_decision": decision, "credit_band": band},
        )
