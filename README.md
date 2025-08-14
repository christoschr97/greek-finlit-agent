# Financial Literacy Agent 💰

A conversational AI agent designed to help with financial literacy, budgeting, and financial planning. Built with [smolagents](https://github.com/huggingface/smolagents) from Hugging Face and powered by Ollama LLM models.

## Features

- **Configurable LLM Models**: Support for various Ollama models (gemma3:12b default)
- **Financial Expertise**: Specialized knowledge about personal finance, budgeting, and planning
- **Interactive Chat**: Real-time conversational interface
- **Financial Calculations**: Built-in Python interpreter for complex financial calculations
- **Web Search**: Access to current financial information via DuckDuckGo
- **Local Processing**: Runs entirely on your local machine using Ollama

## Prerequisites

1. **Python 3.12+**
2. **Ollama** - For running LLM models locally
3. **Git** - For cloning the repository

## Installation

### 1. Install Ollama

First, install Ollama on your system:

```bash
# On Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# On Windows, download from https://ollama.ai/
```

### 2. Pull a Compatible Model

```bash
# Default model (recommended)
ollama pull gemma3:12b

# Alternative smaller model for lower-resource systems
ollama pull gemma3:7b
```

### 3. Clone and Setup the Project

```bash
git clone https://github.com/christoschr97/greek-finlit-agent.git
cd greek-finlit-agent
```

### 4. Install Dependencies

Using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

## Quick Start

### Option 1: Interactive Setup (Recommended for first-time users)

```bash
python3 quickstart.py
```

This will guide you through the setup process, check your system, and help you select the best model.

### Option 2: Manual Setup

```bash
# Install a model
ollama pull gemma3:12b

# Start the agent
python3 main.py
```

## Usage

### Start the Agent

```bash
python3 main.py
```

This will start an interactive chat session where you can ask questions about:

- 💰 **Budgeting** and money management
- 🏦 **Savings and Investments**
- 📊 **Taxes and Insurance**
- 🏠 **Retirement Planning**
- 💳 **Loans and Credit**

### Example Conversation

```
💰 Hello! I'm your digital financial literacy advisor.

You: How can I create a budget for my household?

Agent: Creating an effective budget involves several key steps...
```

## Configuration

You can customize the agent behavior using environment variables:

```bash
# Ollama server URL (default: http://localhost:11434)
export OLLAMA_BASE_URL="http://localhost:11434"

# Model name (default: gemma3:12b)
export OLLAMA_MODEL="gemma3:12b"

# Alternative models you can try:
# export OLLAMA_MODEL="gemma3:7b"     # Smaller, faster model
# export OLLAMA_MODEL="llama3.2:8b"  # Alternative model

# Logging level (default: INFO)
export LOG_LEVEL="DEBUG"
```

## Project Structure

```
finlit-agent/
├── src/                           # Source code (modular package)
│   └── finlit_agent/              # Main package
│       ├── agent/                 # Core agent logic
│       │   ├── core.py            # FinancialAgent class
│       │   └── __init__.py
│       ├── config/                # Configuration management
│       │   ├── settings.py        # Model configs and settings
│       │   └── __init__.py
│       ├── tools/                 # Custom tools (future expansion)
│       │   └── __init__.py
│       └── utils/                 # Utility functions
│           ├── ollama.py          # Ollama connection utilities
│           └── __init__.py
├── scripts/                       # CLI utilities and setup
│   ├── models.py                  # Model management CLI
│   ├── quickstart.py              # Interactive setup script
│   ├── setup.py                   # Dependency setup
│   └── run_agent.sh               # Shell launcher
├── tests/                         # Test suite
│   ├── test_agent.py              # Agent tests
│   ├── test_config.py             # Configuration tests
│   └── test_setup.py              # Setup validation
├── examples/                      # Usage examples
│   └── examples.py                # Example conversations
├── docs/                          # Documentation
│   └── CHANGES.md                 # Change history
├── main.py                        # Main entry point
├── pyproject.toml                 # Project metadata and deps
├── PROJECT_STRUCTURE.md           # Architecture documentation
└── README.md                      # This file
```

For detailed architecture information, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

## Development

### Adding New Tools

To extend the agent with new capabilities, you can add tools to the `_setup_agent` method in `main.py`:

```python
from smolagents import YourCustomTool

tools = [
    DuckDuckGoSearchTool(),
    PythonInterpreterTool(),
    YourCustomTool(),  # Add your custom tool here
]
```

### Customizing the System Prompt

The agent's behavior is controlled by the system prompt in the `_setup_agent` method. Modify it to adjust the agent's personality and expertise.

### Model Management

List available models:
```bash
python3 models.py list
```

Get information about a specific model:
```bash
python3 models.py info gemma3:7b
```

### Testing

Run the test script to verify your installation:

```bash
python3 test_setup.py
```

Run example conversations:
```bash
python3 examples.py
```

## Troubleshooting

### Ollama Connection Issues

If you get connection errors:

1. Ensure Ollama is running: `ollama serve`
2. Check if the model is available: `ollama list`
3. Verify the server is accessible: `curl http://localhost:11434/api/tags`

### Model Not Found

If the model isn't found:

```bash
ollama pull gemma3:12b
```

### Memory Issues

The gemma3:12b model requires significant RAM. If you encounter memory issues:

1. Try the smaller 7B model: `ollama pull gemma3:7b`
2. Update the model in your environment: `export OLLAMA_MODEL="gemma3:7b"`

### Installation Issues

If dependencies fail to install:

1. Ensure Python 3.12+ is installed
2. Try updating pip: `pip install --upgrade pip`
3. Use virtual environment: `python -m venv venv && source venv/bin/activate`

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test your changes: `python test_setup.py`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Hugging Face](https://huggingface.co/) for the smolagents framework
- [Ollama](https://ollama.ai/) for local LLM inference
- [Google](https://deepmind.google/technologies/gemma/) for the Gemma model family

## Model Recommendations

- **gemma3:12b** (Default): Best quality responses, requires 16GB+ RAM
- **gemma3:7b**: Good balance of quality and performance, requires 8GB+ RAM
- **llama3.2:8b**: Alternative model with different strengths

Choose the model that best fits your hardware capabilities and use case.