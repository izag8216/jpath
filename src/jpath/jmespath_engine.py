"""JMESPath query execution engine."""

import jmespath
from typing import Any


class JMESPathError(Exception):
    """Raised when JMESPath query fails."""


def execute_jmespath(data: Any, query: str) -> Any:
    """Execute a JMESPath query against JSON data.

    Args:
        data: Parsed JSON data.
        query: JMESPath query string.

    Returns:
        Query result.

    Raises:
        JMESPathError: If query is invalid.
    """
    try:
        result = jmespath.search(query, data)
        return result
    except jmespath.exceptions.ParseError as e:
        raise JMESPathError(f"Invalid JMESPath query: {e}")


def validate_jmespath(query: str) -> tuple[bool, str]:
    """Validate a JMESPath query without executing.

    Args:
        query: JMESPath query string.

    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        jmespath.parser.Parser().parse(query)
        return True, ""
    except jmespath.exceptions.ParseError as e:
        return False, str(e)
