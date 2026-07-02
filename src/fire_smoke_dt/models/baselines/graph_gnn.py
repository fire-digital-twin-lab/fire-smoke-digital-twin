"""Graph baseline placeholder; choose one architecture and keep it reproducible."""

from __future__ import annotations


def build_model(*args, **kwargs):
    raise NotImplementedError(
        "Implement GCN or GraphSAGE after dataset feature dimensions are locked"
    )
