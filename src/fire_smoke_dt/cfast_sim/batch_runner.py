"""Run CFAST cases with explicit timeout, captured logs, and parallel batching."""

from __future__ import annotations

import concurrent.futures
import logging
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunResult:
    returncode: int
    stdout: str
    stderr: str
    elapsed_timeout: bool = False
    scenario_id: str = ""


def verify_binary(binary: str | Path) -> None:
    """Check that the CFAST binary exists and is executable."""
    path = Path(binary)
    if not path.exists():
        raise FileNotFoundError(f"CFAST binary not found: {path}")
    try:
        subprocess.run([str(path), "-v"], capture_output=True, timeout=10, check=False)
    except OSError as exc:
        raise RuntimeError(f"CFAST binary not executable: {path}") from exc


def run_case(
    binary: str | Path, input_file: str | Path, *, timeout_s: float = 600, scenario_id: str = ""
) -> RunResult:
    """Run a single CFAST case."""
    try:
        process = subprocess.run(
            [str(binary), str(input_file)],
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
        return RunResult(
            returncode=process.returncode,
            stdout=process.stdout,
            stderr=process.stderr,
            scenario_id=scenario_id,
        )
    except subprocess.TimeoutExpired as exc:
        return RunResult(
            returncode=-1,
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
            elapsed_timeout=True,
            scenario_id=scenario_id,
        )


def run_batch(
    binary: str | Path,
    inputs: Sequence[tuple[str, str | Path]],  # list of (scenario_id, path)
    *,
    timeout_s: float = 600,
    max_workers: int | None = None,
) -> list[RunResult]:
    """Run multiple CFAST cases in parallel.
    
    inputs should be a list of tuples containing (scenario_id, input_file_path).
    Supports resume by only providing the remaining inputs to run.
    """
    verify_binary(binary)
    results: list[RunResult] = []
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(run_case, binary, input_path, timeout_s=timeout_s, scenario_id=scen_id): scen_id
            for scen_id, input_path in inputs
        }
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(futures):
            try:
                res = future.result()
                results.append(res)
            except Exception as e:
                # Handle unexpected executor errors
                scen_id = futures[future]
                results.append(
                    RunResult(returncode=-99, stdout="", stderr=str(e), scenario_id=scen_id)
                )
                
    return results
