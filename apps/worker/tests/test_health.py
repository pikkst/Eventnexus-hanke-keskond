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
