"""Topology checks and markdown reporting."""

from __future__ import annotations

import networkx as nx


def topology_summary(graph: nx.Graph) -> dict[str, object]:
    components = (
        [sorted(c) for c in nx.connected_components(graph)] if graph.number_of_nodes() else []
    )
    return {
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "connected": len(components) <= 1,
        "component_count": len(components),
        "isolated_nodes": sorted(nx.isolates(graph)),
        "components": components,
    }


def to_markdown(summary: dict[str, object]) -> str:
    return (
        "# Graph check report\n\n"
        f"- Nodes: {summary['node_count']}\n"
        f"- Edges: {summary['edge_count']}\n"
        f"- Connected: {summary['connected']}\n"
        f"- Isolated nodes: {summary['isolated_nodes']}\n"
    )
