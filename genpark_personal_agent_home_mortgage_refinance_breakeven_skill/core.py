# -*- coding: utf-8 -*-
"""Home Mortgage Refinance Amortization & Breakeven Copilot for GenPark Personal Agent."""
import json
import hashlib
import time
import math
from typing import Dict, Any

class HomeMortgageRefinanceBreakevenCalculator:
    """Core amortization and refinance breakeven calculation engine."""

    @staticmethod
    def _monthly_payment(balance: float, rate_pct: float, months: int) -> float:
        if months <= 0:
            return 0.0
        r = (rate_pct / 100.0) / 12.0
        if r == 0:
            return balance / months
        return balance * (r * ((1 + r) ** months)) / (((1 + r) ** months) - 1)

    @staticmethod
    def calculate_refinance_breakeven(current_balance_usd: float, current_rate_pct: float, current_remaining_months: int, proposed_rate_pct: float, proposed_term_months: int, total_closing_costs_usd: float) -> Dict[str, Any]:
        """Compute monthly payment reduction, lifetime interest delta, and breakeven horizon."""
        curr_monthly = HomeMortgageRefinanceBreakevenCalculator._monthly_payment(current_balance_usd, current_rate_pct, current_remaining_months)
        prop_monthly = HomeMortgageRefinanceBreakevenCalculator._monthly_payment(current_balance_usd, proposed_rate_pct, proposed_term_months)
        
        monthly_savings = max(0.0, curr_monthly - prop_monthly)
        
        if monthly_savings > 0:
            breakeven_months = math.ceil(total_closing_costs_usd / monthly_savings)
        else:
            breakeven_months = 999  # No savings

        # 5-year net savings (60 months)
        net_5yr_savings = (monthly_savings * 60) - total_closing_costs_usd

        # Total interest comparison
        curr_total_paid = curr_monthly * current_remaining_months
        prop_total_paid = (prop_monthly * proposed_term_months) + total_closing_costs_usd
        lifetime_delta = round(curr_total_paid - prop_total_paid, 2)

        return {
            "current_monthly_payment_usd": round(curr_monthly, 2),
            "proposed_monthly_payment_usd": round(prop_monthly, 2),
            "monthly_cashflow_savings_usd": round(monthly_savings, 2),
            "total_closing_costs_usd": round(total_closing_costs_usd, 2),
            "breakeven_months": breakeven_months,
            "breakeven_years": round(breakeven_months / 12.0, 1),
            "net_5yr_accumulated_savings_usd": round(net_5yr_savings, 2),
            "lifetime_cost_delta_usd": lifetime_delta,
            "is_financially_beneficial": breakeven_months <= 36 and monthly_savings > 50.0
        }

    @staticmethod
    def generate_mortgage_refinance_decision_memo(breakeven_months: int, monthly_savings_usd: float, planned_occupancy_years: float, net_5yr_savings_usd: float = 0.0) -> Dict[str, Any]:
        """Synthesize decision recommendation memo based on homeowner stay duration."""
        planned_months = planned_occupancy_years * 12.0
        if breakeven_months > planned_months:
            verdict = "REJECT_REFINANCE"
            rationale = f"Planned move/sale in {planned_occupancy_years} yrs ({int(planned_months)} mos) occurs BEFORE closing cost breakeven at {breakeven_months} mos."
        elif breakeven_months <= 24:
            verdict = "STRONGLY_RECOMMEND_LOCK"
            rationale = f"Fast breakeven at {breakeven_months} months produces ${monthly_savings_usd:.2f}/mo immediate cashflow and positive return well within occupancy."
        else:
            verdict = "MARGINAL_PROCEED_WITH_CAUTION"
            rationale = f"Breakeven at {breakeven_months} months acceptable only if strictly maintaining residence over {breakeven_months // 12} years."

        return {
            "verdict": verdict,
            "planned_tenure_months": int(planned_months),
            "breakeven_months": breakeven_months,
            "buffer_months_after_breakeven": max(0, int(planned_months - breakeven_months)),
            "summary_rationale": rationale,
            "key_next_steps": [
                "Obtain official Loan Estimate (LE) from lender to verify closing cost disclosures.",
                "Review escrow impound refund from existing lender to offset upfront closing capital.",
                "Lock interest rate with float-down provision if market volatility is elevated."
            ]
        }
