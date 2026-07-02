"""Generate selected FDS reference input files from aligned scenario configs."""

from __future__ import annotations

from typing import Any


def render_fds_input(graph_payload: dict[str, Any], scenario: dict[str, Any]) -> str:
    raise NotImplementedError(
        "Implement after the pilot case fixes mesh, devices and output quantities"
    )
