#!/bin/bash

# AI Financial Portfolio Manager - Installation Script

echo "================================================"
echo "AI Financial Portfolio Manager - Setup Script"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Error: Python 3.8 or higher is required"
    exit 1
fi
echo "✅ Python version OK"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env from example
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your GEMINI_API_KEY"
    echo ""
else
    echo "ℹ️  .env file already exists"
    echo ""
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p logs
mkdir -p output/recommendations
mkdir -p output/history
echo "✅ Directories created"
echo ""

# Display next steps
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your Gemini API key:"
echo "   nano .env"
echo ""
echo "2. Edit portfolio.json to add your stocks:"
echo "   nano portfolio.json"
echo ""
echo "3. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "4. Run the agent:"
echo "   python main.py"
echo ""
echo "For help:"
echo "   python main.py --help"
echo ""
echo "================================================"
