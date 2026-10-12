"""Structured JSON Output Repair & Schema Coercion Engine.
100% Python Standard Library.
"""

import re
import json

class StructuredOutputRepairEngine:
    """Repairs malformed LLM JSON outputs (markdown fences, trailing commas) and validates required fields."""

    @staticmethod
    def repair_and_validate(raw_output: str, required_keys: list) -> dict:
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_output.strip(), flags=re.IGNORECASE)
        cleaned = re.sub(r",\s*([\]}])", r"\1", cleaned)

        parsed = None
        repair_applied = (cleaned != raw_output.strip())
        try:
            parsed = json.loads(cleaned)
        except Exception as e:
            return {
                "valid": False,
                "repair_applied": repair_applied,
                "error": str(e),
                "missing_keys": required_keys,
                "data": None
            }

        missing = [k for k in required_keys if k not in parsed] if isinstance(parsed, dict) else required_keys
        return {
            "valid": len(missing) == 0,
            "repair_applied": repair_applied,
            "missing_keys": missing,
            "data": parsed
        }
