#!/bin/bash

# TAFLEX PY Modular Documentation Runner
# This script serves the Docusaurus documentation locally.

DOCS_DIR="docs"

if [ ! -d "$DOCS_DIR" ]; then
    echo "❌ Error: Documentation directory '$DOCS_DIR' not found."
    exit 1
fi

echo "🚀 Preparing TAFLEX PY Modular Documentation..."

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing documentation dependencies..."
    npm install
fi

echo "🌐 Starting local documentation server at http://localhost:3000"
echo "💡 Press Ctrl+C to stop the server."

npm start
