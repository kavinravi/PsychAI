"""
PsychAI - Child Psychology Support Assistant
Main Streamlit Application Entry Point
"""

import streamlit as st
from utils.auth import check_authentication, logout_user

# Page configuration
st.set_page_config(
    page_title="PsychAI - Child Psychology Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Modern CSS styling
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Top navigation bar */
    .nav-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        z-index: 1000;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .nav-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .nav-buttons {
        display: flex;
        gap: 1rem;
    }
    
    /* Add top padding to main content */
    .main .block-container {
        padding-top: 5rem;
    }
    
    /* Hero section */
    .hero {
        text-align: center;
        padding: 3rem 0;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #94a3b8;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Feature cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .feature-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 2rem;
        border: 1px solid #334155;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
        border-color: #6366f1;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #94a3b8;
        line-height: 1.6;
    }
    
    /* Warning box */
    .warning-card {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: #0f172a;
        margin: 2rem 0;
    }
    
    .warning-card strong {
        font-weight: 600;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def main():
    # Check if user is authenticated
    auth_status = check_authentication()
    
    if not auth_status["authenticated"]:
        show_welcome_page()
    else:
        show_main_app(auth_status)

def show_welcome_page():
    """Display welcome page for unauthenticated users"""
    
    # Top navigation bar with inline buttons using query params
    st.markdown("""
        <div class="nav-container">
            <div class="nav-logo">
                <span>🧠</span>
                <span>PsychAI</span>
            </div>
            <div class="nav-buttons">
                <a href="?page=auth&tab=signin" style="text-decoration: none;">
                    <button class="nav-btn nav-btn-secondary">Sign In</button>
                </a>
                <a href="?page=auth&tab=signup" style="text-decoration: none;">
                    <button class="nav-btn nav-btn-primary">Create Account</button>
                </a>
            </div>
        </div>
        
        <style>
        .nav-btn {
            padding: 0.5rem 1.5rem;
            border-radius: 8px;
            font-weight: 500;
            font-size: 15px;
            cursor: pointer;
            transition: all 0.2s;
            font-family: 'Inter', sans-serif;
        }
        
        .nav-btn-secondary {
            background: rgba(255,255,255,0.2);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        .nav-btn-secondary:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .nav-btn-primary {
            background: white;
            color: #667eea;
            border: none;
            font-weight: 600;
        }
        
        .nav-btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Check if we should redirect to auth page
    query_params = st.query_params
    if query_params.get("page") == "auth":
        st.switch_page("pages/1_Authentication.py")
    
    # Hero section
    st.markdown("""
        <div class="hero">
            <h1 class="hero-title">AI-Powered Child Psychology Support</h1>
            <p class="hero-subtitle">
                A specialized assistant designed to provide empathetic, evidence-based guidance 
                for child and adolescent mental health concerns.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Features (with proper markdown parsing)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Specialized Support</div>
                <div class="feature-desc">
                    Trained on child psychology and family counseling data to provide 
                    age-appropriate, evidence-based guidance.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <div class="feature-title">Private & Secure</div>
                <div class="feature-desc">
                    Your conversations are confidential, encrypted, and stored securely. 
                    We take your privacy seriously.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">💙</div>
                <div class="feature-title">Empathetic Guidance</div>
                <div class="feature-desc">
                    Supportive, therapist-like responses designed to help without 
                    providing diagnoses or medical advice.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">⏰</div>
                <div class="feature-title">Always Available</div>
                <div class="feature-desc">
                    Access mental health support 24/7, whenever you need someone to talk to 
                    about your concerns.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Important notice
    st.markdown("""
        <div class="warning-card">
            <strong>⚠️ Important Notice:</strong><br>
            This AI assistant provides supportive guidance only and does not replace professional 
            mental health services. In case of emergency or crisis, please contact your local 
            emergency services or crisis hotline (US: 988).
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_main_app(auth_status):
    """Display main application for authenticated users"""
    
    # Top navigation bar for authenticated users
    st.markdown(f"""
        <div class="top-nav">
            <div class="nav-logo">
                <span>🧠</span>
                <span>PsychAI</span>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem; color: white;">
                <span style="opacity: 0.9;">Welcome, {auth_status['name']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
        if st.button("💬 Chat with AI", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Chat.py")
        
        st.markdown("---")
        
        st.markdown("### Account")
        st.info(f"📧 {auth_status['email']}")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
    
    # Main dashboard content
    st.markdown("""
        <div class="hero">
            <h1 class="hero-title">Welcome Back!</h1>
            <p class="hero-subtitle">
                How can I support you today?
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <div class="feature-title">Start a Conversation</div>
                <div class="feature-desc">
                    Connect with our AI assistant for child and adolescent mental health support.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Chatting →", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Chat.py")
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📚</div>
                <div class="feature-title">About This Project</div>
                <div class="feature-desc">
                    PsychAI uses advanced language models fine-tuned on counseling data.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()