# 🏦 Multi-Agent Autonomous Investment Analyst

> A simulated hedge fund powered by 6 specialized AI agents that research, debate, and deliver investment decisions — like a mini Wall Street desk running on your laptop.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Anthropic](https://img.shields.io/badge/Claude-Sonnet-orange?style=flat-square)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🧠 What It Does

Enter any stock or crypto ticker. Six AI agents activate in sequence:

1. **📊 Data Agent** — Fetches live price data and financials from Yahoo Finance
2. **📰 News Analyst** — Performs sentiment analysis and detects material events
3. **📉 Technical Analyst** — Computes RSI, MACD, moving averages, and chart patterns
4. **🧠 Fundamental Analyst** — Evaluates revenue growth, margins, valuation, and moat
5. **🐂 Bull Agent** — Argues the strongest possible case for buying
6. **🐻 Bear Agent** — Argues the strongest possible case for selling
7. **⚖️ Portfolio Manager** — Weighs all evidence and delivers: `BUY / HOLD / SELL` + confidence score + entry strategy + risk management

---

## 🏗️ Architecture

```
User Input (ticker)
       │
       ▼
┌──────────────┐
│  Data Agent  │ ← yfinance (price, fundamentals)
└──────┬───────┘
       │
       ├──────────────────┐
       ▼                  ▼
┌─────────────┐   ┌───────────────────┐
│ News Agent  │   │ Technical Agent   │
│ (Sentiment) │   │ (RSI/MACD/MA)     │
└──────┬──────┘   └────────┬──────────┘
       │                   │
       └──────────┬────────┘
                  ▼
       ┌──────────────────────┐
       │  Fundamental Agent   │
       │ (Revenue/Margin/Debt)│
       └──────────┬───────────┘
                  │
          ┌───────┴───────┐
          ▼               ▼
    ┌──────────┐   ┌──────────┐
    │  Bull    │   │  Bear    │
    │  Agent   │   │  Agent   │
    └────┬─────┘   └────┬─────┘
         └──────┬────────┘
                ▼
    ┌───────────────────────┐
    │   Portfolio Manager   │
    │  (Final Decision)     │
    └───────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/ChuksForge/investment-analyst.git
cd investment-analyst
pip install -r requirements.txt
```

### 2. Set Environment Variable

```bash
# Windows (Git Bash)
export ANTHROPIC_API_KEY=sk-ant-...

# Or create a .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### 3. Run CLI (quick mode)

```bash
python orchestrator.py NVDA
python orchestrator.py BTC-USD
python orchestrator.py TSLA
```

### 4. Run Full Dashboard

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
investment-analyst/
├── agents/
│   └── prompts.py          # All 7 agent system prompts
├── examples/
│   └── example_outputs.py  # Realistic NVDA + ETH worked examples
├── orchestrator.py         # Main pipeline controller
├── app.py                  # Streamlit dashboard UI
├── demo/                   # demo screenshots of app ui
├── requirements.txt
└── README.md
```

---

## 💡 Prompt Design Philosophy

Each agent uses three techniques:

**Role Prompting** — Each agent has a distinct identity, mandate, and perspective. The Bull and Bear agents are intentionally adversarial; the Portfolio Manager is explicitly neutral.

**Structured Outputs** — Every agent returns a strict JSON schema. This enables deterministic downstream composition — each agent's output feeds the next as structured data, not free text.

**Chain-of-Thought Reasoning** — Every agent has a numbered `## Reasoning process` section in its system prompt that forces step-by-step analysis before outputting conclusions. This dramatically improves output quality vs. asking for direct answers.

---

## 🔄 Interaction Flow

```
START → User enters ticker (e.g. "NVDA")
      → Optional: paste news context (simulates RAG)

PIPELINE (sequential):
  [Data]       → Fetch yfinance data, compute technical indicators
  [News]       → Sentiment analysis on news context
  [Technical]  → Interpret pre-computed indicator data
  [Fundamental]→ Evaluate financials vs. sector
  [Bull]       → Build buy case using all prior reports
  [Bear]       → Build sell case using all prior reports
  [PM]         → Weigh all signals with explicit scoring weights:
                   Fundamental: 30%
                   Technical:   25%
                   Sentiment:   20%
                   Debate:      25%

OUTPUT → Dashboard with:
  - Price chart (6mo with MA50/MA200)
  - Signal radar chart
  - Confidence gauge
  - Bull vs. Bear debate log
  - PM thesis + entry strategy + risk management
  - Decision upgrade/downgrade triggers

EDGE CASES:
  - Invalid ticker → yfinance throws, error surfaced gracefully
  - Missing data → data_quality.completeness_score warns agents
  - Conflicting signals → PM explicitly lists dissenting_signals
  - Crypto assets → fundamentals marked null where not applicable
```

---

## 📊 Example Outputs

### Example 1 — NVDA

```
DECISION: BUY | CONFIDENCE: 72%

Composite Score:   +0.68
Fundamental:       +0.71  (Revenue +122% YoY, 74.8% gross margin, wide moat)
Technical:         +0.62  (Golden cross, bullish MACD, bull flag pattern)
Sentiment:         +0.74  (Q4 beat, raised guidance, bullish analyst changes)
Debate Winner:     Bull

Entry Strategy:    Scale in — 50% now, 25% on MA50 pullback (~$812), 25% on Q1 confirm
Stop Loss:         -15%
Profit Target:     +25%
Risk/Reward:       1.67x

Would downgrade if: Hyperscaler capex guides down 15%+, or price breaks 200MA
```

### Example 2 — ETH-USD

```
DECISION: HOLD | CONFIDENCE: 58%

Composite Score:   +0.13
Fundamental:       +0.22  (ETF adoption positive, L2 fee compression negative)
Technical:         -0.15  (ETH/BTC ratio in downtrend, no clear momentum)
Sentiment:         +0.31  (Pectra upgrade anticipation, but Solana gaining share)
Debate Winner:     Draw

Entry Strategy:    Wait for confirmed support at $2,800 before adding
Stop Loss:         -18%
Profit Target:     +35%
Risk/Reward:       1.94x

Would upgrade if: ETH reclaims $3,500 with volume, or BTC breaks ATH
```

---

## ⚠️ Disclaimer

**For educational and portfolio demonstration purposes only.**  
This system does not constitute financial advice. All outputs are AI-generated and should not be used as the basis for real investment decisions. Always consult a qualified financial advisor.

---

## 👤 Author

Built by **ChuksForge**  
AI Systems Engineer | [chuksforge.github.io](https://chuksforge.github.io)  
Twitter / X: [@ChuksForge](https://x.com/ChuksForge)

---

## 📄 License

MIT — free to use, modify, and build upon.
