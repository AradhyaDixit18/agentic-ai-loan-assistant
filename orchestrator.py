from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class ApplicationData:
    full_name: str = ""
    age: int = 0
    employment_type: str = ""
    monthly_income: float = 0.0
    existing_emi: float = 0.0
    loan_amount: float = 0.0
    loan_tenure_months: int = 0
    credit_score: int = 0
    purpose: str = ""
    kyc_uploaded: bool = False
    bank_statement_uploaded: bool = False
    residence_type: str = ""
    city_tier: str = ""
    years_in_current_job: float = 0.0
    has_previous_default: bool = False

@dataclass
class AgentResponse:
    status: str
    message: str
    data: Dict[str, Any] = field(default_factory=dict)

class Orchestrator:
    def __init__(
        self,
        document_agent,
        credit_agent,
        risk_agent,
        affordability_agent,
        compliance_agent,
        offer_agent
    ):
        self.document_agent = document_agent
        self.credit_agent = credit_agent
        self.risk_agent = risk_agent
        self.affordability_agent = affordability_agent
        self.compliance_agent = compliance_agent
        self.offer_agent = offer_agent

    def run_full_pipeline(self, app_data: ApplicationData) -> Dict[str, Any]:
        results: List[AgentResponse] = []

        doc_res = self.document_agent.verify(app_data)
        results.append(doc_res)

        credit_res = self.credit_agent.evaluate(app_data)
        results.append(credit_res)

        risk_res = self.risk_agent.assess(app_data, credit_res.data)
        results.append(risk_res)

        afford_res = self.affordability_agent.evaluate(app_data)
        results.append(afford_res)

        comp_res = self.compliance_agent.check(
            app_data,
            credit_res.data,
            risk_res.data,
            doc_res.data,
            afford_res.data
        )
        results.append(comp_res)

        final_decision = comp_res.data.get("final_decision", "review")

        offer_data: Optional[Dict[str, Any]] = None
        if final_decision in ["approve", "approve_with_caution", "review"]:
            offer_data = self.offer_agent.propose_offer(
                app_data,
                credit_res.data,
                risk_res.data,
                afford_res.data,
                comp_res.data
            )

        return {
            "final_decision": final_decision,
            "agent_messages": [r.message for r in results],
            "agent_data": [r.data for r in results],
            "offer": offer_data,
        }
