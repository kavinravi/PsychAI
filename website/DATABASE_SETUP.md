# Quick Database Setup Guide

## Why Database?

The app now uses **Supabase (PostgreSQL)** instead of local JSON files. This means:
- ✅ Data persists across deployments
- ✅ Works on Streamlit Community Cloud
- ✅ Scalable and production-ready
- ✅ Secure with Row Level Security

## 5-Minute Setup

### 1. Create Free Supabase Account
1. Go to [https://supabase.com](https://supabase.com)
2. Sign up (free forever for small projects)
3. Create a new project
4. Wait ~2 minutes for it to provision

### 2. Set Up Database Tables
1. In Supabase dashboard, click **SQL Editor** (left sidebar)
2. Open `website/database_schema.sql` in your code editor
3. Copy all the SQL code
4. Paste into Supabase SQL Editor
5. Click **Run** (or press Cmd/Ctrl + Enter)
6. You should see "Success" messages

### 3. Get Your Credentials
1. In Supabase: Go to **Settings** > **API**
2. Copy two things:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon/public key** (long string starting with `eyJ...`)

### 4. Configure Your App
1. In your terminal:
   ```bash
   cd website
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Edit `.streamlit/secrets.toml`:
   ```toml
   [supabase]
   url = "https://your-project-id.supabase.co"  # Paste your URL
   key = "eyJhbGc..."  # Paste your anon key
   ```

3. Save the file

### 5. Test It!
```bash
streamlit run app.py
```

Create an account and verify:
- You can sign up
- You can log in
- Chat messages persist
- You can see data in Supabase dashboard (Table Editor > users, chat_messages)

---

## For Streamlit Cloud Deployment

When deploying to Streamlit Cloud:

1. Go to your app settings
2. Click "Secrets" in advanced settings
3. Paste your secrets:
   ```toml
   [supabase]
   url = "https://your-project-id.supabase.co"
   key = "your-anon-key"
   ```
4. Deploy!

---

## Verify It's Working

After setup, check Supabase dashboard:

1. Go to **Table Editor**
2. You should see 3 tables:
   - `users` - User accounts
   - `chat_messages` - All chat history
   - `user_activity` - Login/logout logs

3. After creating an account in your app:
   - Check `users` table - you should see your account
   - Send a message in chat
   - Check `chat_messages` - you should see your messages

---

## Troubleshooting

**"Missing Supabase credentials" error:**
- Check that `secrets.toml` exists in `website/.streamlit/`
- Verify URL and key are correct
- Make sure you're using the **anon/public** key, not the secret key

**Can't create account:**
- Check Supabase project is not paused (go to dashboard)
- Look in Supabase logs (Logs > API) for errors
- Verify database tables were created correctly

**Data not persisting:**
- Check RLS (Row Level Security) policies are enabled
- Verify user email matches in session state
- Check Supabase logs for permission errors

---

## What Changed?

**Old (JSON files):**
- Data stored in `website/data/users.json`
- Lost on every Streamlit Cloud deployment
- Not suitable for production

**New (Supabase):**
- Data stored in cloud PostgreSQL database
- Persists forever
- Production-ready with backups
- Secure with Row Level Security

---

## Free Tier Limits

Supabase free tier includes:
- ✅ 500MB database storage
- ✅ 50,000 monthly active users
- ✅ 2GB file storage
- ✅ 50MB file uploads
- ✅ Automatic backups (7 days)

This is more than enough for getting started!

---

**That's it!** Your app is now ready for production deployment. 🎉

For full production deployment guide, see `PRODUCTION_CHECKLIST.md`.
