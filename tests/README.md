# Test Suite for Bloatware Remover

This directory contains comprehensive tests for the Bloatware Remover application, covering unit tests, integration tests, and HTTP endpoint tests.

## 📁 Test Structure

```
tests/
├── __init__.py                 # Package initialization
├── conftest.py                 # Pytest configuration and fixtures
├── test_bloatware_removal.py   # Unit tests for core functionality
├── test_main.py                # Tests for main application
├── test_integration.py         # End-to-end workflow tests
├── test_main.http              # HTTP endpoint tests
├── README.md                   # This file
└── pytest.ini                 # Pytest configuration
```

## 🧪 Test Categories

### 1. Unit Tests (`test_bloatware_removal.py`)
- **ConnectionManager**: Tests for device connection functionality
- **PackageManager**: Tests for package operations (list, disable, uninstall)
- **CommandManager**: Tests for command execution and error handling

### 2. Integration Tests (`test_routes.py`)
- **API Endpoints**: Tests for all FastAPI routes
- **Template Rendering**: Tests for HTML template rendering
- **Form Handling**: Tests for form validation and processing
- **Error Handling**: Tests for exception handling

### 3. Application Tests (`test_main.py`)
- **Application Configuration**: Tests for FastAPI app setup
- **Middleware**: Tests for application middleware
- **Security**: Tests for security headers and configurations
- **Performance**: Tests for response times and performance

### 4. End-to-End Tests (`test_integration.py`)
- **Complete Workflow**: Tests for the entire user journey
- **User Interface**: Tests for UI components and navigation
- **Template Integration**: Tests for Bootstrap integration
- **Security Integration**: Tests for security features

### 5. HTTP Tests (`test_main.http`)
- **Endpoint Testing**: Manual HTTP endpoint testing
- **Request/Response**: Tests for different HTTP methods and data

## 🚀 Running Tests

### Prerequisites
```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

### Run All Tests
```bash
# Run all tests with coverage
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html
```

### Run Specific Test Categories
```bash
# Run only unit tests
pytest tests/test_bloatware_removal.py

# Run only integration tests
pytest tests/test_integration.py

# Run only route tests
pytest tests/test_routes.py

# Run tests with specific markers
pytest -m "unit"
pytest -m "integration"
pytest -m "asyncio"
```

### Run HTTP Tests
```bash
# Using VS Code REST Client or similar tool
# Open test_main.http and run individual requests
```

## 📊 Test Coverage

The test suite aims for **80%+ code coverage** and includes:

- **Core Business Logic**: 100% coverage of bloatware removal functionality
- **API Endpoints**: 100% coverage of all routes
- **Error Handling**: Comprehensive error scenario testing
- **Template Rendering**: Full template integration testing
- **Security**: Basic security testing and validation

### Coverage Report
```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# View coverage in browser
open htmlcov/index.html
```

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)
- **Test Discovery**: Automatically finds test files
- **Coverage**: Generates coverage reports
- **Markers**: Custom markers for test categorization
- **Warnings**: Filters out deprecation warnings

### Fixtures (`conftest.py`)
- **Client Fixture**: FastAPI test client
- **Mock Fixtures**: Mocked external dependencies
- **Data Fixtures**: Test data for various scenarios
- **Async Support**: Async test configuration

## 🎯 Test Scenarios

### Connection Testing
- ✅ Successful device connection
- ❌ Failed device connection
- ⚠️ Invalid connection parameters
- 🔄 Connection timeout handling

### Package Management Testing
- 📦 Package listing functionality
- 🚫 Package disable operations
- 🗑️ Package uninstall operations
- ⚠️ Protected package handling

### User Interface Testing
- 🎨 Template rendering
- 📱 Responsive design
- 🔗 Navigation flow
- 📝 Form validation

### Error Handling Testing
- 🚨 Exception handling
- 🔄 Graceful degradation
- 📋 Error message display
- 🛡️ Security error handling

## 🛠️ Mocking Strategy

### External Dependencies
- **ADB Commands**: Mocked subprocess calls
- **Device Communication**: Mocked connection responses
- **File System**: Mocked file operations
- **Network Calls**: Mocked HTTP requests

### Test Data
- **Sample Packages**: Realistic package names
- **Connection Data**: Valid/invalid connection parameters
- **Action Forms**: Various action combinations
- **Error Scenarios**: Different error conditions

## 📈 Performance Testing

### Response Time Tests
- Root endpoint: < 1 second
- Package listing: < 2 seconds
- Action application: < 3 seconds

### Load Testing
- Multiple concurrent requests
- Memory usage monitoring
- CPU usage validation

## 🔒 Security Testing

### Input Validation
- XSS prevention
- SQL injection prevention
- Command injection prevention

### Security Headers
- Content Security Policy
- X-Frame-Options
- X-Content-Type-Options

## 🐛 Debugging Tests

### Common Issues
1. **Import Errors**: Ensure `src` is in Python path
2. **Async Issues**: Use `pytest-asyncio` for async tests
3. **Mock Issues**: Check mock setup and assertions
4. **Template Issues**: Verify template paths and context

### Debug Commands
```bash
# Run with debug output
pytest -s -v

# Run single test with debug
pytest tests/test_bloatware_removal.py::TestConnectionManager::test_connect_to_device_success -s

# Run with print statements
pytest -s --capture=no
```

## 📝 Adding New Tests

### Unit Test Template
```python
@pytest.mark.asyncio
async def test_new_functionality():
    """Test description"""
    # Arrange
    # Act
    # Assert
```

### Integration Test Template
```python
def test_new_endpoint(client):
    """Test new endpoint"""
    response = client.get("/new-endpoint")
    assert response.status_code == 200
```

### Fixture Template
```python
@pytest.fixture
def new_test_data():
    """New test data fixture"""
    return {
        "key": "value"
    }
```

## 🎯 Best Practices

1. **Test Naming**: Use descriptive test names
2. **Arrange-Act-Assert**: Follow AAA pattern
3. **Mock External Dependencies**: Don't test external systems
4. **Test Edge Cases**: Include error scenarios
5. **Maintain Coverage**: Keep coverage above 80%
6. **Fast Tests**: Keep tests fast and focused
7. **Isolated Tests**: Tests should be independent

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/) 