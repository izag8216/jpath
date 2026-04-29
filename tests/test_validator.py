"""Tests for validator module."""

from jpath.validator import validate_query, _generate_explanation


def test_validate_valid_jmespath():
    """Test validating a valid JMESPath query."""
    result = validate_query("users[*].name", "jmespath")
    assert result["valid"]
    assert result["type"] == "jmespath"
    assert result["error"] == ""
    assert result["explanation"] != ""


def test_validate_invalid_jmespath():
    """Test validating an invalid JMESPath query."""
    result = validate_query("[invalid", "jmespath")
    assert not result["valid"]
    assert result["error"] != ""


def test_validate_valid_jsonpath():
    """Test validating a valid JSONPath query."""
    result = validate_query("$.users[*].name", "jsonpath")
    assert result["valid"]
    assert result["type"] == "jsonpath"


def test_validate_invalid_jsonpath():
    """Test validating an invalid JSONPath query."""
    result = validate_query("$[invalid", "jsonpath")
    assert not result["valid"]
    assert result["error"] != ""


def test_validate_unknown_type():
    """Test validating with unknown query type."""
    result = validate_query("test", "unknown")
    assert not result["valid"]
    assert "Unknown query type" in result["error"]


def test_explanation_jmespath_wildcard():
    """Test explanation includes wildcard note."""
    explanation = _generate_explanation("users[*].name", "jmespath")
    assert "wildcard" in explanation.lower()


def test_explanation_jmespath_dot():
    """Test explanation includes navigation note."""
    explanation = _generate_explanation("users.name", "jmespath")
    assert "nested" in explanation.lower()


def test_explanation_jsonpath_recursive():
    """Test explanation includes recursive descent note."""
    explanation = _generate_explanation("$..value", "jsonpath")
    assert "recursive" in explanation.lower()


def test_explanation_jsonpath_root():
    """Test explanation includes root note."""
    explanation = _generate_explanation("$.users", "jsonpath")
    assert "root" in explanation.lower()
