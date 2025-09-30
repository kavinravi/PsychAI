#!/bin/bash
# Quick launch script for PsychAI website

echo "Starting PsychAI Website..."
echo "================================"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit is not installed!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Launching on http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run streamlit
streamlit run app.py
