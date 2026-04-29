"""Test fixtures for jpath tests."""

import pytest
import json
from pathlib import Path


@pytest.fixture
def sample_json():
    """Sample JSON data for testing."""
    return {
        "users": [
            {"name": "Alice", "email": "alice@example.com", "age": 30, "active": True},
            {"name": "Bob", "email": "bob@example.com", "age": 25, "active": False},
            {"name": "Charlie", "email": "charlie@example.com", "age": 35, "active": True},
        ],
        "metadata": {
            "total": 3,
            "page": 1,
            "per_page": 10,
        },
        "settings": {
            "theme": "dark",
            "notifications": True,
        },
    }


@pytest.fixture
def sample_json_file(tmp_path, sample_json):
    """Create a temporary JSON file."""
    file_path = tmp_path / "sample.json"
    file_path.write_text(json.dumps(sample_json, indent=2))
    return str(file_path)


@pytest.fixture
def nested_json():
    """Deeply nested JSON for testing."""
    return {
        "level1": {
            "level2": {
                "level3": {
                    "value": "deep",
                    "items": [1, 2, 3],
                }
            }
        }
    }


@pytest.fixture
def empty_json():
    """Empty JSON object."""
    return {}


@pytest.fixture
def array_json():
    """JSON array at root level."""
    return [
        {"id": 1, "name": "first"},
        {"id": 2, "name": "second"},
        {"id": 3, "name": "third"},
    ]
