"""Loss functions with explicit masks."""

from __future__ import annotations


def masked_mean(loss, mask):
    import torch

    valid = mask.bool()
    if not torch.any(valid):
        return loss.sum() * 0.0
    return loss[valid].mean()
