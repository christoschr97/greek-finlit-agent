# Tests

Simple unit tests for the Greek Financial Literacy Agent UI components.

## Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── README.md               # This file
└── ui/
    ├── __init__.py
    ├── test_config.py       # Config tests
    ├── test_session_state.py # Session state tests
    ├── test_assessment_ui.py # Assessment UI tests
    └── test_chat_ui.py      # Chat UI tests
```

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run with verbose output
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/ui/test_config.py
```

### Run specific test
```bash
pytest tests/ui/test_config.py::test_page_config_exists
```

### Run with coverage
```bash
pytest tests/ --cov=src/finlit_agent/ui --cov-report=term-missing
```

## Test Coverage

- **test_config.py**: Configuration constants validation
- **test_session_state.py**: Session state initialization and helpers
- **test_assessment_ui.py**: Assessment rendering and interactions
- **test_chat_ui.py**: Chat interface and message handling

## Dependencies

Tests require:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting (optional)

Install with:
```bash
pip install pytest pytest-cov
```

## Writing New Tests

Keep tests simple:
1. One assertion per test (when possible)
2. Use descriptive test names
3. Mock Streamlit components
4. Test one thing at a time

Example:
```python
@patch('module.st')
def test_something_simple(mock_st):
    """Test that something works."""
    mock_st.session_state = {'key': 'value'}
    
    result = my_function()
    
    assert result == expected_value
```
