"""
PsychAI - Child Psychology Support Assistant
Main Streamlit Application Entry Point
"""

import streamlit as st
from utils.auth import check_authentication, logout_user

st.set_page_config(
    page_title="PsychAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GLOBAL_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ---------- animated background mesh ---------- */
.mesh-wrap {
    position: fixed;
    inset: 0;
    overflow: hidden;
    z-index: -1;
    pointer-events: none;
}
.mesh-blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(150px);
    opacity: 0.10;
}
.mesh-blob.purple {
    width: 650px; height: 650px;
    background: #8b5cf6;
    top: -18%; right: -8%;
    animation: drift1 18s ease-in-out infinite;
}
.mesh-blob.blue {
    width: 500px; height: 500px;
    background: #3b82f6;
    bottom: -12%; left: -6%;
    animation: drift2 22s ease-in-out infinite;
}
.mesh-blob.teal {
    width: 400px; height: 400px;
    background: #06b6d4;
    top: 45%; left: 45%;
    animation: drift3 20s ease-in-out infinite;
}
@keyframes drift1 {
    0%,100% { transform: translate(0,0) scale(1); }
    33%     { transform: translate(40px,-60px) scale(1.1); }
    66%     { transform: translate(-30px,40px) scale(.95); }
}
@keyframes drift2 {
    0%,100% { transform: translate(0,0) scale(1); }
    33%     { transform: translate(-50px,30px) scale(1.05); }
    66%     { transform: translate(40px,-40px) scale(.9); }
}
@keyframes drift3 {
    0%,100% { transform: translate(-50%,-50%) scale(1); }
    33%     { transform: translate(-45%,-55%) scale(1.1); }
    66%     { transform: translate(-55%,-45%) scale(.9); }
}

/* ---------- nav ---------- */
.nav {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 999;
    padding: 1rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    background: rgba(8,9,13,0.6);
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.nav-brand {
    font-size: 1.25rem;
    font-weight: 700;
    color: #fafafa;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.nav-actions {
    display: flex;
    gap: 0.75rem;
    align-items: center;
}
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem 1.25rem;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none !important;
    line-height: 1.4;
}
.btn-ghost {
    background: transparent;
    color: #a1a1aa;
    border: 1px solid rgba(255,255,255,0.08);
}
.btn-ghost:hover {
    color: #fafafa;
    border-color: rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.04);
}
.btn-primary {
    background: linear-gradient(135deg, #8b5cf6, #6366f1);
    color: #fff !important;
    border: none;
    font-weight: 600;
}
.btn-primary:hover {
    opacity: 0.9;
    transform: translateY(-1px);
    box-shadow: 0 8px 25px -5px rgba(139,92,246,0.35);
}

/* ---------- hero ---------- */
.hero {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 4rem 2rem 6rem;
    padding-top: calc(4rem + 56px);
    position: relative;
    margin-top: -5vh;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 1.1rem;
    border-radius: 100px;
    border: 1px solid rgba(139,92,246,0.2);
    background: rgba(139,92,246,0.06);
    color: #a78bfa;
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.02em;
    margin-bottom: 2.5rem;
}
.hero-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #8b5cf6;
    animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%,100% { opacity: 1; }
    50%     { opacity: 0.3; }
}
.hero-brand {
    font-size: clamp(4rem, 9vw, 7.5rem);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
    margin: 0 0 0.75rem;
    color: #fafafa;
}
.hero-brand .ai {
    background: linear-gradient(135deg, #a78bfa, #818cf8, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero h1 {
    font-size: clamp(1.8rem, 3.5vw, 2.8rem);
    font-weight: 600;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin: 0 0 1.5rem;
    color: #a1a1aa;
    max-width: 720px;
}
.hero h1 em {
    font-style: normal;
    color: #d4d4d8;
}
.hero-sub {
    font-size: 1.15rem;
    color: #71717a;
    max-width: 500px;
    line-height: 1.7;
    margin: 0 auto 2.5rem;
}
.hero-cta {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}
.hero-cta .btn {
    padding: 0.7rem 1.75rem;
    font-size: 0.95rem;
}
.scroll-hint {
    position: absolute;
    bottom: 2.5rem;
    left: 50%;
    transform: translateX(-50%);
    color: #3f3f46;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform: translateX(-50%) translateY(0); }
    50%     { transform: translateX(-50%) translateY(8px); }
}

/* ---------- sections ---------- */
.section {
    padding: 5rem 2rem 6rem;
    max-width: 1100px;
    margin: 0 auto;
}
.section-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #8b5cf6;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.75rem;
}
.section-title {
    font-size: clamp(1.75rem, 3vw, 2.4rem);
    font-weight: 700;
    color: #fafafa;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
}
.section-desc {
    font-size: 1.05rem;
    color: #71717a;
    max-width: 560px;
    line-height: 1.7;
    margin-bottom: 3rem;
}

