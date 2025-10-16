#!/bin/bash

# Run the AI Financial Portfolio Manager Agent

echo "🤖 Starting AI Financial Portfolio Manager Agent..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup.sh first:"
    echo "  ./setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create .env and add your GEMINI_API_KEY"
    echo "You can copy from .env.example:"
    echo "  cp .env.example .env"
    echo ""
fi

# Run the agent
python main.py "$@"
