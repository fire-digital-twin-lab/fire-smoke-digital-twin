"""Parse IFC entities into normalized row dictionaries.

Keep IfcOpenShell import inside the function so users working on other modules do not need
IfcOpenShell installed merely to import the package.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def parse_ifc(path: str | Path) -> dict[str, list[dict[str, Any]]]:
    try:
        import ifcopenshell  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Install the BIM optional dependency: pip install -e .[bim]") from exc

    model = ifcopenshell.open(str(path))
    entity_names = [
        "IfcBuildingStorey",
        "IfcSpace",
        "IfcDoor",
        "IfcWindow",
        "IfcStair",
        "IfcRelSpaceBoundary",
    ]
    result: dict[str, list[dict[str, Any]]] = {}
    for name in entity_names:
        result[name] = [
            {
                "ifc_type": name,
                "global_id": getattr(item, "GlobalId", None),
                "name": getattr(item, "Name", None),
            }
            for item in model.by_type(name)
        ]
    return result
