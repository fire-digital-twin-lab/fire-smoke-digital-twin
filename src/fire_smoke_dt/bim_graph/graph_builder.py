"""Build a NetworkX graph from normalized node and edge records."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

import networkx as nx


def build_graph(
    nodes: Iterable[Mapping[str, Any]],
    edges: Iterable[Mapping[str, Any]],
) -> nx.Graph:
    graph = nx.Graph()
    for node in nodes:
        row = dict(node)
        node_id = str(row.pop("node_id"))
        graph.add_node(node_id, **row)
    for edge in edges:
        row = dict(edge)
        source = str(row.pop("source"))
        target = str(row.pop("target"))
        edge_id = str(row.pop("edge_id", f"{source}--{target}"))
        if source not in graph or target not in graph:
            raise ValueError(f"Edge {edge_id} references unknown node")
        graph.add_edge(source, target, edge_id=edge_id, **row)
    return graph
