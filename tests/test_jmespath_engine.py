"""Tests for JMESPath engine."""

import pytest
from jpath.jmespath_engine import execute_jmespath, validate_jmespath, JMESPathError


def test_simple_field(sample_json):
    """Test extracting a simple field."""
    result = execute_jmespath(sample_json, "metadata.total")
    assert result == 3


def test_array_access(sample_json):
    """Test array element access."""
    result = execute_jmespath(sample_json, "users[0].name")
    assert result == "Alice"


def test_array_slice(sample_json):
    """Test array slicing."""
    result = execute_jmespath(sample_json, "users[:2].name")
    assert result == ["Alice", "Bob"]


def test_wildcard(sample_json):
    """Test wildcard projection."""
    result = execute_jmespath(sample_json, "users[*].email")
    assert result == ["alice@example.com", "bob@example.com", "charlie@example.com"]


def test_filter_expression(sample_json):
    """Test filter expression."""
    result = execute_jmespath(sample_json, "users[?active==`true`].name")
    assert result == ["Alice", "Charlie"]


def test_multiselect(sample_json):
    """Test multiselect hash."""
    result = execute_jmespath(sample_json, "users[0].{name: name, email: email}")
    assert result == {"name": "Alice", "email": "alice@example.com"}


def test_invalid_query():
    """Test error on invalid query."""
    with pytest.raises(JMESPathError, match="Invalid JMESPath query"):
        execute_jmespath({}, "[invalid")


def test_validate_valid():
    """Test validation of valid query."""
    is_valid, error = validate_jmespath("users[*].name")
    assert is_valid
    assert error == ""


def test_validate_invalid():
    """Test validation of invalid query."""
    is_valid, error = validate_jmespath("[invalid")
    assert not is_valid
    assert error != ""


def test_nested_object(nested_json):
    """Test nested object access."""
    result = execute_jmespath(nested_json, "level1.level2.level3.value")
    assert result == "deep"


def test_empty_object(empty_json):
    """Test query on empty object."""
    result = execute_jmespath(empty_json, "missing")
    assert result is None
