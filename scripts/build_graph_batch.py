"""Batch graph builder from parsed IFC data."""

import argparse
import sys
from pathlib import Path

from fire_smoke_dt.shared.paths import OUTPUT_DIR
from fire_smoke_dt.shared.io_utils import read_json, write_json


def main():
    parser = argparse.ArgumentParser(description="Build BIM Graph from parsed IFC data.")
    parser.add_argument("--input-dir", type=str, default=str(OUTPUT_DIR / "parsed_ifc"), help="Directory containing parsed IFC JSONs")
    parser.add_argument("--output-dir", type=str, default=str(OUTPUT_DIR / "bim_graphs"), help="Output directory")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    if not input_dir.exists():
        print(f"Error: input directory {input_dir} not found.")
        sys.exit(1)
        
    output_dir.mkdir(parents=True, exist_ok=True)

    inputs = list(input_dir.glob("*.json"))
    if not inputs:
        print(f"No json files found in {input_dir}")
        sys.exit(0)
        
    print(f"Found {len(inputs)} JSON files. Building graphs...")
    
    for p in inputs:
        print(f"Processing {p.name}...")
        try:
            data = read_json(p)
            # A simple stub conversion for now
            # Typically you'd have a build_graph(data) function
            graph = {"nodes": data.get("IfcSpace", []), "edges": data.get("IfcDoor", [])}
            out_path = output_dir / f"{p.stem}_graph.json"
            write_json(out_path, graph)
        except Exception as e:
            print(f"Error building graph for {p.name}: {e}")
            
    print("Done building graphs.")

if __name__ == "__main__":
    main()
