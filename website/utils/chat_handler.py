"""
Chat handler utilities for PsychAI
Manages conversation with the fine-tuned LLM
Uses Supabase database for persistent storage
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict

from .database import (
    save_message_db,
    get_chat_history_db,
    delete_chat_db,
    log_user_activity_db
)

def initialize_chat():
    """Initialize chat session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chat_id" not in st.session_state:
        st.session_state.chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")

def get_chat_history() -> List[Dict]:
    """Get current chat history from session state"""
    return st.session_state.get("messages", [])

def add_message(role: str, content: str, save_to_db: bool = False, user_email: str = None):
    """
    Add a message to chat history
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
        save_to_db: Whether to save to database immediately
        user_email: User email (required if save_to_db is True)
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    
    st.session_state.messages.append(message)
    
    # Save to database if requested
    if save_to_db and user_email:
        try:
            save_message_db(
                user_email=user_email,
                chat_id=st.session_state.chat_id,
                role=role,
                content=content
            )
        except Exception as e:
            print(f"Error saving message to database: {e}")

def clear_chat():
    """Clear current chat history and start a new session"""
    st.session_state.messages = []
    st.session_state.chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")

def save_chat_history(user_email: str):
    """
    Save entire chat history to database
    This is called to persist the session to the database
    """
    if not st.session_state.get("messages"):
        return
    
    chat_id = st.session_state.get("chat_id")
    
    try:
        # Save all messages that haven't been saved yet
        for message in st.session_state.messages:
            save_message_db(
                user_email=user_email,
                chat_id=chat_id,
                role=message["role"],
                content=message["content"]
            )
        
        # Log activity
        log_user_activity_db(
            user_email=user_email,
            activity_type="chat_saved",
            metadata={"chat_id": chat_id, "message_count": len(st.session_state.messages)}
        )
        
        return True
    except Exception as e:
        print(f"Error saving chat history: {e}")
        return False

def load_chat_history(user_email: str, chat_id: str):
    """Load a previous chat session from database"""
    try:
        messages = get_chat_history_db(user_email, chat_id)
        
        # Convert database format to session state format
        st.session_state.messages = [
            {
                "role": msg["role"],
                "content": msg["content"],
                "timestamp": msg["timestamp"]
            }
            for msg in messages
        ]
        st.session_state.chat_id = chat_id
        
        return True
    except Exception as e:
        print(f"Error loading chat history: {e}")
        return False

def delete_chat(user_email: str, chat_id: str):
    """Delete a chat and all its messages"""
    try:
        success = delete_chat_db(user_email, chat_id)
        
        # If it's the current chat, clear the session
        if st.session_state.get("chat_id") == chat_id:
            clear_chat()
        
        return success
    except Exception as e:
        print(f"Error deleting chat: {e}")
        return False

def get_llm_response(user_message: str, conversation_history: List[Dict]) -> str:
    """
    Get a reply from the fine-tuned PsychAI model (Qwen3-8B + LoRA on HF Hub).

    Args:
        user_message: The user's latest message.
        conversation_history: Prior messages in the same chat (excluding the
            new user message).

    Returns:
        The model's response text.
    """
    try:
        from .model_inference import generate_reply
        return generate_reply(user_message, conversation_history)
    except Exception as e:
        print(f"[chat_handler] Model inference failed: {type(e).__name__}: {e}")
        return (
            "I'm having trouble reaching the model right now. Please try again in a moment. "
            "If this keeps happening, let the team know — and remember, if you're in crisis "
            "you can call or text **988** for immediate support."
        )


def format_conversation_for_model(messages: List[Dict]) -> str:
    """Simple text rendering of a conversation (used for logging/debugging)."""
    formatted = ""
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        formatted += f"{role.capitalize()}: {content}\n"
    return formatted