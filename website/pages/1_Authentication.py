"""
Authentication page for PsychAI
Handles user login and registration
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth import (
    create_user,
    authenticate_user,
    login_user,
    check_authentication,
    get_google_oauth_url,
)

st.set_page_config(
    page_title="Sign in — PsychAI",
    page_icon="🧠",
    layout="centered",
)

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.stApp { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }

/* mesh background */
.mesh-wrap {
    position: fixed; inset: 0; overflow: hidden;
    z-index: -1; pointer-events: none;
}
.mesh-blob {
    position: absolute; border-radius: 50%;
    filter: blur(150px); opacity: 0.10;
}
.mesh-blob.purple {
    width: 500px; height: 500px; background: #8b5cf6;
    top: -15%; right: -10%;
    animation: d1 18s ease-in-out infinite;
}
.mesh-blob.blue {
    width: 400px; height: 400px; background: #3b82f6;
    bottom: -10%; left: -8%;
    animation: d2 22s ease-in-out infinite;
}
@keyframes d1 {
    0%,100% { transform: translate(0,0); }
    50%     { transform: translate(30px,-40px); }
}
@keyframes d2 {
    0%,100% { transform: translate(0,0); }
    50%     { transform: translate(-40px,30px); }
}

/* back link */
.back-link {
    display: inline-flex; align-items: center; gap: 0.4rem;
    color: #71717a; font-size: 0.85rem; text-decoration: none;
    margin-bottom: 2rem; transition: color 0.2s;
}
.back-link:hover { color: #a1a1aa; }

/* center the main content area and constrain width */
.main .block-container {
    max-width: 480px !important;
    margin: 0 auto;
    padding: 2rem 1.5rem !important;
}
.auth-title {
    font-size: 1.75rem;
    font-weight: 700;
    color: #fafafa;
    text-align: center;
    margin-bottom: 0.3rem;
}
.auth-sub {
    text-align: center;
    color: #71717a;
    font-size: 0.92rem;
    margin-bottom: 2rem;
}

/* google button */
.g-btn {
    display: flex; align-items: center; justify-content: center;
    gap: 10px; width: 100%; padding: 0.7rem 1rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px; color: #e4e4e7;
    font-weight: 500; font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
    cursor: pointer; transition: all 0.2s;
    text-decoration: none !important;
}
.g-btn:hover {
    background: rgba(255,255,255,0.08);
    border-color: rgba(255,255,255,0.18);
}
.g-btn.disabled {
    opacity: 0.4; cursor: not-allowed;
    pointer-events: none;
}
.g-logo { width: 18px; height: 18px; }

/* divider */
.or-divider {
    display: flex; align-items: center;
    margin: 1.75rem 0; color: #3f3f46;
    font-size: 0.8rem;
}
.or-divider::before, .or-divider::after {
    content: ''; flex: 1;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.or-divider:not(:empty)::before { margin-right: 1rem; }
.or-divider:not(:empty)::after  { margin-left: 1rem; }

/* streamlit overrides */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
.stTextInput > div > div > input {
    border-radius: 10px !important;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    padding: 0.6rem 1.5rem;
}
</style>""", unsafe_allow_html=True)

GOOGLE_SVG = """<svg class="g-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
</svg>"""


def main():
    st.markdown("""
        <div class="mesh-wrap">
            <div class="mesh-blob purple"></div>
            <div class="mesh-blob blue"></div>
        </div>
    """, unsafe_allow_html=True)

    auth_status = check_authentication()
    if auth_status["authenticated"]:
        st.success(f"Already signed in as **{auth_status['name']}**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Home", use_container_width=True):
                st.switch_page("app.py")
        with col2:
            if st.button("Chat →", use_container_width=True, type="primary"):
                st.switch_page("pages/2_Chat.py")
        return

    st.markdown("""
        <a href="/" target="_self" class="back-link">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            Back to home
        </a>
    """, unsafe_allow_html=True)

    st.markdown('<div class="auth-title">Welcome</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="auth-sub">Sign in to start chatting with PsychAI</div>',
        unsafe_allow_html=True,
    )

    requested_tab = st.session_state.pop("_auth_tab", None) or st.query_params.get("tab", "signin")

    if requested_tab == "signup":
        tab_signup, tab_signin = st.tabs(["Create Account", "Sign In"])
        with tab_signup:
            _show_signup()
        with tab_signin:
            _show_login()
    else:
        tab_signin, tab_signup = st.tabs(["Sign In", "Create Account"])
        with tab_signin:
            _show_login()
        with tab_signup:
            _show_signup()


def _google_button(label: str):
    url = get_google_oauth_url()
    if url:
        st.markdown(
            f'<a href="{url}" class="g-btn">{GOOGLE_SVG}<span>{label}</span></a>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="g-btn disabled">{GOOGLE_SVG}<span>{label} (not configured)</span></div>',
            unsafe_allow_html=True,
        )


def _show_login():
    _google_button("Continue with Google")
    st.markdown('<div class="or-divider">or</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Your password")
        submit = st.form_submit_button("Sign In", use_container_width=True, type="primary")

        if submit:
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                ok, msg, name = authenticate_user(email, password)
                if ok:
                    login_user(email, name, "custom")
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)


def _show_signup():
    _google_button("Sign up with Google")
    st.markdown('<div class="or-divider">or</div>', unsafe_allow_html=True)

    with st.form("signup_form"):
        name = st.text_input("Full Name", placeholder="Jane Doe")
        email = st.text_input("Email", placeholder="you@example.com")
        pw = st.text_input("Password", type="password", placeholder="Min 8 characters")
        pw2 = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")

        tos_c1, tos_c2 = st.columns([0.08, 0.92], vertical_alignment="center")
        with tos_c1:
            agree = st.checkbox(" ", key="agree_tos", label_visibility="collapsed")
        with tos_c2:
            st.markdown(
                'I agree to the <a href="/Terms_of_Service" target="_blank" '
                'style="color:#a78bfa;text-decoration:underline;">Terms of Service</a>',
                unsafe_allow_html=True,
            )

        submit = st.form_submit_button("Create Account", use_container_width=True, type="primary")

        if submit:
            if not all([name, email, pw, pw2]):
                st.error("Please fill in all fields.")
            elif pw != pw2:
                st.error("Passwords do not match.")
            elif not agree:
                st.error("Please agree to the Terms of Service.")
            else:
                ok, msg = create_user(email, pw, name)
                if ok:
                    st.success(msg)
                    st.info("Switch to the **Sign In** tab to log in.")
                else:
                    st.error(msg)


if __name__ == "__main__":
    main()
