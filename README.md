# jpath

<p align="center">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" width="100%" height="200">
    <defs>
      <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#1a1a2e;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#16213e;stop-opacity:1" />
      </linearGradient>
      <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#0f3460;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#533483;stop-opacity:1" />
      </linearGradient>
      <filter id="glow">
        <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
        <feMerge>
          <feMergeNode in="coloredBlur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>
    <rect width="800" height="200" fill="url(#bg)" rx="12"/>
    <!-- JSON tree structure -->
    <g opacity="0.15">
      <circle cx="100" cy="100" r="4" fill="#e94560"/>
      <circle cx="200" cy="60" r="4" fill="#e94560"/>
      <circle cx="200" cy="140" r="4" fill="#e94560"/>
      <circle cx="300" cy="40" r="4" fill="#e94560"/>
      <circle cx="300" cy="80" r="4" fill="#e94560"/>
      <circle cx="300" cy="160" r="4" fill="#e94560"/>
      <line x1="100" y1="100" x2="200" y2="60" stroke="#e94560" stroke-width="1"/>
      <line x1="100" y1="100" x2="200" y2="140" stroke="#e94560" stroke-width="1"/>
      <line x1="200" y1="60" x2="300" y2="40" stroke="#e94560" stroke-width="1"/>
      <line x1="200" y1="60" x2="300" y2="80" stroke="#e94560" stroke-width="1"/>
      <line x1="200" y1="140" x2="300" y2="160" stroke="#e94560" stroke-width="1"/>
    </g>
    <!-- Magnifying glass -->
    <g transform="translate(580, 70)" filter="url(#glow)">
      <circle cx="30" cy="30" r="28" fill="none" stroke="#e94560" stroke-width="4"/>
      <line x1="50" y1="50" x2="75" y2="75" stroke="#e94560" stroke-width="6" stroke-linecap="round"/>
      <path d="M 20 25 L 25 20 L 35 30 L 30 35 Z" fill="#e94560" opacity="0.8"/>
    </g>
    <!-- Highlighted path -->
    <g transform="translate(580, 70)">
      <circle cx="30" cy="30" r="12" fill="#e94560" opacity="0.3"/>
      <text x="30" y="34" text-anchor="middle" font-family="monospace" font-size="14" fill="#ffffff" font-weight="bold">$</text>
    </g>
    <!-- Title -->
    <text x="400" y="90" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="56" font-weight="800" fill="#ffffff" letter-spacing="-1">jpath</text>
    <!-- Description -->
    <text x="400" y="130" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="22" fill="#a0a0b0" letter-spacing="0.5">JSON Path Query Tool</text>
    <!-- Subtitle -->
    <text x="400" y="160" text-anchor="middle" font-family="monospace" font-size="14" fill="#6c63ff">JMESPath  •  JSONPath  •  CLI</text>
    <!-- Decorative brackets -->
    <text x="180" y="95" font-family="monospace" font-size="48" fill="#6c63ff" opacity="0.6">{</text>
    <text x="620" y="95" font-family="monospace" font-size="48" fill="#6c63ff" opacity="0.6">}</text>
  </svg>
</p>

