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

# Custom CSS
st.markdown("""
    <style>
    .auth-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
    }
    .auth-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
        margin-bottom: 0.5rem;
    }
    .auth-subheader {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .divider {
        text-align: center;
        margin: 2rem 0;
        color: #999;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Check if already authenticated
    auth_status = check_authentication()
    if auth_status["authenticated"]:
        st.success(f"✅ Already logged in as {auth_status['name']}")
        if st.button("Go to Home"):
            st.switch_page("app.py")
        if st.button("Go to Chat"):
            st.switch_page("pages/2_Chat.py")
        return
    
    # Show auth page
    st.markdown('<div class="auth-header">🔐 Welcome</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subheader">Sign in to access PsychAI</div>', unsafe_allow_html=True)
    
    # Tab selection for Login vs Sign Up
    tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Create Account"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_signup_form()

def show_login_form():
    """Display login form"""
    st.markdown("### Sign in to your account")
    
    # Google OAuth option
    st.markdown("#### Sign in with Google")
    google_oauth_url = get_google_oauth_url()
    
    if google_oauth_url:
        if st.button("🔵 Continue with Google", use_container_width=True):
            st.info("🔄 Google OAuth integration in progress. Please use email/password for now.")
    else:
        st.info("ℹ️ Google Sign-In will be available once OAuth credentials are configured.")
    
    st.markdown('<div class="divider">── OR ──</div>', unsafe_allow_html=True)
    
    # Email/Password login
    st.markdown("#### Sign in with Email")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your.email@example.com")
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
    
    # Demo account info
    st.info("💡 **Demo Account**: If this is your first time, create an account in the 'Create Account' tab.")

def show_signup_form():
    """Display signup form"""
    st.markdown("### Create a new account")
    
    # Google OAuth option
    st.markdown("#### Sign up with Google")
    google_oauth_url = get_google_oauth_url()
    
    if google_oauth_url:
        if st.button("🔵 Sign up with Google", use_container_width=True):
            st.info("🔄 Google OAuth integration in progress. Please use email/password for now.")
    else:
        st.info("ℹ️ Google Sign-Up will be available once OAuth credentials are configured.")
    
    st.markdown('<div class="divider">── OR ──</div>', unsafe_allow_html=True)
    
    # Email/Password signup
    st.markdown("#### Create account with Email")
    
    with st.form("signup_form"):
        name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email", placeholder="your.email@example.com")
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
    
    # Terms and Privacy
    with st.expander("📋 Terms of Service & Privacy Policy"):
        st.markdown("""
        **Terms of Service (Summary)**
        - This service is for supportive guidance only
        - Not a replacement for professional mental health care
        - In emergencies, contact local emergency services
        - Users must be 13+ or have parental consent
        
        **Privacy Policy (Summary)**
        - Conversations are stored securely and privately
        - Data is not shared with third parties
        - Users can request data deletion at any time
        - We use industry-standard encryption
        
        *Note: These are simplified summaries. Full legal documents would be required for production use.*
        """)

if __name__ == "__main__":
    main()