/* ---------- feature cards ---------- */
.features-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
}
@media (max-width: 700px) {
    .features-grid { grid-template-columns: 1fr; }
}
.f-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 2rem;
    transition: all 0.3s ease;
}
.f-card:hover {
    background: rgba(255,255,255,0.04);
    border-color: rgba(139,92,246,0.2);
    transform: translateY(-2px);
}
.f-icon {
    width: 44px; height: 44px;
    border-radius: 12px;
    background: rgba(139,92,246,0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.25rem;
    color: #a78bfa;
}
.f-card h3 {
    font-size: 1.05rem;
    font-weight: 600;
    color: #e4e4e7;
    margin: 0 0 0.5rem;
}
.f-card p {
    font-size: 0.9rem;
    color: #71717a;
    line-height: 1.65;
    margin: 0;
}

/* ---------- notice ---------- */
.notice {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 2rem 5rem;
}
.notice-card {
    background: rgba(250,204,21,0.03);
    border: 1px solid rgba(250,204,21,0.1);
    border-radius: 12px;
    padding: 1.5rem 2rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}
.notice-icon { font-size: 1.2rem; flex-shrink: 0; margin-top: 2px; }
.notice-card p {
    margin: 0;
    font-size: 0.88rem;
    color: #a1a1aa;
    line-height: 1.65;
}
.notice-card strong { color: #e4e4e7; }

/* ---------- footer ---------- */
.site-footer {
    border-top: 1px solid rgba(255,255,255,0.04);
    padding: 2.5rem 2rem;
    text-align: center;
    color: #3f3f46;
    font-size: 0.8rem;
}

/* ---------- streamlit button overrides ---------- */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
}

/* ---------- dashboard (auth'd landing) ---------- */
.dash-hero {
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 7rem 2rem 4rem;
}
.dash-hero h1 {
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #fafafa;
    margin: 0 0 1rem;
}
.dash-hero h1 em {
    font-style: normal;
    background: linear-gradient(135deg, #a78bfa, #818cf8, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.dash-hero p {
    font-size: 1.1rem;
    color: #71717a;
    margin-bottom: 2.5rem;
}
</style>"""

MESH_BG = """
<div class="mesh-wrap">
    <div class="mesh-blob purple"></div>
    <div class="mesh-blob blue"></div>
    <div class="mesh-blob teal"></div>
</div>"""

SVG_TARGET = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
SVG_LOCK = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/><circle cx="12" cy="16" r="1"/></svg>'
SVG_HEART = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>'
SVG_CLOCK = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg>'
SVG_ARROW = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 5v14M5 12l7 7 7-7"/></svg>'


def main():
    auth_status = check_authentication()
    if not auth_status["authenticated"]:
        show_welcome_page()
    else:
        show_main_app(auth_status)


def show_welcome_page():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(MESH_BG, unsafe_allow_html=True)

    if st.query_params.get("page") == "auth":
        st.switch_page("pages/1_Authentication.py")

    st.markdown(f"""
        <div class="nav">
            <div class="nav-brand">🧠 PsychAI</div>
            <div class="nav-actions">
                <a href="?page=auth&tab=signin" target="_self" class="btn btn-ghost">Sign in</a>
                <a href="?page=auth&tab=signup" target="_self" class="btn btn-primary">Get Started</a>
            </div>
        </div>

        <div class="hero">
            <div class="hero-badge">
                <span class="dot"></span>
                AI-Powered Mental Health Support
            </div>
            <div class="hero-brand">Fr<span class="ai">AI</span>nd.ly</div>
            <h1>A safe space to <em>talk.</em></h1>
            <p class="hero-sub">
                An AI companion designed to support teens through anxiety,
                stress, and everyday challenges. No judgment — just understanding.
            </p>
            <div class="hero-cta">
                <a href="?page=auth&tab=signup" target="_self" class="btn btn-primary">Get Started</a>
                <a href="#about" class="btn btn-ghost">Learn more ↓</a>
            </div>
            <div class="scroll-hint">{SVG_ARROW}</div>
        </div>

        <div class="section" id="about">
            <div class="section-label">Why PsychAI</div>
            <div class="section-title">Built for the moments that matter</div>
            <div class="section-desc">
                Whether it's school stress, social pressure, or just needing
                someone to listen — PsychAI is here for you, anytime.
            </div>
            <div class="features-grid">
                <div class="f-card">
                    <div class="f-icon">{SVG_TARGET}</div>
                    <h3>Specialized Support</h3>
                    <p>Trained on child psychology and family counseling data
                       to provide age-appropriate, evidence-based guidance.</p>
                </div>
                <div class="f-card">
                    <div class="f-icon">{SVG_LOCK}</div>
                    <h3>Private &amp; Secure</h3>
                    <p>Your conversations stay yours. Encrypted, secure, and
                       never shared with anyone.</p>
                </div>
                <div class="f-card">
                    <div class="f-icon">{SVG_HEART}</div>
                    <h3>Empathetic Guidance</h3>
                    <p>Warm, therapist-like responses designed to validate your
                       feelings — never diagnose or prescribe.</p>
                </div>
                <div class="f-card">
                    <div class="f-icon">{SVG_CLOCK}</div>
                    <h3>Always Available</h3>
                    <p>24/7 access to mental health support, whenever you need
                       someone to talk to.</p>
                </div>
            </div>
        </div>

        <div class="notice">
            <div class="notice-card">
                <span class="notice-icon">⚠️</span>
                <p>
                    <strong>Important:</strong> PsychAI provides supportive guidance
                    only and does not replace professional mental health services.
                    If you or someone you know is in crisis, please contact your
                    local emergency services or the
                    <strong>988 Suicide &amp; Crisis Lifeline</strong> (call or text 988).
                </p>
            </div>
        </div>

        <div class="site-footer">
            PsychAI · Built with care for those who need it most
        </div>
    """, unsafe_allow_html=True)


def show_main_app(auth_status):
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(MESH_BG, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="nav">
            <div class="nav-brand">🧠 PsychAI</div>
            <div class="nav-actions">
                <span style="color:#71717a;font-size:0.875rem;">Hey, {auth_status['name']}</span>
            </div>
        </div>

        <div class="dash-hero">
            <div class="hero-badge">
                <span class="dot"></span>
                Welcome back
            </div>
            <h1>Ready to <em>talk?</em></h1>
            <p>Pick up where you left off, or start a new conversation.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        if st.button("💬  Start Chatting", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Chat.py")

        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

        if st.button("🚪  Logout", use_container_width=True):
            logout_user()
            st.rerun()


if __name__ == "__main__":
    main()
