# UI Module

This module contains all Streamlit UI components for the Greek Financial Literacy Agent.

## Structure

```
ui/
├── __init__.py           # Public API exports
├── config.py            # Configuration constants (UI strings, session keys)
├── session_state.py     # Session state management with helpers
├── assessment_ui.py     # Assessment phase UI (type-safe)
└── chat_ui.py          # Chat interface UI (with error handling)
```

## Components

### `config.py`
- **Page configuration**: Title, icon, layout settings
- **UI strings**: All text displayed to users (i18n-ready)
- **Session keys**: Constants for session state (prevents typos)
- **Benefits**: Single source of truth, easy translations, no magic strings

### `session_state.py`
- **Initialization**: Sets up all session state variables
- **Helper functions**: `get_state()` and `set_state()` for consistent access
- **Type hints**: Full type annotations for safety
- **Benefits**: Testable, mockable, maintainable

### `assessment_ui.py`
- **Question rendering**: Dynamic question display with progress
- **Results display**: Shows score, level, and detailed feedback
- **Chat initialization**: Sets up agent with assessment context
- **Type-safe**: All functions have proper type hints
- **Benefits**: No magic numbers, clear function responsibilities

### `chat_ui.py`
- **Message display**: Shows chat history (user and assistant)
- **Input handling**: Processes user input and generates responses
- **Error handling**: Gracefully handles failures, maintains history integrity
- **Separation of concerns**: Clean function breakdown
- **Benefits**: Robust error recovery, clear code flow

## Adding New Features

When adding new UI features:

1. **Create a new module** for substantial features (e.g., `settings_ui.py`)
2. **Add small utilities** to existing modules if they fit thematically
3. **Export public functions** from `__init__.py`
4. **Update config.py** for any new configuration constants
5. **Keep components focused** - each module should have a single responsibility

## Example: Adding a Settings Panel

```python
# ui/settings_ui.py
import streamlit as st

def render_settings():
    """Render the settings panel."""
    st.sidebar.header("Settings")
    # ... settings implementation

# ui/__init__.py
from .settings_ui import render_settings
__all__ = [..., 'render_settings']

# app.py
from finlit_agent.ui import render_settings
render_settings()
```
