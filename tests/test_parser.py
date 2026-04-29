"""Tests for JSON parser module."""

import json
import pytest
from io import StringIO
import sys
from jpath.parser import load_json, JSONLoadError


def test_load_from_file(sample_json_file, sample_json):
    """Test loading JSON from file."""
    result = load_json(sample_json_file)
    assert result == sample_json


def test_load_from_stdin(sample_json, monkeypatch):
    """Test loading JSON from stdin."""
    monkeypatch.setattr(sys, "stdin", StringIO(json.dumps(sample_json)))
    result = load_json()
    assert result == sample_json


def test_load_file_not_found():
    """Test error when file doesn't exist."""
    with pytest.raises(JSONLoadError, match="File not found"):
        load_json("nonexistent.json")


def test_load_invalid_json(tmp_path):
    """Test error when JSON is invalid."""
    file_path = tmp_path / "invalid.json"
    file_path.write_text("{invalid json}")
    with pytest.raises(JSONLoadError, match="Invalid JSON"):
        load_json(str(file_path))


def test_load_empty_stdin(monkeypatch):
    """Test error when stdin is empty."""
    monkeypatch.setattr(sys, "stdin", StringIO(""))
    with pytest.raises(JSONLoadError, match="No input provided"):
        load_json()


def test_load_not_a_file(tmp_path):
    """Test error when path is a directory."""
    dir_path = tmp_path / "dir"
    dir_path.mkdir()
    with pytest.raises(JSONLoadError, match="Not a file"):
        load_json(str(dir_path))
