"""Boundary-Aware Temporal GNN placeholder.

Required encoders: graph, temporal IoT, boundary, fire and system state. Required P0 heads:
smoke classification and masked time-to-arrival regression.
"""

from __future__ import annotations


def build_model(*args, **kwargs):
    raise NotImplementedError("Implement as the final P0 model, not before baseline completion")
