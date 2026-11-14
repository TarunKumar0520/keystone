"""FastAPI application entry point.

Run locally:
    uvicorn keystone.main:app --reload
Then open http://127.0.0.1:8000/docs for the interactive API docs.
"""

from __future__ import annotations

from fastapi import FastAPI

from keystone import __version__
from keystone.api import health


def create_app() -> FastAPI:
    """App factory: builds a fresh FastAPI instance (handy for tests)."""
    app = FastAPI(
        title="KeyStone",
        description="Agentic tax research assistant that answers only from cited IRS documents.",
        version=__version__,
    )
    app.include_router(health.router)
    # Phase 3 adds the retrieval router, Phase 4 the /ask router.
    return app


# Module-level instance that uvicorn imports.
app = create_app()
