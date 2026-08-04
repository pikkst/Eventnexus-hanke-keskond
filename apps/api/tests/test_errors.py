from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from httpx import AsyncClient

from app.config import AppEnvironment, Settings
from app.core.correlation import correlation_id_ctx


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

    async def test_validation_error_sanitizes_input(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.post(
            "/test/validation",
            json={"name": 123},
        )
        assert response.status_code == 422
        body = response.json()
        for error in body["errors"]:
            assert error.get("input") == "<redacted>"

    async def test_custom_validator_error_returns_422(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.post(
            "/test/custom-validation", json={"code": "INVALID"}
        )
        assert response.status_code == 422
        body = response.json()
        assert body["error_code"] == "validation_error"
        assert len(body["errors"]) > 0

    async def test_custom_validator_error_sanitizes_ctx(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.post(
            "/test/custom-validation", json={"code": "INVALID"}
        )
        assert response.status_code == 422
        body = response.json()
        for error in body["errors"]:
            if "ctx" in error:
                for _key, value in error["ctx"].items():
                    assert not isinstance(value, Exception)

    async def test_method_not_allowed_preserves_allow_header(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.post("/health")
        assert response.status_code == 405
        assert "allow" in response.headers
        assert "GET" in response.headers["allow"]

    async def test_correlation_header_is_single(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.get("/test/error")
        assert response.status_code == 500
        header_values = response.headers.get_list("x-request-id")
        assert len(header_values) == 1

    async def test_correlation_header_preserves_valid_client_id(
        self, test_client: AsyncClient
    ) -> None:
        custom_id = "valid-correlation-id-123"
        response = await test_client.get(
            "/health", headers={"x-request-id": custom_id}
        )
        assert response.headers["x-request-id"] == custom_id

    async def test_correlation_header_rejects_invalid_client_id(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.get(
            "/health", headers={"x-request-id": "bad id with spaces!"}
        )
        assert response.status_code == 200
        received = response.headers["x-request-id"]
        assert received != "bad id with spaces!"
        assert len(received) == 32

    async def test_correlation_context_reset_after_unhandled_error(
        self, test_client: AsyncClient
    ) -> None:
        await test_client.get("/test/error")
        assert correlation_id_ctx.get() is None

    async def test_correlation_context_isolation_after_error_then_request(
        self, test_client: AsyncClient
    ) -> None:
        await test_client.get("/test/error")
        assert correlation_id_ctx.get() is None

        response = await test_client.get("/health")
        assert response.status_code == 200
        assert correlation_id_ctx.get() is None

    async def test_validation_logs_do_not_leak_rejected_value(
        self, test_client: AsyncClient, capfd
    ) -> None:
        secret_value = "SECRET-12345"
        response = await test_client.post(
            "/test/leaky-validation",
            json={"code": secret_value},
        )
        assert response.status_code == 422
        captured = capfd.readouterr()
        assert secret_value not in captured.out


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

    async def test_production_method_not_allowed_preserves_allow_header(
        self, prod_client: AsyncClient
    ) -> None:
        response = await prod_client.post("/health")
        assert response.status_code == 405
        assert "allow" in response.headers
        assert "GET" in response.headers["allow"]

    async def test_production_correlation_header_is_single(
        self, prod_client: AsyncClient
    ) -> None:
        response = await prod_client.get("/test/error")
        assert response.status_code == 500
        header_values = response.headers.get_list("x-request-id")
        assert len(header_values) == 1

    async def test_production_cors_does_not_allow_wildcard(
        self, prod_client: AsyncClient
    ) -> None:
        response = await prod_client.get(
            "/health",
            headers={"origin": "https://evil.example.com"},
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" not in response.headers

    async def test_production_cors_on_unhandled_error(
        self, prod_client: AsyncClient
    ) -> None:
        response = await prod_client.get(
            "/test/error",
            headers={"origin": "http://127.0.0.1:3000"},
        )
        assert response.status_code == 500
        assert response.headers.get("access-control-allow-origin") == "http://127.0.0.1:3000"
        assert response.headers.get("access-control-expose-headers") == "X-Request-ID"

    async def test_production_host_validation_blocks_unknown_hosts(
        self, prod_client: AsyncClient
    ) -> None:
        response = await prod_client.get(
            "/health",
            headers={"host": "evil.example.com"},
        )
        assert response.status_code == 400


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

    def test_production_rejects_wildcard_allowed_hosts(self) -> None:
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            Settings(
                app_env=AppEnvironment.PRODUCTION,
                secret_key="a-very-secure-secret-key-with-32-chars!",
                debug=False,
                allowed_hosts=["*"],
            )
        assert "ALLOWED_HOSTS" in str(exc_info.value)

    def test_production_rejects_wildcard_cors_origins(self) -> None:
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            Settings(
                app_env=AppEnvironment.PRODUCTION,
                secret_key="a-very-secure-secret-key-with-32-chars!",
                debug=False,
                cors_origins=["*"],
            )
        assert "CORS_ORIGINS" in str(exc_info.value)


class TestDockerfileRegression:
    def test_dockerfile_copies_app_before_pip_install(self) -> None:
        dockerfile = Path(__file__).resolve().parents[1] / "Dockerfile"
        content = dockerfile.read_text(encoding="utf-8")
        deps_section = content.split("FROM base AS deps")[1].split("FROM base AS runtime")[0]
        app_copy_index = deps_section.index("COPY app ./app")
        pip_install_index = deps_section.index("pip install")
        assert app_copy_index < pip_install_index

    def test_dockerfile_builds(self) -> None:
        dockerfile = Path(__file__).resolve().parents[1] / "Dockerfile"
        result = subprocess.run(
            ["docker", "build", "-t", "eventnexus-api-test", str(dockerfile.parent)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
