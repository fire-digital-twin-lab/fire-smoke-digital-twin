"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI

from .routers import comparison, graph, inference, labels, scenarios, timeseries


def create_app() -> FastAPI:
    app = FastAPI(title="Fire Smoke Digital Twin API", version="0.1.0")
    for router in [
        scenarios.router,
        graph.router,
        timeseries.router,
        labels.router,
        inference.router,
        comparison.router,
    ]:
        app.include_router(router)
    return app


app = create_app()
