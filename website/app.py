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
    initial_sidebar_state="expanded",
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4A90E2;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Check if user is authenticated
    auth_status = check_authentication()
    
    if not auth_status["authenticated"]:
        # Show welcome page if not authenticated
        show_welcome_page()
    else:
        # Show main app with sidebar navigation
        show_main_app(auth_status)

def show_welcome_page():
    """Display welcome page for unauthenticated users"""
    st.markdown('<div class="main-header">🧠 PsychAI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">AI-Powered Child Psychology Support Assistant</div>', 
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h3>Welcome to PsychAI</h3>
        <p>A specialized AI assistant trained to provide supportive guidance for child and adolescent mental health concerns.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### What We Offer")
        st.markdown("""
        - 🎯 **Specialized Support**: Trained specifically on child psychology and family counseling data
        - 🔒 **Safe & Private**: Your conversations are confidential and secure
        - 💙 **Empathetic Guidance**: Supportive, therapist-like responses without diagnoses
        - 🌟 **Always Available**: 24/7 access to mental health support
        """)
        
        st.markdown("""
        <div class="warning-box">
        <strong>⚠️ Important Notice:</strong><br>
        This AI assistant provides supportive guidance only and does not replace professional mental health services. 
        In case of emergency or crisis, please contact your local emergency services or crisis hotline.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Authentication buttons
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔐 Sign In", use_container_width=True, type="primary"):
                st.switch_page("pages/1_Authentication.py")
        with col_b:
            if st.button("📝 Create Account", use_container_width=True):
                st.switch_page("pages/1_Authentication.py")

def show_main_app(auth_status):
    """Display main application for authenticated users"""
    # Sidebar
    with st.sidebar:
        st.title("🧠 PsychAI")
        st.markdown(f"**Welcome, {auth_status['name']}!**")
        st.markdown("---")
        
        # Navigation
        st.markdown("### Navigation")
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
        if st.button("💬 Chat with AI", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Chat.py")
        
        st.markdown("---")
        
        # User info and logout
        st.markdown("### Account")
        st.info(f"📧 {auth_status['email']}")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
    
    # Main content
    st.markdown('<div class="main-header">Welcome to PsychAI</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h3>💬 Start a Conversation</h3>
        <p>Connect with our AI assistant trained specifically for child and adolescent mental health support.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Chatting →", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Chat.py")
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h3>📚 About This Project</h3>
        <p>PsychAI uses advanced language models fine-tuned on counseling data to provide empathetic, 
        supportive responses for child psychology concerns.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Guidelines
    st.markdown("### 🌟 How to Get the Most Out of PsychAI")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Be Open**
        - Share your concerns honestly
        - Provide context about situations
        - Ask follow-up questions
        """)
    
    with col2:
        st.markdown("""
        **Stay Safe**
        - No personal identifying info
        - Use for guidance, not diagnosis
        - Seek professional help when needed
        """)
    
    with col3:
        st.markdown("""
        **Take Action**
        - Apply suggested strategies
        - Follow up on resources
        - Consider professional therapy
        """)

if __name__ == "__main__":
    main()
