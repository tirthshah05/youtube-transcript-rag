import html

import streamlit as st
import streamlit.components.v1 as components

from transcript import extract_video_id, get_transcript
from chunking import create_chunks
from embedding import encode_text
from retriever import build_index, retrieve
from llm import generate_answer
from video_meta import get_video_meta
import style


# ----------------------------
# Page setup
# ----------------------------

st.set_page_config(
    page_title="Reel Desk — YouTube Transcript RAG",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="expanded",
)

style.inject(st)


# ----------------------------
# Session State Initialization
# ----------------------------

for key, default in [
    ("transcript", None),
    ("chunks", None),
    ("index", None),
    ("messages", []),
    ("video_id", None),
    ("video_meta", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:

    st.markdown(
        "<div class='reel-eyebrow'>REEL DESK</div>"
        "<div style='font-family:Space Grotesk,sans-serif;font-weight:700;"
        "font-size:1.15rem;margin-bottom:0.2rem;'>Control Panel</div>",
        unsafe_allow_html=True,
    )

    with st.expander("About this tool", expanded=False):
        st.markdown(
            """
Paste any YouTube link, and this tool pulls the transcript,
indexes it for semantic search, and lets you ask questions that
get answered strictly from what's said in the video.
"""
        )

        st.markdown("<div class='side-eyebrow'>Features</div>", unsafe_allow_html=True)

        FEATURE_ICONS = {
            "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"></circle><line x1="3" y1="12" x2="21" y2="12"></line><path d="M12 3a13.5 13.5 0 0 1 3.5 9A13.5 13.5 0 0 1 12 21a13.5 13.5 0 0 1-3.5-9A13.5 13.5 0 0 1 12 3z"></path></svg>',
            "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="10.5" cy="10.5" r="6.5"></circle><line x1="20" y1="20" x2="15.3" y2="15.3"></line></svg>',
            "spark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 14.4 9 22 9 15.8 13.6 18 21 12 16.6 6 21 8.2 13.6 2 9 9.6 9"></polygon></svg>',
            "video": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="1.5" y="5.5" width="14" height="13" rx="2"></rect><polygon points="22.5 8 16.5 12 22.5 16"></polygon></svg>',
        }

        for icon, label in [
            ("globe", "Multilingual transcript support"),
            ("search", "Semantic search with FAISS"),
            ("spark", "Gemini answer generation"),
            ("video", "YouTube transcript RAG"),
        ]:
            st.markdown(
                f"<div class='feature-row'>{FEATURE_ICONS[icon]}<span>{label}</span></div>",
                unsafe_allow_html=True,
            )

        st.markdown("<div class='side-eyebrow'>Tech stack</div>", unsafe_allow_html=True)
        st.markdown(
            "".join(
                f"<span class='tag-pill'>{t}</span>"
                for t in ["Streamlit", "FAISS", "Sentence Transformers", "Gemini API"]
            ),
            unsafe_allow_html=True,
        )

    st.divider()

    k = st.slider(
        "Context depth (chunks retrieved per question)",
        min_value=1,
        max_value=10,
        value=3,
    )

    st.divider()

    if st.button("🗑️  Clear chat"):
        st.session_state["messages"] = []
        st.rerun()


# ----------------------------
# Hero
# ----------------------------

st.markdown(
    """
    <div class="reel-eyebrow">TRANSCRIPT DESK</div>
    <div class="reel-title">Ask the reel.</div>
    <div class="reel-subtitle">
        Drop in a YouTube link — the transcript gets indexed for semantic
        search, and every answer below is grounded strictly in what the
        video actually says, in whatever language you ask.
    </div>
    <div class="reel-stripe"></div>
    """,
    unsafe_allow_html=True,
)


# ----------------------------
# URL bar
# ----------------------------

url_col, btn_col = st.columns([5, 1], vertical_alignment="bottom")

with url_col:
    url = st.text_input(
        "Enter YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed",
    )

with btn_col:
    load_clicked = st.button("Load video", use_container_width=True)

if load_clicked:
    try:
        video_id = extract_video_id(url)

        with st.spinner("Reading the transcript and building the index..."):
            transcript = get_transcript(video_id)
            chunks = create_chunks(transcript)
            embeddings = encode_text(chunks)
            index = build_index(embeddings)
            meta = get_video_meta(video_id)

        st.session_state["transcript"] = transcript
        st.session_state["chunks"] = chunks
        st.session_state["index"] = index
        st.session_state["video_id"] = video_id
        st.session_state["video_meta"] = meta
        st.session_state["messages"] = []

        st.success("Video loaded — the transcript desk is open below.")

    except ValueError:
        st.error("That doesn't look like a valid YouTube URL. Try pasting the full link.")

    except Exception:
        st.exception(Exception)
        raise


# ----------------------------
# Main workspace
# ----------------------------

st.write("")

if st.session_state["index"] is None:

    st.markdown(
        """
        <div class="empty-state">
            <div class="glyph">🎞️</div>
            <div class="headline">Nothing loaded yet</div>
            <div>Paste a YouTube link above and hit <b>Load video</b> to open the transcript desk.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:

    reel_col, chat_col = st.columns([0.26, 0.74], gap="large")

    # ---- Left: reel card ----
    with reel_col:
        meta = st.session_state["video_meta"] or {}
        video_id = st.session_state["video_id"]

        with st.container(border=True):
            st.video(f"https://www.youtube.com/watch?v={video_id}")

            title = html.escape(meta.get("title", "Untitled video"))
            author = html.escape(meta.get("author", ""))

            st.markdown(f"<div class='reel-card-title'>{title}</div>", unsafe_allow_html=True)
            if author:
                st.markdown(f"<div class='reel-card-channel'>{author}</div>", unsafe_allow_html=True)

            st.markdown(
                f"""
                <div class="reel-chip-row">
                    <span class="reel-chip">{len(st.session_state["chunks"])} chunks indexed</span>
                    <span class="reel-chip">top-{k} retrieval</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ---- Right: chat ----
    with chat_col:

        st.markdown(
            "<div class='reel-eyebrow' style='margin-bottom:0.6rem;'>CHAT WITH THE VIDEO</div>",
            unsafe_allow_html=True,
        )

        if not st.session_state["messages"]:
            st.markdown(
                "<div class='empty-state' style='padding:1.6rem;'>"
                "Ask a question below to start the conversation.</div>",
                unsafe_allow_html=True,
            )

        for message in st.session_state["messages"]:
            role = message["role"]
            label = "You" if role == "user" else "From the transcript"
            content = (
                html.escape(message["content"])
                if role == "user"
                else message["content"]
            )

            st.markdown(
                f"""
                <div class="msg-row {role}">
                    <div class="msg-bubble {role}">
                        <span class="msg-label">{label}</span>
                        {content}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Invisible anchor + script: scrolls the page to the latest
        # message every time the app reruns, so new answers are always
        # visible without the user scrolling manually.
        st.markdown("<div id='chat-anchor'></div>", unsafe_allow_html=True)
        components.html(
            """
            <script>
                var doc = window.parent.document;
                var anchor = doc.getElementById('chat-anchor');
                if (anchor) { anchor.scrollIntoView({behavior: 'smooth', block: 'end'}); }
            </script>
            """,
            height=0,
        )

    # Chat input is called outside the columns so Streamlit pins it to
    # the bottom of the app — it stays visible without scrolling.
    question = st.chat_input("Ask anything about the video...")

    if question:
        st.session_state["messages"].append({"role": "user", "content": question})

        with st.spinner("Searching the transcript..."):
            retrieved_chunks = retrieve(
                st.session_state["index"],
                question,
                st.session_state["chunks"],
                k=k,
            )

            recent_history = st.session_state["messages"][:-1][-10:]

            answer = generate_answer(question, retrieved_chunks, recent_history)

        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.rerun()
