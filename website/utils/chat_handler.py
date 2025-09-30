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
    Get response from the fine-tuned LLM
    
    This is a placeholder function. You'll replace this with actual model inference
    once your fine-tuned model is ready.
    
    Args:
        user_message: The user's current message
        conversation_history: List of previous messages in the conversation
    
    Returns:
        The LLM's response as a string
    """
    # TODO: Replace this placeholder with actual model inference
    # For now, return a helpful placeholder message
    
    placeholder_responses = [
        "I understand you're reaching out for support. While I'm still being set up, "
        "I want you to know that your feelings are valid and it's brave of you to seek help. "
        "Once our system is fully configured, I'll be able to provide more personalized guidance.",
        
        "Thank you for sharing that with me. I'm currently in development mode, but I want "
        "to acknowledge what you've expressed. In the meantime, if you're experiencing a crisis, "
        "please reach out to a trusted adult or call a crisis helpline.",
        
        "I hear you, and I appreciate you opening up. My AI capabilities are still being "
        "configured, but I want you to know that seeking support is an important step. "
        "Remember, there are always people who care and want to help.",
    ]
    
    # Simple logic to vary responses
    import random
    response = random.choice(placeholder_responses)
    
    return response

def load_model_placeholder():
    """
    Placeholder function for loading the fine-tuned model
    
    Once your model is trained, you'll implement this function to:
    1. Load the base model and LoRA adapters
    2. Set up the tokenizer
    3. Configure generation parameters
    
    Example implementation (for later):
    ```python
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import PeftModel
    
    base_model = "Qwen/Qwen2.5-7B-Instruct"
    adapter_path = "path/to/your/lora/adapters"
    
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    model = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto")
    model = PeftModel.from_pretrained(model, adapter_path)
    
    return model, tokenizer
    ```
    """
    return None, None

def format_conversation_for_model(messages: List[Dict]) -> str:
    """
    Format conversation history for model input
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
    
    Returns:
        Formatted string ready for model input
    """
    # This will depend on your model's chat template
    # For now, a simple format
    formatted = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        formatted += f"{role.capitalize()}: {content}\n"
    
    return formatted