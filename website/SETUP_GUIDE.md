# Quick Setup Guide for PsychAI Website

## What's Already Done

Your Streamlit website is fully built and ready to use! Here's what's included:

- User authentication system (email/password)
- Google OAuth support (needs configuration)
- Chat interface with placeholder AI responses
- Session management and security
- Chat history saving
- Modern, professional UI
- All dependencies added to requirements.txt

## Getting Started (3 Easy Steps)

### Step 1: Install Dependencies

From your project root directory (`/Users/kavinravi/Downloads/Cursor/PsychAI`):

```bash
pip install -r requirements.txt
```

This will install Streamlit and all necessary packages.

### Step 2: Launch the Website

```bash
cd website
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`

### Step 3: Create an Account & Test

1. Click "Create Account" 
2. Fill in your details (any valid email format works)
3. Sign in and explore the chat interface!

**That's it!** The website is fully functional with custom authentication.

## Optional: Enable Google Sign-In

If you want to add Google OAuth authentication:

### What You Need to Do:

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create or Select a Project**
   - Click "Select a project" at the top
   - Click "New Project"
   - Name it "PsychAI" (or anything you like)
   - Click "Create"

3. **Enable Google+ API**
   - In the left sidebar: "APIs & Services" > "Library"
   - Search for "Google+ API"
   - Click on it and click "Enable"

4. **Create OAuth Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client ID"
   - If prompted, configure OAuth consent screen first:
     - User Type: "External"
     - App name: "PsychAI"
     - User support email: your email
     - Developer contact: your email
     - Save and continue through the remaining screens
   - Back to Create OAuth Client ID:
     - Application type: "Web application"
     - Name: "PsychAI Web App"
     - Authorized redirect URIs: `http://localhost:8501`
     - Click "Create"
   - **Copy your Client ID and Client Secret!**

5. **Add Credentials to Your App**
   
   Create `.streamlit/secrets.toml` in the website directory:
   
   ```bash
   cd /Users/kavinravi/Downloads/Cursor/PsychAI/website
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```
   
   Edit `.streamlit/secrets.toml` and add your credentials:
   
   ```toml
   [google_oauth]
   client_id = "YOUR_CLIENT_ID_HERE.apps.googleusercontent.com"
   client_secret = "YOUR_CLIENT_SECRET_HERE"
   redirect_uri = "http://localhost:8501"
   
   [environment]
   session_timeout_hours = 24
   enable_google_auth = true
   ```

6. **Restart the App**
   
   ```bash
   streamlit run app.py
   ```
   
   The "Sign in with Google" button will now be functional!

## Integrating Your Fine-Tuned Model

Currently, the chat uses placeholder responses. When your model is trained:

### Option 1: Quick Integration (Recommended)

Edit `website/utils/chat_handler.py` - find the `get_llm_response()` function and follow the TODO comments there.

### Option 2: I'll Help You!

Just let me know when your model is trained, and I'll help you integrate it. You'll need to tell me:
- Path to your LoRA adapters
- Base model name
- Any special generation parameters you want

## What API Keys/Credentials You Need

| Service | Required? | Purpose | How to Get |
|---------|-----------|---------|------------|
| **Google OAuth** | ❌ Optional | Google Sign-In button | Google Cloud Console (see above) |
| **Model Hosting** | ❌ Not yet | If you deploy model to API | Depends on hosting choice |

**That's it!** No other API keys needed for basic functionality.

## Testing Your Setup

### Test Custom Authentication:
1. Go to http://localhost:8501
2. Click "Create Account"
3. Sign up with email: `test@example.com`, password: `password123`, name: `Test User`
4. Sign in with those credentials
5. Navigate to Chat page
6. Send a message and get a placeholder response

### Test Features:
- Create account
- Sign in / Sign out
- Navigate between pages
- Send chat messages
- Clear chat
- Save chat history

## Common Issues & Solutions

### "Port 8501 is already in use"
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### "Module not found" errors
```bash
# Make sure you're in the right environment and reinstall
pip install -r requirements.txt --upgrade
```

### Can't create account / sign in
```bash
# Check permissions
mkdir -p website/data
chmod 755 website/data
```

### Google OAuth not working
- Double-check your credentials in `.streamlit/secrets.toml`
- Ensure redirect URI is exactly `http://localhost:8501`
- Try adding `http://localhost:8501/` (with trailing slash) as another authorized URI

## Where Your Data is Stored

- **User accounts**: `website/data/users.json`
- **Chat histories**: `website/data/chat_history/[user_email]/`
- **Sessions**: In-memory (cleared when you restart)

**Important**: For production, you'll want to use a proper database instead of JSON files.

## Customizing the UI

Want to change colors, fonts, or styling?

- **Theme**: Edit `website/.streamlit/config.toml`
- **Custom CSS**: Modify the `st.markdown()` sections in each page file
- **Layout**: Edit the page files directly

## Ready for Production?

Before deploying publicly:
1. [ ] Replace JSON storage with a database (PostgreSQL, MongoDB)
2. [ ] Set up proper HTTPS/SSL
3. [ ] Implement rate limiting
4. [ ] Add comprehensive logging
5. [ ] Create proper Terms of Service and Privacy Policy
6. [ ] Test security thoroughly
7. [ ] Set up monitoring and alerts

## Need Help?

If you run into any issues or need help with:
- Integrating your trained model
- Deploying to production
- Adding new features
- Fixing bugs

Just let me know! I'm here to help.

---

## Next Steps

1. **Now**: Test the website with custom authentication
2. **Soon**: Train your model using the data preparation notebook
3. **Then**: Integrate the trained model into the chat interface
4. **Finally**: Deploy to production!
