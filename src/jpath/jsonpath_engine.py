"""JSONPath query execution engine."""

from typing import Any
from jsonpath_ng.ext import parse
from jsonpath_ng import jsonpath


class JSONPathError(Exception):
    """Raised when JSONPath query fails."""


def execute_jsonpath(data: Any, query: str) -> list[Any]:
    """Execute a JSONPath query against JSON data.

    Args:
        data: Parsed JSON data.
        query: JSONPath query string.

    Returns:
        List of matching values.

    Raises:
        JSONPathError: If query is invalid.
    """
    try:
        jsonpath_expr = parse(query)
        matches = jsonpath_expr.find(data)
        return [match.value for match in matches]
    except Exception as e:
        raise JSONPathError(f"Invalid JSONPath query: {e}")


def validate_jsonpath(query: str) -> tuple[bool, str]:
    """Validate a JSONPath query without executing.

    Args:
        query: JSONPath query string.

    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        parse(query)
        return True, ""
    except Exception as e:
        return False, str(e)
