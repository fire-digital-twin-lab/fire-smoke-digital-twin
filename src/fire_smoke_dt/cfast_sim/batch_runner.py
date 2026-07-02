"""Run CFAST cases with explicit timeout and captured logs."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunResult:
    returncode: int
    stdout: str
    stderr: str
    elapsed_timeout: bool = False


def run_case(binary: str | Path, input_file: str | Path, *, timeout_s: float = 600) -> RunResult:
    try:
        process = subprocess.run(
            [str(binary), str(input_file)],
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
        return RunResult(process.returncode, process.stdout, process.stderr)
    except subprocess.TimeoutExpired as exc:
        return RunResult(-1, exc.stdout or "", exc.stderr or "", elapsed_timeout=True)
