import streamlit as st
import time
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=Nunito:ital,wght@0,300;0,400;0,500;0,600;1,400&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    color: #241f3d;
}

.stApp {
    background: #fff5ee;
    background-image:
        radial-gradient(circle at top left, rgba(255,140,90,0.42), transparent 40%),
        radial-gradient(circle at top right, rgba(130,90,255,0.38), transparent 38%),
        radial-gradient(circle at bottom left, rgba(255,190,60,0.32), transparent 42%),
        radial-gradient(circle at bottom right, rgba(34,180,95,0.18), transparent 35%),
        linear-gradient(180deg, #fff5ee 0%, #fdeee2 100%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

.hero { text-align: center; padding: 3rem 0 2rem; }
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff6f3c;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Quicksand', sans-serif;
    font-size: clamp(2.6rem, 5.5vw, 4.4rem);
    font-weight: 700;
    line-height: 1.05;
    color: #2e2a44;
    margin: 0 0 1rem;
}
.hero h1 span {
    background: linear-gradient(135deg, #ff6f3c, #7c4dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1.05rem;
    color: #5b5570;
    max-width: 540px;
    margin: 0 auto;
    line-height: 1.7;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,111,60,0.5), transparent);
    margin: 2rem 0;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.9) !important;
    border: 1.5px solid rgba(255,111,60,0.45) !important;
    border-radius: 14px !important;
    color: #241f3d !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.1rem !important;
    transition: all 0.2s ease !important;
}
.stTextInput > div > div > input::placeholder { color: #9b94b3 !important; }
.stTextInput > div > div > input:focus {
    border-color: #ff6f3c !important;
    box-shadow: 0 0 0 4px rgba(255,111,60,0.25) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.74rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #ff6f3c !important;
    font-weight: 500 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #ff6f3c 0%, #7c4dff 100%) !important;
    color: white !important;
    font-family: 'Quicksand', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 2.2rem !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 10px 28px rgba(255,111,60,0.4) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 14px 32px rgba(255,111,60,0.5) !important;
}

div[data-testid="column"] .stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.75) !important;
    color: #5b5570 !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    border: 1px solid rgba(255,140,90,0.6) !important;
    border-radius: 10px !important;
    padding: 0.5rem 0.9rem !important;
    box-shadow: none !important;
    width: 100%;
}
div[data-testid="column"] .stButton > button[kind="secondary"]:hover {
    border-color: #ff6f3c !important;
    color: #ff6f3c !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(255,111,60,0.25) !important;
}

.chip-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #9b94b3;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
    margin-top: 0.3rem;
}

/* ── Step cards ── */
.step-card {
    background: rgba(255,255,255,0.55);
    border: 1px solid rgba(124,77,255,0.28);
    border-radius: 18px;
    padding: 1.4rem 1.7rem;
    margin-bottom: 1.1rem;
    position: relative;
    overflow: hidden;
    transition: all 0.35s ease;
    backdrop-filter: blur(8px);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    border-radius: 18px 0 0 18px;
    background: rgba(124,77,255,0.22);
    transition: background 0.35s;
}

/* waiting — default, no change */

