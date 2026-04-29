---
title: "jpath -- JSON Path Query Tool PRD"
version: 0.6.0
status: approved
project_type: CLI Tool
mode: full
---

# jpath -- JSON Path Query Tool

## Problem Statement

Querying nested JSON files from the command line requires `jq`, whose domain-specific language has a steep learning curve for occasional users. Developers who know JMESPath or JSONPath from AWS SDKs and API testing want to use those familiar query syntaxes against local JSON files without learning a new language.

## Solution Overview

jpath provides JMESPath and JSONPath query interfaces for local JSON files with intuitive CLI syntax. It supports piping input from stdin, multiple output formats (JSON, CSV, flat text), query validation with helpful error messages, and schema inference from query results.

## Architecture

### System Diagram

```
stdin/file -> JSON Parser -> Query Engine (JMESPath/JSONPath) -> Output Formatter -> stdout
                                      |
                              Query Validator/Explainer
```

### Directory Structure

```
jpath/
  pyproject.toml
  README.md
  CONTRIBUTING.md
  LICENSE
  THIRD_PARTY_LICENSES.md
  src/
    jpath/
      __init__.py
      __main__.py
      cli.py            # CLI entry point with click
      parser.py         # JSON file loading + stdin support
      jmespath_engine.py # JMESPath query execution
      jsonpath_engine.py # JSONPath query execution
      validator.py      # Query validation + explanation
      schema.py         # Schema inference from results
      formatter.py      # Output formatting (JSON, CSV, text)
  tests/
    __init__.py
    test_parser.py
    test_jmespath_engine.py
    test_jsonpath_engine.py
    test_validator.py
    test_schema.py
    test_formatter.py
    test_cli.py
    conftest.py
  examples/
    basic/
      sample.json
      queries.jmes
      queries.jsonpath
```

### Technology Choices

| Component | Choice | Rationale |
|-----------|--------|-----------|
| CLI Framework | click | Standard Python CLI, intuitive decorators |
| JMESPath | jmespath | Official Python implementation, battle-tested |
| JSONPath | jsonpath-ng | Most comprehensive JSONPath implementation |
| Testing | pytest | Standard Python testing framework |
| Coverage | pytest-cov | Coverage reporting |

### Project Type

CLI Tool

## Feature Specifications

### F1: JMESPath Query Execution

- **Input:** JSON file path or stdin + JMESPath query string
- **Output:** Query result in specified format
- **Acceptance Criteria:**
  - Supports all JMESPath expressions (wildcards, filters, functions)
  - Handles nested objects and arrays correctly
  - Returns proper error messages for invalid queries

### F2: JSONPath Query Execution

- **Input:** JSON file path or stdin + JSONPath query string
- **Output:** Query result in specified format
- **Acceptance Criteria:**
  - Supports standard JSONPath syntax ($, ., [], *, ..)
  - Handles filter expressions and array slices
  - Returns proper error messages for invalid queries

### F3: Query Validation & Explanation

- **Input:** Query string + query type (jmespath/jsonpath)
- **Output:** Validation result + human-readable explanation
- **Acceptance Criteria:**
  - Validates syntax without executing
  - Provides step-by-step explanation of what the query does
  - Highlights syntax errors with position information

### F4: Schema Inference

- **Input:** JSON file + optional path to focus on
- **Output:** JSON Schema inferred from data
- **Acceptance Criteria:**
  - Infers types, required fields, nested structures
  - Handles arrays of objects correctly
  - Outputs valid JSON Schema draft-07

### F5: Multiple Output Formats

- **Input:** Query result + format specifier
- **Output:** Formatted result
- **Acceptance Criteria:**
  - Supports JSON (pretty + compact), CSV, flat text
  - CSV output handles nested data by flattening
  - Flat text outputs one value per line

### F6: Stdin Support

- **Input:** Piped JSON from stdin
- **Output:** Query result
- **Acceptance Criteria:**
  - Auto-detects stdin when no file provided
  - Handles large inputs efficiently
  - Works with curl, cat, jq pipelines

## Testing Strategy

- **Unit Tests:** Each engine module tested independently with varied JSON structures
- **Integration Tests:** CLI end-to-end tests with file and stdin input
- **Edge Cases:** Empty JSON, deeply nested structures, invalid JSON, malformed queries
- **Coverage Target:** 80%+

## CI/CD Pipeline

GitHub Actions workflow:
1. Lint (ruff)
2. Test (pytest with coverage)
3. Build (python -m build)
4. Coverage report

## Milestones

| Milestone | Description | Effort |
|-----------|-------------|--------|
| M1 | Project scaffold + core query engines (JMESPath + JSONPath) | M |
| M2 | CLI commands (query, search, validate, schema) | M |
| M3 | Test suite (80%+ coverage) | L |
| M4 | Documentation (README, CONTRIBUTING, API docs, examples) | M |
| M5 | CI/CD, package config, license audit | S |

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| JSONPath syntax ambiguity | Medium | Use jsonpath-ng which has well-defined semantics |
| Large JSON file performance | Low | Stream parsing where possible, document limitations |
| Query explanation accuracy | Low | Focus on syntax validation, keep explanations conservative |

## Out of Scope

- JSON editing/modification (read-only queries)
- JSON Schema validation (only inference)
- GUI or web interface

## Dependency License Audit

| Dependency | License | Compatible |
|------------|---------|------------|
| click | BSD-3-Clause | Yes (MIT) |
| jmespath | MIT | Yes |
| jsonpath-ng | Apache-2.0 | Yes |
| pytest | MIT | Dev only |
| pytest-cov | MIT | Dev only |
| ruff | MIT | Dev only |
