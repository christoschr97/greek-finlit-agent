#!/bin/bash
# Financial Literacy Agent Launcher Script

echo "💰 Starting Financial Literacy Agent..."

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the project directory."
    exit 1
fi

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv not found. Please install uv or run: python3 main.py"
    exit 1
fi

# Run the agent
echo "🚀 Launching agent..."
uv run python main.py
