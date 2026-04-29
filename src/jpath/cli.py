"""CLI entry point with click commands."""

import click
import sys
from jpath.parser import load_json, JSONLoadError
from jpath.jmespath_engine import execute_jmespath, JMESPathError
from jpath.jsonpath_engine import execute_jsonpath, JSONPathError
from jpath.validator import validate_query
from jpath.schema import infer_schema
from jpath.formatter import format_output


@click.group()
@click.version_option()
def main():
    """jpath -- JSON Path Query Tool.

    Query JSON files using JMESPath or JSONPath syntax from the command line.
    """
    pass


@main.command()
@click.argument("query")
@click.argument("file", required=False)
@click.option("--type", "query_type", default="jmespath", help="Query type: jmespath or jsonpath")
@click.option("--format", "output_format", default="json", help="Output format: json, json-compact, csv, text")
def query(query, file, query_type, output_format):
    """Execute a query against a JSON file.

    QUERY: The JMESPath or JSONPath query string.
    FILE: Path to JSON file (reads from stdin if omitted).
    """
    try:
        data = load_json(file)
    except JSONLoadError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    try:
        if query_type == "jmespath":
            result = execute_jmespath(data, query)
        elif query_type == "jsonpath":
            result = execute_jsonpath(data, query)
        else:
            click.echo(f"Error: Unknown query type '{query_type}'. Use 'jmespath' or 'jsonpath'.", err=True)
            sys.exit(1)
    except (JMESPathError, JSONPathError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    try:
        click.echo(format_output(result, output_format))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("query")
@click.argument("file", required=False)
@click.option("--format", "output_format", default="csv", help="Output format: json, json-compact, csv, text")
def search(query, file, output_format):
    """Search JSON using JSONPath syntax.

    QUERY: The JSONPath query string.
    FILE: Path to JSON file (reads from stdin if omitted).
    """
    try:
        data = load_json(file)
    except JSONLoadError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    try:
        result = execute_jsonpath(data, query)
    except JSONPathError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    try:
        click.echo(format_output(result, output_format))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("query")
@click.option("--type", "query_type", default="jmespath", help="Query type: jmespath or jsonpath")
@click.option("--explain", is_flag=True, help="Show explanation of what the query does")
def validate(query, query_type, explain):
    """Validate a query syntax.

    QUERY: Query string to validate.
    """
    query_str = query

    if not query_str:
        click.echo("Error: Provide a query string.", err=True)
        sys.exit(1)

    result = validate_query(query_str, query_type)

    if result["valid"]:
        click.echo("Valid query.")
        if explain and result["explanation"]:
            click.echo()
            click.echo(result["explanation"])
    else:
        click.echo(f"Invalid query: {result['error']}", err=True)
        sys.exit(1)


@main.command()
@click.argument("file", required=False)
@click.option("--path", "focus_path", help="JMESPath to focus schema inference on a subset")
@click.option("--output", "output_file", help="Write schema to file instead of stdout")
def schema(file, focus_path, output_file):
    """Infer JSON Schema from data.

    FILE: Path to JSON file (reads from stdin if omitted).
    """
    try:
        data = load_json(file)
    except JSONLoadError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    try:
        result = infer_schema(data, path=focus_path)
    except Exception as e:
        click.echo(f"Error inferring schema: {e}", err=True)
        sys.exit(1)

    output = format_output(result, "json")

    if output_file:
        from pathlib import Path
        Path(output_file).write_text(output, encoding="utf-8")
        click.echo(f"Schema written to {output_file}")
    else:
        click.echo(output)


if __name__ == "__main__":
    main()
