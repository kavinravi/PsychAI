"""
Chat interface page for PsychAI
Allows authenticated users to interact with the fine-tuned LLM
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth import check_authentication, logout_user
from utils.chat_handler import (
    initialize_chat,
    get_chat_history,
    add_message,
    clear_chat,
    save_chat_history,
    get_llm_response
)

st.set_page_config(
    page_title="Chat - PsychAI",
    page_icon="💬",
    layout="wide"
)

# Custom CSS for chat interface
st.markdown("""
    <style>
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    .message-role {
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .message-content {
        line-height: 1.6;
    }
    .message-timestamp {
        font-size: 0.75rem;
        color: #999;
        margin-top: 0.5rem;
    }
    .warning-banner {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin-bottom: 1rem;
    }
    .info-banner {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Check authentication
    auth_status = check_authentication()
    
    if not auth_status["authenticated"]:
        st.warning("🔒 Please sign in to access the chat")
        if st.button("Go to Sign In"):
            st.switch_page("pages/1_Authentication.py")
        return
    
    # Initialize chat
    initialize_chat()
    
    # Sidebar
    with st.sidebar:
        st.title("💬 PsychAI Chat")
        st.markdown(f"**{auth_status['name']}**")
        st.markdown("---")
        
        # Navigation
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
        
        st.markdown("---")
        
        # Chat controls
        st.markdown("### Chat Controls")
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat()
            st.rerun()
        
        if st.button("💾 Save History", use_container_width=True):
            save_chat_history(auth_status["email"])
            st.success("Chat saved!")
        
        st.markdown("---")
        
        # Crisis resources
        st.markdown("### 🆘 Crisis Resources")
        st.markdown("""
        **If you're in crisis:**
        - 🇺🇸 National Suicide Prevention Lifeline: 988
        - 🇺🇸 Crisis Text Line: Text HOME to 741741
        - 🇺🇸 Trevor Project (LGBTQ+): 1-866-488-7386
        """)
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
    
    # Main chat interface
    st.title("💬 Chat with PsychAI")
    
    # Important disclaimer
    st.markdown("""
    <div class="warning-banner">
    <strong>⚠️ Important Disclaimer:</strong><br>
    This AI provides supportive guidance only and is not a substitute for professional mental health care, 
    diagnosis, or treatment. If you're experiencing a mental health crisis, please contact emergency services 
    or a crisis hotline immediately.
    </div>
    """, unsafe_allow_html=True)
    
    # Model status indicator
    st.markdown("""
    <div class="info-banner">
    <strong>ℹ️ Model Status:</strong> Currently in development mode with placeholder responses. 
    Full AI capabilities will be available once the fine-tuned model is loaded.
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat history
    messages = get_chat_history()
    
    if not messages:
        st.info("👋 Welcome! Start the conversation by typing a message below.")
        st.markdown("""
        ### How can I help you today?
        
        I'm here to provide supportive guidance for concerns related to:
        - Child and adolescent mental health
        - School-related stress and anxiety
        - Family relationships
        - Social challenges
        - Emotional wellbeing
        
        Feel free to share what's on your mind. 💙
        """)
    else:
        # Display messages
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            timestamp = msg.get("timestamp", "")
            
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    time_str = dt.strftime("%I:%M %p")
                except:
                    time_str = ""
            else:
                time_str = ""
            
            if role == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <div class="message-role">👤 You</div>
                    <div class="message-content">{content}</div>
                    <div class="message-timestamp">{time_str}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <div class="message-role">🧠 PsychAI</div>
                    <div class="message-content">{content}</div>
                    <div class="message-timestamp">{time_str}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    # Use a form for better UX
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_input = st.text_area(
                "Your message",
                placeholder="Type your message here... (Shift+Enter for new line, Enter to send)",
                label_visibility="collapsed",
                height=100,
                key="user_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Send 📤", use_container_width=True, type="primary")
    
    # Handle message submission
    if submit and user_input and user_input.strip():
        # Add user message
        add_message("user", user_input.strip())
        
        # Get AI response
        with st.spinner("🤔 Thinking..."):
            response = get_llm_response(user_input.strip(), messages)
        
        # Add assistant response
        add_message("assistant", response)
        
        # Auto-save after each exchange
        save_chat_history(auth_status["email"])
        
        # Rerun to display new messages
        st.rerun()
    
    # Helpful tips
    with st.expander("💡 Tips for getting the most out of your chat"):
        st.markdown("""
        **Effective Communication:**
        - Be specific about your concerns
        - Provide context about situations
        - Ask follow-up questions
        - Share how you're feeling
        
        **Remember:**
        - Your privacy is protected
        - There's no judgment here
        - Take your time to express yourself
        - You can take breaks whenever needed
        
        **When to seek additional help:**
        - If you're having thoughts of self-harm
        - If you're in an abusive situation
        - If symptoms are severely impacting daily life
        - If you need immediate crisis support
        """)

if __name__ == "__main__":
    main()
