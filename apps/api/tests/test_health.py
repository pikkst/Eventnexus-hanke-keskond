from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestHealthEndpoint:
    async def test_health_returns_ok(self, test_client: AsyncClient) -> None:
        response = await test_client.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert "timestamp" in body

    async def test_health_returns_iso_timestamp(self, test_client: AsyncClient) -> None:
        response = await test_client.get("/health")
        body = response.json()
        timestamp = body["timestamp"]
        assert "T" in timestamp

    async def test_health_has_correlation_id_header(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.get("/health")
        assert "x-request-id" in response.headers

    async def test_health_preserves_client_request_id(
        self, test_client: AsyncClient
    ) -> None:
        custom_id = "test-correlation-id-12345"
        response = await test_client.get("/health", headers={"x-request-id": custom_id})
        assert response.headers["x-request-id"] == custom_id


@pytest.mark.asyncio
class TestReadinessEndpoint:
    async def test_ready_returns_ok(self, test_client: AsyncClient) -> None:
        response = await test_client.get("/ready")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert "timestamp" in body
        assert "version" in body
        assert "environment" in body

    async def test_ready_returns_testing_environment(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.get("/ready")
        body = response.json()
        assert body["environment"] == "testing"

    async def test_ready_returns_version(self, test_client: AsyncClient) -> None:
        from app.version import __version__

        response = await test_client.get("/ready")
        body = response.json()
        assert body["version"] == __version__

    async def test_ready_has_correlation_id_header(
        self, test_client: AsyncClient
    ) -> None:
        response = await test_client.get("/ready")
        assert "x-request-id" in response.headers


@pytest.mark.asyncio
class TestEndpointMetadata:
    async def test_openapi_document_generated(self, test_client: AsyncClient) -> None:
        response = await test_client.get("/openapi.json")
        assert response.status_code == 200
        spec = response.json()
        assert "info" in spec
        assert spec["info"]["title"] == "EventNexus Hanke Keskond"

    async def test_health_path_in_openapi(self, test_client: AsyncClient) -> None:
        response = await test_client.get("/openapi.json")
        spec = response.json()
        assert "/health" in spec["paths"]
        assert "/ready" in spec["paths"]
