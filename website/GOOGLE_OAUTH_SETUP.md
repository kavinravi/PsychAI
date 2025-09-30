# Google OAuth Setup Guide for PsychAI

This guide will help you set up Google Sign-In for your PsychAI application.

---

## Why Set This Up?

Google OAuth provides:
- ✅ One-click sign-in/sign-up
- ✅ No password to remember
- ✅ Trusted authentication
- ✅ Better user experience

---

## Step-by-Step Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click the project dropdown at the top
4. Click "New Project"
5. Enter project name: **"PsychAI"**
6. Click "Create"
7. Wait for the project to be created (~30 seconds)

### 2. Enable Google+ API

1. In the left sidebar, go to **"APIs & Services"** > **"Library"**
2. Search for **"Google+ API"** or **"Google Identity"**
3. Click on it
4. Click **"Enable"**
5. Wait for it to enable

### 3. Configure OAuth Consent Screen

1. Go to **"APIs & Services"** > **"OAuth consent screen"**
2. Choose **"External"** (unless you have a Google Workspace)
3. Click "Create"
4. Fill in the required fields:
   - **App name:** PsychAI
   - **User support email:** Your email
   - **Developer contact information:** Your email
5. Click "Save and Continue"
6. **Scopes:** Click "Add or Remove Scopes"
   - Select: `email`, `profile`, `openid`
   - Click "Update" then "Save and Continue"
7. **Test users:** Add your email and any friend's emails you want to test with
8. Click "Save and Continue"
9. Review and click "Back to Dashboard"

### 4. Create OAuth 2.0 Credentials

1. Go to **"APIs & Services"** > **"Credentials"**
2. Click **"Create Credentials"** > **"OAuth 2.0 Client ID"**
3. Choose application type: **"Web application"**
4. Enter name: **"PsychAI Web App"**
5. Under **"Authorized JavaScript origins"**, click "Add URI":
   - For local testing: `http://localhost:8501`
   - For production (after deployment): `https://your-app-name.streamlit.app`
6. Under **"Authorized redirect URIs"**, click "Add URI":
   - For local testing: `http://localhost:8501`
   - For production: `https://your-app-name.streamlit.app`
7. Click **"Create"**
8. **IMPORTANT:** Copy the **Client ID** and **Client Secret** that appear
   - Client ID looks like: `xxxxx.apps.googleusercontent.com`
   - Client Secret is a shorter string
   - Save these somewhere safe!

---

## Configure Your App

### For Local Development:

1. Open `website/.streamlit/secrets.toml`
2. Update the `[google_oauth]` section:

```toml
[google_oauth]
client_id = "your-client-id-here.apps.googleusercontent.com"
client_secret = "your-client-secret-here"
redirect_uri = "http://localhost:8501"

[environment]
session_timeout_hours = 24
enable_google_auth = true  # Set to true!
```

3. Save the file
4. Restart Streamlit

### For Streamlit Cloud Deployment:

1. In your Streamlit Cloud app settings, go to "Secrets"
2. Add/update:

```toml
[google_oauth]
client_id = "your-client-id-here.apps.googleusercontent.com"
client_secret = "your-client-secret-here"
redirect_uri = "https://your-actual-app-url.streamlit.app"

[environment]
enable_google_auth = true
```

3. **IMPORTANT:** Go back to Google Cloud Console:
   - APIs & Services > Credentials
   - Edit your OAuth 2.0 Client ID
   - Add your Streamlit Cloud URL to both:
     - Authorized JavaScript origins
     - Authorized redirect URIs
   - Save

---

## Testing

1. Restart your Streamlit app
2. Go to the Authentication page
3. You should now see a working **"Continue with Google"** button with the Google logo
4. Click it - you'll be redirected to Google
5. Sign in with your Google account
6. You'll be redirected back to your app, signed in!

---

## Troubleshooting

### "Error 400: redirect_uri_mismatch"
- Go to Google Cloud Console > Credentials
- Make sure your redirect URI exactly matches what you entered
- For local: `http://localhost:8501` (no trailing slash)
- For Streamlit Cloud: `https://your-app.streamlit.app` (exact URL)

### "Error 403: access_denied"
- Check OAuth consent screen is published
- Make sure your email is added as a test user
- Verify the app is not restricted

### Button says "Setup Required"
- Check that secrets.toml has `enable_google_auth = true`
- Verify client_id and client_secret are set
- Make sure secrets.toml file exists and is properly formatted

### Still not working?
- Check Streamlit app logs for errors
- Verify Google Cloud project has Google+ API enabled
- Make sure OAuth consent screen is completed
- Try creating new credentials

---

## Security Best Practices

1. **Never commit secrets:**
   - `secrets.toml` is already in `.gitignore`
   - Never push Client Secret to GitHub

2. **Restrict your OAuth:**
   - Only add trusted redirect URIs
   - Keep test user list limited during testing
   - Publish consent screen only when ready for public use

3. **Rotate credentials if exposed:**
   - If Client Secret is leaked, delete and create new credentials
   - Update everywhere it's used

---

## Production Publishing (Optional)

To make Google Sign-In available to everyone (not just test users):

1. Go to OAuth consent screen
2. Click "Publish App"
3. Fill in verification form (if required by Google)
4. Wait for Google review (can take days/weeks)

**Note:** You can use it with test users without publishing!

---

## Summary

**What you need:**
- ✅ Google Cloud Project
- ✅ OAuth consent screen configured
- ✅ OAuth 2.0 Client ID and Secret
- ✅ Secrets configured in `secrets.toml`

**Result:**
- Users can sign in with one click
- No password management needed
- Professional authentication experience

---

**Questions?** Check the [Google Identity documentation](https://developers.google.com/identity/protocols/oauth2) or reach out for help!
