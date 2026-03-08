#!/bin/bash

# TAFLEX PY Modular Documentation Runner
# This script serves the MkDocs documentation locally.

echo "🚀 Preparing TAFLEX PY Modular Documentation..."

# Check if mkdocs is installed
if ! command -v mkdocs &> /dev/null; then
    echo "📦 Installing MkDocs and Material theme..."
    pip install mkdocs-material mkdocs-mermaid2-plugin
fi

echo "🌐 Starting local documentation server at http://localhost:8000"
echo "💡 Press Ctrl+C to stop the server."

mkdocs serve
