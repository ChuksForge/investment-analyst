"""
orchestrator.py — Multi-Agent Investment Analyst
Coordinates all agents sequentially and manages state.
"""

import json
import asyncio
from datetime import datetime, date
from typing import Optional
import yfinance as yf
import pandas as pd
import numpy as np
from anthropic import Anthropic
from agents.prompts import (
    DATA_AGENT_SYSTEM, DATA_AGENT_USER_TEMPLATE,
    NEWS_AGENT_SYSTEM, NEWS_AGENT_USER_TEMPLATE,
    TECHNICAL_AGENT_SYSTEM, TECHNICAL_AGENT_USER_TEMPLATE,
    FUNDAMENTAL_AGENT_SYSTEM, FUNDAMENTAL_AGENT_USER_TEMPLATE,
    BULL_AGENT_SYSTEM, BULL_AGENT_USER_TEMPLATE,
    BEAR_AGENT_SYSTEM, BEAR_AGENT_USER_TEMPLATE,
    PORTFOLIO_MANAGER_SYSTEM, PORTFOLIO_MANAGER_USER_TEMPLATE,
)

client = Anthropic()
MODEL = "claude-sonnet-4-20250514"


# ─────────────────────────────────────────────
# HELPERS: Data Collection
# ─────────────────────────────────────────────

def fetch_yfinance_data(ticker: str) -> dict:
    """Pull price + fundamental data from yfinance."""
    try:
        t = yf.Ticker(ticker)
        info = t.info
        hist = t.history(period="1y")

        current_price = info.get("currentPrice") or info.get("regularMarketPrice")

        # Price changes
        def pct_change(days):
            if len(hist) > days:
                old = hist["Close"].iloc[-days]
                new = hist["Close"].iloc[-1]
                return round((new - old) / old * 100, 2)
            return None

        return {
            "ticker": ticker.upper(),
            "asset_type": "crypto" if "-USD" in ticker.upper() else "stock",
            "price_data": {
                "current": current_price,
                "change_1d_pct": pct_change(1),
                "change_7d_pct": pct_change(7),
                "change_30d_pct": pct_change(30),
                "52w_high": info.get("fiftyTwoWeekHigh"),
                "52w_low": info.get("fiftyTwoWeekLow"),
                "avg_volume": info.get("averageVolume"),
            },
            "fundamentals": {
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "eps": info.get("trailingEps"),
                "revenue_ttm": info.get("totalRevenue"),
                "gross_margin": info.get("grossMargins"),
                "debt_to_equity": info.get("debtToEquity"),
                "free_cash_flow": info.get("freeCashflow"),
                "revenue_growth_yoy": info.get("revenueGrowth"),
            },
            "sector": info.get("sector", "Unknown"),
            "industry": info.get("industry", "Unknown"),
            "history_df": hist,  # kept for technical indicators
        }
    except Exception as e:
        return {"error": str(e), "ticker": ticker}


def compute_technical_indicators(hist_df: pd.DataFrame, current_price: float) -> dict:
    """Compute RSI, MACD, MAs from price history."""
    close = hist_df["Close"]

    # Moving averages
    ma50 = close.rolling(50).mean().iloc[-1] if len(close) >= 50 else None
    ma200 = close.rolling(200).mean().iloc[-1] if len(close) >= 200 else None

    # RSI
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    rsi = (100 - 100 / (1 + rs)).iloc[-1] if len(close) >= 15 else None

    # MACD
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    macd_line = (ema12 - ema26).iloc[-1]
    signal_line = (ema12 - ema26).ewm(span=9).mean().iloc[-1]
    histogram = macd_line - signal_line

    # Support/Resistance (simple: 52w low/high)
    support = close.rolling(252).min().iloc[-1] if len(close) >= 252 else close.min()
    resistance = close.rolling(252).max().iloc[-1] if len(close) >= 252 else close.max()

    def safe_round(v, n=4):
        return round(float(v), n) if v is not None and not np.isnan(v) else None

    return {
        "current_price": safe_round(current_price),
        "ma50": safe_round(ma50),
        "ma200": safe_round(ma200),
        "price_vs_ma50_pct": safe_round((current_price - ma50) / ma50 * 100) if ma50 else None,
        "golden_cross": bool(ma50 > ma200) if (ma50 and ma200) else None,
        "rsi_14": safe_round(rsi),
        "macd_line": safe_round(macd_line),
        "macd_signal": safe_round(signal_line),
        "macd_histogram": safe_round(histogram),
        "key_support": safe_round(support),
        "key_resistance": safe_round(resistance),
        "volume_last": int(hist_df["Volume"].iloc[-1]),
        "volume_avg": int(hist_df["Volume"].mean()),
    }


# ─────────────────────────────────────────────
# AGENT RUNNER
# ─────────────────────────────────────────────

def run_agent(system_prompt: str, user_prompt: str, agent_name: str) -> dict:
    """Call Claude with a given system + user prompt. Returns parsed JSON."""
    print(f"\n🤖 Running {agent_name}...")
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        raw = response.content[0].text.strip()
        # Strip any accidental markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ⚠️  JSON parse error in {agent_name}: {e}")
        return {"error": "JSON parse failed", "agent": agent_name, "raw": raw}
    except Exception as e:
        print(f"  ❌  {agent_name} failed: {e}")
        return {"error": str(e), "agent": agent_name}


