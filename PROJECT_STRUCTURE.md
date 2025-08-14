# Project Structure

This document describes the reorganized project structure for the Financial Literacy Agent, following best practices for scalable ML/AI projects.

## Directory Structure

```
finlit-agent/
├── src/                           # Source code (modular package structure)
│   └── finlit_agent/              # Main package
│       ├── __init__.py            # Package initialization
│       ├── agent/                 # Core agent logic
│       │   ├── __init__.py        # Agent module exports
│       │   └── core.py            # FinancialAgent class
│       ├── config/                # Configuration management
│       │   ├── __init__.py        # Config module exports
│       │   └── settings.py        # Configuration and model definitions
│       ├── tools/                 # Custom agent tools (future expansion)
│       │   └── __init__.py        # Tools module placeholder
│       └── utils/                 # Utility functions
│           ├── __init__.py        # Utils module exports
│           └── ollama.py          # Ollama connection utilities
├── scripts/                       # CLI utilities and setup scripts
│   ├── models.py                  # Model management CLI
│   ├── quickstart.py              # Interactive setup script
│   ├── setup.py                   # Dependency setup script
│   └── run_agent.sh               # Shell launcher script
├── tests/                         # Test suite
│   ├── __init__.py                # Test package initialization
│   ├── test_setup.py              # Setup validation tests
│   ├── test_agent.py              # Agent functionality tests
│   └── test_config.py             # Configuration tests
├── examples/                      # Usage examples
│   └── examples.py                # Example conversations
├── docs/                          # Documentation
│   └── CHANGES.md                 # Change history
├── main.py                        # Main entry point (imports from src/)
├── pyproject.toml                 # Project configuration and dependencies
├── README.md                      # Project documentation
└── PROJECT_STRUCTURE.md           # This file
```

## Key Design Principles

### 1. **Separation of Concerns**
- **`src/finlit_agent/`**: Core business logic, well-organized and importable
- **`scripts/`**: CLI utilities and setup tools
- **`tests/`**: Comprehensive testing suite
- **`examples/`**: Usage demonstrations
- **`docs/`**: Documentation and guides

### 2. **Modular Architecture**
- **`agent/`**: Core agent implementation (scalable for multiple agent types)
- **`config/`**: Centralized configuration management
- **`tools/`**: Custom tools (ready for financial calculators, data connectors, etc.)
- **`utils/`**: Shared utilities (Ollama, logging, helpers)

### 3. **Scalability for ML/AI Projects**
- Package structure supports easy imports: `from finlit_agent.agent.core import FinancialAgent`
- Tools module ready for custom financial tools and integrations
- Configuration system supports multiple models and environments
- Test structure supports unit, integration, and end-to-end testing

### 4. **Developer Experience**
- Clear entry points: `main.py` for direct usage
- CLI utilities: `scripts/models.py`, `scripts/quickstart.py`
- Comprehensive testing: `python3 tests/test_*.py`
- Easy package installation: `pip install -e .`

## Usage Patterns

### Direct Import (for development)
```python
from src.finlit_agent.agent.core import FinancialAgent
from src.finlit_agent.config.settings import get_config

agent = FinancialAgent()
config = get_config()
```

### Package Import (after installation)
```python
from finlit_agent import FinancialAgent, get_config

agent = FinancialAgent()
config = get_config()
```

### CLI Usage
```bash
# Main agent
python3 main.py

# Model management
python3 scripts/models.py list
python3 scripts/models.py info gemma3:7b

# Setup assistance
python3 scripts/quickstart.py

# Testing
python3 tests/test_config.py
python3 tests/test_agent.py
```

## Future Expansion Ready

This structure supports future enhancements:

### 1. **Custom Financial Tools** (`src/finlit_agent/tools/`)
```python
# Future: src/finlit_agent/tools/calculators.py
class MortgageCalculator:
    def calculate_monthly_payment(self, principal, rate, term):
        # Implementation
        pass

# Future: src/finlit_agent/tools/data_connectors.py
class StockDataConnector:
    def get_stock_price(self, symbol):
        # Implementation
        pass
```

### 2. **Multiple Agent Types** (`src/finlit_agent/agent/`)
```python
# Future: src/finlit_agent/agent/specialized.py
class GreekTaxAgent(FinancialAgent):
    # Specialized for Greek tax system
    pass

class InvestmentAgent(FinancialAgent):
    # Specialized for investment advice
    pass
```

### 3. **Data Management** (`src/finlit_agent/data/`)
```python
# Future data handling modules
- processors.py    # Data processing utilities
- validators.py    # Data validation
- connectors.py    # External data connections
```

### 4. **Web Interface** (`src/finlit_agent/web/`)
```python
# Future web interface components
- app.py          # FastAPI/Flask application
- routes.py       # API endpoints
- templates/      # Web templates
```

## Benefits of This Structure

1. **Maintainability**: Clear module boundaries and responsibilities
2. **Testability**: Easy to write unit tests for individual components
3. **Reusability**: Components can be imported and used independently
4. **Extensibility**: Easy to add new tools, agents, or features
5. **Professional**: Follows Python packaging and ML project best practices
6. **CI/CD Ready**: Structure supports automated testing and deployment

## Migration Notes

- All original functionality preserved
- Import paths updated to use new modular structure
- Backward compatibility maintained through main.py entry point
- No breaking changes to user-facing functionality
- Enhanced with better error handling and modularity
