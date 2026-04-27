#!/bin/bash
# Smart Insights Hub - Installation and Setup Script
# For Linux/Mac users

set -e  # Exit on error

echo "=================================================="
echo "Smart Insights Hub - Installation Script"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

PIP_VERSION=$(pip3 --version | awk '{print $2}')
echo "✓ pip version: $PIP_VERSION"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Verify installation
echo "Verifying installation..."
python test_setup.py
echo ""

echo "=================================================="
echo "✅ Installation Complete!"
echo "=================================================="
echo ""
echo "To run the project:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Run pipeline:        python main.py"
echo "  3. Run dashboard:       streamlit run app.py"
echo ""
echo "For more information, see README.md or QUICKSTART.md"
