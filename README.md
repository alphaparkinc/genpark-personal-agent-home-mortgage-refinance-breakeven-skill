# Home Mortgage Refinance Amortization & Breakeven Copilot Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Dynamic mortgage escrow amortization, current vs. candidate loan rate differential, closing points & fees amortization breakeven window analysis, and automated refinance lock-in trigger. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `calculate_refinance_breakeven`: Calculate monthly principal & interest payment savings, total closing friction costs, and exact breakeven month count for mortgage refinancing.\n- `generate_mortgage_refinance_decision_memo`: Generate an executive mortgage refinance advisory memo assessing planned occupancy horizon against breakeven threshold.\n
## 🚀 Installation & Usage
Run directly with pure Python standard library:
```bash
python -m genpark_personal_agent_home_mortgage_refinance_breakeven_skill.server --test
```
