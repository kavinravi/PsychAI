"""
Authentication utilities for PsychAI
Supports both Google OAuth and custom email/password authentication
Uses Supabase database for persistent storage
"""

import streamlit as st
import os
from datetime import datetime, timedelta
import hashlib
import secrets
from typing import Optional, Dict

from .database import (
    create_user_db,
    get_user_db,
    user_exists_db,
    log_user_activity_db
)

# Session timeout (in hours)
SESSION_TIMEOUT_HOURS = 24

def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    """Hash a password with a salt"""
    if salt is None:
        salt = secrets.token_hex(32)
    
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return pwd_hash.hex(), salt

def verify_password(password: str, pwd_hash: str, salt: str) -> bool:
    """Verify a password against a hash"""
    new_hash, _ = hash_password(password, salt)
    return new_hash == pwd_hash

def create_user(email: str, password: str, name: str) -> tuple[bool, str]:
    """
    Create a new user account
    Returns: (success, message)
    """
    # Check if user already exists
    if user_exists_db(email):
        return False, "An account with this email already exists"
    
    # Validate email format
    if '@' not in email or '.' not in email.split('@')[1]:
        return False, "Please enter a valid email address"
    
    # Validate password strength
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # Hash the password
    pwd_hash, salt = hash_password(password)
    
    # Create user in database
    success = create_user_db(email, pwd_hash, salt, name, "custom")
    
    if success:
        return True, "Account created successfully!"
    else:
        return False, "Failed to create account. Please try again."

def authenticate_user(email: str, password: str) -> tuple[bool, str, Optional[str]]:
    """
    Authenticate a user with email and password
    Returns: (success, message, name)
    """
    user = get_user_db(email)
    
    if not user:
        return False, "Invalid email or password", None
    
    # Verify password
    if not verify_password(password, user["password_hash"], user["salt"]):
        return False, "Invalid email or password", None
    
    # Log login activity
    try:
        log_user_activity_db(email, "login", {"auth_method": "custom"})
    except:
        pass  # Don't fail authentication if logging fails
    
    return True, "Login successful!", user["name"]

def authenticate_with_google(google_credentials: Dict) -> tuple[bool, str, Optional[str]]:
    """
    Authenticate user with Google OAuth
    Returns: (success, message, name)
    """
    email = google_credentials.get("email")
    name = google_credentials.get("name")
    google_id = google_credentials.get("id")
    
    if not email or not name:
        return False, "Failed to retrieve Google account information", None
    
    # Check if user exists
    user = get_user_db(email)
    
    if not user:
        # Create new Google user
        success = create_user_db(
            email=email,
            password_hash="",  # No password for OAuth users
            salt="",
            name=name,
            auth_method="google"
        )
        
        if not success:
            return False, "Failed to create account", None
    
    # Log login activity
    try:
        log_user_activity_db(email, "login", {"auth_method": "google"})
    except:
        pass
    
    return True, "Google login successful!", name

def login_user(email: str, name: str, auth_method: str = "custom"):
    """Set session state for logged-in user"""
    st.session_state.authenticated = True
    st.session_state.user_email = email
    st.session_state.user_name = name
    st.session_state.auth_method = auth_method
    st.session_state.login_time = datetime.now().isoformat()

def logout_user():
    """Clear session state and log out user"""
    # Log logout activity before clearing session
    if st.session_state.get("user_email"):
        try:
            log_user_activity_db(st.session_state.user_email, "logout", {})
        except:
            pass
    
    for key in ["authenticated", "user_email", "user_name", "auth_method", "login_time"]:
        if key in st.session_state:
            del st.session_state[key]

def check_authentication() -> Dict:
    """
    Check if user is authenticated and session is valid
    Returns: dict with authenticated status and user info
    """
    # Check if authenticated
    if not st.session_state.get("authenticated", False):
        return {"authenticated": False}
    
    # Check session timeout
    login_time_str = st.session_state.get("login_time")
    if login_time_str:
        login_time = datetime.fromisoformat(login_time_str)
        if datetime.now() - login_time > timedelta(hours=SESSION_TIMEOUT_HOURS):
            logout_user()
            return {"authenticated": False, "message": "Session expired"}
    
    return {
        "authenticated": True,
        "email": st.session_state.get("user_email"),
        "name": st.session_state.get("user_name"),
        "auth_method": st.session_state.get("auth_method")
    }

def get_google_oauth_url() -> Optional[str]:
    """
    Generate Google OAuth URL
    Requires GOOGLE_CLIENT_ID to be set in environment or secrets
    """
    client_id = os.getenv("GOOGLE_CLIENT_ID") or st.secrets.get("google_oauth", {}).get("client_id")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI") or st.secrets.get("google_oauth", {}).get("redirect_uri", "http://localhost:8501")
    
    if not client_id:
        return None
    
    # This is a simplified version - actual implementation would use google-auth-oauthlib
    oauth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile"
    )
    
    return oauth_url