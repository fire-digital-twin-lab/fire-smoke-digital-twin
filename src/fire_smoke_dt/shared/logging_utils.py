"""DEPRECATED: nội dung thật đã chuyển sang shared/logging.py.
Giữ file này 1 sprint để không phá import cũ, sẽ xoá sau khi xác nhận
không còn nơi nào import từ logging_utils.
"""
from __future__ import annotations

import warnings

from fire_smoke_dt.shared.logging import *  # noqa: F401,F403

warnings.warn(
    "fire_smoke_dt.shared.logging_utils is deprecated; import from "
    "fire_smoke_dt.shared.logging instead.",
    DeprecationWarning,
    stacklevel=2,
)
