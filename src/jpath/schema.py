"""Schema inference from JSON data."""

import json
from typing import Any, Optional


def infer_schema(data: Any, path: Optional[str] = None) -> dict:
    """Infer JSON Schema from data.

    Args:
        data: Parsed JSON data.
        path: Optional JMESPath to focus on a subset of data.

    Returns:
        JSON Schema (draft-07) as dict.
    """
    if path:
        from jpath.jmespath_engine import execute_jmespath
        data = execute_jmespath(data, path)

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Inferred Schema",
        "type": _infer_type(data),
    }

    if isinstance(data, dict):
        schema["properties"] = {}
        schema["required"] = []
        for key, value in data.items():
            schema["properties"][key] = infer_schema(value)
            schema["required"].append(key)
        if not schema["required"]:
            del schema["required"]
    elif isinstance(data, list) and len(data) > 0:
        schema["items"] = _infer_array_items(data)

    return schema


def _infer_type(value: Any) -> str:
    """Infer JSON Schema type from Python value."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "string"


def _infer_array_items(data: list) -> dict:
    """Infer schema for array items."""
    if not data:
        return {}

    if all(isinstance(item, dict) for item in data):
        merged = {}
        for item in data:
            for key, value in item.items():
                if key not in merged:
                    merged[key] = value
        return infer_schema(merged)

    types = set(_infer_type(item) for item in data)
    if len(types) == 1:
        return {"type": types.pop()}
    return {"type": list(types)}
