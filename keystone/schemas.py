"""Pydantic models for every API input and output.

Keeping them in one module makes the API contract easy to read in one place.
Later phases add RetrieveRequest/Response, AskRequest/Response, Citation, etc.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response for GET /health."""

    status: Literal["ok"] = Field(description="Always 'ok' if the API process is up.")
    app: str = Field(description="Application name.")
    version: str = Field(description="KeyStone version string.")
    environment: Literal["dev", "test", "prod"]
    openai_configured: bool = Field(
        description="True if an OpenAI API key is set. The key itself is never returned."
    )
