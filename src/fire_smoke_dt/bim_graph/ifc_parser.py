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
        import ifcopenshell.util.element  # type: ignore
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
    
    def get_properties(item: Any) -> dict[str, Any]:
        props: dict[str, Any] = {}
        # ifcopenshell.util.element.get_psets returns all property sets and quantities
        psets = ifcopenshell.util.element.get_psets(item)
        if not psets:
            return props
        for _pset_name, pset_data in psets.items():
            if not isinstance(pset_data, dict):
                continue
            for k, v in pset_data.items():
                if k not in props and v is not None:
                    props[k] = v
        return props

    for name in entity_names:
        parsed_items = []
        for item in model.by_type(name):
            data: dict[str, Any] = {
                "ifc_type": name,
                "global_id": getattr(item, "GlobalId", None),
                "name": getattr(item, "Name", None),
            }
            if name == "IfcSpace":
                props = get_properties(item)
                # Attempt to extract geometry quantities for compartment sizing
                data["area_m2"] = props.get("GrossFloorArea") or props.get("NetFloorArea") or props.get("Area")
                data["volume_m3"] = props.get("GrossVolume") or props.get("NetVolume") or props.get("Volume")
                data["ceiling_height_m"] = props.get("Height")
                
            parsed_items.append(data)
        result[name] = parsed_items
        
    return result
