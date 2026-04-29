"""Tests for CLI commands."""

import json
from click.testing import CliRunner
from jpath.cli import main


def test_query_jmespath_file(sample_json_file):
    """Test JMESPath query on file."""
    runner = CliRunner()
    result = runner.invoke(main, ["query", "metadata.total", sample_json_file])
    assert result.exit_code == 0
    assert "3" in result.output


def test_query_jsonpath_file(sample_json_file):
    """Test JSONPath query on file."""
    runner = CliRunner()
    result = runner.invoke(main, ["query", "$.metadata.total", sample_json_file, "--type", "jsonpath"])
    assert result.exit_code == 0
    assert "3" in result.output


def test_query_stdin(sample_json):
    """Test query from stdin."""
    runner = CliRunner()
    result = runner.invoke(main, ["query", "users[0].name"], input=json.dumps(sample_json))
    assert result.exit_code == 0
    assert "Alice" in result.output


def test_query_invalid_file():
    """Test query on nonexistent file."""
    runner = CliRunner()
    result = runner.invoke(main, ["query", "test", "nonexistent.json"])
    assert result.exit_code != 0
    assert "Error" in result.output


def test_query_invalid_jmespath(sample_json_file):
    """Test query with invalid JMESPath."""
    runner = CliRunner()
    result = runner.invoke(main, ["query", "[invalid", sample_json_file])
    assert result.exit_code != 0
    assert "Error" in result.output


def test_query_output_format_text(sample_json_file):
    """Test query with text output format."""
    runner = CliRunner()
    result = runner.invoke(main, ["query", "users[*].name", sample_json_file, "--format", "text"])
    assert result.exit_code == 0
    assert "Alice" in result.output


def test_query_output_format_csv(sample_json_file):
    """Test query with CSV output format."""
    runner = CliRunner()
    result = runner.invoke(main, ["query", "users[*].{name: name, email: email}", sample_json_file, "--format", "csv"])
    assert result.exit_code == 0
    assert "Alice" in result.output


def test_search_jsonpath(sample_json_file):
    """Test search command with JSONPath."""
    runner = CliRunner()
    result = runner.invoke(main, ["search", "$.users[*].email", sample_json_file])
    assert result.exit_code == 0
    assert "alice@example.com" in result.output


def test_search_invalid_jsonpath(sample_json_file):
    """Test search with invalid JSONPath."""
    runner = CliRunner()
    result = runner.invoke(main, ["search", "$[invalid", sample_json_file])
    assert result.exit_code != 0


def test_validate_valid():
    """Test validate command with valid query."""
    runner = CliRunner()
    result = runner.invoke(main, ["validate", "users[*].name"])
    assert result.exit_code == 0
    assert "Valid query" in result.output


def test_validate_invalid():
    """Test validate command with invalid query."""
    runner = CliRunner()
    result = runner.invoke(main, ["validate", "[invalid"])
    assert result.exit_code != 0
    assert "Invalid query" in result.output


def test_validate_with_explain():
    """Test validate command with explain flag."""
    runner = CliRunner()
    result = runner.invoke(main, ["validate", "users[*].name", "--explain"])
    assert result.exit_code == 0
    assert "Valid query" in result.output
    assert "wildcard" in result.output.lower()


def test_validate_jsonpath():
    """Test validate command with JSONPath."""
    runner = CliRunner()
    result = runner.invoke(main, ["validate", "$.users[*].name", "--type", "jsonpath"])
    assert result.exit_code == 0
    assert "Valid query" in result.output


def test_schema_inference(sample_json_file):
    """Test schema inference command."""
    runner = CliRunner()
    result = runner.invoke(main, ["schema", sample_json_file])
    assert result.exit_code == 0
    assert "json-schema.org" in result.output
    assert "users" in result.output


def test_schema_with_path(sample_json_file):
    """Test schema inference with focus path."""
    runner = CliRunner()
    result = runner.invoke(main, ["schema", sample_json_file, "--path", "users[0]"])
    assert result.exit_code == 0
    assert "name" in result.output


def test_schema_output_file(sample_json_file, tmp_path):
    """Test schema inference with output file."""
    runner = CliRunner()
    output_file = tmp_path / "schema.json"
    result = runner.invoke(main, ["schema", sample_json_file, "--output", str(output_file)])
    assert result.exit_code == 0
    assert "Schema written to" in result.output
    assert output_file.exists()


def test_version():
    """Test version flag."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0


def test_help():
    """Test help flag."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "jpath" in result.output.lower()
