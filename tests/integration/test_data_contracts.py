from fire_smoke_dt.shared.schema import EdgeStatic, EdgeType, NodeStatic, NodeType


def test_minimum_graph_contract_models():
    node = NodeStatic(node_id="R1", node_type=NodeType.ROOM, floor_id="F1")
    edge = EdgeStatic(edge_id="D1", source="R1", target="C1", edge_type=EdgeType.DOOR)
    assert node.node_id == "R1"
    assert edge.edge_type == "door"
