"""Translate validated graph and scenario records into CFAST input text."""

from __future__ import annotations

import logging
import math
from typing import Any

logger = logging.getLogger(__name__)


def _format_time(t_end: float, dt_out: float) -> str:
    return f"&TIME SIMULATION={t_end:.1f} PRINT={dt_out:.1f} SMOKEVIEW={dt_out:.1f} SPREADSHEET={dt_out:.1f} /\n"


def _format_comp(node: dict[str, Any], idx: int) -> str:
    area = node.get("area_m2") or 10.0
    height = node.get("ceiling_height_m") or node.get("height_m") or 3.0

    width = node.get("width_m")
    depth = node.get("depth_m")

    if not (width and depth):
        # Fallback: estimate from area with type-specific aspect ratio
        node_type = node.get("node_type", "room")
        default_ratio = 5.0 if node_type in ("corridor", "corridor_link") else 1.5
        aspect = node.get("aspect_ratio", default_ratio)
        # area = width * depth, aspect = depth / width → width = sqrt(area / aspect)
        width = math.sqrt(area / aspect)
        depth = area / width
        logger.warning(
            "Node %s: no explicit width/depth, using fallback (aspect=%.1f)",
            node["node_id"], aspect,
        )

    return f"&COMP ID='{node['node_id']}' DEPTH={depth:.2f} HEIGHT={height:.2f} WIDTH={width:.2f} /\n"


def _format_vent(edge: dict[str, Any], idx: int) -> str:
    # edge source and target, map to ID
    # if target is outside, CFAST uses 'OUTSIDE'
    target = edge.get("target", "OUTSIDE")
    if target.lower() == "outside":
        target = "OUTSIDE"
        
    width = 1.0  # default door width
    height = 2.1 # default door height
    if "opening_area_m2" in edge and "opening_height_m" in edge:
        h = edge["opening_height_m"]
        w = edge["opening_area_m2"] / h if h > 0 else 1.0
        width = w
        height = h

    return (
        f"&VENT ID='{edge['edge_id']}' COMP_ID='{edge['source']}' "
        f"COMP_ID_2='{target}' WIDTH={width:.2f} TOP={height:.2f} BOTTOM=0.00 /\n"
    )


def _format_fire(scenario: dict[str, Any]) -> str:
    comp_id = scenario["fire_node"]
    config = scenario.get("config", {})
    
    # Calculate a simple t-squared fire curve
    peak_hrr = config.get("hrr_peak_kW", 1000.0)
    growth = config.get("fire_growth_class", {})
    alpha = growth.get("alpha_kW_s2", 0.01172) # medium growth by default
    soot = config.get("soot_yield_kg_per_kg", 0.04)
    
    # t_peak = sqrt(peak_hrr / alpha)
    t_peak = math.sqrt(peak_hrr / alpha) if alpha > 0 else 300.0
    
    times = [0.0, t_peak, t_peak + 600.0]
    hrrs = [0.0, peak_hrr, peak_hrr]
    
    time_str = ",".join(f"{t:.1f}" for t in times)
    hrr_str = ",".join(f"{h:.1f}" for h in hrrs)
    
    return (
        f"&FIRE ID='Fire_{comp_id}' COMP_ID='{comp_id}' FIRE_PLUME_TYPE=1 "
        f"TIME={time_str} HRR={hrr_str} SOOT_YIELD={soot} /\n"
    )


def render_cfast_input(graph_payload: dict[str, Any], scenario: dict[str, Any]) -> str:
    """Return deterministic CFAST input text."""
    required = {"scenario_id", "fire_node", "t_end_s", "dt_out_s"}
    missing = required - scenario.keys()
    if missing:
        raise ValueError(f"Scenario missing fields: {sorted(missing)}")

    lines = []
    lines.append(f"&HEAD VERSION=7700 TITLE='Scenario {scenario['scenario_id']}' /\n")
    lines.append(_format_time(scenario["t_end_s"], scenario["dt_out_s"]))
    
    nodes = graph_payload.get("nodes", [])
    for i, node in enumerate(nodes):
        if node.get("node_type") != "outside":
            lines.append(_format_comp(node, i + 1))
            
    edges = graph_payload.get("edges", [])
    for i, edge in enumerate(edges):
        if edge.get("edge_type") in ["door", "window", "opening"]:
            lines.append(_format_vent(edge, i + 1))
            
    lines.append(_format_fire(scenario))
    
    return "".join(lines)
