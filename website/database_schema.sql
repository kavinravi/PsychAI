-- PsychAI Database Schema for Supabase (PostgreSQL)
-- Run this in your Supabase SQL Editor to create the tables

-- Enable UUID extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password_hash TEXT,  -- NULL for OAuth users
    salt TEXT,           -- NULL for OAuth users
    auth_method TEXT NOT NULL DEFAULT 'custom',  -- 'custom' or 'google'
    google_id TEXT UNIQUE,  -- For Google OAuth users
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Chat messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_email TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
    chat_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB  -- For future extensibility (attachments, ratings, etc.)
);

-- User activity log (optional, for analytics)
CREATE TABLE IF NOT EXISTS user_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_email TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
    activity_type TEXT NOT NULL,  -- 'login', 'logout', 'message_sent', 'chat_created', etc.
    metadata JSONB,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_chat_messages_user_email ON chat_messages(user_email);
CREATE INDEX IF NOT EXISTS idx_chat_messages_chat_id ON chat_messages(chat_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_timestamp ON chat_messages(timestamp);
CREATE INDEX IF NOT EXISTS idx_user_activity_user_email ON user_activity(user_email);
CREATE INDEX IF NOT EXISTS idx_user_activity_timestamp ON user_activity(timestamp);

-- Row Level Security (RLS) policies
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activity ENABLE ROW LEVEL SECURITY;

-- Users can only read their own data
CREATE POLICY "Users can view own profile"
    ON users FOR SELECT
    USING (auth.email() = email);

CREATE POLICY "Users can update own profile"
    ON users FOR UPDATE
    USING (auth.email() = email);

-- Users can only access their own chat messages
CREATE POLICY "Users can view own messages"
    ON chat_messages FOR SELECT
    USING (auth.email() = user_email);

CREATE POLICY "Users can insert own messages"
    ON chat_messages FOR INSERT
    WITH CHECK (auth.email() = user_email);

CREATE POLICY "Users can delete own messages"
    ON chat_messages FOR DELETE
    USING (auth.email() = user_email);

-- Users can only access their own activity logs
CREATE POLICY "Users can view own activity"
    ON user_activity FOR SELECT
    USING (auth.email() = user_email);

-- Service role bypass (for server-side operations)
-- These policies allow the service role key to access all data
CREATE POLICY "Service role can do anything on users"
    ON users FOR ALL
    USING (auth.role() = 'service_role');

CREATE POLICY "Service role can do anything on chat_messages"
    ON chat_messages FOR ALL
    USING (auth.role() = 'service_role');

CREATE POLICY "Service role can do anything on user_activity"
    ON user_activity FOR ALL
    USING (auth.role() = 'service_role');

-- Function to update last_login timestamp
CREATE OR REPLACE FUNCTION update_last_login()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users
    SET last_login = NOW()
    WHERE email = NEW.user_email;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update last_login on chat activity
CREATE TRIGGER update_last_login_trigger
    AFTER INSERT ON chat_messages
    FOR EACH ROW
    EXECUTE FUNCTION update_last_login();

-- Comments for documentation
COMMENT ON TABLE users IS 'Stores user account information';
COMMENT ON TABLE chat_messages IS 'Stores all chat messages between users and the AI';
COMMENT ON TABLE user_activity IS 'Logs user activity for analytics and monitoring';

COMMENT ON COLUMN users.auth_method IS 'Authentication method: custom (email/password) or google (OAuth)';
COMMENT ON COLUMN chat_messages.chat_id IS 'Groups messages into conversation sessions';
COMMENT ON COLUMN chat_messages.metadata IS 'Extensible field for future features like message ratings, attachments, etc.';

-- Optional: Create a view for chat statistics
CREATE OR REPLACE VIEW chat_statistics AS
SELECT 
    user_email,
    COUNT(DISTINCT chat_id) as total_chats,
    COUNT(*) as total_messages,
    MAX(timestamp) as last_activity
FROM chat_messages
GROUP BY user_email;

COMMENT ON VIEW chat_statistics IS 'Aggregated statistics per user for dashboard display';
