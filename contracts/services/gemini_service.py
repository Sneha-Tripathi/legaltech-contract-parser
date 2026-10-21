"""
Gemini API Service
==================
Handles communication with Google Gemini 2.5 Flash API.
Reads API key from .env file. Never hardcodes secrets.
"""

import json
import os
import traceback

from dotenv import load_dotenv

from contracts.services.logger import logger

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY", "")


def is_configured() -> bool:
    """Check if Gemini API key is configured."""
    return bool(API_KEY)


def analyze_text(prompt: str, timeout: int = 30) -> dict:
    """
    Send a prompt to Gemini 2.5 Flash and return parsed JSON response.

    Args:
        prompt: The formatted prompt string to send.
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON dict on success, or error dict on failure.
    """
    if not is_configured():
        logger.warning("Gemini API key not configured in .env")
        return {
            "error": True,
            "message": "AI analysis is temporarily unavailable. GEMINI_API_KEY not set."
        }

    try:
        import google.generativeai as genai

        # Configure Gemini
        genai.configure(api_key=API_KEY)

        # Use Gemini 2.5 Flash model
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 4096,
            }
        )

        logger.info("Sending prompt to Gemini API...")

        # Send request
        response = model.generate_content(prompt)

        if not response or not response.text:
            logger.error("Gemini returned empty response")
            return {
                "error": True,
                "message": "AI analysis returned empty response."
            }

        raw_text = response.text.strip()

        # Clean potential markdown code fences
        if raw_text.startswith("```"):
            # Remove opening fence
            raw_text = raw_text.split("\n", 1)[-1]
            # Remove closing fence
            if "```" in raw_text:
                raw_text = raw_text.split("```")[0]
            raw_text = raw_text.strip()

        # Remove any "json" prefix after code fence
        if raw_text.startswith("json"):
            raw_text = raw_text[4:].strip()

        # Parse JSON
        try:
            result = json.loads(raw_text)
        except json.JSONDecodeError as je:
            logger.error(f"Failed to parse Gemini JSON: {je}")
            logger.debug(f"Raw response: {raw_text[:500]}")
            return {
                "error": True,
                "message": "AI analysis returned invalid format."
            }

        # Basic validation of required fields
        if not isinstance(result, dict):
            return {
                "error": True,
                "message": "AI analysis returned unexpected format."
            }

        logger.info("Gemini analysis completed successfully")
        return result

    except ImportError:
        logger.error("google-generativeai package not installed")
        return {
            "error": True,
            "message": "AI analysis is temporarily unavailable. Package not installed."
        }
    except Exception as e:
        logger.error(f"Gemini API error: {traceback.format_exc()}")
        return {
            "error": True,
            "message": f"AI analysis is temporarily unavailable. Error: {str(e)}"
        }
