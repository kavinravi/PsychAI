# Production Deployment Checklist for PsychAI

This comprehensive checklist covers everything you need to deploy PsychAI to production.

---

## Phase 1: Database Setup (REQUIRED)

### Step 1.1: Create Supabase Account
- [ ] Go to [https://supabase.com](https://supabase.com)
- [ ] Sign up for a free account
- [ ] Create a new project
- [ ] Choose a secure database password
- [ ] Wait for project to finish provisioning (~2 minutes)

### Step 1.2: Set Up Database Schema
- [ ] In Supabase dashboard, go to SQL Editor
- [ ] Open the file `website/database_schema.sql`
- [ ] Copy all contents
- [ ] Paste into Supabase SQL Editor
- [ ] Click "Run" to execute the schema
- [ ] Verify tables were created: Go to Table Editor and check for:
  - `users`
  - `chat_messages`
  - `user_activity`

### Step 1.3: Get Database Credentials
- [ ] In Supabase: Settings > API
- [ ] Copy your **Project URL** (looks like: `https://xxxxx.supabase.co`)
- [ ] Copy your **anon/public key** (for Streamlit Cloud)
  - OR copy **service_role key** (for local dev, more permissive)
- [ ] Save these securely - you'll need them for configuration

### Step 1.4: Configure Row Level Security (Optional but Recommended)
- [ ] Review RLS policies created by the schema
- [ ] Test that users can only access their own data
- [ ] Adjust policies if needed for your use case

---

## Phase 2: Local Testing with Database

### Step 2.1: Install Dependencies
```bash
cd /Users/kavinravi/Downloads/Cursor/PsychAI
pip install -r requirements.txt --upgrade
```

### Step 2.2: Configure Secrets
```bash
cd website
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:
```toml
[supabase]
url = "YOUR_SUPABASE_URL_HERE"
key = "YOUR_SUPABASE_KEY_HERE"

[google_oauth]
client_id = "your-google-client-id"  # Optional
client_secret = "your-client-secret"  # Optional
redirect_uri = "http://localhost:8501"

[environment]
session_timeout_hours = 24
enable_google_auth = false
```

### Step 2.3: Test Locally
```bash
cd website
streamlit run app.py
```

- [ ] Create a test account
- [ ] Sign in
- [ ] Send chat messages
- [ ] Verify data appears in Supabase dashboard
- [ ] Test logout and re-login
- [ ] Verify chat history persists
- [ ] Test clear chat
- [ ] Create second account to test isolation

---

## Phase 3: Google OAuth Setup (Optional)

### Step 3.1: Create Google Cloud Project
- [ ] Go to [https://console.cloud.google.com/](https://console.cloud.google.com/)
- [ ] Create new project or select existing
- [ ] Enable Google+ API (APIs & Services > Library)

### Step 3.2: Configure OAuth Consent Screen
- [ ] Go to: APIs & Services > OAuth consent screen
- [ ] User Type: External
- [ ] App name: "PsychAI"
- [ ] User support email: your email
- [ ] Developer contact: your email
- [ ] Scopes: email, profile, openid (default)
- [ ] Test users: Add your email(s)
- [ ] Submit for verification (optional, for production)

### Step 3.3: Create OAuth Credentials
- [ ] Go to: APIs & Services > Credentials
- [ ] Create Credentials > OAuth 2.0 Client ID
- [ ] Application type: Web application
- [ ] Name: "PsychAI Web App"
- [ ] Authorized JavaScript origins: 
  - `http://localhost:8501` (local)
  - `https://your-app.streamlit.app` (production - add after deployment)
- [ ] Authorized redirect URIs:
  - `http://localhost:8501`
  - `https://your-app.streamlit.app` (production)
- [ ] Save Client ID and Client Secret

### Step 3.4: Add to Secrets
- [ ] Update `.streamlit/secrets.toml` with OAuth credentials
- [ ] Set `enable_google_auth = true`
- [ ] Test Google Sign-In locally

---

## Phase 4: Prepare for Deployment

### Step 4.1: Code Review
- [ ] Review all code for hardcoded secrets (there should be none)
- [ ] Check `.gitignore` includes:
  - `.streamlit/secrets.toml`
  - `website/data/`
  - `__pycache__/`
- [ ] Remove any test/debug code
- [ ] Verify error handling is production-ready

### Step 4.2: Security Hardening
- [ ] Ensure all database queries use parameterized queries
- [ ] Verify RLS policies are active in Supabase
- [ ] Test that users cannot access other users' data
- [ ] Review password hashing (currently PBKDF2 with 100k iterations - good!)
- [ ] Consider rate limiting for auth attempts
- [ ] Review session timeout settings

### Step 4.3: Create Production README
- [ ] Document deployment process
- [ ] List all environment variables needed
- [ ] Include troubleshooting section
- [ ] Add contact information for support

---

## Phase 5: Streamlit Community Cloud Deployment

### Step 5.1: Prepare Repository
- [ ] Ensure all changes are committed
- [ ] Push to GitHub (private or public repo)
- [ ] Verify `requirements.txt` is in project root
- [ ] Ensure `website/app.py` is the entry point

### Step 5.2: Deploy to Streamlit Cloud
- [ ] Go to [https://share.streamlit.io](https://share.streamlit.io)
- [ ] Sign in with GitHub
- [ ] Click "New app"
- [ ] Select your repository
- [ ] Set main file path: `website/app.py`
- [ ] Click "Advanced settings"

### Step 5.3: Configure Secrets in Streamlit Cloud
In the Secrets section, paste your secrets in TOML format:

```toml
[supabase]
url = "YOUR_SUPABASE_URL"
key = "YOUR_SUPABASE_KEY"

[google_oauth]
client_id = "YOUR_GOOGLE_CLIENT_ID"
client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
redirect_uri = "https://your-actual-app-url.streamlit.app"

[environment]
session_timeout_hours = 24
enable_google_auth = true
```

- [ ] Save secrets
- [ ] Click "Deploy"
- [ ] Wait for deployment (2-5 minutes)

### Step 5.4: Post-Deployment Configuration
- [ ] Note your app URL (e.g., `https://yourapp.streamlit.app`)
- [ ] Update Google OAuth redirect URI with production URL
- [ ] Test full authentication flow
- [ ] Test chat functionality
- [ ] Verify database persistence

---

## Phase 6: Alternative Deployment Options

### Option A: Docker Deployment

#### Step 6A.1: Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY website/ ./website/

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run app
WORKDIR /app/website
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Step 6A.2: Build and Test
```bash
docker build -t psychai .
docker run -p 8501:8501 --env-file .env psychai
```

- [ ] Create `.env` file with secrets
- [ ] Test container locally
- [ ] Push to Docker Hub or container registry

### Option B: Cloud Platform Deployment (AWS/GCP/Azure)

#### For AWS Elastic Beanstalk:
- [ ] Create `requirements.txt` in root
- [ ] Create `.ebextensions/` directory
- [ ] Configure environment variables in EB console
- [ ] Deploy using EB CLI

#### For Google Cloud Run:
- [ ] Build container
- [ ] Push to Google Container Registry
- [ ] Deploy to Cloud Run
- [ ] Configure secrets in Cloud Run
- [ ] Set up custom domain (optional)

#### For Azure Web Apps:
- [ ] Create Web App resource
- [ ] Configure Python runtime
- [ ] Set application settings (secrets)
- [ ] Deploy via GitHub Actions or Azure CLI

### Option C: VPS Deployment (DigitalOcean, Linode, etc.)

- [ ] Set up Ubuntu 22.04 server
- [ ] Install Python, nginx, and dependencies
- [ ] Clone repository
- [ ] Set up systemd service for Streamlit
- [ ] Configure nginx as reverse proxy with SSL
- [ ] Set up SSL certificate (Let's Encrypt)
- [ ] Configure firewall

---

## Phase 7: Model Integration (When Ready)

### Step 7.1: Prepare Model
- [ ] Train your model using `data_and_model_training.ipynb`
- [ ] Save LoRA adapters
- [ ] Test model locally
- [ ] Measure model size and memory requirements

### Step 7.2: Choose Hosting Strategy

**Option 1: Include in App (Small Models)**
- [ ] Add model files to repository (if < 100MB)
- [ ] Update `chat_handler.py` to load model
- [ ] Test locally
- [ ] Deploy to cloud with GPU instance

**Option 2: Separate Model API (Recommended for Large Models)**
- [ ] Set up separate server with GPU
- [ ] Deploy model as API (FastAPI, TensorFlow Serving, etc.)
- [ ] Update `chat_handler.py` to call API
- [ ] Add API endpoint to secrets
- [ ] Test end-to-end

**Option 3: Use Hugging Face Inference API**
- [ ] Upload model to Hugging Face Hub
- [ ] Get API token
- [ ] Update code to use HF Inference API
- [ ] Test with rate limits

### Step 7.3: Update Chat Handler
Edit `website/utils/chat_handler.py`:

```python
def get_llm_response(user_message: str, conversation_history: List[Dict]) -> str:
    # Replace placeholder with actual model inference
    # See comments in file for implementation examples
    pass
```

- [ ] Implement actual model loading
- [ ] Add error handling for model failures
- [ ] Implement caching for better performance
- [ ] Add timeout handling
- [ ] Test with various inputs

---

## Phase 8: Production Monitoring & Maintenance

### Step 8.1: Set Up Monitoring
- [ ] Enable Streamlit Cloud analytics (if using Streamlit Cloud)
- [ ] Set up Supabase monitoring and alerts
- [ ] Monitor database growth and plan for scaling
- [ ] Track error rates in application logs
- [ ] Set up uptime monitoring (UptimeRobot, Pingdom, etc.)

### Step 8.2: Analytics (Optional)
- [ ] Integrate Google Analytics or similar
- [ ] Set up custom event tracking
- [ ] Monitor user engagement metrics
- [ ] Track model performance (response quality)

### Step 8.3: Logging
- [ ] Review application logs regularly
- [ ] Set up log aggregation (if using cloud platform)
- [ ] Monitor for security events
- [ ] Track API usage and costs

### Step 8.4: Backup Strategy
- [ ] Enable Supabase automated backups (Pro plan)
- [ ] Set up regular database exports
- [ ] Test restore procedures
- [ ] Document backup locations

### Step 8.5: Scaling Considerations
- [ ] Monitor Supabase database size (free tier: 500MB)
- [ ] Plan for paid tier if needed
- [ ] Consider caching strategies for frequent queries
- [ ] Monitor app performance and response times
- [ ] Plan for CDN if serving static assets

---

## Phase 9: Legal & Compliance

### Step 9.1: Terms of Service
- [ ] Draft comprehensive Terms of Service
- [ ] Include liability disclaimers
- [ ] Specify not a replacement for professional care
- [ ] Define acceptable use policy
- [ ] Add to website footer

### Step 9.2: Privacy Policy
- [ ] Draft Privacy Policy (REQUIRED if collecting user data)
- [ ] Specify what data is collected
- [ ] Explain how data is used
- [ ] Detail data retention policy
- [ ] Provide data deletion process
- [ ] Address GDPR/CCPA compliance if applicable
- [ ] Add to website footer

### Step 9.3: HIPAA Compliance (If Applicable)
**Note: Mental health data may be considered PHI**
- [ ] Consult with legal counsel
- [ ] Ensure Supabase BAA (Business Associate Agreement)
- [ ] Implement audit logging
- [ ] Add encryption at rest and in transit
- [ ] Create incident response plan
- [ ] Train team on HIPAA requirements

### Step 9.4: Crisis Management
- [ ] Add prominent crisis hotline information
- [ ] Implement keyword detection for crisis situations
- [ ] Create escalation procedures
- [ ] Consider integration with crisis text lines
- [ ] Test crisis response flows

### Step 9.5: Age Restrictions
- [ ] Determine minimum age (typically 13+ with parental consent)
- [ ] Add age verification to signup
- [ ] Include in Terms of Service
- [ ] Consider parental consent mechanisms

---

## Phase 10: Performance Optimization

### Step 10.1: Database Optimization
- [ ] Review and optimize slow queries
- [ ] Add additional indexes if needed
- [ ] Implement connection pooling
- [ ] Enable query caching
- [ ] Monitor database performance metrics

### Step 10.2: Application Performance
- [ ] Enable Streamlit caching where appropriate
- [ ] Optimize image sizes and assets
- [ ] Minimize database calls per page load
- [ ] Profile application for bottlenecks
- [ ] Consider lazy loading for chat history

### Step 10.3: Model Performance
- [ ] Optimize model inference time
- [ ] Implement request queuing for high load
- [ ] Consider model quantization (int8, int4)
- [ ] Cache common responses
- [ ] Monitor GPU/CPU usage

---

## Phase 11: Testing & Quality Assurance

### Step 11.1: Functional Testing
- [ ] Test all user flows end-to-end
- [ ] Test authentication (signup, login, logout)
- [ ] Test chat functionality
- [ ] Test data persistence
- [ ] Test error states
- [ ] Test on multiple browsers
- [ ] Test on mobile devices

### Step 11.2: Security Testing
- [ ] Test SQL injection protection
- [ ] Test XSS (cross-site scripting) protection
- [ ] Test authentication bypass attempts
- [ ] Test authorization (users accessing others' data)
- [ ] Test rate limiting
- [ ] Review dependency vulnerabilities
- [ ] Run security scan (OWASP ZAP, etc.)

### Step 11.3: Load Testing
- [ ] Test with multiple concurrent users
- [ ] Monitor database performance under load
- [ ] Test model API under load
- [ ] Identify bottlenecks
- [ ] Plan for capacity

### Step 11.4: User Acceptance Testing
- [ ] Recruit beta testers
- [ ] Gather feedback on UI/UX
- [ ] Test with target audience (parents, teens, counselors)
- [ ] Iterate based on feedback
- [ ] Fix critical issues before launch

---

## Phase 12: Launch Preparation

### Step 12.1: Pre-Launch Checklist
- [ ] All features working as expected
- [ ] Database properly configured and tested
- [ ] Secrets properly secured
- [ ] Terms of Service and Privacy Policy published
- [ ] Crisis resources prominently displayed
- [ ] Help/FAQ section created
- [ ] Contact information available
- [ ] Error pages customized
- [ ] Analytics set up

### Step 12.2: Soft Launch
- [ ] Launch to limited audience
- [ ] Monitor closely for issues
- [ ] Gather initial feedback
- [ ] Fix any critical bugs
- [ ] Iterate on UX issues

### Step 12.3: Marketing Materials
- [ ] Create landing page
- [ ] Prepare social media posts
- [ ] Create demo video
- [ ] Write blog post/announcement
- [ ] Prepare press kit (if applicable)

### Step 12.4: Support Plan
- [ ] Set up support email
- [ ] Create FAQ documentation
- [ ] Establish response time SLA
- [ ] Train support team (if applicable)
- [ ] Create escalation procedures

---

## Phase 13: Post-Launch

### Step 13.1: First 24 Hours
- [ ] Monitor application closely
- [ ] Watch for error spikes
- [ ] Monitor user signups
- [ ] Check database performance
- [ ] Be ready for quick fixes

### Step 13.2: First Week
- [ ] Analyze user feedback
- [ ] Fix critical bugs
- [ ] Monitor usage patterns
- [ ] Adjust capacity if needed
- [ ] Send thank you to early users

### Step 13.3: First Month
- [ ] Review analytics
- [ ] Plan feature improvements
- [ ] Optimize based on usage data
- [ ] Conduct user interviews
- [ ] Plan next iteration

### Step 13.4: Ongoing
- [ ] Regular security updates
- [ ] Dependency updates
- [ ] Feature releases
- [ ] Performance monitoring
- [ ] User feedback integration
- [ ] Model retraining with new data

---

## Quick Reference: Essential Credentials

### What You MUST Have:
1. **Supabase URL and Key** (REQUIRED)
2. **Streamlit Cloud Account** (if using Streamlit Cloud)

### What You SHOULD Have:
3. **Google OAuth Credentials** (recommended for better UX)
4. **Custom Domain** (optional but professional)

### What You MIGHT Have:
5. **Model Hosting API Key** (when model is ready)
6. **Analytics API Key** (for tracking)
7. **Monitoring Service API Key** (for uptime/performance)

---

## Estimated Costs (Monthly)

### Free Tier (Good for MVP):
- Supabase Free: $0/month (500MB database, 50,000 monthly active users)
- Streamlit Cloud Free: $0/month (1 private app)
- Google OAuth: $0
- **Total: $0/month**

### Production Tier (Recommended):
- Supabase Pro: $25/month (8GB database, 100,000 MAU, daily backups)
- Streamlit Cloud: $0-$250/month (depending on resources)
- Model Hosting (GPU): $50-500/month (depending on usage)
- Monitoring: $0-50/month
- Domain: $10-20/year
- **Total: ~$100-800/month**

---

## Support & Troubleshooting

### Common Issues:

**Database Connection Fails:**
- Check Supabase credentials in secrets
- Verify project is not paused (Supabase pauses after 1 week of inactivity on free tier)
- Check network connectivity

**Streamlit Cloud Build Fails:**
- Review requirements.txt for incompatible versions
- Check build logs for specific errors
- Verify Python version compatibility

**Google OAuth Not Working:**
- Verify redirect URIs match exactly
- Check OAuth consent screen is published
- Ensure test users are added (if in testing mode)

**Chat Messages Not Saving:**
- Check database RLS policies
- Verify user email is correct
- Check Supabase logs for errors

---

## Final Notes

This is a living document. As you deploy and encounter issues, update this checklist for future reference.

**Remember:**
- Start small (MVP with core features)
- Test thoroughly before launching
- Monitor closely after launch
- Iterate based on feedback
- Prioritize user safety and privacy

**Good luck with your deployment! 🚀**
