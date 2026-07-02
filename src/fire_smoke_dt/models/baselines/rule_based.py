"""Rule-based graph-spread baseline; intentionally simple and auditable."""

from __future__ import annotations

import networkx as nx


def predict_affected(graph: nx.Graph, observed_smoke_nodes: set[str], *, hops: int = 1) -> set[str]:
    affected = set(observed_smoke_nodes)
    frontier = set(observed_smoke_nodes)
    for _ in range(hops):
        frontier = {n for node in frontier for n in graph.neighbors(node)} - affected
        affected |= frontier
    return affected
