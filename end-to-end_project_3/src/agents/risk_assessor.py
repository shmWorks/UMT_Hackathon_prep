"""
Risk Assessor Agent
Identifies potential legal risks and red flags in contracts.
"""
from pydantic import BaseModel
from src.llm import invoke_llm


class RiskItem(BaseModel):
    """A single identified risk."""
    risk_title: str
    severity: str  # HIGH, MEDIUM, LOW
    description: str
    recommendation: str


class RiskReport(BaseModel):
    """Complete risk assessment report."""
    overall_risk_level: str
    risks: list[RiskItem]
    summary: str


RISK_PROMPT = """You are a legal risk assessment specialist.

Analyze the following contract excerpts for potential legal risks and red flags.

Document Context:
{context}

Identify risks such as:
- Unlimited liability clauses
- Auto-renewal traps
- Missing termination rights
- Unfavorable payment terms
- Broad indemnification requirements
- One-sided dispute resolution

For each risk found, provide:
RISK: [Title]
SEVERITY: [HIGH/MEDIUM/LOW]
DESCRIPTION: [What the risk is]
RECOMMENDATION: [How to mitigate]

End with:
OVERALL_RISK: [HIGH/MEDIUM/LOW]
SUMMARY: [1-2 sentence overall assessment]
"""


def assess_risks(context: str) -> RiskReport:
    """
    Analyzes document context for legal risks.
    
    Args:
        context: The document context from retrieval.
        
    Returns:
        RiskReport with identified risks and recommendations.
    """
    prompt = RISK_PROMPT.format(context=context)
    response = invoke_llm(prompt)
    
    # Parse risks from response
    risks = []
    current_risk = {}
    overall_risk = "MEDIUM"
    summary = "Risk assessment completed."
    
    lines = response.strip().split("\n")
    
    for line in lines:
        line = line.strip()
        if line.startswith("RISK:"):
            if current_risk.get("risk_title"):
                risks.append(RiskItem(**current_risk))
            current_risk = {"risk_title": line.split(":", 1)[1].strip()}
        elif line.startswith("SEVERITY:"):
            current_risk["severity"] = line.split(":", 1)[1].strip().upper()
        elif line.startswith("DESCRIPTION:"):
            current_risk["description"] = line.split(":", 1)[1].strip()
        elif line.startswith("RECOMMENDATION:"):
            current_risk["recommendation"] = line.split(":", 1)[1].strip()
        elif line.startswith("OVERALL_RISK:"):
            overall_risk = line.split(":", 1)[1].strip().upper()
        elif line.startswith("SUMMARY:"):
            summary = line.split(":", 1)[1].strip()
    
    # Don't forget the last risk
    if current_risk.get("risk_title"):
        risks.append(RiskItem(
            risk_title=current_risk.get("risk_title", "Unknown"),
            severity=current_risk.get("severity", "MEDIUM"),
            description=current_risk.get("description", ""),
            recommendation=current_risk.get("recommendation", "")
        ))
    
    return RiskReport(
        overall_risk_level=overall_risk,
        risks=risks,
        summary=summary
    )
