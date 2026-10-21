"""
AI Analyzer Service
===================
Orchestrates the AI analysis workflow:
1. Builds the prompt from contract text
2. Sends to Gemini API
3. Validates and saves results to the AIAnalysis model
4. Returns structured data or error fallback

Never blocks the upload flow. Errors are caught and returned gracefully.
"""

import json
import traceback

from contracts.services.logger import logger
from contracts.services.prompt_builder import build_analysis_prompt
from contracts.services.gemini_service import analyze_text, is_configured


def analyze_contract(contract_text: str) -> dict:
    """
    Run full AI analysis on contract text.

    Args:
        contract_text: The extracted text from the contract PDF.

    Returns:
        A dict with analysis results or error info.
        Always returns a dict, never None.
    """
    if not contract_text or not contract_text.strip():
        return {
            "error": True,
            "message": "No contract text provided for analysis."
        }

    # Check if Gemini is configured
    if not is_configured():
        logger.warning("AI analysis skipped: Gemini API not configured")
        return get_fallback_response()

    try:
        # Step 1: Build the prompt
        logger.info("Building AI analysis prompt...")
        prompt = build_analysis_prompt(contract_text)

        # Step 2: Send to Gemini
        logger.info("Sending to Gemini for analysis...")
        result = analyze_text(prompt)

        # Step 3: Check for errors from Gemini service
        if isinstance(result, dict) and result.get("error"):
            logger.warning(f"AI analysis failed: {result.get('message', 'Unknown error')}")
            return get_fallback_response()

        # Step 4: Validate that result has the expected structure
        validated = validate_and_fill(result)

        logger.info("AI analysis completed successfully")
        return validated

    except Exception as e:
        logger.error(f"AI analysis error: {traceback.format_exc()}")
        return get_fallback_response()


def validate_and_fill(result: dict) -> dict:
    """
    Validate the AI response and fill in defaults for missing fields.

    Args:
        result: Raw dict from Gemini.

    Returns:
        A sanitized dict with all expected fields.
    """
    defaults = {
        "summary": "AI summary could not be generated.",
        "overall_risk": "Risk assessment unavailable.",
        "risk_analysis": [],
        "missing_clauses": [],
        "recommendations": ["AI recommendations unavailable."],
        "confidence": "N/A",
        "tags": ["Contract"],
    }

    # Sanitize confidence: remove any existing % sign
    if result.get("confidence"):
        result["confidence"] = str(result["confidence"]).replace("%", "").strip()

    # Only override defaults if the field exists and has content
    for key, default_value in defaults.items():
        if key not in result or not result[key]:
            result[key] = default_value
        # Specifically for lists, ensure they are lists
        if isinstance(default_value, list) and not isinstance(result.get(key), list):
            result[key] = default_value

    # Ensure risk_analysis items have required sub-fields
    if isinstance(result.get("risk_analysis"), list):
        cleaned_risks = []
        for item in result["risk_analysis"]:
            if isinstance(item, dict):
                cleaned_risks.append({
                    "level": item.get("level", "Unknown"),
                    "clause": item.get("clause", "Unspecified"),
                    "explanation": item.get("explanation", ""),
                    "why_risky": item.get("why_risky", ""),
                    "legal_impact": item.get("legal_impact", ""),
                })
        result["risk_analysis"] = cleaned_risks

    # Ensure missing_clauses items have required sub-fields
    if isinstance(result.get("missing_clauses"), list):
        cleaned_missing = []
        for item in result["missing_clauses"]:
            if isinstance(item, dict):
                cleaned_missing.append({
                    "clause": item.get("clause", "Unknown"),
                    "importance": item.get("importance", ""),
                })
        result["missing_clauses"] = cleaned_missing

    return result


def get_fallback_response() -> dict:
    """
    Return a safe fallback when AI analysis is unavailable.

    This ensures the upload flow never crashes due to AI failure.
    """
    return {
        "error": True,
        "message": "AI analysis is temporarily unavailable.",
        "summary": "AI analysis is temporarily unavailable.",
        "overall_risk": "Unable to assess.",
        "risk_analysis": [],
        "missing_clauses": [],
        "recommendations": ["Please try again later."],
        "confidence": "N/A",
        "tags": ["Contract"],
    }