/* running — orange pulse */
.step-card.active {
    border-color: rgba(255,111,60,0.65);
    background: rgba(255,140,90,0.18);
    animation: pulse-orange 1.6s ease-in-out infinite;
}
.step-card.active::before { background: #ff6f3c; }

@keyframes pulse-orange {
    0%, 100% { box-shadow: 0 0 0 0 rgba(255,111,60,0.0); }
    50%       { box-shadow: 0 0 0 6px rgba(255,111,60,0.18); }
}

/* done — solid green */
.step-card.done {
    border-color: rgba(34,180,95,0.6);
    background: rgba(34,180,95,0.13);
    animation: none;
}
.step-card.done::before { background: #22b45f; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.3rem;
}
.step-num   { font-family: 'DM Mono', monospace; font-size: 0.7rem; font-weight: 500; letter-spacing: 0.12em; color: #ff6f3c; }
.step-title { font-family: 'Quicksand', sans-serif; font-size: 1.02rem; font-weight: 700; color: #2e2a44; }
.step-status { margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.68rem; letter-spacing: 0.08em; }
.status-waiting { color: #9b94b3; }
.status-running { color: #ff6f3c; }
.status-done    { color: #22b45f; font-weight: 700; }

/* ── Source cards ── */
.source-card {
    background: rgba(255,255,255,0.8);
    border: 1px solid rgba(124,77,255,0.2);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.source-number {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #ff6f3c;
    margin-bottom: 0.4rem;
}
.source-title {
    font-family: 'Quicksand', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #2e2a44;
    margin-bottom: 0.3rem;
}
.source-url {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #7c4dff;
    margin-bottom: 0.7rem;
    word-break: break-all;
}
.source-snippet { font-size: 0.88rem; line-height: 1.75; color: #3a3556; }

/* ── Scraped content cards ── */
.scraped-card {
    background: rgba(255,255,255,0.8);
    border: 1px solid rgba(124,77,255,0.2);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.scraped-url {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #7c4dff;
    margin-bottom: 0.6rem;
    word-break: break-all;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(124,77,255,0.15);
}
.scraped-body { font-size: 0.88rem; line-height: 1.75; color: #3a3556; white-space: pre-wrap; }

/* ── Report / feedback panels ── */
.report-panel {
    background: rgba(255,255,255,0.6);
    border: 1px solid rgba(255,111,60,0.45);
    border-radius: 22px;
    padding: 2rem 2.4rem;
    margin-top: 1rem;
    backdrop-filter: blur(10px);
}
.feedback-panel {
    background: rgba(255,255,255,0.6);
    border: 1px solid rgba(78,194,126,0.3);
    border-radius: 22px;
    padding: 2rem 2.4rem;
    margin-top: 1rem;
    backdrop-filter: blur(10px);
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
}
.panel-label.orange { color: #ff6f3c; border-bottom: 1px solid rgba(255,111,60,0.32); }
.panel-label.green  { color: #22b45f; border-bottom: 1px solid rgba(78,194,126,0.18); }

/* ── Force dark text everywhere ── */
[data-testid="stMarkdownContainer"] * { color: #2e2a44 !important; }
[data-testid="stMarkdownContainer"] a { color: #7c4dff !important; text-decoration: underline; }
.stMarkdown p, .stMarkdown li, .stMarkdown ul, .stMarkdown ol,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4,
.stMarkdown strong, .stMarkdown em, .stMarkdown blockquote,
.stMarkdown td, .stMarkdown th, .stMarkdown code { color: #2e2a44 !important; }

.stSpinner > div { color: #ff6f3c !important; }

details {
    background: rgba(255,255,255,0.4);
    border-radius: 14px;
    padding: 0.3rem 0.8rem;
    border: 1px solid rgba(124,77,255,0.22);
}
details summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.76rem !important;
    color: #5b5570 !important;
    letter-spacing: 0.08em !important;
    cursor: pointer;
}

.section-heading {
    font-family: 'Quicksand', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #2e2a44;
    margin: 1.8rem 0 1rem;
}
.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #9b94b3;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.06em;
}
.helper-text {
    font-size: 0.8rem;
    color: #8780a0;
    margin-top: -0.5rem;
    margin-bottom: 1rem;
}

[data-testid="stDownloadButton"] > button {
    background: rgba(255,255,255,0.8) !important;
    color: #2e2a44 !important;
    border: 1.5px solid rgba(255,111,60,0.5) !important;
    border-radius: 12px !important;
    font-family: 'Quicksand', sans-serif !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    width: auto !important;
    padding: 0.6rem 1.4rem !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: #ff6f3c !important;
    color: #ff6f3c !important;
    box-shadow: 0 6px 18px rgba(255,111,60,0.2) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def step_card(num, title, state, desc=""):
    status_map = {
        "waiting": ("WAITING",   "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",    "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#8780a0;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


def parse_search_results(raw: str) -> list:
    sources = []
    current = {}
    for line in raw.splitlines():
        line = line.strip()
        if line.lower().startswith("title:"):
            if current:
                sources.append(current)
                current = {}
            current["title"] = line[6:].strip()
        elif line.lower().startswith("url:"):
            current["url"] = line[4:].strip()
        elif line.lower().startswith("snippet:"):
            current["snippet"] = line[8:].strip()
        elif "snippet" in current and line:
            current["snippet"] = current.get("snippet", "") + " " + line
    if current:
        sources.append(current)
    return [s for s in sources if s.get("title") or s.get("url")]


def render_search_results(raw: str):
    sources = parse_search_results(raw)
    if not sources:
        st.markdown(f'<div class="scraped-body">{raw}</div>', unsafe_allow_html=True)
        return
    for i, src in enumerate(sources, 1):
        title   = src.get("title", "—")
        url     = src.get("url", "")
        snippet = src.get("snippet", "")
        url_display = f'<a href="{url}" target="_blank">{url}</a>' if url.startswith("http") else url
        st.markdown(f"""
        <div class="source-card">
            <div class="source-number">Source {i}</div>
            <div class="source-title">{title}</div>
            <div class="source-url">{url_display}</div>
            <div class="source-snippet">{snippet}</div>
        </div>
        """, unsafe_allow_html=True)


def render_scraped_content(raw: str):
    import re
    blocks = re.split(r'(?:^|\n)(?:URL:\s*)?(https?://\S+)', raw)
    if len(blocks) < 2:
        st.markdown(f'<div class="scraped-body">{raw}</div>', unsafe_allow_html=True)
        return
    for url, content in zip(blocks[1::2], blocks[2::2]):
        url = url.strip()
        content = content.strip()[:3000]
        url_display = f'<a href="{url}" target="_blank">{url}</a>'
        st.markdown(f"""
        <div class="scraped-card">
            <div class="scraped-url">🔗 {url_display}</div>
            <div class="scraped-body">{content}</div>
        </div>
        """, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for key in ("results", "running", "done", "current_step"):
    if key not in st.session_state:
        if key == "results":
            st.session_state[key] = {}
        elif key == "current_step":
            st.session_state[key] = None
        else:
            st.session_state[key] = False

if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

if "pending_topic" in st.session_state:
    st.session_state.topic_input = st.session_state.pending_topic
    del st.session_state.pending_topic


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Researcher<span>Agent</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout ────────────────────────────────────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Roadmap for AGI development in next 5 years",
        key="topic_input",
    )
    st.markdown(
        '<div class="helper-text">💡 Type any topic, or click an example below to get started.</div>',
        unsafe_allow_html=True
    )
    run_btn = st.button("⚡ Run Research Pipeline", use_container_width=True)

    st.markdown('<div class="chip-label">✨ TRY ONE OF THESE</div>', unsafe_allow_html=True)
    examples = [
        "Future of LLM in Tech Industry",
        "All Latest AI Agents in 2026",
        "Roadmap for AGI development in next 5 years",
    ]
    chip_cols = st.columns(len(examples))
    for col, ex in zip(chip_cols, examples):
        with col:
            if st.button(ex, key=f"chip_{ex}", use_container_width=True):
                st.session_state.pending_topic = ex
                st.rerun()

with col_pipeline:
    st.markdown('<div class="section-heading">🧩 Pipeline</div>', unsafe_allow_html=True)

    r    = st.session_state.results
    step = st.session_state.current_step   # which step is currently running

    STEPS = ["search", "reader", "writer", "critic"]

    def step_state(key):
        """Return 'done' / 'running' / 'waiting' for a pipeline step."""
        if key in r:
            return "done"
        if step == key:
            return "running"
        return "waiting"

    step_card("01", "Search Agent",  step_state("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  step_state("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  step_state("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  step_state("critic"), "Reviews & scores the report")


# ── Trigger ───────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results      = {}
        st.session_state.running      = True
        st.session_state.done         = False
        st.session_state.current_step = "search"   # kick off at step 1
        st.rerun()


# ── Pipeline execution — one step per rerun ───────────────────────────────────
if st.session_state.running and not st.session_state.done:

    topic_val = st.session_state.topic_input
    r         = st.session_state.results
    step      = st.session_state.current_step

    # ── Step 1: Search ──
    if step == "search":
        with st.spinner("🔍 Search Agent is working…"):
            search_agent = build_search_agent()
            sr = search_agent.invoke({
                "messages": [("user", f"""
Search for information about: {topic_val}

Use the web_search tool.

Among all search results, select ONLY the 3 most relevant sources.

Return in this EXACT format for each source (repeat 3 times):

Title: <title of the page>
URL: <full url>
Snippet: <1-2 sentence summary of what the page covers>

Do not summarize the topic itself.
Do not add any extra commentary before or after.
Return only the 3 best sources using exactly the format above.
""")]
            })
        r["search"] = sr["messages"][-1].content
        st.session_state.results      = r
        st.session_state.current_step = "reader"   # advance to next step
        st.rerun()                                  # rerun → pipeline turns green, reader starts

    # ── Step 2: Reader ──
    elif step == "reader":
        with st.spinner("📄 Reader Agent is scraping top resources…"):
            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({
                "messages": [("user", f"""
You are a web scraper agent. Below are 3 search results about '{topic_val}'.

For EACH of the 3 URLs listed in the search results, scrape the page and return the content.

Search Results:
{r['search']}

For each URL you scrape, return in this exact format:

URL: <the url you scraped>
Content:
<scraped text content from that page, at least 3-5 paragraphs>

---

Repeat this block for all 3 URLs. Do not skip any URL.
""")]
            })
        r["reader"] = rr["messages"][-1].content
        st.session_state.results      = r
        st.session_state.current_step = "writer"
        st.rerun()

    # ── Step 3: Writer ──
    elif step == "writer":
        with st.spinner("✍️ Writer is drafting the report…"):
            research_combined = (
                f"SEARCH RESULTS:\n{r['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{r['reader']}"
            )
            r["writer"] = writer_chain.invoke({
                "topic": topic_val,
                "research": research_combined
            })
        st.session_state.results      = r
        st.session_state.current_step = "critic"
        st.rerun()

    # ── Step 4: Critic ──
    elif step == "critic":
        with st.spinner("🧐 Critic is reviewing the report…"):
            r["critic"] = critic_chain.invoke({"report": r["writer"]})
        st.session_state.results      = r
        st.session_state.current_step = None        # all done
        st.session_state.running      = False
        st.session_state.done         = True
        st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📊 Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔍 Search Results — Sources Found", expanded=True):
            render_search_results(r["search"])

    if "reader" in r:
        with st.expander("📄 Scraped Content — Full Page Extracts", expanded=False):
            render_scraped_content(r["reader"])

    if "writer" in r:
        st.markdown(
            '<div class="report-panel">'
            '<div class="panel-label orange">📝 Final Research Report</div>'
            '</div>',
            unsafe_allow_html=True
        )
        with st.container():
            st.markdown(r["writer"])
        st.download_button(
            label="⬇ Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown(
            '<div class="feedback-panel">'
            '<div class="panel-label green">🧐 Critic Feedback</div>'
            '</div>',
            unsafe_allow_html=True
        )
        with st.container():
            st.markdown(r["critic"])


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchAgent · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)