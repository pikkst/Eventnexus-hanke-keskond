from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.config import AppEnvironment, Settings


@pytest.mark.asyncio
class TestErrorHandlingInTestingMode:
    async def test_unhandled_exception_returns_500(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.get("/test/error")
        assert response.status_code == 500

    async def test_internal_error_has_error_code(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.get("/test/error")
        body = response.json()
        assert body["error_code"] == "internal_error"

    async def test_internal_error_has_correlation_id(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.get("/test/error")
        body = response.json()
        assert "correlation_id" in body
        assert body["correlation_id"] == response.headers["x-request-id"]

    async def test_testing_mode_shows_error_detail(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.get("/test/error")
        body = response.json()
        assert "Test error message" in body["detail"]

    async def test_not_found_returns_404(self, test_client: AsyncClient) -> None:
        response = await test_client.get("/nonexistent-path-12345")
        assert response.status_code == 404

    async def test_not_found_has_error_code(self, test_client: AsyncClient) -> None:
        response = await test_client.get("/nonexistent-path-12345")
        body = response.json()
        assert body["error_code"] == "http_error"

    async def test_validation_error_returns_422(self, test_client: AsyncClient) -> None:
        response = await test_client.post("/test/validation", json={"name": ""})
        assert response.status_code == 422

    async def test_validation_error_has_details(self, test_client: AsyncClient) -> None:
        response = await test_client.post("/test/validation", json={"name": ""})
        body = response.json()
        assert body["error_code"] == "validation_error"
        assert "errors" in body
        assert len(body["errors"]) > 0


@pytest.mark.asyncio
class TestErrorHandlingInProductionMode:
    async def test_unhandled_exception_returns_500(
        self, prod_client: AsyncClient
    ) -> None:
        response = await prod_client.get("/test/error")
        assert response.status_code == 500

    async def test_production_does_not_expose_stack_trace(
        self, prod_client: AsyncClient
    ) -> None:
        response = await prod_client.get("/test/error")
        body = response.json()
        assert "Test error message" not in body["detail"]
        assert body["detail"] == "Internal server error"

    async def test_production_error_has_error_code(
        self, prod_client: AsyncClient
    ) -> None:
        response = await prod_client.get("/test/error")
        body = response.json()
        assert body["error_code"] == "internal_error"

    async def test_production_error_has_correlation_id(
        self, prod_client: AsyncClient
    ) -> None:
        response = await prod_client.get("/test/error")
        body = response.json()
        assert "correlation_id" in body
        assert body["correlation_id"] == response.headers["x-request-id"]

    async def test_production_not_found_returns_404(
        self, prod_client: AsyncClient
    ) -> None:
        response = await prod_client.get("/nonexistent-path-12345")
        assert response.status_code == 404

    async def test_production_validation_error_returns_422(
        self, prod_client: AsyncClient
    ) -> None:
        response = await prod_client.post("/test/validation", json={"name": ""})
        assert response.status_code == 422


class TestConfigurationValidation:
    def test_production_requires_secret_key(self) -> None:
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            Settings(
                app_env=AppEnvironment.PRODUCTION,
                secret_key="",
                debug=False,
            )
        assert "SECRET_KEY" in str(exc_info.value)

    def test_production_rejects_short_secret_key(self) -> None:
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            Settings(
                app_env=AppEnvironment.PRODUCTION,
                secret_key="short",
                debug=False,
            )

    def test_production_rejects_debug_true(self) -> None:
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            Settings(
                app_env=AppEnvironment.PRODUCTION,
                secret_key="a-very-secure-secret-key-with-32-chars!",
                debug=True,
            )
        assert "DEBUG" in str(exc_info.value)

    def test_invalid_log_level_raises_error(self) -> None:
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            Settings(
                app_env=AppEnvironment.TESTING,
                secret_key="test-secret-key-for-testing-purposes-only",
                log_level="INVALID_LEVEL",
            )

    def test_invalid_log_format_raises_error(self) -> None:
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            Settings(
                app_env=AppEnvironment.TESTING,
                secret_key="test-secret-key-for-testing-purposes-only",
                log_format="invalid_format",
            )
