"""Output helpers for condition-search results."""

from __future__ import annotations

import os
from pathlib import Path


def append_condition_result(filename: str, code: str, name: str) -> Path:
    output_dir = Path(os.getenv("STOCK_COLLECT_OUTPUT_DIR", "files"))
    output_dir.mkdir(parents=True, exist_ok=True)

    path = output_dir / filename
    with path.open("a", encoding="utf8") as output:
        output.write(f"{code} \t {name} \n")
    return path
