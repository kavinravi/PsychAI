"""
Authentication page for PsychAI
Handles user login and registration
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth import (
    create_user, 
    authenticate_user, 
    login_user, 
    check_authentication,
    get_google_oauth_url
)

st.set_page_config(
    page_title="Authentication - PsychAI",
    page_icon="🔐",
    layout="centered"
)

# Modern CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .auth-container {
        max-width: 450px;
        margin: 2rem auto;
        padding: 2.5rem;
        background: #1e293b;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
    }
    
    .auth-header {
        font-size: 2rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .auth-subheader {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 2rem;
        font-size: 0.95rem;
    }
    
    .google-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        width: 100%;
        padding: 12px 24px;
        background: white;
        color: #1f2937;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        font-weight: 500;
        font-size: 15px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .google-btn:hover {
        background: #f9fafb;
        border-color: #d1d5db;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .google-logo {
        width: 20px;
        height: 20px;
    }
    
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 2rem 0;
        color: #64748b;
        font-size: 0.875rem;
    }
    
    .divider::before,
    .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #334155;
    }
    
    .divider:not(:empty)::before {
        margin-right: 1rem;
    }
    
    .divider:not(:empty)::after {
        margin-left: 1rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def main():
    # Check if already authenticated
    auth_status = check_authentication()
    if auth_status["authenticated"]:
        st.success(f"✅ Already logged in as {auth_status['name']}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go to Home", use_container_width=True):
                st.switch_page("app.py")
        with col2:
            if st.button("Go to Chat", use_container_width=True, type="primary"):
                st.switch_page("pages/2_Chat.py")
        return
    
    st.markdown('<div class="auth-header">Welcome Back</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subheader">Sign in to access PsychAI</div>', unsafe_allow_html=True)
    
    # Tab selection for Login vs Sign Up
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_signup_form()

def show_login_form():
    """Display login form"""
    
    # Google OAuth option
    google_oauth_url = get_google_oauth_url()
    
    if google_oauth_url:
        st.markdown("""
            <a href="{}" style="text-decoration: none;">
                <div class="google-btn">
                    <svg class="google-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                    </svg>
                    <span>Continue with Google</span>
                </div>
            </a>
        """.format(google_oauth_url), unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="google-btn" style="opacity: 0.5; cursor: not-allowed;">
                <svg class="google-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                <span>Continue with Google (Setup Required)</span>
            </div>
        """, unsafe_allow_html=True)
        st.caption("ℹ️ Google Sign-In will be available once OAuth is configured.")
    
    st.markdown('<div class="divider">OR</div>', unsafe_allow_html=True)
    
    # Email/Password login
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Sign In", use_container_width=True, type="primary")
        
        if submit:
            if not email or not password:
                st.error("❌ Please enter both email and password")
            else:
                success, message, name = authenticate_user(email, password)
                
                if success:
                    login_user(email, name, "custom")
                    st.success(f"✅ {message}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

def show_signup_form():
    """Display signup form"""
    
    # Google OAuth option
    google_oauth_url = get_google_oauth_url()
    
    if google_oauth_url:
        st.markdown("""
            <a href="{}" style="text-decoration: none;">
                <div class="google-btn">
                    <svg class="google-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                    </svg>
                    <span>Sign up with Google</span>
                </div>
            </a>
        """.format(google_oauth_url), unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="google-btn" style="opacity: 0.5; cursor: not-allowed;">
                <svg class="google-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                <span>Sign up with Google (Setup Required)</span>
            </div>
        """, unsafe_allow_html=True)
        st.caption("ℹ️ Google Sign-Up will be available once OAuth is configured.")
    
    st.markdown('<div class="divider">OR</div>', unsafe_allow_html=True)
    
    # Email/Password signup
    with st.form("signup_form"):
        name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Minimum 8 characters")
        password_confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        
        agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        submit = st.form_submit_button("Create Account", use_container_width=True, type="primary")
        
        if submit:
            # Validation
            if not all([name, email, password, password_confirm]):
                st.error("❌ Please fill in all fields")
            elif password != password_confirm:
                st.error("❌ Passwords do not match")
            elif not agree_terms:
                st.error("❌ Please agree to the Terms of Service")
            else:
                success, message = create_user(email, password, name)
                
                if success:
                    st.success(f"✅ {message}")
                    st.info("👉 Please sign in using the 'Sign In' tab")
                    st.balloons()
                else:
                    st.error(f"❌ {message}")

if __name__ == "__main__":
    main()