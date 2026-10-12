"""MCP server for Structured JSON Output Repair & Schema Coercion Engine."""
import sys
import json
from client import StructuredOutputRepairEngine

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "repair_and_validate_json",
                "description": "Repairs malformed LLM JSON strings and verifies required schema keys",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "raw_output": {"type": "string"},
                        "required_keys": {"type": "array"}
                    },
                    "required": ["raw_output", "required_keys"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "repair_and_validate_json":
            args = params.get("arguments", {})
            res = StructuredOutputRepairEngine.repair_and_validate(
                args.get("raw_output", ""),
                args.get("required_keys", [])
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
