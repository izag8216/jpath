"""Tests for formatter module."""

import json
import pytest
from jpath.formatter import format_output, _to_csv, _to_text


def test_format_json_pretty():
    """Test pretty JSON output."""
    data = {"name": "Alice", "age": 30}
    result = format_output(data, "json")
    parsed = json.loads(result)
    assert parsed == data
    assert "\n" in result


def test_format_json_compact():
    """Test compact JSON output."""
    data = {"name": "Alice", "age": 30}
    result = format_output(data, "json-compact")
    assert "\n" not in result
    assert " " not in result.replace("Alice", "")


def test_format_csv_list_of_dicts():
    """Test CSV output for list of dicts."""
    data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
    ]
    result = format_output(data, "csv")
    assert "name,age" in result
    assert "Alice,30" in result
    assert "Bob,25" in result


def test_format_csv_list_of_primitives():
    """Test CSV output for list of primitives."""
    data = ["Alice", "Bob", "Charlie"]
    result = format_output(data, "csv")
    assert "Alice" in result
    assert "Bob" in result


def test_format_text_list():
    """Test text output for list."""
    data = ["Alice", "Bob", "Charlie"]
    result = format_output(data, "text")
    lines = result.split("\n")
    assert len(lines) == 3
    assert "Alice" in lines[0]


def test_format_text_list_of_dicts():
    """Test text output for list of dicts."""
    data = [{"name": "Alice"}]
    result = format_output(data, "text")
    assert "Alice" in result


def test_format_text_scalar():
    """Test text output for scalar value."""
    result = format_output(42, "text")
    assert result == "42"


def test_format_unsupported():
    """Test error on unsupported format."""
    with pytest.raises(ValueError, match="Unsupported format"):
        format_output({}, "xml")


def test_flatten_value_dict():
    """Test flattening dict value."""
    from jpath.formatter import _flatten_value
    result = _flatten_value({"key": "value"})
    assert result == '{"key": "value"}'


def test_flatten_value_list():
    """Test flattening list value."""
    from jpath.formatter import _flatten_value
    result = _flatten_value([1, 2, 3])
    assert result == "[1, 2, 3]"


def test_flatten_value_none():
    """Test flattening None value."""
    from jpath.formatter import _flatten_value
    result = _flatten_value(None)
    assert result == ""


def test_flatten_value_string():
    """Test flattening string value."""
    from jpath.formatter import _flatten_value
    result = _flatten_value("hello")
    assert result == "hello"
