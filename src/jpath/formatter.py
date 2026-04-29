"""Output formatting for query results."""

import csv
import io
import json
from typing import Any


def format_output(data: Any, fmt: str = "json") -> str:
    """Format query result for output.

    Args:
        data: Query result data.
        fmt: Output format ('json', 'json-compact', 'csv', 'text').

    Returns:
        Formatted string.

    Raises:
        ValueError: If format is unsupported.
    """
    if fmt == "json":
        return json.dumps(data, indent=2, ensure_ascii=False)
    if fmt == "json-compact":
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    if fmt == "csv":
        return _to_csv(data)
    if fmt == "text":
        return _to_text(data)
    raise ValueError(f"Unsupported format: {fmt}. Use 'json', 'json-compact', 'csv', or 'text'.")


def _to_csv(data: Any) -> str:
    """Convert data to CSV format."""
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow({k: _flatten_value(v) for k, v in row.items()})
        return output.getvalue()
    elif isinstance(data, list):
        output = io.StringIO()
        writer = csv.writer(output)
        for item in data:
            if isinstance(item, list):
                writer.writerow(item)
            else:
                writer.writerow([item])
        return output.getvalue()
    else:
        return str(data)


def _to_text(data: Any) -> str:
    """Convert data to flat text (one value per line)."""
    if isinstance(data, list):
        lines = []
        for item in data:
            if isinstance(item, dict):
                lines.append(json.dumps(item, ensure_ascii=False))
            else:
                lines.append(str(item))
        return "\n".join(lines)
    return str(data)


def _flatten_value(value: Any) -> str:
    """Flatten a value for CSV output."""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return ""
    return str(value)
