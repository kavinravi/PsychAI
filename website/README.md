# PsychAI Web Application

A Streamlit-based web interface for the PsychAI child psychology support assistant.

## Features

- 🔐 **User Authentication**
  - Custom email/password authentication
  - Google OAuth support (optional)
  - Secure password hashing with PBKDF2
  - Session management with timeout

- 💬 **Chat Interface**
  - Real-time conversation with fine-tuned LLM
  - Chat history saving and loading
  - Clean, intuitive UI designed for mental health support
  - Crisis resources readily available

- 🎨 **User Experience**
  - Modern, calming design
  - Mobile-responsive layout
  - Clear disclaimers and safety information
  - Easy navigation

## Project Structure

```
website/
├── app.py                      # Main application entry point
├── pages/
│   ├── 1_Authentication.py     # Login/signup page
│   └── 2_Chat.py               # Chat interface
├── utils/
│   ├── __init__.py
│   ├── auth.py                 # Authentication utilities
│   └── chat_handler.py         # Chat and LLM interaction
├── .streamlit/
│   ├── config.toml             # Streamlit configuration
│   └── secrets.toml.example    # Example secrets file
├── data/                       # Created at runtime
│   ├── users.json              # User database (custom auth)
│   └── chat_history/           # Saved chat histories
├── .gitignore
└── README.md
```

## Quick Start

### 1. Install Dependencies

From the project root directory:

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
cd website
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### 3. Create an Account

- Click "Create Account" or navigate to the Authentication page
- Fill in your details (name, email, password)
- Sign in and start chatting!

## Configuration

### Basic Configuration

The application works out of the box with custom email/password authentication. No additional setup required!

### Google OAuth (Optional)

To enable Google Sign-In:

1. **Set up Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Google+ API

2. **Create OAuth 2.0 Credentials**
   - Navigate to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client ID"
   - Application type: "Web application"
   - Authorized redirect URIs: `http://localhost:8501` (for local dev)
   - Note down your Client ID and Client Secret

3. **Configure Secrets**
   - Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
   - Fill in your Google OAuth credentials:
   
   ```toml
   [google_oauth]
   client_id = "your-actual-client-id.apps.googleusercontent.com"
   client_secret = "your-actual-client-secret"
   redirect_uri = "http://localhost:8501"
   
   [environment]
   enable_google_auth = true
   ```

4. **Set Environment Variables** (alternative to secrets.toml)
   
   ```bash
   export GOOGLE_CLIENT_ID="your-client-id"
   export GOOGLE_CLIENT_SECRET="your-client-secret"
   export GOOGLE_REDIRECT_URI="http://localhost:8501"
   ```

## Loading Your Fine-Tuned Model

The chat interface currently uses placeholder responses. To integrate your fine-tuned model:

### 1. Update `utils/chat_handler.py`

Replace the `load_model_placeholder()` function:

```python
def load_model():
    """Load the fine-tuned model"""
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import PeftModel
    import torch
    
    base_model = "Qwen/Qwen2.5-7B-Instruct"  # Or your base model
    adapter_path = "../path/to/your/lora/adapters"
    
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        device_map="auto",
        torch_dtype=torch.float16,
        load_in_8bit=True  # If using 8-bit
    )
    model = PeftModel.from_pretrained(model, adapter_path)
    
    return model, tokenizer
```

### 2. Update `get_llm_response()` function

Replace the placeholder implementation with actual inference:

```python
def get_llm_response(user_message: str, conversation_history: List[Dict]) -> str:
    """Get response from the fine-tuned LLM"""
    
    # Load model (cache this in production)
    if 'model' not in st.session_state:
        st.session_state.model, st.session_state.tokenizer = load_model()
    
    model = st.session_state.model
    tokenizer = st.session_state.tokenizer
    
    # Format conversation
    messages = conversation_history + [{"role": "user", "content": user_message}]
    
    # Use your model's chat template
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # Generate response
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )
    
    response = tokenizer.decode(outputs[0][len(inputs.input_ids[0]):], skip_special_tokens=True)
    
    return response
```

## Security Considerations

- **Passwords**: Hashed using PBKDF2-HMAC-SHA256 with random salts
- **Session Management**: 24-hour timeout (configurable)
- **Data Storage**: Local JSON files (replace with database for production)
- **HTTPS**: Recommended for production deployment
- **Environment Variables**: Never commit `.streamlit/secrets.toml` to version control

## Production Deployment

For production deployment, consider:

1. **Database**: Replace JSON file storage with PostgreSQL/MongoDB
2. **Authentication**: Use proper OAuth implementation or service like Auth0
3. **HTTPS**: Deploy behind reverse proxy (nginx) with SSL
4. **Scaling**: Use Streamlit Cloud, AWS, or containerize with Docker
5. **Monitoring**: Add logging and error tracking
6. **Rate Limiting**: Prevent abuse of the LLM endpoint
7. **Legal**: Implement proper Terms of Service and Privacy Policy

### Deployment Options

**Streamlit Cloud** (Easiest):
```bash
# Push to GitHub and connect at share.streamlit.io
```

**Docker**:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY website/ .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

**AWS/GCP/Azure**: Follow platform-specific Streamlit deployment guides

## Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Model Loading Issues
- Ensure sufficient GPU/RAM for your model
- Check CUDA installation if using GPU
- Consider using quantization (8-bit/4-bit) for large models

### Authentication Issues
- Check that `data/users.json` has proper write permissions
- Verify secrets.toml is in `.streamlit/` directory
- Clear browser cookies if session issues persist

## Support

For issues or questions about the web application, please refer to the main project README or open an issue on GitHub.

## License

Part of the PsychAI project. See main project LICENSE for details.
