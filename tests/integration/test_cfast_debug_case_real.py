"""Real integration test: build graph → render CFAST input → run CFAST binary → postprocess.

Requires CFAST binary on the machine. Set CFAST_BINARY env var to the path.
Skipped automatically on CI or machines without CFAST installed.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from fire_smoke_dt.cfast_sim.input_writer import render_cfast_input
from fire_smoke_dt.cfast_sim.postprocess import load_raw_output, normalize_output

CFAST_BINARY = os.environ.get("CFAST_BINARY", "")


def _has_cfast() -> bool:
    """Check if CFAST binary is available."""
    if not CFAST_BINARY:
        return False
    path = Path(CFAST_BINARY)
    if not path.exists():
        return False
    try:
        subprocess.run(
            [str(path), "-v"], capture_output=True, timeout=10, check=False,
        )
        return True
    except (OSError, subprocess.TimeoutExpired):
        return False


requires_cfast = pytest.mark.requires_cfast_binary


@requires_cfast
@pytest.mark.skipif(not _has_cfast(), reason="CFAST binary not available (set CFAST_BINARY env var)")
class TestCfastDebugCaseReal:
    """End-to-end test with the real CFAST executable."""

    def _debug_graph(self) -> dict:
        """Small debug building: 2 rooms + 1 corridor + outside."""
        return {
            "nodes": [
                {
                    "node_id": "ROOM_A",
                    "node_type": "room",
                    "area_m2": 12.0,
                    "ceiling_height_m": 3.0,
                    "width_m": 3.0,
                    "depth_m": 4.0,
                },
                {
                    "node_id": "CORRIDOR_1",
                    "node_type": "corridor",
                    "area_m2": 20.0,
                    "ceiling_height_m": 2.8,
                    "width_m": 2.0,
                    "depth_m": 10.0,
                },
                {
                    "node_id": "ROOM_B",
                    "node_type": "room",
                    "area_m2": 15.0,
                    "ceiling_height_m": 3.0,
                    "width_m": 3.0,
                    "depth_m": 5.0,
                },
            ],
            "edges": [
                {
                    "edge_id": "DOOR_A_CORR",
                    "edge_type": "door",
                    "source": "ROOM_A",
                    "target": "CORRIDOR_1",
                    "opening_area_m2": 1.8,
                    "opening_height_m": 2.0,
                },
                {
                    "edge_id": "DOOR_CORR_B",
                    "edge_type": "door",
                    "source": "CORRIDOR_1",
                    "target": "ROOM_B",
                    "opening_area_m2": 1.8,
                    "opening_height_m": 2.0,
                },
                {
                    "edge_id": "DOOR_CORR_OUT",
                    "edge_type": "door",
                    "source": "CORRIDOR_1",
                    "target": "OUTSIDE",
                    "opening_area_m2": 2.0,
                    "opening_height_m": 2.1,
                },
            ],
        }

    def _debug_scenario(self) -> dict:
        return {
            "scenario_id": "DEBUG_REAL_01",
            "fire_node": "ROOM_A",
            "t_end_s": 300.0,
            "dt_out_s": 10.0,
            "config": {
                "hrr_peak_kW": 500.0,
                "fire_growth_class": {"alpha_kW_s2": 0.01172},
                "soot_yield_kg_per_kg": 0.04,
            },
        }

    def test_full_pipeline(self, tmp_path: Path):
        """Build graph → render input → run CFAST → postprocess output."""
        graph = self._debug_graph()
        scenario = self._debug_scenario()

        # 1. Render CFAST input
        cfast_text = render_cfast_input(graph, scenario)
        input_file = tmp_path / "debug_real.in"
        input_file.write_text(cfast_text, encoding="utf-8")

        # 2. Run CFAST binary
        result = subprocess.run(
            [CFAST_BINARY, str(input_file)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(tmp_path),
            check=False,
        )

        assert result.returncode == 0, (
            f"CFAST failed (rc={result.returncode}):\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )

        # 3. Find and load spreadsheet output
        # CFAST typically writes *_n.csv or *_s.csv files
        csv_files = list(tmp_path.glob("*.csv"))
        assert csv_files, f"No CSV output found in {tmp_path}. Files: {list(tmp_path.iterdir())}"

        # Pick the first CSV output to validate
        raw = load_raw_output(csv_files[0])
        assert not raw.empty, f"Output CSV {csv_files[0].name} is empty"

        # 4. Normalize and validate
        df = normalize_output(raw, scenario_id="DEBUG_REAL_01")
        assert "scenario_id" in df.columns
        assert (df["scenario_id"] == "DEBUG_REAL_01").all()
        assert len(df) > 0
