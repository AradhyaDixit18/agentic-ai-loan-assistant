from orchestrator import ApplicationData, AgentResponse

class DocumentVerificationAgent:
    def verify(self, app: ApplicationData) -> AgentResponse:
        missing = []
        if not app.kyc_uploaded:
            missing.append("KYC document")
        if not app.bank_statement_uploaded:
            missing.append("Bank statements")

        if missing:
            status = "warning"
            msg = "Missing documents: " + ", ".join(missing) + "."
            quality_score = 0.4
        else:
            status = "ok"
            msg = "KYC and bank statements are marked as uploaded and ready for back-office verification."
            quality_score = 0.9

        return AgentResponse(
            status=status,
            message=msg,
            data={
                "kyc_uploaded": app.kyc_uploaded,
                "bank_statement_uploaded": app.bank_statement_uploaded,
                "document_quality_score": quality_score,
                "missing_documents": missing,
            },
        )
