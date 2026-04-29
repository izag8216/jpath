"""Tests for schema inference module."""

from jpath.schema import infer_schema


def test_infer_simple_object():
    """Test schema inference for simple object."""
    data = {"name": "Alice", "age": 30}
    schema = infer_schema(data)
    assert schema["type"] == "object"
    assert "name" in schema["properties"]
    assert "age" in schema["properties"]
    assert schema["properties"]["name"]["type"] == "string"
    assert schema["properties"]["age"]["type"] == "integer"


def test_infer_nested_object():
    """Test schema inference for nested object."""
    data = {"user": {"name": "Alice", "email": "alice@example.com"}}
    schema = infer_schema(data)
    assert schema["properties"]["user"]["type"] == "object"
    assert "name" in schema["properties"]["user"]["properties"]


def test_infer_array_of_objects():
    """Test schema inference for array of objects."""
    data = [
        {"id": 1, "name": "first"},
        {"id": 2, "name": "second"},
    ]
    schema = infer_schema(data)
    assert schema["type"] == "array"
    assert "items" in schema
    assert schema["items"]["properties"]["id"]["type"] == "integer"


def test_infer_array_of_primitives():
    """Test schema inference for array of primitives."""
    data = [1, 2, 3, 4, 5]
    schema = infer_schema(data)
    assert schema["type"] == "array"
    assert schema["items"]["type"] == "integer"


def test_infer_empty_object():
    """Test schema inference for empty object."""
    data = {}
    schema = infer_schema(data)
    assert schema["type"] == "object"
    assert "required" not in schema


def test_infer_with_path(sample_json):
    """Test schema inference focused on a path."""
    schema = infer_schema(sample_json, path="users[0]")
    assert schema["type"] == "object"
    assert "name" in schema["properties"]
    assert "email" in schema["properties"]


def test_infer_boolean_type():
    """Test boolean type inference."""
    data = {"active": True}
    schema = infer_schema(data)
    assert schema["properties"]["active"]["type"] == "boolean"


def test_infer_null_type():
    """Test null type inference."""
    data = {"value": None}
    schema = infer_schema(data)
    assert schema["properties"]["value"]["type"] == "null"


def test_infer_float_type():
    """Test float type inference."""
    data = {"price": 19.99}
    schema = infer_schema(data)
    assert schema["properties"]["price"]["type"] == "number"


def test_schema_has_draft():
    """Test schema includes draft-07 reference."""
    data = {"key": "value"}
    schema = infer_schema(data)
    assert "draft-07" in schema["$schema"]
