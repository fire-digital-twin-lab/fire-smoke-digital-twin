"""Translate validated graph and scenario records into CFAST input text."""

from __future__ import annotations

from typing import Any


def render_cfast_input(graph_payload: dict[str, Any], scenario: dict[str, Any]) -> str:
    """Return deterministic CFAST input text.

    TODO: implement exact CFAST syntax after a debug case is locked. Keep mapping functions
    small and testable: compartment, vent, fire, detector and boundary sections.
    """
    required = {"scenario_id", "fire_node", "t_end_s", "dt_out_s"}
    missing = required - scenario.keys()
    if missing:
        raise ValueError(f"Scenario missing fields: {sorted(missing)}")
    raise NotImplementedError(
        "Lock the CFAST debug-case syntax before implementing the full writer"
    )
