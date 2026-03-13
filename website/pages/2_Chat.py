"""
Chat interface page for PsychAI
Allows authenticated users to interact with the fine-tuned LLM
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth import check_authentication, logout_user
from utils.chat_handler import (
    initialize_chat,
    get_chat_history,
    add_message,
    clear_chat,
    save_chat_history,
    get_llm_response,
)

st.set_page_config(
    page_title="Chat — PsychAI",
    page_icon="🧠",
    layout="wide",
)

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stHeader"] { display: none !important; }

/* sidebar styling */
section[data-testid="stSidebar"] {
    background: #0c0d12 !important;
    border-right: 1px solid rgba(255,255,255,0.04) !important;
}
section[data-testid="stSidebar"] .stButton > button {
    font-family: 'Inter', sans-serif !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* top bar */
.chat-topbar {
    position: sticky; top: 0; z-index: 100;
    padding: 1rem 1.5rem;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    background: rgba(8,9,13,0.75);
    border-bottom: 1px solid rgba(255,255,255,0.04);
    display: flex; align-items: center; gap: 0.75rem;
}
.chat-topbar .brand {
    font-weight: 700; font-size: 1.1rem; color: #fafafa;
}
.chat-topbar .sep {
    color: #3f3f46; font-weight: 300;
}
.chat-topbar .page-name {
    color: #71717a; font-size: 0.95rem; font-weight: 500;
}

/* messages */
.msg {
    padding: 1.25rem 1.5rem;
    border-radius: 16px;
    margin-bottom: 1rem;
    animation: msgIn 0.25s ease-out;
    line-height: 1.7;
    font-size: 0.95rem;
}
@keyframes msgIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.msg-user {
    background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(99,102,241,0.10));
    border: 1px solid rgba(139,92,246,0.15);
    color: #e4e4e7;
    margin-left: 12%;
}
.msg-ai {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    color: #d4d4d8;
    margin-right: 12%;
}
.msg-role {
    font-weight: 600; font-size: 0.8rem;
    margin-bottom: 0.5rem; opacity: 0.6;
    text-transform: uppercase; letter-spacing: 0.04em;
}
.msg-time {
    font-size: 0.72rem; opacity: 0.35;
    margin-top: 0.6rem;
}

/* disclaimer */
.chat-disclaimer {
    background: rgba(250,204,21,0.04);
    border: 1px solid rgba(250,204,21,0.1);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
    font-size: 0.85rem;
    color: #a1a1aa;
    line-height: 1.6;
}
.chat-disclaimer strong { color: #e4e4e7; }

/* welcome state */
.chat-welcome {
    text-align: center;
    padding: 4rem 2rem;
    color: #52525b;
}
.chat-welcome h2 {
    font-size: 1.5rem; font-weight: 700;
    color: #e4e4e7; margin-bottom: 0.5rem;
}
.chat-welcome p {
    font-size: 0.95rem; color: #71717a;
    max-width: 400px; margin: 0 auto 2rem;
    line-height: 1.6;
}
.chat-welcome .topics {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    justify-content: center; max-width: 450px;
    margin: 0 auto;
}
.chat-welcome .topic-tag {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 100px;
    padding: 0.35rem 0.9rem;
    font-size: 0.8rem;
    color: #a1a1aa;
}

/* status badge */
.status-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(139,92,246,0.08);
    border: 1px solid rgba(139,92,246,0.15);
    border-radius: 100px;
    padding: 0.3rem 0.8rem;
    font-size: 0.75rem;
    color: #a78bfa; font-weight: 500;
    margin-bottom: 1.5rem;
}
.status-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: #8b5cf6;
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink {
    0%,100% { opacity: 1; }
    50%     { opacity: 0.3; }
}

/* streamlit overrides */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    border-radius: 10px !important;
}
.stTextArea textarea {
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
}
</style>""", unsafe_allow_html=True)


def main():
    auth_status = check_authentication()

    if not auth_status["authenticated"]:
        st.warning("Please sign in to access the chat.")
        if st.button("Go to Sign In"):
            st.switch_page("pages/1_Authentication.py")
        return

    initialize_chat()

    # ---- sidebar ----
    with st.sidebar:
        st.markdown("### 🧠 PsychAI")
        st.caption(f"Signed in as **{auth_status['name']}**")
        st.markdown("---")

        if st.button("🏠  Home", use_container_width=True):
            st.switch_page("app.py")

        if st.button("🗑️  New Chat", use_container_width=True):
            clear_chat()
            st.rerun()

        if st.button("💾  Save History", use_container_width=True):
            save_chat_history(auth_status["email"])
            st.success("Saved!")

        st.markdown("---")
        st.markdown(
            "<span style='font-size:0.78rem;color:#71717a;font-weight:600;"
            "text-transform:uppercase;letter-spacing:0.06em'>Crisis Resources</span>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<span style='font-size:0.82rem;color:#a1a1aa;line-height:1.7'>"
            "**988** — Suicide & Crisis Lifeline<br>"
            "**741741** — Crisis Text Line<br>"
            "**1-866-488-7386** — Trevor Project"
            "</span>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        if st.button("🚪  Logout", use_container_width=True):
            logout_user()
            st.rerun()

    # ---- top bar ----
    st.markdown("""
        <div class="chat-topbar">
            <span class="brand">🧠 PsychAI</span>
            <span class="sep">/</span>
            <span class="page-name">Chat</span>
        </div>
    """, unsafe_allow_html=True)

    # ---- disclaimer ----
    st.markdown("""
        <div class="chat-disclaimer">
            <strong>⚠️ Reminder:</strong> PsychAI is not a substitute for
            professional care. If you're in crisis, please contact
            <strong>988</strong> or your local emergency services.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="status-badge">
            <span class="status-dot"></span>
            Development mode — placeholder responses
        </div>
    """, unsafe_allow_html=True)

    # ---- messages ----
    messages = get_chat_history()

    if not messages:
        st.markdown("""
            <div class="chat-welcome">
                <h2>How can I help today?</h2>
                <p>I'm here to listen and offer supportive guidance.
                   Share whatever's on your mind.</p>
                <div class="topics">
                    <span class="topic-tag">School stress</span>
                    <span class="topic-tag">Anxiety</span>
                    <span class="topic-tag">Friendships</span>
                    <span class="topic-tag">Family</span>
                    <span class="topic-tag">Self-esteem</span>
                    <span class="topic-tag">Emotions</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            ts = msg.get("timestamp", "")
            time_str = ""
            if ts:
                try:
                    time_str = datetime.fromisoformat(ts).strftime("%I:%M %p")
                except Exception:
                    pass

            if role == "user":
                st.markdown(f"""
                    <div class="msg msg-user">
                        <div class="msg-role">You</div>
                        {content}
                        <div class="msg-time">{time_str}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="msg msg-ai">
                        <div class="msg-role">PsychAI</div>
                        {content}
                        <div class="msg-time">{time_str}</div>
                    </div>
                """, unsafe_allow_html=True)

    # ---- input ----
    st.markdown("---")

    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_area(
                "Message",
                placeholder="Type your message here…",
                label_visibility="collapsed",
                height=80,
                key="user_input",
            )
        with col2:
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            submit = st.form_submit_button("Send", use_container_width=True, type="primary")

    if submit and user_input and user_input.strip():
        add_message("user", user_input.strip())

        with st.spinner("Thinking…"):
            response = get_llm_response(user_input.strip(), messages)

        add_message("assistant", response)
        save_chat_history(auth_status["email"])
        st.rerun()


if __name__ == "__main__":
    main()
