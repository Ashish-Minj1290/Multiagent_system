import streamlit as st
import time
import sys
import os

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ORACLE // Research Intel System",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
#  STYLES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;700&family=Archivo+Black&display=swap');

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
    background: #0b0900 !important;
    color: #e8a800 !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── SCANLINE OVERLAY ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.15) 2px,
        rgba(0,0,0,0.15) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── PHOSPHOR FLICKER ── */
@keyframes phosphor-flicker {
    0%,100% { opacity: 1; }
    92%     { opacity: 1; }
    93%     { opacity: 0.88; }
    94%     { opacity: 1; }
    97%     { opacity: 0.93; }
    98%     { opacity: 1; }
}
body { animation: phosphor-flicker 10s infinite; }

@keyframes blink {
    0%, 49%   { opacity: 1; }
    50%, 100% { opacity: 0; }
}
@keyframes sweep-in {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-border {
    0%,100% { border-color: #e8a80055; box-shadow: none; }
    50%     { border-color: #e8a800bb; box-shadow: 0 0 24px #e8a80020; }
}
@keyframes progress-fill {
    from { width: 0%; }
    to   { width: 100%; }
}
@keyframes glow-text {
    0%,100% { text-shadow: 0 0 20px #e8a80040; }
    50%     { text-shadow: 0 0 40px #e8a80080, 0 0 80px #e8a80020; }
}

/* ── TOP BAR ── */
.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #e8a80020;
    padding: 1.2rem 2rem;
    background: #0b0900;
    animation: sweep-in 0.5s ease both;
}
.oracle-logo {
    font-family: 'Archivo Black', sans-serif;
    font-size: 1.35rem;
    letter-spacing: 0.3em;
    color: #e8a800;
    text-shadow: 0 0 30px #e8a80050, 0 0 60px #e8a80020;
    animation: glow-text 4s ease-in-out infinite;
}
.oracle-logo em { font-style: normal; color: #ff6b1a; }
.top-bar-center {
    font-size: 0.58rem;
    letter-spacing: 0.22em;
    color: #e8a80040;
    border: 1px solid #e8a80018;
    padding: 0.22rem 0.9rem;
    border-radius: 2px;
    background: #e8a80006;
}
.top-bar-right {
    font-size: 0.58rem;
    color: #e8a80040;
    letter-spacing: 0.1em;
    text-align: right;
    line-height: 2;
}
.status-dot {
    display: inline-block;
    width: 5px; height: 5px;
    background: #4ade80;
    border-radius: 50%;
    box-shadow: 0 0 8px #4ade80;
    animation: blink 1.6s infinite;
    vertical-align: middle;
    margin-right: 4px;
}

/* ── MAIN CONTENT WRAPPER ── */
.content-wrap {
    max-width: 1060px;
    margin: 0 auto;
    padding: 3rem 2rem 5rem;
}

/* ── HERO ── */
.hero-section { margin-bottom: 3.5rem; animation: sweep-in 0.6s 0.1s ease both; }
.classified-badge {
    font-family: 'Archivo Black', sans-serif;
    font-size: 0.56rem;
    letter-spacing: 0.38em;
    color: #cc2200;
    border: 2px solid #cc220035;
    border-radius: 2px;
    padding: 0.22rem 0.85rem;
    display: inline-block;
    margin-bottom: 1.6rem;
    transform: rotate(-1.2deg);
    text-shadow: 0 0 14px #cc220060;
    background: #cc220008;
}
.hero-headline {
    font-family: 'Archivo Black', sans-serif;
    font-size: clamp(2.4rem, 6vw, 4.2rem);
    line-height: 0.95;
    color: #e8a800;
    letter-spacing: -0.01em;
    margin-bottom: 1.2rem;
    animation: glow-text 5s ease-in-out infinite;
}
.hero-headline em { font-style: normal; color: #ff6b1a; }
.hero-sub {
    font-size: 0.68rem;
    color: #e8a80045;
    letter-spacing: 0.14em;
    line-height: 2.1;
}
.hero-sub b { color: #e8a80070; font-weight: 500; }

/* ── COMMAND TERMINAL ── */
.cmd-terminal {
    background: #0d0a00;
    border: 1px solid #e8a80025;
    border-top: 2px solid #e8a80050;
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 3rem;
    animation: sweep-in 0.6s 0.2s ease both;
    box-shadow: 0 0 80px #e8a80006, inset 0 0 60px #00000030;
}
.cmd-titlebar {
    background: #e8a80010;
    border-bottom: 1px solid #e8a80018;
    padding: 0.5rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.55rem;
}
.cmd-dot { width: 8px; height: 8px; border-radius: 50%; }
.cmd-dot-r { background: #ff5f57; box-shadow: 0 0 5px #ff5f5780; }
.cmd-dot-y { background: #ffbd2e; box-shadow: 0 0 5px #ffbd2e80; }
.cmd-dot-g { background: #28c840; box-shadow: 0 0 5px #28c84080; }
.cmd-title-text {
    font-size: 0.6rem;
    color: #e8a80035;
    letter-spacing: 0.18em;
    margin-left: 0.4rem;
}
.cmd-body { padding: 1.3rem 1.6rem; }
.cmd-prompt {
    font-size: 0.68rem;
    color: #e8a80040;
    letter-spacing: 0.1em;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.cmd-prompt-sym { color: #4ade8070; }

/* ── Input override ── */
[data-testid="stTextInput"] label { display: none !important; }
[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #e8a80025 !important;
    border-radius: 0 !important;
    color: #e8a800 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 0 !important;
    caret-color: #e8a800 !important;
    letter-spacing: 0.04em;
    box-shadow: none !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input::placeholder { color: #e8a80020 !important; }
[data-testid="stTextInput"] input:focus {
    border-bottom-color: #e8a800 !important;
    box-shadow: 0 2px 0 #e8a80030 !important;
    outline: none !important;
}

/* ── Execute button ── */
[data-testid="stButton"] > button {
    background: #e8a800 !important;
    color: #080600 !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.25em !important;
    padding: 0.72rem 2rem !important;
    width: 100% !important;
    margin-top: 1.1rem !important;
    cursor: pointer !important;
    transition: background 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 0 40px #e8a80020 !important;
    text-transform: uppercase;
}
[data-testid="stButton"] > button:hover {
    background: #ffc107 !important;
    box-shadow: 0 0 60px #e8a80040 !important;
}

/* ── PIPELINE LOG ── */
.log-section-label {
    font-size: 0.58rem;
    letter-spacing: 0.28em;
    color: #e8a80035;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.2rem;
}
.log-section-label::after { content: ''; flex: 1; height: 1px; background: #e8a80015; }

/* ── STEP CARDS ── */
.step-card {
    display: grid;
    grid-template-columns: 52px 1fr auto;
    align-items: start;
    gap: 0 1rem;
    padding: 1.1rem 1.4rem;
    border: 1px solid transparent;
    border-radius: 2px;
    margin-bottom: 0.6rem;
    transition: border-color 0.3s, background 0.3s, box-shadow 0.3s;
    position: relative;
}
.step-card.pending {
    border-color: #e8a80012;
    background: #0d0a0090;
    opacity: 0.38;
}
.step-card.active {
    border-color: #e8a80055;
    background: #e8a8000a;
    animation: pulse-border 2s ease-in-out infinite;
}
.step-card.done {
    border-color: #4ade8025;
    background: #4ade8005;
}

.step-num-big {
    font-family: 'Archivo Black', sans-serif;
    font-size: 2rem;
    line-height: 1;
    color: #e8a80012;
    user-select: none;
    padding-top: 2px;
    text-align: center;
}
.step-card.active .step-num-big { color: #e8a80035; }
.step-card.done   .step-num-big { color: #4ade8020; }

.step-inner { min-width: 0; }

.step-op {
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    color: #e8a80030;
    margin-bottom: 0.25rem;
}
.step-card.active .step-op { color: #e8a800aa; }
.step-card.done   .step-op { color: #4ade8060; }

.step-name {
    font-family: 'Archivo Black', sans-serif;
    font-size: 1rem;
    letter-spacing: 0.04em;
    color: #e8a80050;
    margin-bottom: 0.3rem;
}
.step-card.active .step-name { color: #e8a800f0; text-shadow: 0 0 20px #e8a80040; }
.step-card.done   .step-name { color: #4ade80c0; text-shadow: 0 0 16px #4ade8025; }

.step-desc {
    font-size: 0.65rem;
    color: #e8a80025;
    line-height: 1.7;
    letter-spacing: 0.02em;
}
.step-card.active .step-desc { color: #e8a80055; }
.step-card.done   .step-desc { color: #4ade8040; }

.step-bar-wrap {
    height: 1px;
    background: #e8a80015;
    margin-top: 0.9rem;
    overflow: hidden;
    border-radius: 1px;
}
.step-bar {
    height: 100%;
    background: linear-gradient(to right, #e8a800, #ff6b1a);
    animation: progress-fill 2.5s ease-in-out infinite;
    box-shadow: 0 0 8px #e8a800;
}

.step-badge {
    font-size: 0.56rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    padding: 0.22rem 0.55rem;
    border-radius: 2px;
    margin-top: 3px;
    white-space: nowrap;
}
.badge-pending { background: #e8a80008; color: #e8a80030; border: 1px solid #e8a80015; }
.badge-active  {
    background: #e8a80012; color: #e8a800; border: 1px solid #e8a80050;
    box-shadow: 0 0 10px #e8a80015;
    animation: blink 1s infinite;
}
.badge-done { background: #4ade8010; color: #4ade80; border: 1px solid #4ade8030; }

.connector-line {
    width: 1px; height: 0.6rem;
    background: #e8a80015;
    margin: 0 0 0 calc(1.4rem + 26px);
}

/* ── AMBER DIVIDER ── */
.amber-divider {
    border: none;
    border-top: 1px solid #e8a80015;
    margin: 2.5rem 0;
}

/* ── OUTPUT SECTION LABEL ── */
.output-label {
    font-size: 0.58rem;
    letter-spacing: 0.25em;
    color: #e8a80035;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 0.9rem;
}
.output-label::after { content: ''; flex: 1; height: 1px; background: #e8a80012; }

/* ── RAW INTEL PANELS ── */
.intel-panel {
    background: #0d0a00;
    border: 1px solid #e8a80018;
    border-top: 2px solid #e8a80040;
    border-radius: 2px;
    padding: 1.2rem;
    font-size: 0.7rem;
    color: #e8a80070;
    line-height: 1.85;
    letter-spacing: 0.02em;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 240px;
    overflow-y: auto;
    box-shadow: inset 0 0 40px #00000030;
}
.intel-panel::-webkit-scrollbar { width: 2px; }
.intel-panel::-webkit-scrollbar-thumb { background: #e8a80030; }

/* ── METRICS ── */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 2rem 0;
}
.metric-block {
    background: #0d0a00;
    border: 1px solid #e8a80015;
    border-radius: 2px;
    padding: 1.1rem 1rem;
    text-align: center;
}
.metric-val {
    font-family: 'Archivo Black', sans-serif;
    font-size: 1.8rem;
    color: #e8a800;
    text-shadow: 0 0 20px #e8a80040;
    display: block;
    line-height: 1;
    margin-bottom: 0.45rem;
}
.metric-lbl {
    font-size: 0.52rem;
    letter-spacing: 0.22em;
    color: #e8a80035;
    text-transform: uppercase;
}

/* ── FINAL REPORT ── */
.report-masthead {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    background: #0d0a00;
    border: 1px solid #e8a80025;
    border-top: 3px solid #e8a800;
    padding: 1.5rem 1.8rem 1.2rem;
    border-radius: 2px 2px 0 0;
}
.report-doc-id {
    font-size: 0.57rem;
    color: #e8a80035;
    letter-spacing: 0.18em;
    margin-bottom: 0.5rem;
}
.report-doc-title {
    font-family: 'Archivo Black', sans-serif;
    font-size: 1.25rem;
    color: #e8a800;
    letter-spacing: 0.06em;
    text-shadow: 0 0 20px #e8a80030;
}
.report-stamp {
    font-family: 'Archivo Black', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.32em;
    color: #cc2200;
    border: 2px solid #cc220035;
    padding: 0.28rem 0.7rem;
    border-radius: 2px;
    transform: rotate(2.5deg);
    display: inline-block;
    text-shadow: 0 0 12px #cc220050;
    background: #cc220008;
    margin-top: 0.3rem;
}
.report-body-wrap {
    border: 1px solid #e8a80018;
    border-top: none;
    background: #0c0900;
    padding: 1.8rem 2rem;
    border-radius: 0 0 2px 2px;
    font-size: 0.78rem;
    color: #e8a80090;
    line-height: 1.95;
    letter-spacing: 0.02em;
    margin-bottom: 1rem;
}

/* ── CRITIC PANEL ── */
.critic-wrap {
    border: 1px solid #ff6b1a18;
    border-top: 2px solid #ff6b1a;
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 1rem;
}
.critic-header {
    background: #ff6b1a0a;
    padding: 0.8rem 1.5rem;
    border-bottom: 1px solid #ff6b1a15;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.critic-title {
    font-family: 'Archivo Black', sans-serif;
    font-size: 0.78rem;
    color: #ff6b1a;
    letter-spacing: 0.15em;
    text-shadow: 0 0 15px #ff6b1a30;
}
.critic-tag {
    font-size: 0.55rem;
    color: #ff6b1a40;
    letter-spacing: 0.15em;
}
.critic-body-wrap {
    background: #0d0900;
    padding: 1.5rem 1.8rem;
    font-size: 0.77rem;
    color: #ff6b1a65;
    line-height: 1.9;
    letter-spacing: 0.02em;
}

/* ── DOWNLOAD ── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: #e8a800 !important;
    border: 1px solid #e8a80035 !important;
    border-radius: 2px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.22em !important;
    padding: 0.55rem 1.5rem !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #e8a80008 !important;
    border-color: #e8a800 !important;
    box-shadow: 0 0 20px #e8a80015 !important;
}

/* ── ALERTS ── */
[data-testid="stAlert"] {
    background: #0d0a00 !important;
    border: 1px solid #4ade8020 !important;
    border-left: 2px solid #4ade8060 !important;
    border-radius: 2px !important;
    color: #4ade8060 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stAlert"][data-baseweb="notification"] {
    background: #0d0a00 !important;
    border: 1px solid #e8a80020 !important;
    border-left: 2px solid #e8a80060 !important;
    color: #e8a80060 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  TOP BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-bar">
  <div class="oracle-logo">ORA<em>EON</em></div>
  <div class="top-bar-center">MULTIAGENT RESEARCH INTEL SYSTEM // v2.1</div>
  <div class="top-bar-right">
    <span class="status-dot"></span>SYSTEM ONLINE &nbsp;|&nbsp; {time.strftime("%Y.%m.%d")}<br>
    SESSION ID: {hex(int(time.time()))[-6:].upper()} &nbsp;|&nbsp; CLEARANCE: OPEN
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  LAYOUT: LEFT + RIGHT via columns
# ─────────────────────────────────────────────────────────────────────────────
# wrap in some padding
st.markdown("<div style='padding: 2.5rem 1.5rem 0;'>", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.1], gap="large")

with left_col:
    # ── HERO ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
      <div class="classified-badge">▲ CLASSIFIED RESEARCH SYSTEM ▲</div>
      <div class="hero-headline">DEEP<br>INTEL<br>ON <em>ANY<br>TOPIC.</em></div>
      <p class="hero-sub">
        <b>FOUR AUTONOMOUS AGENTS.</b><br>
        ONE UNIFIED PIPELINE.<br><br>
        SEARCH &rarr; SCRAPE &rarr; WRITE &rarr; CRITIQUE.<br>
        INTELLIGENCE BRIEF. READY IN SECONDS.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── COMMAND TERMINAL INPUT ─────────────────────────────────────────────────
    st.markdown("""
    <div class="cmd-terminal">
      <div class="cmd-titlebar">
        <div class="cmd-dot cmd-dot-r"></div>
        <div class="cmd-dot cmd-dot-y"></div>
        <div class="cmd-dot cmd-dot-g"></div>
        <span class="cmd-title-text">oracle@research-node ~ $</span>
      </div>
      <div class="cmd-body">
        <div class="cmd-prompt">
          <span class="cmd-prompt-sym">▶</span>
          oracle // enter research directive
        </div>
    """, unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g.  quantum error correction breakthroughs 2025",
        label_visibility="collapsed",
    )
    run_btn = st.button("⬡  EXECUTE PIPELINE", use_container_width=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

with right_col:
    # ── PIPELINE STEPS ────────────────────────────────────────────────────────
    STEPS = [
        ("01", "SEARCH AGENT",
         "Querying live sources. Indexing recent and reliable results for the directive."),
        ("02", "READER AGENT",
         "Selecting highest-relevance URL. Scraping full content for deep extraction."),
        ("03", "WRITER CHAIN",
         "Synthesising all signals into a structured intelligence briefing."),
        ("04", "CRITIC CHAIN",
         "Running adversarial quality review. Validating accuracy, depth, completeness."),
    ]

    def render_pipeline(current: int, done: set):
        st.markdown("""
        <div class="log-section-label">// PIPELINE EXECUTION LOG</div>
        """, unsafe_allow_html=True)

        for i, (num, title, desc) in enumerate(STEPS):
            if i in done:
                cls, b_cls, b_txt = "done",    "badge-done",    "✓ DONE"
            elif i == current:
                cls, b_cls, b_txt = "active",  "badge-active",  "◉ ACTIVE"
            else:
                cls, b_cls, b_txt = "pending", "badge-pending", "○ QUEUED"

            ts_str = time.strftime("%H:%M:%S") if (i == current or i in done) else "--:--:--"
            bar    = '<div class="step-bar-wrap"><div class="step-bar"></div></div>' if i == current else ""

            st.markdown(f"""
            <div class="step-card {cls}">
              <div class="step-num-big">{num}</div>
              <div class="step-inner">
                <div class="step-op">OPERATION_{num} &nbsp;//&nbsp; {ts_str}</div>
                <div class="step-name">{title}</div>
                <div class="step-desc">{desc}</div>
                {bar}
              </div>
              <div><span class="step-badge {b_cls}">{b_txt}</span></div>
            </div>
            """, unsafe_allow_html=True)

            if i < len(STEPS) - 1:
                st.markdown('<div class="connector-line"></div>', unsafe_allow_html=True)

    pipeline_ph = st.empty()

    def show_pipeline(current=-1, done=set()):
        with pipeline_ph.container():
            render_pipeline(current, done)

    # Default idle view
    show_pipeline(-1, set())

st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  EXECUTION
# ─────────────────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("⚠ NO DIRECTIVE — PROVIDE A RESEARCH TOPIC TO PROCEED.")
        st.stop()

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    state    = {}
    done_set = set()
    t0       = time.time()
    spinner_ph = st.empty()

    def show(current=-1):
        show_pipeline(current, done_set)

    # ── STEP 1: Search ────────────────────────────────────────────────────────
    show(0)
    with spinner_ph:
        with st.spinner(""):
            from agents import build_search_agent
            sa     = build_search_agent()
            sr     = sa.invoke({"messages": [
                ("user", f"Find recent, reliable and detailed information about: {topic}")
            ]})
            state["search_results"] = sr["messages"][-1].content
    done_set.add(0)
    show(1)

    # ── STEP 2: Reader ────────────────────────────────────────────────────────
    with spinner_ph:
        with st.spinner(""):
            from agents import build_reader_agent
            ra     = build_reader_agent()
            rr     = ra.invoke({"messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]})
            state["scraped_content"] = rr["messages"][-1].content
    done_set.add(1)
    show(2)

    # ── STEP 3: Writer ────────────────────────────────────────────────────────
    with spinner_ph:
        with st.spinner(""):
            from agents import writer_chain
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": (
                    f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                    f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
                ),
            })
    done_set.add(2)
    show(3)

    # ── STEP 4: Critic ────────────────────────────────────────────────────────
    with spinner_ph:
        with st.spinner(""):
            from agents import critic_chain
            state["feedback"] = critic_chain.invoke({"report": state["report"]})
    done_set.add(3)
    show(-1)
    spinner_ph.empty()

    elapsed    = time.time() - t0
    report_str = state["report"] if isinstance(state["report"], str) else str(state["report"])
    fb_str     = state["feedback"] if isinstance(state["feedback"], str) else str(state["feedback"])
    word_count = len(report_str.split())
    src_count  = state["search_results"].count("http")
    doc_id     = f"RPT-{hex(int(t0))[-6:].upper()}"

    st.markdown('<hr class="amber-divider">', unsafe_allow_html=True)

    # ── METRICS ───────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="metrics-grid">
      <div class="metric-block">
        <span class="metric-val">{elapsed:.0f}s</span>
        <span class="metric-lbl">Elapsed Time</span>
      </div>
      <div class="metric-block">
        <span class="metric-val">{word_count:,}</span>
        <span class="metric-lbl">Report Words</span>
      </div>
      <div class="metric-block">
        <span class="metric-val">{src_count}</span>
        <span class="metric-lbl">Sources Found</span>
      </div>
      <div class="metric-block">
        <span class="metric-val">4/4</span>
        <span class="metric-lbl">Agents Done</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── RAW INTEL FEEDS ───────────────────────────────────────────────────────
    st.markdown('<div class="output-label">// RAW INTELLIGENCE FEEDS</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="output-label">SEARCH AGENT OUTPUT</div>', unsafe_allow_html=True)
        p = state["search_results"][:850]
        if len(state["search_results"]) > 850: p += "\n\n[...TRUNCATED...]"
        st.markdown(f'<div class="intel-panel">{p}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="output-label">READER AGENT OUTPUT</div>', unsafe_allow_html=True)
        p2 = state["scraped_content"][:850]
        if len(state["scraped_content"]) > 850: p2 += "\n\n[...TRUNCATED...]"
        st.markdown(f'<div class="intel-panel">{p2}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="amber-divider">', unsafe_allow_html=True)

    # ── INTELLIGENCE BRIEFING ─────────────────────────────────────────────────
    st.markdown(f"""
    <div class="report-masthead">
      <div>
        <div class="report-doc-id">
          DOCUMENT: {doc_id} &nbsp;//&nbsp;
          {time.strftime("%Y-%m-%d %H:%M:%S")} UTC &nbsp;//&nbsp;
          SUBJECT: {topic.upper()[:50]}
        </div>
        <div class="report-doc-title">INTELLIGENCE BRIEFING</div>
      </div>
      <div><span class="report-stamp">TOP SECRET</span></div>
    </div>
    <div class="report-body-wrap">
    """, unsafe_allow_html=True)
    st.markdown(report_str)
    st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        label="⬡  DOWNLOAD BRIEFING  (.md)",
        data=report_str,
        file_name=f"oracle_{topic[:35].replace(' ','_').lower()}.md",
        mime="text/markdown",
    )

    st.markdown('<hr class="amber-divider">', unsafe_allow_html=True)

    # ── ADVERSARIAL REVIEW ────────────────────────────────────────────────────
    st.markdown("""
    <div class="critic-wrap">
      <div class="critic-header">
        <span class="critic-title">⬡ ADVERSARIAL REVIEW // CRITIC CHAIN</span>
        <span class="critic-tag">QUALITY ASSURANCE LAYER</span>
      </div>
      <div class="critic-body-wrap">
    """, unsafe_allow_html=True)
    st.markdown(fb_str)
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown('<hr class="amber-divider">', unsafe_allow_html=True)
    st.success(f"✓  ALL 4 AGENTS COMPLETE — BRIEFING GENERATED IN {elapsed:.1f}s")