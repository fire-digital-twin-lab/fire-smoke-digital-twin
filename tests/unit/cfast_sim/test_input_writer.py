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
    assert "DEPTH=4.00 HEIGHT=3.00 WIDTH=4.00" in out
    assert "ID='D1'" in out
    assert "COMP_ID='R1' COMP_ID_2='OUTSIDE'" in out
    assert "&FIRE ID='Fire_R1'" in out
    assert "SOOT_YIELD=0.05" in out


def test_render_cfast_input_missing_fields():
    with pytest.raises(ValueError, match="Scenario missing fields:"):
        render_cfast_input({}, {"scenario_id": "1"})
