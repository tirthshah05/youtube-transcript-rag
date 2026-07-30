"""
Design system for the app — a "screening room" aesthetic:
dark editing-suite background, warm subtitle-amber accent for the
assistant's voice, cool teal for the viewer's voice, monospace
timecodes for structure. Import once and inject via st.markdown.
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --void: #0b0e0c;
    --panel: #121613;
    --panel-raised: #191f1b;
    --hairline: #262c27;
    --amber: #e3b341;
    --amber-dim: rgba(227, 179, 65, 0.14);
    --teal: #55d6b0;
    --teal-dim: rgba(85, 214, 176, 0.12);
    --text: #eceeec;
    --muted: #8b968f;
    --danger: #e3695f;
}

/* ---------- base ---------- */
html, body, .stApp {
    background: var(--void) !important;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

.block-container { padding-top: 2.2rem; max-width: 1180px; }

h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.01em; }

/* ---------- hero ---------- */
.reel-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    color: var(--amber);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.reel-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1.08;
    margin: 0 0 0.5rem 0;
}
.reel-subtitle {
    color: var(--muted);
    font-size: 1rem;
    max-width: 640px;
    margin-bottom: 1.1rem;
}
.reel-stripe {
    height: 6px;
    width: 100%;
    border-radius: 4px;
    margin-bottom: 2rem;
    background: repeating-linear-gradient(
        -45deg,
        var(--amber) 0px, var(--amber) 10px,
        var(--panel-raised) 10px, var(--panel-raised) 20px
    );
    opacity: 0.85;
}

/* ---------- inputs ---------- */
[data-testid="stTextInput"] input {
    background: var(--panel) !important;
    border: 1px solid var(--hairline) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.92rem;
    padding: 0.7rem 0.9rem !important;
    box-shadow: none !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--amber) !important;
    box-shadow: 0 0 0 1px var(--amber) !important;
}
[data-testid="stTextInput"] label { color: var(--muted) !important; font-size: 0.82rem; }
[data-testid="InputInstructions"] { display: none !important; }

.stButton > button {
    background: var(--amber) !important;
    color: #171208 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.3rem !important;
    transition: transform 0.12s ease, opacity 0.12s ease;
}
.stButton > button:hover { opacity: 0.88; transform: translateY(-1px); }
.stButton > button:active { transform: translateY(0px); }

[data-testid="stSidebar"] .stButton > button {
    background: var(--panel-raised) !important;
    color: var(--text) !important;
    border: 1px solid var(--hairline) !important;
    width: 100%;
}
[data-testid="stSidebar"] .stButton > button:hover { border-color: var(--danger) !important; color: var(--danger) !important; }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
    background: var(--panel) !important;
    border-right: 1px solid var(--hairline);
}
[data-testid="stSidebar"] .block-container { padding-top: 1.6rem; }

/* Sidebar text contrast — force light text everywhere in the sidebar,
   overriding Streamlit's own default paragraph/link colors. */
[data-testid="stSidebar"] * {
    color: var(--text);
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li {
    color: var(--text) !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #c7ccc8 !important;
    line-height: 1.55;
}

/* Expander (About this tool) */
[data-testid="stExpander"] {
    background: var(--panel-raised) !important;
    border: 1px solid var(--hairline) !important;
    border-radius: 10px !important;
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    background: var(--panel-raised) !important;
    color: var(--text) !important;
    font-weight: 500;
}
[data-testid="stExpander"] summary:hover { color: var(--amber) !important; }
[data-testid="stExpander"] svg { fill: var(--muted) !important; }
[data-testid="stExpander"] details { background: transparent !important; }

.side-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    color: var(--muted);
    text-transform: uppercase;
    margin: 1.1rem 0 0.6rem 0;
}
.feature-row {
    display: flex; align-items: center; gap: 0.6rem;
    font-size: 0.87rem; color: var(--text);
    padding: 0.32rem 0;
}
.feature-row svg {
    flex-shrink: 0;
    width: 15px;
    height: 15px;
    stroke: var(--muted);
}
.tag-pill {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--teal);
    background: var(--teal-dim);
    border: 1px solid rgba(85, 214, 176, 0.25);
    border-radius: 999px;
    padding: 0.18rem 0.62rem;
    margin: 0 0.3rem 0.3rem 0;
}

hr { border-color: var(--hairline) !important; margin: 1.1rem 0 !important; }

[data-testid="stSlider"] label { color: var(--muted) !important; font-size: 0.82rem; }

/* ---------- alerts ---------- */
[data-testid="stAlert"] {
    background: var(--panel-raised) !important;
    border: 1px solid var(--hairline) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

/* ---------- reel / video card ---------- */
/* st.container(border=True) wrapper — used for the reel card */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--panel);
    border: 1px solid var(--hairline) !important;
    border-radius: 14px;
}
[data-testid="stVerticalBlockBorderWrapper"] > div { border-radius: 14px; }
.reel-card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.02rem;
    color: var(--text);
    margin: 0.8rem 0 0.15rem 0;
    line-height: 1.3;
}
.reel-card-channel {
    color: var(--muted);
    font-size: 0.82rem;
    margin-bottom: 0.9rem;
}
.reel-chip-row { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.reel-chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--amber);
    background: var(--amber-dim);
    border: 1px solid rgba(227, 179, 65, 0.25);
    border-radius: 6px;
    padding: 0.28rem 0.55rem;
}

/* ---------- empty state ---------- */
.empty-state {
    border: 1px dashed var(--hairline);
    border-radius: 14px;
    padding: 2.6rem 1.5rem;
    text-align: center;
    color: var(--muted);
}
.empty-state .glyph { font-size: 1.8rem; margin-bottom: 0.6rem; }
.empty-state .headline { font-family: 'Space Grotesk', sans-serif; color: var(--text); font-size: 1.05rem; margin-bottom: 0.3rem; }

/* ---------- chat ---------- */
.chat-scroll { padding-right: 0.2rem; }

.msg-row { display: flex; margin: 0.55rem 0; }
.msg-row.user { justify-content: flex-end; }
.msg-row.assistant { justify-content: flex-start; }

.msg-bubble {
    max-width: 78%;
    padding: 0.7rem 0.95rem;
    border-radius: 12px;
    font-size: 0.93rem;
    line-height: 1.5;
}
.msg-bubble p { margin: 0.2rem 0; }

.msg-bubble.user {
    background: var(--teal-dim);
    border: 1px solid rgba(85, 214, 176, 0.28);
    color: var(--text);
    border-bottom-right-radius: 3px;
}
.msg-bubble.assistant {
    background: var(--panel-raised);
    border-left: 3px solid var(--amber);
    color: var(--text);
    border-bottom-left-radius: 3px;
}
.msg-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.3rem;
    display: block;
}

/* Chat input — ChatGPT-style soft rounded pill, single surface
   (no nested box), targeted broadly since Streamlit's internal
   class names shift between versions. */
[data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
    background: var(--void) !important;
}
[data-testid="stChatInput"] {
    background: var(--panel-raised) !important;
    border: 1px solid var(--hairline) !important;
    border-radius: 26px !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25) !important;
    padding: 0.15rem 0.3rem !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #3a423c !important;
}
[data-testid="stChatInput"] > div {
    background: transparent !important;
    border: none !important;
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInputTextArea"],
textarea[data-testid="stChatInputTextArea"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #f4f5f3 !important;
    caret-color: #f4f5f3 !important;
    -webkit-text-fill-color: #f4f5f3 !important;
    font-size: 0.95rem;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #9aa39c !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] button {
    background: #3a423c !important;
    border: none !important;
    border-radius: 50% !important;
}
[data-testid="stChatInput"] button:hover { background: var(--amber) !important; }
[data-testid="stChatInput"] button svg { fill: #f4f5f3 !important; }

/* ---------- scrollbar ---------- */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--void); }
::-webkit-scrollbar-thumb { background: var(--hairline); border-radius: 8px; }
</style>
"""


def inject(st):
    st.markdown(CSS, unsafe_allow_html=True)
