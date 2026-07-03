"""Batch runner script for CFAST simulations."""

import argparse
import sys
from pathlib import Path

from fire_smoke_dt.cfast_sim.batch_runner import run_batch
from fire_smoke_dt.shared.paths import OUTPUT_DIR


def main():
    parser = argparse.ArgumentParser(description="Run a batch of CFAST simulations.")
    parser.add_argument("--binary", type=str, default="cfast", help="Path to CFAST binary")
    parser.add_argument("--input-dir", type=str, default=str(OUTPUT_DIR / "cfast_inputs"), help="Directory containing .in files")
    parser.add_argument("--max-workers", type=int, default=2, help="Max parallel jobs")
    parser.add_argument("--timeout", type=float, default=600.0, help="Timeout per simulation in seconds")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"Error: input directory {input_dir} not found.")
        sys.exit(1)

    inputs = []
    for p in input_dir.glob("*.in"):
        inputs.append((p.stem, p))
        
    if not inputs:
        print(f"No .in files found in {input_dir}")
        sys.exit(0)
        
    print(f"Found {len(inputs)} input files. Starting batch run with {args.max_workers} workers...")
    
    results = run_batch(args.binary, inputs, max_workers=args.max_workers, timeout_s=args.timeout)
    
    success = sum(1 for r in results if r.returncode == 0)
    failed = len(results) - success
    
    print(f"Batch completed. Success: {success}, Failed: {failed}")
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
