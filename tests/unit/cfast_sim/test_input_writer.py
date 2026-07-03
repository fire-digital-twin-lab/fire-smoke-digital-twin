"""Tests for CFAST input writer."""

import pytest

from fire_smoke_dt.cfast_sim.input_writer import render_cfast_input


def test_render_cfast_input_valid():
    graph = {
        "nodes": [
            {"node_id": "R1", "node_type": "room", "area_m2": 16.0, "ceiling_height_m": 3.0}
        ],
        "edges": [
            {"edge_id": "D1", "edge_type": "door", "source": "R1", "target": "OUTSIDE", "opening_area_m2": 2.1, "opening_height_m": 2.1}
        ]
    }
    scenario = {
        "scenario_id": "test_01",
        "fire_node": "R1",
        "t_end_s": 600.0,
        "dt_out_s": 10.0,
        "config": {
            "hrr_peak_kW": 1000.0,
            "fire_growth_class": {"alpha_kW_s2": 0.01},
            "soot_yield_kg_per_kg": 0.05
        }
    }

    out = render_cfast_input(graph, scenario)

    assert "&HEAD VERSION=7700" in out
    assert "&TIME SIMULATION=600.0" in out
    assert "ID='R1'" in out
    # Room 16m², default aspect_ratio 1.5: width=sqrt(16/1.5)≈3.27, depth≈4.90
    assert "DEPTH=" in out
    assert "HEIGHT=3.00" in out
    assert "ID='D1'" in out
    assert "COMP_ID='R1' COMP_ID_2='OUTSIDE'" in out
    assert "&FIRE ID='Fire_R1'" in out
    assert "SOOT_YIELD=0.05" in out


def test_render_cfast_input_missing_fields():
    with pytest.raises(ValueError, match="Scenario missing fields:"):
        render_cfast_input({}, {"scenario_id": "1"})


def test_render_cfast_input_explicit_geometry():
    """When width_m and depth_m are provided, use them directly."""
    graph = {
        "nodes": [
            {"node_id": "R1", "node_type": "room", "area_m2": 20.0,
             "ceiling_height_m": 3.0, "width_m": 4.0, "depth_m": 5.0}
        ],
        "edges": []
    }
    scenario = {
        "scenario_id": "test_explicit",
        "fire_node": "R1",
        "t_end_s": 600.0,
        "dt_out_s": 10.0,
    }

    out = render_cfast_input(graph, scenario)
    assert "DEPTH=5.00 HEIGHT=3.00 WIDTH=4.00" in out


def test_render_cfast_input_corridor_not_square():
    """Corridor with large area should NOT produce a square compartment."""
    graph = {
        "nodes": [
            {"node_id": "CORR_1", "node_type": "corridor", "area_m2": 40.0,
             "ceiling_height_m": 2.8}
        ],
        "edges": []
    }
    scenario = {
        "scenario_id": "test_corridor",
        "fire_node": "CORR_1",
        "t_end_s": 600.0,
        "dt_out_s": 10.0,
    }

    out = render_cfast_input(graph, scenario)

    # Extract DEPTH and WIDTH from output
    for line in out.splitlines():
        if "CORR_1" in line and "&COMP" in line:
            # Parse WIDTH and DEPTH values
            parts = line.split()
            width_val = depth_val = None
            for part in parts:
                if part.startswith("WIDTH="):
                    width_val = float(part.split("=")[1])
                if part.startswith("DEPTH="):
                    depth_val = float(part.split("=")[1])
            assert width_val is not None and depth_val is not None
            # Corridor default aspect_ratio=5.0 → depth should be ~5x width
            assert depth_val > width_val * 2, (
                f"Corridor should be elongated, got WIDTH={width_val}, DEPTH={depth_val}"
            )
            # Should NOT be square (sqrt(40) ≈ 6.32)
            assert abs(width_val - depth_val) > 1.0, "Corridor must not be square"
            break
    else:
        pytest.fail("CORR_1 compartment line not found in CFAST output")
