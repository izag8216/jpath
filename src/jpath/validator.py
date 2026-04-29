"""Query validation and explanation."""

from jpath.jmespath_engine import validate_jmespath
from jpath.jsonpath_engine import validate_jsonpath


def validate_query(query: str, query_type: str) -> dict:
    """Validate a query and return structured result.

    Args:
        query: Query string.
        query_type: 'jmespath' or 'jsonpath'.

    Returns:
        Dict with 'valid', 'type', 'error', 'explanation' keys.
    """
    if query_type == "jmespath":
        is_valid, error = validate_jmespath(query)
    elif query_type == "jsonpath":
        is_valid, error = validate_jsonpath(query)
    else:
        return {
            "valid": False,
            "type": query_type,
            "error": f"Unknown query type: {query_type}. Use 'jmespath' or 'jsonpath'.",
            "explanation": "",
        }

    explanation = _generate_explanation(query, query_type) if is_valid else ""

    return {
        "valid": is_valid,
        "type": query_type,
        "error": error if not is_valid else "",
        "explanation": explanation,
    }


def _generate_explanation(query: str, query_type: str) -> str:
    """Generate human-readable explanation of what the query does.

    Args:
        query: Query string.
        query_type: 'jmespath' or 'jsonpath'.

    Returns:
        Human-readable explanation.
    """
    parts = []

    if query_type == "jmespath":
        parts.append(f"JMESPath query: {query}")
        if "*" in query:
            parts.append("  - Uses wildcard (*) to match all elements")
        if "[" in query:
            parts.append("  - Uses array indexing or filtering")
        if "." in query:
            parts.append("  - Navigates nested object properties")
        if "||" in query:
            parts.append("  - Uses alternative operator (||) for fallback")
        if "?" in query:
            parts.append("  - Uses projection or conditional logic")
    elif query_type == "jsonpath":
        parts.append(f"JSONPath query: {query}")
        if query.startswith("$"):
            parts.append("  - Starts at root ($)")
        if ".." in query:
            parts.append("  - Uses recursive descent (..) to search all levels")
        if "*" in query:
            parts.append("  - Uses wildcard (*) to match all elements")
        if "[" in query:
            parts.append("  - Uses array subscript or filter expression")

    if not parts:
        parts.append(f"Simple {query_type} query")

    return "\n".join(parts)
