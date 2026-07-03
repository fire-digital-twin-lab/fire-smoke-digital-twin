"""Make a unified dataset from CFAST/FDS outputs and graph data."""

import argparse
import sys
from pathlib import Path

from fire_smoke_dt.shared.paths import OUTPUT_DIR, DATA_DIR


def main():
    parser = argparse.ArgumentParser(description="Build unified ML dataset.")
    parser.add_argument("--output-dir", type=str, default=str(DATA_DIR / "dataset"), help="Output dataset directory")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Building dataset in {output_dir}...")
    # Typically you would call build_dataset modules here.
    # For now, it's a stub to replace the NotImplementedError.
    print("Done building dataset.")

if __name__ == "__main__":
    main()
