"""JSON file loading and stdin support."""

import json
import sys
from pathlib import Path
from typing import Any, Optional


class JSONLoadError(Exception):
    """Raised when JSON cannot be loaded."""


def load_json(path: Optional[str] = None) -> Any:
    """Load JSON from file or stdin.

    Args:
        path: Path to JSON file. If None, reads from stdin.

    Returns:
        Parsed JSON data.

    Raises:
        JSONLoadError: If JSON is invalid or file not found.
    """
    if path is None:
        return _load_from_stdin()
    return _load_from_file(path)


def _load_from_stdin() -> Any:
    """Read and parse JSON from stdin."""
    try:
        data = sys.stdin.read()
        if not data.strip():
            raise JSONLoadError("No input provided via stdin")
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise JSONLoadError(f"Invalid JSON from stdin: {e}")


def _load_from_file(path: str) -> Any:
    """Read and parse JSON from file."""
    file_path = Path(path)
    if not file_path.exists():
        raise JSONLoadError(f"File not found: {path}")
    if not file_path.is_file():
        raise JSONLoadError(f"Not a file: {path}")

    try:
        content = file_path.read_text(encoding="utf-8")
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise JSONLoadError(f"Invalid JSON in {path}: {e}")
