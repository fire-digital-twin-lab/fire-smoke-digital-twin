"""Integration test connecting the mock graph to CFAST input generator."""

from fire_smoke_dt.cfast_sim.input_writer import render_cfast_input


def test_pipeline_graph_to_cfast_input():
    # 1. Mock Graph payload — rooms with explicit geometry to avoid fallback ambiguity
    graph_payload = {
        "nodes": [
            {"node_id": "ROOM_1", "node_type": "room", "area_m2": 25.0, "ceiling_height_m": 3.0,
             "width_m": 5.0, "depth_m": 5.0},
            {"node_id": "ROOM_2", "node_type": "room", "area_m2": 15.0, "ceiling_height_m": 3.0,
             "width_m": 3.0, "depth_m": 5.0}
        ],
        "edges": [
            {"edge_id": "DOOR_1", "edge_type": "door", "source": "ROOM_1", "target": "ROOM_2", "opening_area_m2": 2.0, "opening_height_m": 2.0},
            {"edge_id": "DOOR_2", "edge_type": "door", "source": "ROOM_2", "target": "OUTSIDE", "opening_area_m2": 2.0, "opening_height_m": 2.0}
        ]
    }

    # 2. Mock Scenario
    scenario = {
        "scenario_id": "INTEGRATION_01",
        "fire_node": "ROOM_1",
        "t_end_s": 900.0,
        "dt_out_s": 10.0,
        "config": {
            "hrr_peak_kW": 2000.0,
            "fire_growth_class": {"alpha_kW_s2": 0.04689}, # fast
            "soot_yield_kg_per_kg": 0.04
        }
    }

    # 3. Generate CFAST input
    cfast_input = render_cfast_input(graph_payload, scenario)

    # 4. Verify outputs
    assert "&HEAD VERSION=7700 TITLE='Scenario INTEGRATION_01' /" in cfast_input
    assert "&TIME SIMULATION=900.0 PRINT=10.0 SMOKEVIEW=10.0 SPREADSHEET=10.0 /" in cfast_input

    # ROOM_1: explicit 5x5
    assert "&COMP ID='ROOM_1' DEPTH=5.00 HEIGHT=3.00 WIDTH=5.00 /" in cfast_input

    # ROOM_2: explicit 3x5
    assert "&COMP ID='ROOM_2' DEPTH=5.00 HEIGHT=3.00 WIDTH=3.00 /" in cfast_input

    # DOOR_1: area 2, height 2 -> width 1
    assert "&VENT ID='DOOR_1' COMP_ID='ROOM_1' COMP_ID_2='ROOM_2' WIDTH=1.00 TOP=2.00 BOTTOM=0.00 /" in cfast_input
    assert "&VENT ID='DOOR_2' COMP_ID='ROOM_2' COMP_ID_2='OUTSIDE'" in cfast_input

    assert "&FIRE ID='Fire_ROOM_1' COMP_ID='ROOM_1'" in cfast_input
    assert "HRR=0.0,2000.0,2000.0" in cfast_input
