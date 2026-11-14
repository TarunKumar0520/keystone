"""Tests for GET /health.

These override the settings dependency so they never depend on your local .env.
That pattern (dependency_overrides) is how we'll test every endpoint later
without calling OpenAI.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from keystone import __version__
from keystone.config import Settings, get_settings
from keystone.main import create_app

FAKE_KEY = "sk-test-not-a-real-key"


def _client_with(settings: Settings) -> Iterator[TestClient]:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings
    with TestClient(app) as client:
        yield client


@pytest.fixture
def client() -> Iterator[TestClient]:
    yield from _client_with(Settings(openai_api_key=FAKE_KEY, app_env="test"))


@pytest.fixture
def client_without_key() -> Iterator[TestClient]:
    yield from _client_with(Settings(openai_api_key=None, app_env="test"))


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body == {
        "status": "ok",
        "app": "KeyStone",
        "version": __version__,
        "environment": "test",
        "openai_configured": True,
    }


def test_health_never_leaks_the_api_key(client: TestClient) -> None:
    response = client.get("/health")

    assert FAKE_KEY not in response.text


def test_health_reports_missing_key(client_without_key: TestClient) -> None:
    response = client_without_key.get("/health")

    assert response.status_code == 200
    assert response.json()["openai_configured"] is False


def test_placeholder_key_counts_as_not_configured() -> None:
    settings = Settings(openai_api_key="sk-replace-me")

    assert settings.openai_configured is False
