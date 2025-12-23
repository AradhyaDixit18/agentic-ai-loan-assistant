import math
from orchestrator import ApplicationData, AgentResponse

class AffordabilityAgent:
    def evaluate(self, app: ApplicationData) -> AgentResponse:
        if app.monthly_income <= 0:
            foi_ratio = 1.0
        else:
            foi_ratio = app.existing_emi / app.monthly_income

        max_foir = 0.5
        if app.employment_type == "Self-employed":
            max_foir = 0.45
        if app.residence_type == "Rented":
            max_foir -= 0.03
        max_foir = max(0.35, min(0.55, max_foir))

        max_allowed_emi = max(0.0, (max_foir * app.monthly_income) - app.existing_emi)

        annual_rate = 0.14
        r = annual_rate / 12.0
        n = max(app.loan_tenure_months, 1)
        if r > 0:
            emi_factor = (r * math.pow(1 + r, n)) / (math.pow(1 + r, n) - 1)
            max_eligible_loan = max_allowed_emi / emi_factor if emi_factor > 0 else 0.0
        else:
            max_eligible_loan = max_allowed_emi * n

        if app.loan_tenure_months > 0:
            if r > 0:
                denom = (math.pow(1 + r, app.loan_tenure_months) - 1)
                if denom > 0:
                    req_emi = app.loan_amount * r * math.pow(1 + r, app.loan_tenure_months) / denom
                else:
                    req_emi = 0.0
            else:
                req_emi = app.loan_amount / app.loan_tenure_months
        else:
            req_emi = 0.0

        if max_allowed_emi <= 0:
            affordability_flag = "Not affordable"
        elif req_emi <= max_allowed_emi:
            affordability_flag = "Comfortable"
        elif req_emi <= max_allowed_emi * 1.2:
            affordability_flag = "Stretched"
        else:
            affordability_flag = "Not affordable"

        msg = f"Affordability classified as {affordability_flag}. Maximum estimated EMI comfort is around ₹{max_allowed_emi:,.0f}."

        return AgentResponse(
            status="ok",
            message=msg,
            data={
                "max_foir": float(max_foir),
                "current_foir": float(foi_ratio),
                "max_allowed_emi": float(max_allowed_emi),
                "max_eligible_loan": float(max_eligible_loan),
                "requested_emi": float(req_emi),
                "affordability_flag": affordability_flag,
            },
        )