[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg?style=flat-square)](https://pypi.org/project/jpath/)
[![Python versions](https://img.shields.io/badge/python-3.9%2B-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-76%20passing-brightgreen.svg?style=flat-square)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-89%25-brightgreen.svg?style=flat-square)](tests/)

**Query JSON files from the command line using JMESPath or JSONPath syntax.**

No need to learn `jq`'s domain-specific language. Use the query syntax you already know from AWS SDKs, API testing, and web development.

## Installation

```bash
# From PyPI
pip install jpath

# From source
git clone https://github.com/izag8216/jpath.git
cd jpath
pip install -e .

# With dev dependencies
pip install -e ".[dev]"
```

## Quick Start

```bash
# Query a JSON file with JMESPath
jpath query "users[*].name" data.json

# Query with JSONPath syntax
jpath query "$.users[*].email" data.json --type jsonpath

# Pipe from stdin
cat data.json | jpath query "metadata.total"

# Search with JSONPath (shorthand)
jpath search "$..host" config.json

# Validate a query before running it
jpath validate "users[?active==\`true\`].name" --explain

# Infer JSON Schema from data
jpath schema data.json --output schema.json
```

## Features

| Feature | Description |
|---------|-------------|
| **JMESPath queries** | Full JMESPath support with wildcards, filters, functions, multiselect |
| **JSONPath queries** | Standard JSONPath with recursive descent, filter expressions, array slices |
| **Query validation** | Check syntax before execution with human-readable explanations |
| **Schema inference** | Auto-generate JSON Schema from sample data |
| **Multiple output formats** | JSON (pretty/compact), CSV, flat text |
| **Stdin support** | Pipe from `curl`, `cat`, `jq`, or any command |
| **Zero config** | Sensible defaults, works out of the box |

## Commands

### `jpath query`

Execute a query against a JSON file.

```bash
jpath query QUERY [FILE] [OPTIONS]

Arguments:
  QUERY     The JMESPath or JSONPath query string
  FILE      Path to JSON file (reads from stdin if omitted)

Options:
  --type TEXT       Query type: jmespath or jsonpath [default: jmespath]
  --format TEXT     Output format: json, json-compact, csv, text [default: json]
```

**Examples:**

```bash
# Extract all user names
jpath query "users[*].name" data.json

# Filter active users
jpath query "users[?active==\`true\`].{name: name, email: email}" data.json

# JSONPath recursive search
jpath query "$..host" config.json --type jsonpath

# CSV output for spreadsheets
jpath query "users[*].{name: name, age: age}" data.json --format csv
```

### `jpath search`

Shorthand for JSONPath queries.

```bash
jpath search QUERY [FILE] [OPTIONS]

Arguments:
  QUERY     The JSONPath query string
  FILE      Path to JSON file (reads from stdin if omitted)

Options:
  --format TEXT     Output format: json, json-compact, csv, text [default: csv]
```

**Examples:**

```bash
# Find all hosts in config
jpath search "$.database..host" config.json

# Extract nested values
jpath search "$.users[*].contact.email" data.json
```

### `jpath validate`

Validate query syntax without executing.

```bash
jpath validate QUERY [OPTIONS]

Arguments:
  QUERY     Query string to validate

Options:
  --type TEXT       Query type: jmespath or jsonpath [default: jmespath]
  --explain         Show explanation of what the query does
```

**Examples:**

```bash
# Check if query is valid
jpath validate "users[*].name"

# Get explanation of query behavior
jpath validate "users[?age > \`25\`]" --explain

# Validate JSONPath
jpath validate "$.users[*].name" --type jsonpath
```

### `jpath schema`

Infer JSON Schema from data.

```bash
jpath schema [FILE] [OPTIONS]

Arguments:
  FILE      Path to JSON file (reads from stdin if omitted)

Options:
  --path TEXT       JMESPath to focus schema inference on a subset
  --output TEXT     Write schema to file instead of stdout
```

**Examples:**

```bash
# Generate schema from entire file
jpath schema data.json

# Focus on a specific path
jpath schema data.json --path "users[0]"

# Save to file
jpath schema data.json --output schema.json
```

## Output Formats

| Format | Description | Best for |
|--------|-------------|----------|
| `json` | Pretty-printed JSON (2-space indent) | Human reading |
| `json-compact` | Minified JSON | Piping to other tools |
| `csv` | Comma-separated values | Spreadsheets, data analysis |
| `text` | One value per line | Grep, line processing |

## JMESPath Quick Reference

```
users[*].name                  # All user names
users[0].email                 # First user's email
users[:2]                      # First two users
users[?active==`true`]         # Filter active users
users[?age > `25`].name        # Filter by age
users[0].{name: name, email}   # Select specific fields
metadata || default            # Fallback value
length(users)                  # Built-in functions
```

## JSONPath Quick Reference

```
$                              # Root element
$.users                        # Users array
$.users[0].name                # First user's name
$.users[*].email               # All emails
$.users[*].name                # All names
$..host                        # Recursive: all hosts
$.users[?(@.active == true)]   # Filter active users
$.users[-1]                    # Last user
```

## API Reference

### Python API

```python
from jpath.parser import load_json
from jpath.jmespath_engine import execute_jmespath
from jpath.jsonpath_engine import execute_jsonpath
from jpath.schema import infer_schema
from jpath.validator import validate_query
from jpath.formatter import format_output

# Load JSON
data = load_json("data.json")

# Execute queries
result = execute_jmespath(data, "users[*].name")
result = execute_jsonpath(data, "$.users[*].name")

# Validate queries
is_valid, error = validate_query("users[*].name", "jmespath")

# Infer schema
schema = infer_schema(data)

# Format output
output = format_output(result, "csv")
```

## Project Structure

```
jpath/
  src/jpath/
    __init__.py           # Package version
    __main__.py           # python -m jpath entry
    cli.py                # Click CLI commands
    parser.py             # JSON file/stdin loading
    jmespath_engine.py    # JMESPath query execution
    jsonpath_engine.py    # JSONPath query execution
    validator.py          # Query validation + explanation
    schema.py             # JSON Schema inference
    formatter.py          # Output formatting
  tests/                  # Test suite (89% coverage)
  examples/basic/         # Sample data and queries
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, coding standards, and PR process.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Third-Party Licenses

See [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) for dependency licenses.
