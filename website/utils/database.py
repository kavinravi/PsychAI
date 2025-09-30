"""
Database utilities for PsychAI using Supabase (PostgreSQL)
Handles all database connections and operations
"""

import os
from typing import Optional, Dict, List
from datetime import datetime
import streamlit as st
from supabase import create_client, Client

# Initialize Supabase client
_supabase_client: Optional[Client] = None

def get_supabase_client() -> Client:
    """Get or create Supabase client (singleton pattern)"""
    global _supabase_client
    
    if _supabase_client is None:
        supabase_url = os.getenv("SUPABASE_URL") or st.secrets.get("supabase", {}).get("url")
        supabase_key = os.getenv("SUPABASE_KEY") or st.secrets.get("supabase", {}).get("key")
        
        if not supabase_url or not supabase_key:
            raise ValueError(
                "Missing Supabase credentials. "
                "Set SUPABASE_URL and SUPABASE_KEY in environment or .streamlit/secrets.toml"
            )
        
        _supabase_client = create_client(supabase_url, supabase_key)
    
    return _supabase_client

def init_database():
    """
    Initialize database tables if they don't exist.
    This should be run once during setup.
    
    Note: You should run the SQL schema from database_schema.sql in your Supabase dashboard
    instead of calling this function. This is here for reference.
    """
    # The actual table creation should be done via Supabase dashboard SQL editor
    # See database_schema.sql for the schema
    pass

# User management functions
def create_user_db(email: str, password_hash: str, salt: str, name: str, auth_method: str = "custom") -> bool:
    """Create a new user in the database"""
    try:
        client = get_supabase_client()
        
        data = {
            "email": email,
            "name": name,
            "password_hash": password_hash,
            "salt": salt,
            "auth_method": auth_method,
            "created_at": datetime.now().isoformat()
        }
        
        result = client.table("users").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def get_user_db(email: str) -> Optional[Dict]:
    """Get user by email"""
    try:
        client = get_supabase_client()
        result = client.table("users").select("*").eq("email", email).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def user_exists_db(email: str) -> bool:
    """Check if user exists"""
    return get_user_db(email) is not None

# Chat history functions
def save_message_db(user_email: str, chat_id: str, role: str, content: str) -> bool:
    """Save a single message to the database"""
    try:
        client = get_supabase_client()
        
        data = {
            "user_email": user_email,
            "chat_id": chat_id,
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        result = client.table("chat_messages").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error saving message: {e}")
        return False

def get_chat_history_db(user_email: str, chat_id: str) -> List[Dict]:
    """Get all messages for a specific chat"""
    try:
        client = get_supabase_client()
        result = (
            client.table("chat_messages")
            .select("*")
            .eq("user_email", user_email)
            .eq("chat_id", chat_id)
            .order("timestamp", desc=False)
            .execute()
        )
        
        return result.data if result.data else []
    except Exception as e:
        print(f"Error getting chat history: {e}")
        return []

def get_user_chats_db(user_email: str) -> List[Dict]:
    """Get all chat sessions for a user"""
    try:
        client = get_supabase_client()
        result = (
            client.table("chat_messages")
            .select("chat_id, timestamp")
            .eq("user_email", user_email)
            .order("timestamp", desc=True)
            .execute()
        )
        
        if not result.data:
            return []
        
        # Group by chat_id and get the latest timestamp for each
        chats = {}
        for row in result.data:
            chat_id = row["chat_id"]
            if chat_id not in chats:
                chats[chat_id] = row
        
        return list(chats.values())
    except Exception as e:
        print(f"Error getting user chats: {e}")
        return []

def delete_chat_db(user_email: str, chat_id: str) -> bool:
    """Delete a chat and all its messages"""
    try:
        client = get_supabase_client()
        result = (
            client.table("chat_messages")
            .delete()
            .eq("user_email", user_email)
            .eq("chat_id", chat_id)
            .execute()
        )
        return True
    except Exception as e:
        print(f"Error deleting chat: {e}")
        return False

# Analytics/Usage functions (optional)
def log_user_activity_db(user_email: str, activity_type: str, metadata: Optional[Dict] = None):
    """Log user activity for analytics"""
    try:
        client = get_supabase_client()
        
        data = {
            "user_email": user_email,
            "activity_type": activity_type,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        
        client.table("user_activity").insert(data).execute()
    except Exception as e:
        print(f"Error logging activity: {e}")
        pass  # Don't fail on analytics errors

def get_user_stats_db(user_email: str) -> Dict:
    """Get usage statistics for a user"""
    try:
        client = get_supabase_client()
        
        # Count total messages
        messages_result = (
            client.table("chat_messages")
            .select("id", count="exact")
            .eq("user_email", user_email)
            .execute()
        )
        
        # Count unique chats
        chats = get_user_chats_db(user_email)
        
        return {
            "total_messages": messages_result.count if hasattr(messages_result, 'count') else 0,
            "total_chats": len(chats),
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {"total_messages": 0, "total_chats": 0}
