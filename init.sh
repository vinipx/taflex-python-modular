#!/bin/bash

# Exit on error
set -e

echo "============================================"
echo "  taflex-py - Framework Initializer"
echo "============================================"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists."
fi

# Upgrade pip and install dependencies
echo "Installing/Updating dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[all]"

# Install Playwright browsers (since web is part of [all])
if command -v playwright &> /dev/null; then
    echo "Installing Playwright browsers..."
    playwright install --with-deps
else
    echo "⚠️ Playwright not found in PATH, skipping browser installation."
fi

echo ""
echo "✅ Setup complete!"
echo "To start working, activate the environment with:"
echo "   source .venv/bin/activate"
echo "============================================"
