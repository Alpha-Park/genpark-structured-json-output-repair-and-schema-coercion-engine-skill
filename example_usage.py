"""Example usage for Structured JSON Output Repair & Schema Coercion Engine."""
from client import StructuredOutputRepairEngine

if __name__ == "__main__":
    raw = '```json\n{"action": "search", "confidence": 0.95,}\n```'
    res = StructuredOutputRepairEngine.repair_and_validate(raw, ["action", "confidence"])
    print("Valid:", res["valid"], "Data:", res["data"])