# ─────────────────────────────────────────────
# MAIN ORCHESTRATOR
# ─────────────────────────────────────────────

class InvestmentAnalystOrchestrator:
    def __init__(self):
        self.state = {}

    def analyze(self, ticker: str, news_context: Optional[str] = None) -> dict:
        """
        Full pipeline:
        1. Fetch raw data
        2. Run 4 specialist agents
        3. Run bull/bear debate
        4. Portfolio manager decides
        Returns complete state dict with all agent reports.
        """
        ticker = ticker.upper().strip()
        today = date.today().isoformat()
        self.state = {"ticker": ticker, "timestamp": today, "agents": {}}

        print(f"\n{'='*60}")
        print(f"  ANALYZING: {ticker}")
        print(f"  Date: {today}")
        print(f"{'='*60}")

        # ── Step 1: Fetch raw data ──────────────────────────────
        print("\n📊 Fetching market data...")
        raw = fetch_yfinance_data(ticker)

        if "error" in raw:
            return {"error": raw["error"], "ticker": ticker}

        hist_df = raw.pop("history_df")
        sector = raw.pop("sector", "Unknown")
        current_price = raw["price_data"]["current"] or 0
        indicators = compute_technical_indicators(hist_df, current_price)

        # ── Step 2: Data Agent ──────────────────────────────────
        data_report = run_agent(
            DATA_AGENT_SYSTEM,
            DATA_AGENT_USER_TEMPLATE.format(ticker=ticker),
            "Data Agent",
        )
        # Override with actual data fetched (agent enriches structure)
        data_report.update(raw)
        self.state["agents"]["data"] = data_report

        # ── Step 3: News Agent ──────────────────────────────────
        retrieved_context = news_context or f"No real-time news available. Use your training knowledge about {ticker} and its sector ({sector})."
        news_report = run_agent(
            NEWS_AGENT_SYSTEM,
            NEWS_AGENT_USER_TEMPLATE.format(
                ticker=ticker,
                retrieved_context=retrieved_context,
                current_date=today,
            ),
            "News Analyst",
        )
        self.state["agents"]["news"] = news_report

        # ── Step 4: Technical Agent ─────────────────────────────
        tech_report = run_agent(
            TECHNICAL_AGENT_SYSTEM,
            TECHNICAL_AGENT_USER_TEMPLATE.format(
                ticker=ticker,
                indicator_data=json.dumps(indicators, indent=2),
            ),
            "Technical Analyst",
        )
        self.state["agents"]["technical"] = tech_report

        # ── Step 5: Fundamental Agent ───────────────────────────
        fund_report = run_agent(
            FUNDAMENTAL_AGENT_SYSTEM,
            FUNDAMENTAL_AGENT_USER_TEMPLATE.format(
                ticker=ticker,
                financial_data=json.dumps(raw["fundamentals"], indent=2),
                sector=sector,
            ),
            "Fundamental Analyst",
        )
        self.state["agents"]["fundamental"] = fund_report

        # ── Step 6: Bull/Bear Debate ────────────────────────────
        all_reports_str = json.dumps({
            "data": data_report,
            "news": news_report,
            "technical": tech_report,
            "fundamental": fund_report,
        }, indent=2)

        bull_report = run_agent(
            BULL_AGENT_SYSTEM.replace("{ticker}", ticker),
            BULL_AGENT_USER_TEMPLATE.format(
                ticker=ticker,
                all_agent_reports=all_reports_str,
            ),
            "Bull Agent",
        )
        self.state["agents"]["bull"] = bull_report

        bear_report = run_agent(
            BEAR_AGENT_SYSTEM.replace("{ticker}", ticker),
            BEAR_AGENT_USER_TEMPLATE.format(
                ticker=ticker,
                all_agent_reports=all_reports_str,
            ),
            "Bear Agent",
        )
        self.state["agents"]["bear"] = bear_report

        # ── Step 7: Portfolio Manager ───────────────────────────
        pm_report = run_agent(
            PORTFOLIO_MANAGER_SYSTEM,
            PORTFOLIO_MANAGER_USER_TEMPLATE.format(
                ticker=ticker,
                data_report=json.dumps(data_report, indent=2),
                news_report=json.dumps(news_report, indent=2),
                technical_report=json.dumps(tech_report, indent=2),
                fundamental_report=json.dumps(fund_report, indent=2),
                bull_report=json.dumps(bull_report, indent=2),
                bear_report=json.dumps(bear_report, indent=2),
                current_date=today,
            ),
            "Portfolio Manager",
        )
        self.state["agents"]["portfolio_manager"] = pm_report
        self.state["final_decision"] = pm_report

        print(f"\n{'='*60}")
        print(f"  ✅ ANALYSIS COMPLETE: {ticker}")
        decision = pm_report.get("final_decision", "N/A")
        confidence = pm_report.get("confidence_score", 0)
        print(f"  DECISION: {decision}  |  CONFIDENCE: {confidence:.0%}")
        print(f"{'='*60}\n")

        return self.state


# ─────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    orchestrator = InvestmentAnalystOrchestrator()
    result = orchestrator.analyze(ticker)
    print(json.dumps(result["final_decision"], indent=2))
