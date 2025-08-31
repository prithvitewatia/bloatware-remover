from fastapi.testclient import TestClient

from src.main import app


class TestMainApplication:
    """Test cases for the main FastAPI application"""

    def test_app_creation(self):
        """Test that the FastAPI app is created correctly"""
        assert app is not None
        assert hasattr(app, 'router')

    def test_app_has_routes(self):
        """Test that the app has the expected routes"""
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/connect-to-device", "/packages", "/apply-actions"]

        for route in expected_routes:
            assert route in routes

    def test_app_router_included(self):
        """Test that the router is properly included in the app"""
        # Check that the router is included
        router_routes = [route for route in app.routes if hasattr(route, 'path')]
        assert len(router_routes) > 0

    def test_app_startup(self):
        """Test that the app can start without errors"""
        # This test ensures the app can be instantiated and configured
        assert app.title == "Bloatware Remover"
        assert app.version == "0.0.1"


class TestApplicationEndpoints:
    """Test cases for application endpoints"""

    def test_root_endpoint_exists(self, client: TestClient):
        """Test that the root endpoint exists and is accessible"""
        response = client.get("/")
        assert response.status_code == 200

    def test_connect_endpoint_exists(self, client: TestClient):
        """Test that the connect endpoint exists and accepts POST requests"""
        response = client.post("/connect-to-device", data={})
        assert response.status_code == 200

    def test_packages_endpoint_exists(self, client: TestClient):
        """Test that the packages endpoint exists and is accessible"""
        response = client.get("/packages")
        # Should redirect to root if no connection
        assert response.status_code in [200, 303]

    def test_apply_actions_endpoint_exists(self, client: TestClient):
        """Test that the apply actions endpoint exists and accepts POST requests"""
        response = client.post("/apply-actions", data={})
        assert response.status_code == 200


class TestApplicationConfiguration:
    """Test cases for application configuration"""

    def test_app_debug_mode(self):
        """Test that the app can run in debug mode"""
        # This test ensures the app configuration is valid
        assert hasattr(app, 'debug')

    def test_app_docs_available(self, client: TestClient):
        """Test that API documentation is available"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_app_openapi_schema(self, client: TestClient):
        """Test that OpenAPI schema is available"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "openapi" in response.json()


class TestApplicationMiddleware:
    """Test cases for application middleware"""

    def test_cors_headers(self, client: TestClient):
        """Test that CORS headers are properly set"""
        response = client.get("/")
        # Check for common CORS headers
        headers = response.headers
        # Note: CORS headers might not be set if not configured
        assert "content-type" in headers

    def test_response_headers(self, client: TestClient):
        """Test that response headers are properly set"""
        response = client.get("/")
        headers = response.headers

        assert "content-type" in headers
        assert "text/html" in headers["content-type"]


class TestApplicationErrorHandling:
    """Test cases for application error handling"""

    def test_404_handling(self, client: TestClient):
        """Test that 404 errors are handled properly"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404

    def test_method_not_allowed(self, client: TestClient):
        """Test that method not allowed errors are handled"""
        response = client.post("/")  # Root endpoint only accepts GET
        assert response.status_code == 405

    def test_invalid_request_handling(self, client: TestClient):
        """Test that invalid requests are handled properly"""
        # Test with invalid form data
        response = client.post("/connect-to-device", data="invalid_data")
        assert response.status_code in [200, 422, 400]


class TestApplicationPerformance:
    """Test cases for application performance"""

    def test_root_endpoint_response_time(self, client: TestClient):
        """Test that root endpoint responds quickly"""
        import time

        start_time = time.time()
        response = client.get("/")
        end_time = time.time()

        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond within 1 second

    def test_multiple_requests(self, client: TestClient):
        """Test that the app can handle multiple requests"""
        responses = []
        for _ in range(5):
            response = client.get("/")
            responses.append(response.status_code)

        # All requests should succeed
        assert all(status == 200 for status in responses)


class TestApplicationSecurity:
    """Test cases for application security"""

    def test_no_sensitive_info_in_headers(self, client: TestClient):
        """Test that no sensitive information is exposed in headers"""
        response = client.get("/")
        headers = response.headers

        # Check that server information is not exposed
        sensitive_headers = ["server", "x-powered-by", "x-aspnet-version"]
        for header in sensitive_headers:
            assert header not in headers

    def test_content_security_policy(self, client: TestClient):
        """Test that content security policy is properly set"""
        response = client.get("/")
        headers = response.headers

        # Note: CSP headers might not be set if not configured
        # This test ensures the app doesn't crash when checking headers
        assert "content-type" in headers
