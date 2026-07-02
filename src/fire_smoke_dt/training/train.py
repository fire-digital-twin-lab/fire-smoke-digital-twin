"""Training entry point.

The final implementation must snapshot config, split manifest, feature manifest, code commit,
seeds and checkpoint hash. Do not hide experiment state in notebooks.
"""

from __future__ import annotations


def main() -> int:
    raise NotImplementedError("Wire the train loop after dataset and baseline contracts are stable")


if __name__ == "__main__":
    raise SystemExit(main())
