from fire_smoke_dt.bim_graph.graph_builder import build_graph
from fire_smoke_dt.bim_graph.topology_check import topology_summary


def test_graph_and_isolated_node_detection():
    graph = build_graph(
        [{"node_id": "A"}, {"node_id": "B"}, {"node_id": "C"}],
        [{"edge_id": "E1", "source": "A", "target": "B", "edge_type": "door"}],
    )
    summary = topology_summary(graph)
    assert summary["isolated_nodes"] == ["C"]
    assert summary["connected"] is False
