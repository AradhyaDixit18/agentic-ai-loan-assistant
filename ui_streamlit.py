import streamlit as st

from orchestrator import ApplicationData, Orchestrator
from agents.document_verification import DocumentVerificationAgent
from agents.credit_scoring import CreditScoringAgent
from agents.risk_assessment import RiskAssessmentAgent
from agents.compliance import ComplianceAgent
from agents.customer_interaction import CustomerInteractionAgent
from agents.data_collection import DataCollectionAgent
from agents.affordability import AffordabilityAgent
from agents.offer_generation import OfferGenerationAgent

def inject_custom_css():
    st.markdown(
        """
        <style>
        .main {
            background: radial-gradient(circle at top, #020617 0, #020617 40%, #020617 100%);
            color: #e5e7eb;
        }
        .block-container {
            padding-top: 2.5rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 1080px !important;
        }
        .hero-wrap {
            display: flex;
            flex-direction: row;
            gap: 2rem;
            align-items: stretch;
        }
        @media (max-width: 900px) {
            .hero-wrap {
                flex-direction: column;
            }
        }
        .hero-left {
            flex: 2;
        }
        .hero-right {
            flex: 1.4;
        }
        .hero-pill {
            display: inline-flex;
            align-items: center;
            padding: 0.2rem 0.8rem;
            border-radius: 999px;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            background: rgba(56,189,248,0.12);
            color: #7dd3fc;
            border: 1px solid rgba(56,189,248,0.5);
        }
        .hero-title {
            margin-top: 6rem;
            font-size: 2.2rem;
            line-height: 1.2;
            font-weight: 700;
            background: linear-gradient(120deg, #38bdf8, #a855f7, #f97316);
            -webkit-background-clip: text;
            color: transparent;
        }
        .hero-subtitle {
            margin-top: 2rem;
            font-size: 0.98rem;
            color: #9ca3af;
        }
        .hero-stat-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.6rem;
            margin-top: 1.2rem;
        }
        .hero-stat {
            padding: 0.7rem 0.9rem;
            border-radius: 14px;
            background: radial-gradient(circle at top left, rgba(56,189,248,0.22), rgba(15,23,42,0.95));
            border: 1px solid rgba(148,163,184,0.35);
        }
        .hero-stat-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #9ca3af;
        }
        .hero-stat-value {
            margin-top: 1rem;
            font-size: 1.05rem;
            font-weight: 600;
        }
        .card {
            border-radius: 18px;
            padding: 1.2rem 1.3rem;
            background: linear-gradient(145deg, rgba(15,23,42,0.96), rgba(15,23,42,0.92));
            border: 1px solid rgba(148,163,184,0.35);
            box-shadow: 0 24px 60px rgba(15,23,42,0.9);
        }
        .card-soft {
            border-radius: 18px;
            padding: 1.1rem 1.2rem;
            background: radial-gradient(circle at top left, rgba(30,64,175,0.5), rgba(15,23,42,0.98));
            border: 1px solid rgba(129,140,248,0.45);
            box-shadow: 0 24px 60px rgba(15,23,42,0.95);
        }
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 0.3rem;
        }
        .section-title {
            font-size: 1.08rem;
            font-weight: 600;
        }
        .section-subtitle {
            font-size: 0.78rem;
            color: #9ca3af;
        }
        .agent-badge {
            display: inline-block;
            padding: 0.2rem 0.55rem;
            border-radius: 999px;
            font-size: 0.7rem;
            margin-right: 0.35rem;
            margin-bottom: 0.25rem;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(148,163,184,0.4);
        }
        .metric-label {
            font-size: 0.75rem;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .metric-value {
            font-size: 1.2rem;
            font-weight: 600;
        }
        .metric-chip {
            display: inline-flex;
            align-items: center;
            margin-top: 0.25rem;
            padding: 0.1rem 0.5rem;
            border-radius: 999px;
            font-size: 0.7rem;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(148,163,184,0.6);
        }
        .decision-pill {
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.8rem;
            border-radius: 999px;
            font-size: 0.82rem;
            gap: 0.4rem;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(148,163,184,0.6);
        }
        .stProgress > div > div > div {
            border-radius: 999px;
        }
        .small-caption {
            font-size: 0.7rem;
            color: #9ca3af;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def decision_badge_text(decision: str) -> str:
    decision = (decision or "").lower()
    if decision == "approve":
        return "Approved"
    if decision == "approve_with_caution":
        return "Approved with Caution"
    if decision == "review":
        return "Needs Manual Review"
    if decision == "reject":
        return "Rejected"
    return "Pending"

def decision_emoji(decision: str) -> str:
    decision = (decision or "").lower()
    if decision == "approve":
        return "✅"
    if decision == "approve_with_caution":
        return "🟢"
    if decision == "review":
        return "🟡"
    if decision == "reject":
        return "🔴"
    return "ℹ️"

def risk_label(level: str) -> str:
    level = (level or "").lower()
    if level == "low":
        return "✅ Low"
    if level == "medium":
        return "🟡 Medium"
    if level == "high":
        return "🔴 High"
    return "ℹ️ Unknown"

def main():
    st.set_page_config(page_title="Agentic AI Personal Loan Assistant", page_icon="💳", layout="wide")
    inject_custom_css()

    customer_agent = CustomerInteractionAgent()
    data_agent = DataCollectionAgent()
    document_agent = DocumentVerificationAgent()
    credit_agent = CreditScoringAgent()
    risk_agent = RiskAssessmentAgent()
    affordability_agent = AffordabilityAgent()
    compliance_agent = ComplianceAgent()
    offer_agent = OfferGenerationAgent()

    orchestrator = Orchestrator(
        document_agent=document_agent,
        credit_agent=credit_agent,
        risk_agent=risk_agent,
        affordability_agent=affordability_agent,
        compliance_agent=compliance_agent,
        offer_agent=offer_agent,
    )

    st.markdown(
        """
        <div class="hero-wrap">
          <div class="hero-left">
            <div class="hero-pill">EY Techathon 6.0 · Agentic Decisioning</div>
            <div class="hero-title">Agentic AI Personal Loan Assistant<br/>for Tata Capital</div>
            <div class="hero-subtitle">
              A multi-agent orchestration layer that simulates how Tata Capital could blend document intelligence,
              credit scoring, risk and affordability checks, compliance and pricing into a single guided experience.
            </div>
            <div class="hero-stat-grid">
              <div class="hero-stat">
                <div class="hero-stat-label">Agents in play</div>
                <div class="hero-stat-value">7 Coordinated Agents</div>
              </div>
              <div class="hero-stat">
                <div class="hero-stat-label">Decision Scope</div>
                <div class="hero-stat-value">Eligibility · Risk · Offer</div>
              </div>
              <div class="hero-stat">
                <div class="hero-stat-label">User Journey</div>
                <div class="hero-stat-value">Onboarding to Offer in one flow</div>
              </div>
            </div>
          </div>
          <div class="hero-right">
            <div class="card-soft">
              <div class="section-header">
                <div class="section-title">Agent Mesh</div>
                <div class="section-subtitle">Master Orchestrator + Specialists</div>
              </div>
              <div style="margin-top:0.45rem;">
                <span class="agent-badge">Master Orchestrator</span>
                <span class="agent-badge">Customer Interaction</span>
                <span class="agent-badge">Document Intelligence</span>
                <span class="agent-badge">Credit Scoring</span>
                <span class="agent-badge">Risk Engine</span>
                <span class="agent-badge">Affordability</span>
                <span class="agent-badge">Compliance</span>
                <span class="agent-badge">Offer Generation</span>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-header"><div class="section-title">1️⃣ Guided Onboarding</div>'
        '<div class="section-subtitle">Collect only the signals needed for instant decisioning</div></div>',
        unsafe_allow_html=True,
    )
    st.info(customer_agent.greet())

    with st.form(key="loan_form"):
        col_basic, col_fin, col_docs = st.columns([1.5, 1.5, 1.2])

        with col_basic:
            st.markdown("**Applicant Profile**")
            full_name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=18, max_value=80, value=28)
            employment_type = st.selectbox(
                "Employment Type",
                ["Salaried", "Self-employed", "Student", "Retired", "Other"],
            )
            years_in_current_job = st.number_input("Years in current job/business", min_value=0.0, step=0.5, value=2.0)
            residence_type = st.selectbox(
                "Residence Type",
                ["Owned", "Rented", "Company Provided", "Other"],
            )
            city_tier = st.selectbox(
                "City Category",
                ["Tier 1", "Tier 2", "Tier 3/Other"],
            )
            has_previous_default = st.checkbox("Previous loan default/settlement on record", value=False)

        with col_fin:
            st.markdown("**Financial Snapshot**")
            monthly_income = st.number_input("Monthly Income (₹)", min_value=0.0, step=1000.0, value=60000.0)
            existing_emi = st.number_input("Total Existing EMIs per month (₹)", min_value=0.0, step=500.0, value=5000.0)
            loan_amount = st.number_input("Requested Loan Amount (₹)", min_value=0.0, step=10000.0, value=500000.0)
            loan_tenure_months = st.number_input("Loan Tenure (months)", min_value=6, max_value=120, value=48)
            credit_score = st.number_input("Known Credit Score (0 if unknown)", min_value=0, max_value=900, value=0)
            purpose = st.text_area("Purpose of Loan", value="Personal expenses and consolidation of existing smaller loans.")

        with col_docs:
            st.markdown("**Digital KYC & Docs**")
            kyc_uploaded = st.checkbox("KYC Document Uploaded", value=True)
            bank_uploaded = st.checkbox("Bank Statements (last 6 months) Uploaded", value=True)
            st.markdown("")
            st.markdown("**Run Agentic Stack**")
            submitted = st.form_submit_button(label="Run Evaluation")

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        required_issues = []
        if not full_name.strip():
            required_issues.append("Full Name is required.")
        if monthly_income <= 0:
            required_issues.append("Monthly income must be greater than zero.")
        if loan_amount <= 0:
            required_issues.append("Requested loan amount must be greater than zero.")
        if loan_tenure_months <= 0:
            required_issues.append("Loan tenure must be greater than zero months.")

        if required_issues:
            st.markdown("")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-header"><div class="section-title">⚠️ Incomplete Input</div>'
                '<div class="section-subtitle">The orchestrator needs a few more details</div></div>',
                unsafe_allow_html=True,
            )
            st.error("Please resolve the following before running the evaluation:")
            for issue in required_issues:
                st.write("• " + issue)
            st.markdown("</div>", unsafe_allow_html=True)
            return

        st.markdown("")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-header"><div class="section-title">2️⃣ Data Capture</div>'
            '<div class="section-subtitle">Streaming applicant data into the agent mesh</div></div>',
            unsafe_allow_html=True,
        )
        st.write(data_agent.collect())

        app_data = ApplicationData(
            full_name=full_name.strip(),
            age=int(age),
            employment_type=employment_type,
            monthly_income=float(monthly_income),
            existing_emi=float(existing_emi),
            loan_amount=float(loan_amount),
            loan_tenure_months=int(loan_tenure_months),
            credit_score=int(credit_score),
            purpose=purpose,
            kyc_uploaded=kyc_uploaded,
            bank_statement_uploaded=bank_uploaded,
            residence_type=residence_type,
            city_tier=city_tier,
            years_in_current_job=float(years_in_current_job),
            has_previous_default=bool(has_previous_default),
        )

        with st.expander("Structured Application Payload (for architects and reviewers)", expanded=False):
            st.json(
                {
                    "full_name": app_data.full_name,
                    "age": app_data.age,
                    "employment_type": app_data.employment_type,
                    "monthly_income": app_data.monthly_income,
                    "existing_emi": app_data.existing_emi,
                    "loan_amount": app_data.loan_amount,
                    "loan_tenure_months": app_data.loan_tenure_months,
                    "credit_score": app_data.credit_score,
                    "purpose": app_data.purpose,
                    "kyc_uploaded": app_data.kyc_uploaded,
                    "bank_statement_uploaded": app_data.bank_statement_uploaded,
                    "residence_type": app_data.residence_type,
                    "city_tier": app_data.city_tier,
                    "years_in_current_job": app_data.years_in_current_job,
                    "has_previous_default": app_data.has_previous_default,
                }
            )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-header"><div class="section-title">3️⃣ Multi-Agent Decisioning</div>'
            '<div class="section-subtitle">Each agent contributes a shard of the decision</div></div>',
            unsafe_allow_html=True,
        )

        result = orchestrator.run_full_pipeline(app_data)
        decision = result["final_decision"]

        offer = result.get("offer") or {}
        agent_data = result.get("agent_data") or []

        credit_data = agent_data[1] if len(agent_data) > 1 else {}
        risk_data = agent_data[2] if len(agent_data) > 2 else {}
        affordability_data = agent_data[3] if len(agent_data) > 3 else {}

        credit_score_val = credit_data.get("credit_score", 0)
        credit_band = credit_data.get("credit_band", "N/A")
        risk_level = risk_data.get("risk_level", "Unknown")
        risk_score = risk_data.get("risk_score", 0.0)
        max_aff_emi = affordability_data.get("max_allowed_emi", 0.0)
        max_loan = affordability_data.get("max_eligible_loan", 0.0)

        c1, c2, c3 = st.columns([1.4, 1.4, 1.2])

        with c1:
            st.markdown("**Decision Summary**")
            st.markdown(
                f'<div class="decision-pill"><span>{decision_emoji(decision)}</span>'
                f'<span>{decision_badge_text(decision)}</span></div>',
                unsafe_allow_html=True,
            )
            st.markdown("")
            st.markdown('<div class="metric-label">Applicant</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{app_data.full_name or "N/A"}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label" style="margin-top:0.45rem;">Purpose</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value" style="font-size:0.95rem;">{app_data.purpose or "N/A"}</div>', unsafe_allow_html=True)

        with c2:
            st.markdown("**Credit & Risk Snapshot**")
            st.markdown('<div class="metric-label">Internal Credit Score</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{int(credit_score_val)} ({credit_band})</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label" style="margin-top:0.45rem;">Risk Level</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{risk_label(risk_level)}</div>', unsafe_allow_html=True)
            st.progress(min(max(risk_score / 100.0, 0.0), 1.0))
            st.markdown('<div class="small-caption">Bar represents internal risk score normalised to 0–100.</div>', unsafe_allow_html=True)

        with c3:
            st.markdown("**Affordability Envelope**")
            st.markdown('<div class="metric-label">Max Affordable EMI</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">₹{max_aff_emi:,.0f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label" style="margin-top:0.45rem;">Max Eligible Loan</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">₹{max_loan:,.0f}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="metric-chip">Requested: ₹{app_data.loan_amount:,.0f} for {app_data.loan_tenure_months} months</div>',
                unsafe_allow_html=True,
            )

        st.markdown("")
        st.markdown("**Agent Reasoning Trace**")
        for msg in result["agent_messages"]:
            st.write("• " + msg)

        with st.expander("Agent Data (for analytics and model governance)", expanded=False):
            st.json(result["agent_data"])

        st.markdown("</div>", unsafe_allow_html=True)

        if offer:
            st.markdown("")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-header"><div class="section-title">4️⃣ AI-Generated Offer Design</div>'
                '<div class="section-subtitle">Pricing and structuring aligned with internal constraints</div></div>',
                unsafe_allow_html=True,
            )

            oc1, oc2, oc3 = st.columns(3)
            with oc1:
                st.markdown('<div class="metric-label">Suggested Interest Rate (p.a.)</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{offer["suggested_interest_rate_percent"]:.2f}%</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label" style="margin-top:0.45rem;">Recommended EMI</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">₹{offer["recommended_emi"]:,.0f}</div>', unsafe_allow_html=True)
            with oc2:
                st.markdown('<div class="metric-label">Requested Loan Amount</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">₹{app_data.loan_amount:,.0f}</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label" style="margin-top:0.45rem;">Recommended Loan Amount</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">₹{offer["recommended_loan_amount"]:,.0f}</div>', unsafe_allow_html=True)
            with oc3:
                st.markdown('<div class="metric-label">Maximum Eligible Loan</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">₹{offer["max_eligible_loan_amount"]:,.0f}</div>', unsafe_allow_html=True)
                st.markdown('<div class="metric-label" style="margin-top:0.45rem;">Compliance Decision</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{offer["decision_from_compliance"].upper()}</div>', unsafe_allow_html=True)

            st.info(offer["adjustment_note"])
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("EY Techathon 6.0 · Agentic AI Personal Loan Assistant · Multi-Agent Decisioning Prototype")

if __name__ == "__main__":
    main()
