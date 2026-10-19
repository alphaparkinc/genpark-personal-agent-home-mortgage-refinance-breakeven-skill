# -*- coding: utf-8 -*-
"""MCP Server for Home Mortgage Refinance Amortization & Breakeven Copilot Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import HomeMortgageRefinanceBreakevenCalculator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "calculate_refinance_breakeven",
        "description": "Calculate monthly principal & interest payment savings, total closing friction costs, and exact breakeven month count for mortgage refinancing.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current_balance_usd": {
                    "type": "number"
                },
                "current_rate_pct": {
                    "type": "number",
                    "description": "e.g. 6.875"
                },
                "current_remaining_months": {
                    "type": "integer"
                },
                "proposed_rate_pct": {
                    "type": "number",
                    "description": "e.g. 5.625"
                },
                "proposed_term_months": {
                    "type": "integer",
                    "description": "e.g. 360 for 30yr"
                },
                "total_closing_costs_usd": {
                    "type": "number"
                }
            },
            "required": [
                "current_balance_usd",
                "current_rate_pct",
                "current_remaining_months",
                "proposed_rate_pct",
                "proposed_term_months",
                "total_closing_costs_usd"
            ]
        }
    },
    {
        "name": "generate_mortgage_refinance_decision_memo",
        "description": "Generate an executive mortgage refinance advisory memo assessing planned occupancy horizon against breakeven threshold.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "breakeven_months": {
                    "type": "integer"
                },
                "monthly_savings_usd": {
                    "type": "number"
                },
                "planned_occupancy_years": {
                    "type": "number"
                },
                "net_5yr_savings_usd": {
                    "type": "number"
                }
            },
            "required": [
                "breakeven_months",
                "monthly_savings_usd",
                "planned_occupancy_years"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-home-mortgage-refinance-breakeven-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(HomeMortgageRefinanceBreakevenCalculator, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-personal-agent-home-mortgage-refinance-breakeven-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-personal-agent-home-mortgage-refinance-breakeven-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
