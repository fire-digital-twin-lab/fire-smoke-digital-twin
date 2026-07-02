"""Non-graph temporal baseline placeholder."""

from __future__ import annotations


def build_model(*args, **kwargs):
    try:
        import torch.nn as nn
    except ImportError as exc:
        raise RuntimeError("Install ML dependencies: pip install -e .[ml]") from exc

    class NonGraphLSTM(nn.Module):
        def __init__(self, input_dim: int, hidden_dim: int = 64):
            super().__init__()
            self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
            self.smoke_head = nn.Linear(hidden_dim, 1)
            self.tta_head = nn.Linear(hidden_dim, 1)

        def forward(self, x):
            out, _ = self.lstm(x)
            h = out[:, -1]
            return {"smoke_logit": self.smoke_head(h), "tta": self.tta_head(h)}

    return NonGraphLSTM(*args, **kwargs)
