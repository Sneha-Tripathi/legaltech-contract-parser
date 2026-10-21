"""
Prompt Builder Service
======================
Builds structured prompts for Google Gemini AI.
Each prompt instructs Gemini to respond with valid JSON only.
"""


def build_analysis_prompt(contract_text: str) -> str:
    """
    Build a comprehensive analysis prompt for Gemini.

    Args:
        contract_text: The extracted text from the contract PDF.

    Returns:
        A formatted prompt string.
    """
    # Truncate very long texts to stay within token limits
    max_chars = 25000
    if len(contract_text) > max_chars:
        contract_text = contract_text[:max_chars] + "\n\n[TRUNCATED]"

    prompt = f"""
You are an expert legal AI assistant. Analyze the following legal contract text.

INSTRUCTIONS:
1. Analyze the contract thoroughly.
2. Return ONLY valid JSON (no markdown, no code fences, no extra text).
3. Use the exact JSON structure below.

CONTRACT TEXT:
-------------------
{contract_text}
-------------------

REQUIRED JSON OUTPUT FORMAT:
{{
  "summary": "A concise professional summary (max 200 words) covering: parties involved, contract type, main purpose, important obligations, important dates, overall understanding.",

  "overall_risk": "Overall Risk Level: HIGH RISK or MEDIUM RISK or LOW RISK",

  "risk_analysis": [
    {{
      "level": "High",
      "clause": "Name of high-risk clause",
      "explanation": "What this clause means",
      "why_risky": "Why it is risky",
      "legal_impact": "Potential legal impact"
    }}
  ],

  "missing_clauses": [
    {{
      "clause": "Name of missing clause",
      "importance": "Why this clause matters and what risk its absence creates"
    }}
  ],

  "recommendations": [
    "Practical legal recommendation 1",
    "Practical legal recommendation 2"
  ],

  "confidence": "Confidence percentage as a number between 0 and 100, e.g. 94",

  "tags": ["tag1", "tag2", "tag3"]
}}

CHECKLIST OF CLAUSES TO VERIFY:
- Confidentiality
- Governing Law
- Arbitration
- Force Majeure
- Limitation of Liability
- Indemnity
- Termination
- Data Privacy
- Payment Terms

For missing_clauses, include ANY of the above that are absent from the contract.
For risk_analysis, include ALL detected risk clauses with their levels.
For tags, generate relevant tags such as: Employment, NDA, Vendor, Lease, Partnership, Freelancer, Service, License, and any other applicable tags.

Remember: Return ONLY valid JSON. No markdown. No explanation.
"""
    return prompt.strip()
