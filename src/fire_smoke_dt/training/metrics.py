"""AI evaluation metrics; save raw counts as well as summary scores."""

from __future__ import annotations


def classification_counts(y_true, y_pred) -> dict[str, int]:
    yt = [int(v) for v in y_true]
    yp = [int(v) for v in y_pred]
    return {
        "tp": sum(a == 1 and b == 1 for a, b in zip(yt, yp, strict=True)),
        "tn": sum(a == 0 and b == 0 for a, b in zip(yt, yp, strict=True)),
        "fp": sum(a == 0 and b == 1 for a, b in zip(yt, yp, strict=True)),
        "fn": sum(a == 1 and b == 0 for a, b in zip(yt, yp, strict=True)),
    }
