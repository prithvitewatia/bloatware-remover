# Test Suite for Bloatware Remover

This directory contains unit and application tests for the Bloatware Remover application.

## 📁 Test Structure

```
tests/
├── __init__.py               # Package initialization
├── conftest.py               # Shared pytest fixtures and config
├── test_cmd_manager.py       # Unit tests for CommandManager
├── test_connection_manager.py# Unit tests for ConnectionManager
├── test_pkg_manager.py       # Unit tests for PackageManager
├── test_main.py              # Tests for FastAPI application setup and endpoints
├── test-requirements.txt     # Minimal requirements to run the test-suite
└── README.md                 # This file
```

## 🧪 What’s Covered

### 1) Unit Tests
- `test_cmd_manager.py`
  - `CommandManager.execute_command`: success path, stderr handling, exception handling
- `test_connection_manager.py`
  - `ConnectionManager.connect_to_device`: success/failure paths via `subprocess.Popen` mock
- `test_pkg_manager.py`
  - `PackageManager.get_installed_packages`: parsing, empty output, whitespace handling
  - `PackageManager.perform_action_on_packages`: disable/uninstall, invalid/no action, partial failures

### 2) Application Tests
- `test_main.py`
  - FastAPI app creation and route registration
  - Docs and OpenAPI availability (`/docs`, `/openapi.json`)
  - Basic endpoint behavior, error handling, and simple performance checks

## 🚀 Running Tests

### Install test dependencies
Use the dedicated test requirements to avoid polluting your global environment:
```bash
pip install -r tests/test-requirements.txt
```

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=src --cov-report=term-missing

# HTML report (optional)
pytest --cov=src --cov-report=html
open htmlcov/index.html  # macOS
```

### Run a single file or test
```bash
# Single file
pytest tests/test_pkg_manager.py -v

# Single test
pytest tests/test_connection_manager.py::TestConnectionManager::test_connect_to_device_success -v
```

## 🔧 Pytest/Fixtures Notes

- `conftest.py` provides common fixtures (e.g., FastAPI `TestClient`, subprocess mocks, sample data).
- Tests rely on `unittest.mock.patch` to isolate ADB/subprocess interactions.
- The suite assumes imports from the `src` package (project root on `PYTHONPATH`).

## 🧪 Typical Scenarios Validated

- Connection happy-path and error paths (pairing success/failure, empty inputs)
- Package listing parsing and action application outcomes
- Command execution success, stderr presence, and exceptions
- FastAPI app wiring, docs endpoints, 404/405 handling

## 🐛 Troubleshooting

- Import errors: ensure you run `pytest` from the project root so `src` is importable.
- Missing deps: install with `pip install -r tests/test-requirements.txt`.
- Coverage empty: confirm `--cov=src` matches your source directory name.

## 🎯 Best Practices Followed

- AAA (Arrange–Act–Assert) structure
- External commands are mocked; no real ADB calls during tests
- Focus on deterministic behavior and clear failure messages

## 📚 References

- Pytest: https://docs.pytest.org/
- FastAPI Testing: https://fastapi.tiangolo.com/tutorial/testing/
- Coverage.py: https://coverage.readthedocs.io/