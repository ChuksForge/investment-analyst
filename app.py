"""
app.py — Streamlit Dashboard for Multi-Agent Investment Analyst
Run: streamlit run app.py
"""

import streamlit as st
import json
import time
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf
from datetime import date
from orchestrator import InvestmentAnalystOrchestrator

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Investment Analyst",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    .main { background: #0a0e1a; }
    .stApp { background: #0a0e1a; color: #e2e8f0; }
    
    .decision-badge {
        display: inline-block;
        padding: 12px 32px;
        border-radius: 8px;
        font-size: 28px;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 2px;
    }
    .STRONG-BUY  { background: #064e3b; color: #10b981; border: 2px solid #10b981; }
    .BUY         { background: #052e16; color: #4ade80; border: 2px solid #4ade80; }
    .HOLD        { background: #1c1917; color: #fbbf24; border: 2px solid #fbbf24; }
    .SELL        { background: #3b1515; color: #f87171; border: 2px solid #f87171; }
    .STRONG-SELL { background: #450a0a; color: #ef4444; border: 2px solid #ef4444; }

    .agent-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .agent-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #6366f1;
        margin-bottom: 8px;
    }
    .bull-side { border-left: 3px solid #10b981; }
    .bear-side { border-left: 3px solid #ef4444; }
    .pm-side   { border-left: 3px solid #6366f1; }
    
    .metric-box {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .metric-label {
        font-size: 11px;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        font-weight: 600;
        color: #e2e8f0;
        margin-top: 4px;
    }
    
    .debate-log {
        background: #0d1117;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        line-height: 1.7;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #f1f5f9 !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        border: none;
        padding: 12px 40px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 16px;
        letter-spacing: 1px;
        border-radius: 8px;
        width: 100%;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #4338ca, #6d28d9);
    }
    
    .risk-item { 
        color: #f87171; 
        padding: 4px 0;
        font-size: 14px;
    }
    .catalyst-item { 
        color: #4ade80; 
        padding: 4px 0;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏦 AI Investment Analyst")
    st.markdown("*Multi-agent hedge fund simulation*")
    st.divider()

    ticker_input = st.text_input(
        "Ticker Symbol",
        value="AAPL",
        placeholder="e.g. AAPL, TSLA, BTC-USD",
        help="Stocks (e.g. NVDA) or Crypto (e.g. ETH-USD)"
    ).upper().strip()

    news_context = st.text_area(
        "Optional: Paste recent news (RAG context)",
        placeholder="Paste earnings transcripts, news articles, analyst notes...",
        height=120,
        help="This simulates RAG — paste any fresh context you have on this ticker."
    )

    analyze_btn = st.button("🚀 RUN ANALYSIS", use_container_width=True)

    st.divider()
    st.markdown("**Agent Pipeline:**")
    agents_list = [
        ("📊", "Data Agent", "Fetches price & fundamentals"),
        ("📰", "News Analyst", "Sentiment & event detection"),
        ("📉", "Technical Analyst", "RSI, MACD, MAs"),
        ("🧠", "Fundamental Analyst", "Revenue, margins, debt"),
        ("🐂", "Bull Agent", "Builds the buy case"),
        ("🐻", "Bear Agent", "Builds the sell case"),
        ("⚖️", "Portfolio Manager", "Final decision"),
    ]
    for icon, name, desc in agents_list:
        st.markdown(f"{icon} **{name}**  \n<small style='color:#6b7280'>{desc}</small>", unsafe_allow_html=True)

    st.divider()
    st.caption("⚠️ For educational purposes only. Not financial advice.")


# ─────────────────────────────────────────────
# HELPERS: Chart Builders
# ─────────────────────────────────────────────

def build_price_chart(ticker: str) -> go.Figure:
    df = yf.Ticker(ticker).history(period="6mo")
    if df.empty:
        return None

    ma50 = df["Close"].rolling(50).mean()
    ma200 = df["Close"].rolling(200).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"],
        name="Price", line=dict(color="#6366f1", width=2),
        fill="tozeroy", fillcolor="rgba(99,102,241,0.05)"
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=ma50, name="MA50",
        line=dict(color="#f59e0b", width=1.5, dash="dot")
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=ma200, name="MA200",
        line=dict(color="#ef4444", width=1.5, dash="dot")
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis=dict(gridcolor="#1f2937"),
        yaxis=dict(gridcolor="#1f2937"),
    )
    return fig


def build_radar_chart(scores: dict) -> go.Figure:
    categories = list(scores.keys())
    values = [max(0, min(1, (v + 1) / 2)) for v in scores.values()]  # normalize -1..1 to 0..1

    fig = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(99,102,241,0.2)",
        line=dict(color="#6366f1", width=2),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="#111827",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="#1f2937", color="#6b7280"),
            angularaxis=dict(gridcolor="#1f2937", color="#e2e8f0"),
        ),
        paper_bgcolor="#111827",
        height=300,
        margin=dict(l=30, r=30, t=30, b=30),
        showlegend=False,
    )
    return fig


def build_confidence_gauge(score: float) -> go.Figure:
    color = "#10b981" if score >= 0.65 else "#fbbf24" if score >= 0.4 else "#ef4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score * 100,
        number={"suffix": "%", "font": {"color": color, "size": 32}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#6b7280"},
            "bar": {"color": color},
            "bgcolor": "#1f2937",
            "steps": [
                {"range": [0, 40], "color": "#3b1515"},
                {"range": [40, 65], "color": "#1c1917"},
                {"range": [65, 100], "color": "#064e3b"},
            ],
            "threshold": {"line": {"color": "white", "width": 2}, "thickness": 0.75, "value": score * 100},
        }
    ))
    fig.update_layout(
        paper_bgcolor="#111827",
        height=200,
        margin=dict(l=20, r=20, t=20, b=0),
        font=dict(color="#e2e8f0"),
    )
    return fig


def decision_color(d: str) -> str:
    return d.upper().replace(" ", "-")


# ─────────────────────────────────────────────
# MAIN DISPLAY LOGIC
# ─────────────────────────────────────────────

st.markdown("# 🏦 Multi-Agent Investment Analyst")
st.markdown("*A simulated hedge fund — 6 specialized AI agents debate and decide*")
st.divider()

if analyze_btn and ticker_input:
    orchestrator = InvestmentAnalystOrchestrator()

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()

    steps = [
        "📊 Fetching market data...",
        "📰 Analyzing news sentiment...",
        "📉 Running technical analysis...",
        "🧠 Evaluating fundamentals...",
        "🐂 Building bull case...",
        "🐻 Building bear case...",
        "⚖️ Portfolio manager deciding...",
    ]

    with st.spinner(""):
        for i, step in enumerate(steps):
            status_text.markdown(f"**{step}**")
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.3)

        state = orchestrator.analyze(ticker_input, news_context or None)

    progress_bar.empty()
    status_text.empty()

    if "error" in state:
        st.error(f"Analysis failed: {state['error']}")
        st.stop()

    # Cache in session state
    st.session_state["analysis"] = state
    st.session_state["ticker"] = ticker_input

# Display cached or fresh analysis
if "analysis" in st.session_state:
    state = st.session_state["analysis"]
    ticker = st.session_state["ticker"]
    agents = state.get("agents", {})
    pm = agents.get("portfolio_manager", {})
    decision = pm.get("final_decision", "HOLD")
    confidence = pm.get("confidence_score", 0.5)

    # ── HERO SECTION ───────────────────────────────────
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### {ticker}")
        price = agents.get("data", {}).get("price_data", {}).get("current")
        if price:
            change = agents.get("data", {}).get("price_data", {}).get("change_1d_pct", 0) or 0
            arrow = "▲" if change >= 0 else "▼"
            color = "#10b981" if change >= 0 else "#ef4444"
            st.markdown(
                f"<span style='font-size:36px;font-weight:700;font-family:JetBrains Mono'>${price:,.2f}</span>"
                f"<span style='color:{color};font-size:18px;margin-left:12px'>{arrow} {abs(change):.2f}%</span>",
                unsafe_allow_html=True,
            )

    with col2:
        css_class = decision_color(decision)
        st.markdown(
            f"<div style='text-align:center;padding-top:10px'>"
            f"<div class='decision-badge {css_class}'>{decision}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    with col3:
        st.plotly_chart(build_confidence_gauge(confidence), use_container_width=True)

    st.divider()

    # ── PRICE CHART ─────────────────────────────────────
    st.markdown("### 📈 6-Month Price Chart")
    chart = build_price_chart(ticker)
    if chart:
        st.plotly_chart(chart, use_container_width=True)

    st.divider()

    # ── SIGNAL BREAKDOWN ────────────────────────────────
    st.markdown("### 🎯 Signal Breakdown")

    signal_data = pm.get("signal_breakdown", {})
    fund_score = signal_data.get("fundamental_score", 0) or 0
    tech_score = signal_data.get("technical_score", 0) or 0
    sent_score = signal_data.get("sentiment_score", 0) or 0
    composite = signal_data.get("weighted_composite_score", 0) or 0

    c1, c2, c3, c4 = st.columns(4)
    for col, label, score, icon in [
        (c1, "Fundamental", fund_score, "🧠"),
        (c2, "Technical", tech_score, "📉"),
        (c3, "Sentiment", sent_score, "📰"),
        (c4, "Composite", composite, "⚖️"),
    ]:
        color = "#10b981" if score > 0.2 else "#ef4444" if score < -0.2 else "#fbbf24"
        col.markdown(
            f"<div class='metric-box'>"
            f"<div class='metric-label'>{icon} {label}</div>"
            f"<div class='metric-value' style='color:{color}'>{score:+.2f}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    radar_scores = {
        "Fundamental": fund_score,
        "Technical": tech_score,
        "Sentiment": sent_score,
        "Bull Conv.": agents.get("bull", {}).get("conviction", 0),
        "PM Conf.": confidence * 2 - 1,  # rescale
    }
    st.plotly_chart(build_radar_chart(radar_scores), use_container_width=True)

    st.divider()

    # ── DEBATE LOG ──────────────────────────────────────
    st.markdown("### ⚔️ Bull vs. Bear Debate")

    bull = agents.get("bull", {})
    bear = agents.get("bear", {})
    debate_winner = signal_data.get("debate_winner", "Draw")

    col_bull, col_bear = st.columns(2)

    with col_bull:
        st.markdown(
            f"<div class='agent-card bull-side'>"
            f"<div class='agent-header'>🐂 Bull Agent — BUY @ {bull.get('conviction', 0):.0%} conviction</div>"
            f"<p style='color:#d1fae5;font-size:14px'>{bull.get('investment_thesis', 'N/A')}</p>",
            unsafe_allow_html=True,
        )
        for arg in bull.get("bull_arguments", [])[:3]:
            st.markdown(
                f"<p style='color:#4ade80;font-size:13px;margin:4px 0'>✅ <b>{arg.get('title')}</b></p>"
                f"<p style='color:#9ca3af;font-size:12px;margin:0 0 8px 20px'>{', '.join(arg.get('supporting_evidence', [])[:2])}</p>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_bear:
        st.markdown(
            f"<div class='agent-card bear-side'>"
            f"<div class='agent-header'>🐻 Bear Agent — SELL @ {bear.get('conviction', 0):.0%} conviction</div>"
            f"<p style='color:#fee2e2;font-size:14px'>{bear.get('bear_thesis', 'N/A')}</p>",
            unsafe_allow_html=True,
        )
        for arg in bear.get("bear_arguments", [])[:3]:
            st.markdown(
                f"<p style='color:#f87171;font-size:13px;margin:4px 0'>❌ <b>{arg.get('title')}</b></p>"
                f"<p style='color:#9ca3af;font-size:12px;margin:0 0 8px 20px'>{', '.join(arg.get('supporting_evidence', [])[:2])}</p>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    winner_color = "#10b981" if debate_winner == "Bull" else "#ef4444" if debate_winner == "Bear" else "#fbbf24"
    st.markdown(
        f"<p style='text-align:center;margin-top:8px'>Debate Winner: "
        f"<span style='color:{winner_color};font-weight:700'>{debate_winner}</span></p>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── PORTFOLIO MANAGER THESIS ─────────────────────────
    st.markdown("### ⚖️ Portfolio Manager — Final Report")

    st.markdown(
        f"<div class='agent-card pm-side'>"
        f"<div class='agent-header'>Portfolio Manager Thesis</div>"
        f"<p style='color:#c7d2fe;line-height:1.8'>{pm.get('investment_thesis_summary', 'N/A')}</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Risk management table
    rm = pm.get("risk_management", {})
    col_a, col_b, col_c, col_d = st.columns(4)
    for col, label, val, fmt in [
        (col_a, "Stop Loss", rm.get("stop_loss_pct"), "{:.1f}%"),
        (col_b, "Profit Target", rm.get("profit_target_pct"), "{:.1f}%"),
        (col_c, "Risk/Reward", rm.get("risk_reward_ratio"), "{:.2f}x"),
        (col_d, "Position Size", pm.get("position_sizing_recommendation"), "{}"),
    ]:
        display = fmt.format(val) if val is not None else "N/A"
        col.markdown(
            f"<div class='metric-box'>"
            f"<div class='metric-label'>{label}</div>"
            f"<div class='metric-value'>{display}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # Entry strategy
    entry = pm.get("suggested_entry", {})
    if entry.get("strategy"):
        st.markdown(
            f"<div style='background:#1e1b4b;border-left:3px solid #6366f1;padding:12px 16px;border-radius:4px;margin-top:12px'>"
            f"<b style='color:#a5b4fc'>Entry Strategy:</b> "
            f"<span style='color:#e0e7ff'>{entry['strategy']}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── RISKS & CATALYSTS ───────────────────────────────
    col_risks, col_cats = st.columns(2)
    with col_risks:
        st.markdown("#### 🚨 Key Risks")
        risks = rm.get("key_risks_to_monitor", []) or pm.get("dissenting_signals", [])
        for r in risks[:5]:
            st.markdown(f"<div class='risk-item'>⚠ {r}</div>", unsafe_allow_html=True)

    with col_cats:
        st.markdown("#### 🚀 Key Catalysts")
        catalysts = agents.get("bull", {}).get("key_catalysts", [])
        for c in catalysts[:5]:
            st.markdown(f"<div class='catalyst-item'>✦ {c}</div>", unsafe_allow_html=True)

    st.divider()

    # ── DECISION TRIGGERS ───────────────────────────────
    st.markdown("#### 🔄 Decision Triggers")
    triggers = pm.get("decision_triggers", {})
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("**Would UPGRADE if:**")
        for cond in triggers.get("would_upgrade_if", [])[:3]:
            st.markdown(f"<span style='color:#4ade80'>▲ {cond}</span>", unsafe_allow_html=True)
    with t2:
        st.markdown("**Would DOWNGRADE if:**")
        for cond in triggers.get("would_downgrade_if", [])[:3]:
            st.markdown(f"<span style='color:#f87171'>▼ {cond}</span>", unsafe_allow_html=True)

    st.divider()

    # ── RAW JSON EXPANDER ───────────────────────────────
    with st.expander("🔍 View Full Agent Reports (JSON)"):
        tab_names = ["Portfolio Manager", "Bull", "Bear", "Technical", "Fundamental", "News", "Data"]
        tab_keys  = ["portfolio_manager", "bull", "bear", "technical", "fundamental", "news", "data"]
        tabs = st.tabs(tab_names)
        for tab, key in zip(tabs, tab_keys):
            with tab:
                st.json(agents.get(key, {}))

else:
    # Landing state
    st.markdown("""
    <div style='text-align:center;padding:80px 40px'>
        <div style='font-size:80px'>🏦</div>
        <h2 style='color:#e2e8f0;margin-top:16px'>Enter a ticker to begin</h2>
        <p style='color:#6b7280;font-size:16px;max-width:500px;margin:12px auto 0'>
            Six specialized AI agents will research, debate, and deliver an investment decision
            — like a mini hedge fund running on your machine.
        </p>
    </div>
    """, unsafe_allow_html=True)
