# FQL — Flexible Query Layer

FQL (Flexible Query Layer) is a lightweight Python extension that enables natural language querying over structured datasets such as CSV files and SQLite databases.

Instead of writing raw SQL, users can ask questions in plain English. FQL parses intent, generates structured SQL, executes it safely, and returns results.

Designed for small to medium datasets, educational use, and rapid prototyping.

---

## Why FQL?

- Removes SQL friction for non-technical users  
- Works locally on CSV or SQLite  
- Easy integration with Flask applications  
- Lightweight and modular architecture  
- Designed for transparency (inspect generated SQL)  

This project demonstrates:

- Query parsing  
- NLP → SQL translation  
- Dynamic database binding  
- Systems design and modular Python packaging  

---

## Installation

### Install from PyPI

bash
pip install fql
Install Locally
git clone https://github.com/yourusername/fql.git
cd fql
pip install -e .
Quick Start
1. Query a CSV File
from fql import FQL

engine = FQL(
    db_location="data.csv",
    is_flask=False
)

result = engine.query("Show me the top 5 highest revenue entries")
print(result)
2. Use with SQLite
from fql import FQL

engine = FQL(
    db_location="database.db",
    is_flask=False
)

engine.query("What is the average age grouped by department?")
3. Flask Integration
from fql import FQL

engine = FQL(
    db_location="database.db",
    is_flask=True
)
Configuration
Parameter	Type	Description
db_location	str	Path to CSV or SQLite database
is_flask	bool	Enables Flask-specific behavior
Architecture Overview
Natural Language Input
        ↓
Intent Parsing
        ↓
Query Builder
        ↓
SQL Generation
        ↓
Execution Engine
        ↓
Result Formatter
Example Queries

"Show the first 10 rows"

"Count total entries"

"Average salary by department"

"Sort by revenue descending"

"Filter where age > 30"

Project Structure
fql/
│
├── core/
│   ├── parser.py
│   ├── query_builder.py
│   ├── executor.py
│
├── config.py
├── engine.py
└── utils.py
Safety Considerations

Generated SQL is parameterized

No direct raw user SQL execution

Designed for local/offline use

Limitations

Not optimized for very large datasets

Relies on rule-based or lightweight NLP parsing

Complex nested queries may not be supported

Roadmap

Embedding-based semantic parsing

Query caching

Schema introspection auto-learning

Visualization layer

CLI support

Web UI dashboard

Contributing

Pull requests are welcome.

License

MIT License


---

# `DOCUMENTATION.md`

```markdown
# FQL Technical Documentation

## 1. System Design

FQL follows a modular pipeline architecture:

1. Input Processing  
2. Intent Detection  
3. Query Structuring  
4. SQL Generation  
5. Execution  
6. Output Formatting  

Each stage is isolated for extensibility.

---

## 2. Core Components

### FQL Engine

Central interface for users.

Responsibilities:

- Load dataset  
- Manage configuration  
- Route queries  
- Handle output formatting  

---

### Parser Module

Converts natural language into structured intent.

Example output:

```json
{
  "operation": "aggregate",
  "function": "average",
  "column": "salary",
  "group_by": "department"
}
Query Builder

Transforms structured intent into valid SQL.

Example:

SELECT department, AVG(salary)
FROM table
GROUP BY department;
Executor

Handles:

SQLite execution

CSV → temporary SQLite conversion (if applicable)

Safe parameter injection

Result retrieval

3. CSV Handling

When a CSV is provided:

File is loaded

Converted into an in-memory SQLite table

Queries executed against the temporary schema

This maintains SQL consistency across input types.

4. Flask Mode

If ISFLASK=True:

Engine avoids reinitializing connections

Designed for request lifecycle management

Optimized for repeated queries

5. Error Handling

FQL handles:

Invalid column names

Unsupported operations

Malformed natural language

Execution errors

Errors return structured responses.

6. Extensibility

You can extend FQL by:

Adding new NLP intent rules

Integrating transformer-based parsing

Adding a PostgreSQL backend

Adding query plan inspection

7. Performance Considerations

Best suited for:

< 1M rows

Local development

Classroom environments

Rapid prototyping

For large-scale systems, consider integrating a dedicated semantic parser with optimized SQL engines.

8. Example Flow

Input:

Show average GPA grouped by major

Parsed Intent:

aggregate → avg(GPA) → group_by major

Generated SQL:

SELECT major, AVG(GPA)
FROM dataset
GROUP BY major;

Result:

Returned as a pandas DataFrame.