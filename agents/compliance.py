from orchestrator import ApplicationData, AgentResponse

class ComplianceAgent:
    def check(
        self,
        app: ApplicationData,
        credit_data: dict,
        risk_data: dict,
        doc_data: dict,
        affordability_data: dict
    ) -> AgentResponse:
        reasons = []
        final_decision = "approve"

        if app.age < 21:
            final_decision = "reject"
            reasons.append("Applicant age is below minimum threshold of 21.")
        if app.age > 65:
            final_decision = "reject"
            reasons.append("Applicant age is above maximum threshold of 65.")

        score = credit_data.get("credit_score", 0)
        if score < 650 and final_decision != "reject":
            final_decision = "review"
            reasons.append("Credit score is below preferred threshold of 650.")

        risk_level = risk_data.get("risk_level", "Medium")
        if risk_level == "High":
            if final_decision == "approve":
                final_decision = "review"
            reasons.append("Overall risk level is high based on internal risk assessment.")

        missing_docs = doc_data.get("missing_documents", [])
        doc_quality = doc_data.get("document_quality_score", 0.0)
        if missing_docs:
            if final_decision == "approve":
                final_decision = "review"
            reasons.append("Mandatory documents are missing.")
        elif doc_quality < 0.7:
            reasons.append("Document quality appears suboptimal and may require manual verification.")

        affordability_flag = affordability_data.get("affordability_flag", "Stretched")
        if affordability_flag == "Not affordable":
            if final_decision != "reject":
                final_decision = "reject"
            reasons.append("Requested EMI is not affordable within FOIR limits.")
        elif affordability_flag == "Stretched" and final_decision == "approve":
            final_decision = "approve_with_caution"
            reasons.append("EMI is near the upper comfort limit; case should be monitored post-disbursal.")

        if not reasons and final_decision.startswith("approve"):
            reasons.append("Application meets credit, risk, document, and affordability criteria.")

        msg = f"Final decision: {final_decision.upper()}. " + " ".join(reasons)

        return AgentResponse(
            status="ok",
            message=msg,
            data={
                "final_decision": final_decision,
                "compliance_reasons": reasons,
            },
        )
