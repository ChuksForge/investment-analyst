"""
EXAMPLE OUTPUTS
===============
Two realistic worked examples showing the full pipeline output.
These demonstrate what the system produces for real ticker inputs.
"""

# ─────────────────────────────────────────────
# EXAMPLE 1: NVDA (Stock — Bullish scenario)
# ─────────────────────────────────────────────

NVDA_EXAMPLE = {
    "ticker": "NVDA",
    "timestamp": "2025-03-15",
    "agents": {

        "data": {
            "ticker": "NVDA",
            "asset_type": "stock",
            "price_data": {
                "current": 887.42,
                "change_1d_pct": 2.31,
                "change_7d_pct": 5.84,
                "change_30d_pct": 18.2,
                "52w_high": 974.00,
                "52w_low": 435.10,
                "avg_volume": 42_800_000
            },
            "fundamentals": {
                "market_cap": 2_180_000_000_000,
                "pe_ratio": 73.4,
                "eps": 12.09,
                "revenue_ttm": 60_900_000_000,
                "gross_margin": 0.748,
                "debt_to_equity": 0.41,
                "free_cash_flow": 14_500_000_000,
                "revenue_growth_yoy": 1.22
            },
            "data_quality": {
                "completeness_score": 0.97,
                "missing_fields": [],
                "data_timestamp": "2025-03-15T09:00:00Z"
            }
        },

        "news": {
            "ticker": "NVDA",
            "analysis_window": "Last 30 days",
            "overall_sentiment_score": 0.74,
            "sentiment_label": "Bullish",
            "material_events": [
                {
                    "date": "2025-03-05",
                    "event_type": "earnings",
                    "headline": "NVIDIA Q4 FY2025 — Revenue $39.3B, beats by $2.1B",
                    "impact": "positive",
                    "significance": "high",
                    "summary": "NVIDIA crushed Q4 estimates driven by Blackwell GPU ramp. Data center segment grew 93% YoY. Management guided Q1 FY2026 revenue of $43B+, well above the $38.9B consensus."
                },
                {
                    "date": "2025-03-10",
                    "event_type": "regulatory",
                    "headline": "US expands AI chip export restrictions to 120+ countries",
                    "impact": "negative",
                    "significance": "medium",
                    "summary": "The Biden administration's updated chip rules add 120 countries to the restricted list for H100/H200 exports. Analysts estimate 4-7% incremental revenue risk. NVDA noted compliance measures are in progress."
                }
            ],
            "earnings_summary": {
                "last_earnings_date": "2025-03-05",
                "eps_beat": True,
                "revenue_beat": True,
                "guidance_change": "raised"
            },
            "key_risks_from_news": [
                "Export restriction expansion to 120+ countries",
                "China revenue headwind (previously ~20% of revenue)",
                "Sovereign AI cloud competition emerging"
            ],
            "key_catalysts_from_news": [
                "Blackwell GPU ramp accelerating into H1 2025",
                "Enterprise AI capex still in early innings (Microsoft, Google, Meta all guiding higher)",
                "NVIDIA platform lock-in via CUDA ecosystem"
            ],
            "analyst_rating_changes": [
                {"firm": "Goldman Sachs", "from": "Buy", "to": "Buy", "price_target": 1000},
                {"firm": "Morgan Stanley", "from": "Overweight", "to": "Overweight", "price_target": 950},
            ],
            "confidence": 0.91
        },

        "technical": {
            "ticker": "NVDA",
            "technical_signal": "Buy",
            "signal_score": 0.62,
            "trend": {
                "direction": "Uptrend",
                "strength": "Moderate",
                "ma50": 812.30,
                "ma200": 681.00,
                "price_vs_ma50_pct": 9.25,
                "golden_cross": True,
                "death_cross": False
            },
            "momentum": {
                "rsi_14": 63.2,
                "rsi_interpretation": "Neutral",
                "macd_line": 18.42,
                "macd_signal": 12.18,
                "macd_histogram": 6.24,
                "macd_crossover": "Bullish"
            },
            "support_resistance": {
                "key_support": 812.00,
                "key_resistance": 950.00,
                "distance_to_support_pct": 8.5,
                "distance_to_resistance_pct": 7.1
            },
            "volume_analysis": "Volume on recent up-days (+38% above average) significantly outpaces down-day volume, confirming institutional accumulation.",
            "chart_patterns": ["Bull Flag (Daily)", "Ascending Triangle (Weekly)"],
            "technical_summary": "NVDA is in a well-defined uptrend with a strong golden cross and bullish MACD crossover. RSI at 63 leaves room to run before overbought territory. The bull flag pattern on the daily chart targets ~$960 if confirmed. Key risk is a pullback to MA50 at $812 on any macro shock.",
            "confidence": 0.78
        },

        "fundamental": {
            "ticker": "NVDA",
            "fundamental_rating": "Buy",
            "fundamental_score": 0.71,
            "growth_analysis": {
                "revenue_growth_yoy": 1.22,
                "revenue_growth_assessment": "Accelerating",
                "earnings_growth_yoy": 1.48,
                "growth_quality": "Organic"
            },
            "profitability": {
                "gross_margin": 0.748,
                "gross_margin_vs_sector": "Above Average",
                "net_margin": 0.558,
                "is_profitable": True,
                "fcf_positive": True
            },
            "balance_sheet": {
                "debt_to_equity": 0.41,
                "leverage_assessment": "Conservative",
                "cash_runway_concern": False
            },
            "valuation": {
                "pe_ratio": 73.4,
                "pe_vs_sector": "Expensive",
                "qualitative_fair_value": "Fairly Valued",
                "margin_of_safety": "Low"
            },
            "moat_assessment": "Wide",
            "red_flags": [
                "PE at 73x requires perfect execution — zero margin for error",
                "Export restrictions represent 4-7% incremental revenue risk",
                "Customer concentration risk (4 hyperscalers = ~50% revenue)"
            ],
            "green_flags": [
                "CUDA moat — 15+ years of developer lock-in virtually unassailable",
                "74.8% gross margin is extraordinary for a hardware company",
                "122% YoY revenue growth at $61B scale is historically exceptional",
                "$14.5B FCF provides massive reinvestment optionality"
            ],
            "fundamental_summary": "NVIDIA's fundamentals are exceptional by nearly every measure — 122% revenue growth, 74.8% gross margins, and $14.5B in FCF represent best-in-class metrics for a company of this scale. The CUDA ecosystem creates genuine switching costs that act as a wide economic moat. The primary concern is valuation: at 73x trailing earnings, the stock prices in continued hypergrowth and any deceleration could cause a significant multiple contraction. The balance sheet is pristine with conservative leverage. Overall, NVDA is a high-quality compounder priced for perfection.",
            "confidence": 0.87
        },

        "bull": {
            "position": "BUY",
            "conviction": 0.79,
            "price_target_upside_pct": 25.0,
            "investment_thesis": "NVIDIA is the defining infrastructure company of the AI era, with a CUDA moat that competitors cannot replicate in this decade. Blackwell GPU demand is structurally supply-constrained, meaning pricing power is absolute. At current prices, NVDA trades at ~35x FY2026 earnings — reasonable for a company growing EPS 80%+.",
            "bull_arguments": [
                {
                    "argument_id": 1,
                    "title": "Blackwell demand exceeds supply — pricing power is absolute",
                    "supporting_evidence": ["Q4 revenue $39.3B beat by $2.1B", "Q1 guide of $43B+ vs $38.9B consensus", "Data center +93% YoY"],
                    "strength": "Strong"
                },
                {
                    "argument_id": 2,
                    "title": "CUDA moat is a 15-year unassailable competitive advantage",
                    "supporting_evidence": ["74.8% gross margin (hardware company)", "Wide moat designation", "4M+ CUDA developers globally"],
                    "strength": "Strong"
                },
                {
                    "argument_id": 3,
                    "title": "AI capex supercycle still in early innings",
                    "supporting_evidence": ["Microsoft, Google, Meta all raising AI capex guides", "Sovereign AI spending emerging as new vector", "Enterprise AI adoption <5% penetrated"],
                    "strength": "Strong"
                }
            ],
            "bear_case_rebuttals": [
                {"bear_argument": "Valuation is too expensive at 73x PE", "rebuttal": "On FY2026 estimates (accounting for 80% EPS growth), the forward PE is ~38x — not cheap, but defensible for a monopoly-quality business growing this fast."},
                {"bear_argument": "Export restrictions are a material headwind", "rebuttal": "China was already restricted to lower-spec chips. Non-China international demand (Europe, Southeast Asia) is accelerating. Net impact is manageable."}
            ],
            "key_catalysts": [
                "Blackwell GB200 NVL72 rack volume ramp in Q2 2025",
                "NVIDIA GTC 2025 product announcements",
                "Hyperscaler capex guidance re-acceleration",
                "Potential inclusion in additional sovereign AI programs"
            ],
            "time_horizon": "Medium-term (3-12mo)",
            "bull_summary": "Buy NVDA on any 5-10% pullbacks. The structural demand story is intact and Blackwell is a generational product cycle."
        },

        "bear": {
            "position": "SELL",
            "conviction": 0.44,
            "downside_risk_pct": 28.0,
            "bear_thesis": "NVIDIA is an exceptional business priced for a future that must go perfectly right. At $2.2T market cap, it prices in sustained hypergrowth for years. Any deceleration — from export restrictions, custom silicon competition, or a hyperscaler capex pause — could trigger a 25-40% drawdown from current levels.",
            "bear_arguments": [
                {
                    "argument_id": 1,
                    "title": "Custom silicon threat is real and accelerating",
                    "supporting_evidence": ["Google TPU v5 + Amazon Trainium2 in production", "Meta building custom AI chips", "Qualcomm/AMD gaining workload share at margins"],
                    "severity": "Significant"
                },
                {
                    "argument_id": 2,
                    "title": "Hyperscaler capex is inherently cyclical",
                    "supporting_evidence": ["AWS, Azure, GCP all face ROI pressure from investors", "AI model efficiency improving (less compute needed per task)", "Any macro slowdown triggers capex cuts"],
                    "severity": "Significant"
                }
            ],
            "bull_case_rebuttals": [
                {"bull_argument": "CUDA moat is unassailable", "rebuttal": "CUDA matters for training. As inference workloads (where custom silicon excels) become dominant, CUDA lock-in diminishes in the fastest-growing segment."},
            ],
            "key_risks": [
                "Export restriction escalation to additional countries",
                "Hyperscaler earnings guiding down AI capex",
                "DeepSeek/open-source model efficiency reducing GPU demand",
                "Macro recession triggering enterprise IT budget cuts"
            ],
            "time_horizon": "Medium-term (3-12mo)",
            "bear_summary": "Not a structural short, but NVDA is priced for perfection. Risk/reward is asymmetric to the downside at current levels for new entrants."
        },

        "portfolio_manager": {
            "ticker": "NVDA",
            "final_decision": "BUY",
            "confidence_score": 0.72,
            "signal_breakdown": {
                "fundamental_score": 0.71,
                "technical_score": 0.62,
                "sentiment_score": 0.74,
                "debate_winner": "Bull",
                "weighted_composite_score": 0.68
            },
            "position_sizing_recommendation": "Half Position",
            "suggested_entry": {
                "strategy": "Scale in: 50% position now at market, add 25% on any pullback to MA50 (~$812), add final 25% on Blackwell ramp confirmation in May earnings.",
                "entry_zone_low": 812.0,
                "entry_zone_high": 900.0
            },
            "risk_management": {
                "stop_loss_pct": 15.0,
                "profit_target_pct": 25.0,
                "max_drawdown_expected_pct": 28.0,
                "risk_reward_ratio": 1.67,
                "key_risks_to_monitor": [
                    "Export restriction escalation",
                    "Hyperscaler Q1 capex guidance",
                    "Blackwell yield/supply issues"
                ]
            },
            "time_horizon": "Medium-term (6-12 months)",
            "investment_thesis_summary": "NVIDIA earns a BUY with high conviction despite premium valuation. The bull case is compelling: Blackwell GPU supply is constrained against structurally growing demand from hyperscalers, sovereign AI programs, and enterprises — all of which are still in the early innings of AI infrastructure buildout. The CUDA ecosystem represents a genuine, durable moat that custom silicon challengers cannot meaningfully erode in the training-dominated present. The bear case is intellectually valid but premature — risks from custom silicon and export restrictions are real but not imminent enough to justify avoiding the position. Technically, the golden cross and bullish MACD support the uptrend. We size at half-position to respect the valuation risk and use the MA50 pullback as an add point. The 1.67x risk/reward is acceptable given earnings momentum.",
            "dissenting_signals": [
                "PE at 73x trailing — priced for perfection",
                "Bear agent correctly identifies custom silicon as a medium-term threat",
                "Export restrictions may worsen before they improve"
            ],
            "decision_triggers": {
                "would_upgrade_if": [
                    "Blackwell revenue exceeds $45B in Q1 FY2026 report",
                    "US eases export restrictions following geopolitical developments",
                    "Microsoft/Google raise FY2025 AI capex guidance above $60B combined"
                ],
                "would_downgrade_if": [
                    "Hyperscaler capex guides down 15%+ in upcoming earnings",
                    "Export restrictions expand to include NVL72 Blackwell systems",
                    "Price breaks and closes below 200-day MA ($681)"
                ]
            },
            "report_metadata": {
                "agents_consulted": 6,
                "average_agent_confidence": 0.852,
                "analysis_timestamp": "2025-03-15T12:00:00Z"
            }
        }
    }
}


