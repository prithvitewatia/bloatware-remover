import asyncio
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
import pytest

from src.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application"""
    return TestClient(app)


@pytest.fixture
def mock_adb_connection():
    """Mock ADB connection for testing"""
    with patch('subprocess.Popen') as mock_popen:
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Success", "")
        mock_popen.return_value = mock_process
        yield mock_popen


@pytest.fixture
def mock_package_list():
    """Mock package list for testing"""
    return [
        "com.example.app1",
        "com.example.app2",
        "com.system.app",
        "com.google.android.apps.maps",
        "com.android.settings",
    ]


@pytest.fixture
def mock_successful_action():
    """Mock successful package action"""
    with patch('src.cmd_manager.CommandManager.execute_command') as mock_execute:
        mock_execute.return_value = "Success"
        yield mock_execute


@pytest.fixture
def mock_failed_action():
    """Mock failed package action"""
    with patch('src.cmd_manager.CommandManager.execute_command') as mock_execute:
        mock_execute.return_value = "Failure: Package not found"
        yield mock_execute


@pytest.fixture
def sample_action_form():
    """Sample action form data for testing"""
    return {
        "action_com.example.app1": "disable",
        "action_com.example.app2": "uninstall",
        "action_com.system.app": "",
        "action_com.google.android.apps.maps": "disable",
    }


@pytest.fixture
def sample_connection_data():
    """Sample connection data for testing"""
    return {"device_ip": "192.168.1.100", "device_port": "5555", "pair_code": "123456"}


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "asyncio: mark test as async")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")


# Async test configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Test data fixtures
@pytest.fixture
def test_packages_data():
    """Test data for packages"""
    return {
        "system_packages": ["com.android.settings", "com.android.systemui", "com.android.phone"],
        "user_packages": ["com.example.app1", "com.example.app2", "com.facebook.katana"],
        "bloatware_packages": [
            "com.samsung.android.bixby",
            "com.google.android.apps.maps",
            "com.google.android.youtube",
        ],
    }


@pytest.fixture
def test_connection_scenarios():
    """Test scenarios for device connections"""
    return {
        "valid_connection": {
            "ip": "192.168.1.100",
            "port": "5555",
            "code": "123456",
            "expected": True,
        },
        "invalid_ip": {
            "ip": "invalid.ip.address",
            "port": "5555",
            "code": "123456",
            "expected": False,
        },
        "invalid_port": {
            "ip": "192.168.1.100",
            "port": "99999",
            "code": "123456",
            "expected": False,
        },
        "empty_code": {"ip": "192.168.1.100", "port": "5555", "code": "", "expected": False},
    }


@pytest.fixture
def test_action_scenarios():
    """Test scenarios for package actions"""
    return {
        "disable_success": {
            "package": "com.example.app",
            "action": "disable",
            "expected_command": "adb shell pm disable-user --user 0 com.example.app",
            "expected_result": [],
        },
        "uninstall_success": {
            "package": "com.example.app",
            "action": "uninstall",
            "expected_command": "adb shell pm uninstall --user 0 com.example.app",
            "expected_result": [],
        },
        "no_action": {
            "package": "com.example.app",
            "action": "",
            "expected_command": None,
            "expected_result": [],
        },
        "invalid_action": {
            "package": "com.example.app",
            "action": "invalid",
            "expected_command": ":",
            "expected_result": [],
        },
    }


# Mock fixtures for external dependencies
@pytest.fixture
def mock_subprocess():
    """Mock subprocess for testing"""
    with patch('subprocess.Popen') as mock_popen:
        yield mock_popen


@pytest.fixture
def mock_logging():
    """Mock logging for testing"""
    with patch('logging.getLogger') as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        yield mock_logger


# Performance test fixtures
@pytest.fixture
def performance_thresholds():
    """Performance thresholds for testing"""
    return {
        "response_time_ms": 1000,  # 1 second
        "memory_usage_mb": 100,  # 100 MB
        "cpu_usage_percent": 50,  # 50%
    }


# Security test fixtures
@pytest.fixture
def security_headers():
    """Expected security headers"""
    return {
        "content-security-policy": "default-src 'self'",
        "x-content-type-options": "nosniff",
        "x-frame-options": "DENY",
        "x-xss-protection": "1; mode=block",
    }


# Error handling test fixtures
@pytest.fixture
def error_scenarios():
    """Error scenarios for testing"""
    return {
        "connection_timeout": Exception("Connection timeout"),
        "invalid_command": Exception("Invalid command"),
        "permission_denied": Exception("Permission denied"),
        "device_not_found": Exception("Device not found"),
    }
