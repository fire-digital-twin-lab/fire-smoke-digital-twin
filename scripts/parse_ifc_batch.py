"""Batch parser for IFC files to BIM Graph."""

import argparse
import sys
from pathlib import Path

from fire_smoke_dt.bim_graph.ifc_parser import parse_ifc
from fire_smoke_dt.shared.paths import DATA_DIR, OUTPUT_DIR
from fire_smoke_dt.shared.io_utils import write_json


def main():
    parser = argparse.ArgumentParser(description="Parse a batch of IFC files.")
    parser.add_argument("--input-dir", type=str, default=str(DATA_DIR / "ifc"), help="Directory containing .ifc files")
    parser.add_argument("--output-dir", type=str, default=str(OUTPUT_DIR / "parsed_ifc"), help="Output directory")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    if not input_dir.exists():
        print(f"Error: input directory {input_dir} not found.")
        sys.exit(1)
        
    output_dir.mkdir(parents=True, exist_ok=True)

    inputs = list(input_dir.glob("*.ifc"))
    if not inputs:
        print(f"No .ifc files found in {input_dir}")
        sys.exit(0)
        
    print(f"Found {len(inputs)} IFC files. Parsing...")
    
    for p in inputs:
        print(f"Parsing {p.name}...")
        try:
            result = parse_ifc(p)
            out_path = output_dir / f"{p.stem}.json"
            write_json(out_path, result)
        except Exception as e:
            print(f"Error parsing {p.name}: {e}")
            
    print("Done parsing.")

if __name__ == "__main__":
    main()
