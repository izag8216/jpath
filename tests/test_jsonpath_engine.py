"""Tests for JSONPath engine."""

import pytest
from jpath.jsonpath_engine import execute_jsonpath, validate_jsonpath, JSONPathError


def test_root_access(sample_json):
    """Test accessing root element."""
    result = execute_jsonpath(sample_json, "$")
    assert len(result) == 1
    assert result[0] == sample_json


def test_dot_notation(sample_json):
    """Test dot notation access."""
    result = execute_jsonpath(sample_json, "$.metadata.total")
    assert result == [3]


def test_array_index(sample_json):
    """Test array index access."""
    result = execute_jsonpath(sample_json, "$.users[0].name")
    assert result == ["Alice"]


def test_wildcard(sample_json):
    """Test wildcard access."""
    result = execute_jsonpath(sample_json, "$.users[*].name")
    assert result == ["Alice", "Bob", "Charlie"]


def test_recursive_descent(nested_json):
    """Test recursive descent."""
    result = execute_jsonpath(nested_json, "$..value")
    assert result == ["deep"]


def test_filter_expression(sample_json):
    """Test filter expression."""
    result = execute_jsonpath(sample_json, "$.users[?(@.active == true)].name")
    assert "Alice" in result
    assert "Charlie" in result


def test_invalid_query():
    """Test error on invalid query."""
    with pytest.raises(JSONPathError, match="Invalid JSONPath query"):
        execute_jsonpath({}, "$[invalid")


def test_validate_valid():
    """Test validation of valid query."""
    is_valid, error = validate_jsonpath("$.users[*].name")
    assert is_valid
    assert error == ""


def test_validate_invalid():
    """Test validation of invalid query."""
    is_valid, error = validate_jsonpath("$[invalid")
    assert not is_valid
    assert error != ""


def test_array_root(array_json):
    """Test query on array root."""
    result = execute_jsonpath(array_json, "$[*].name")
    assert result == ["first", "second", "third"]
