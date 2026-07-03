"""Tests for CFAST batch runner."""

import sys
from pathlib import Path

import pytest

from fire_smoke_dt.cfast_sim.batch_runner import run_case, run_batch


def test_run_case_success(tmp_path):
    dummy_exe = tmp_path / "dummy.bat"
    dummy_exe.write_text("@echo off\necho Success")
    
    input_file = tmp_path / "dummy.in"
    input_file.touch()
    
    res = run_case(dummy_exe, input_file, scenario_id="S1")
    assert res.returncode == 0
    assert "Success" in res.stdout
    assert res.scenario_id == "S1"


def test_run_batch_parallel(tmp_path):
    dummy_exe = tmp_path / "dummy.bat"
    dummy_exe.write_text("@echo off\ntimeout /t 1 > nul\necho Done")
    
    inputs = []
    for i in range(3):
        in_path = tmp_path / f"{i}.in"
        in_path.touch()
        inputs.append((f"S{i}", in_path))
        
    results = run_batch(dummy_exe, inputs, max_workers=2)
    
    assert len(results) == 3
    for r in results:
        assert r.returncode == 0
        assert "Done" in r.stdout
        assert r.scenario_id.startswith("S")