# ─────────────────────────────────────────────
# EXAMPLE 2: ETH-USD (Crypto — Cautious scenario)
# ─────────────────────────────────────────────

ETH_EXAMPLE_PM = {
    "ticker": "ETH-USD",
    "final_decision": "HOLD",
    "confidence_score": 0.58,
    "signal_breakdown": {
        "fundamental_score": 0.22,
        "technical_score": -0.15,
        "sentiment_score": 0.31,
        "debate_winner": "Draw",
        "weighted_composite_score": 0.13
    },
    "position_sizing_recommendation": "Starter Position",
    "suggested_entry": {
        "strategy": "Wait for confirmed support at $2,800 before adding. Current price at $3,150 is mid-range — neither a great entry nor a red flag.",
        "entry_zone_low": 2750.0,
        "entry_zone_high": 2900.0
    },
    "risk_management": {
        "stop_loss_pct": 18.0,
        "profit_target_pct": 35.0,
        "max_drawdown_expected_pct": 40.0,
        "risk_reward_ratio": 1.94,
        "key_risks_to_monitor": [
            "BTC dominance trend — ETH tends to lag in BTC-led markets",
            "Layer-2 fee compression cannibalizing L1 revenue",
            "Stablecoin migration to competing L1s (Solana, Sui)"
        ]
    },
    "time_horizon": "Long-term (> 1 year)",
    "investment_thesis_summary": "Ethereum holds as a HOLD with moderate conviction. The bull case rests on ETH's position as the dominant smart contract platform with deep developer mindshare, growing institutional interest via spot ETH ETFs, and the Pectra upgrade improving staking economics. However, the bear case is not trivial: L2 fee compression has structurally damaged L1 revenue, Solana has taken meaningful market share in DeFi and NFTs, and ETH/BTC ratio has underperformed for 18 months. The technical picture is mixed with no clear trend. We hold existing positions but do not add aggressively until either (a) BTC breaks $80K and alt season begins, or (b) ETH reclaims $3,500 with volume.",
    "dissenting_signals": [
        "ETH/BTC ratio in sustained downtrend — relative weakness vs. Bitcoin",
        "L2 revenue extraction is compressing L1 economics",
        "Technical indicators non-committal — no clear trend signal"
    ],
    "decision_triggers": {
        "would_upgrade_if": [
            "ETH reclaims $3,500 with volume confirmation",
            "Bitcoin breaks $80K ATH triggering altcoin rotation",
            "Pectra upgrade ships on schedule with positive staking yield impact"
        ],
        "would_downgrade_if": [
            "ETH breaks below $2,500 on high volume",
            "SEC takes adverse action on ETH ETF",
            "Major DeFi protocol exploits on Ethereum mainnet"
        ]
    },
    "report_metadata": {
        "agents_consulted": 6,
        "average_agent_confidence": 0.67,
        "analysis_timestamp": "2025-03-15T14:30:00Z"
    }
}

if __name__ == "__main__":
    import json
    print("=== EXAMPLE 1: NVDA — Final Decision ===")
    print(json.dumps(NVDA_EXAMPLE["agents"]["portfolio_manager"], indent=2))
    print("\n=== EXAMPLE 2: ETH-USD — Final Decision ===")
    print(json.dumps(ETH_EXAMPLE_PM, indent=2))
