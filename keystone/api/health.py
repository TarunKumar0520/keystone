"""Health-check endpoint: confirms the API is running and config loaded."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from keystone import __version__
from keystone.config import Settings, get_settings
from keystone.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    """Cheap liveness check. Makes no external calls, so it costs nothing to hit."""
    return HealthResponse(
        status="ok",
        app="KeyStone",
        version=__version__,
        environment=settings.app_env,
        openai_configured=settings.openai_configured,
    )
