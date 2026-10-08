# AI Data Analyst

A Streamlit application that combines a Gemini-powered conversational assistant
with analysis of user-uploaded files or database tables. General conversation
and data analysis use separate response paths: the app only creates SQL-backed
metrics or charts when the user asks about loaded data or explicitly requests a
visualization.

## Features

- Conversational chat for greetings, jokes, general questions, and follow-up
  conversation.
- Data analysis from uploaded files or a database connection.
- SQL-backed answers to direct questions about loaded data.
- Optional KPI cards and charts for requests to create a dashboard or visual
  summary.
- SQL and returned data are available in the interface so analysis results can
  be checked.
- SQLite upload handling works on Windows, macOS, and Linux.

## Requirements

- Python 3.10 or newer.
- A Gemini API key for chat and data-analysis responses.
- A supported database driver when connecting to a database. The requirements
  include `psycopg2-binary` for PostgreSQL.

## Setup

### Windows PowerShell

From the project folder:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell blocks script activation, you can use the environment's Python
directly instead:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

## Configure Gemini

Open `.env` and replace the placeholder with your Gemini API key:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
```

Optional model settings:

```dotenv
GEMINI_MODEL=gemini-3.8-flash
GEMINI_FALLBACK_MODEL=
```

`GEMINI_FALLBACK_MODEL` can contain a comma-separated list of alternate model
names. The app retries temporary rate-limit or service-unavailable responses.
Do not commit `.env` or share its API key.

## Run the application

With the virtual environment activated:

```bash
streamlit run app.py
```

On Windows, if the `streamlit` command is not on `PATH`, run:

```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

Streamlit prints the local URL, usually `http://localhost:8501`. Stop the
server with `Ctrl+C` in the terminal where it is running.

## Use the chat

1. Enter a normal message in the chat box to start a conversation. Examples:
   `hello`, `tell me a joke`, or `explain what a data analyst does`.
2. Load data only when you want to ask questions about it.
3. Ask a specific data question, such as `How many orders are in the file?`.
4. Request a chart or dashboard explicitly when you want visualizations.
5. Review the displayed answer and its **Exact data used to answer** or
   **SQL / data** section to inspect the executed SQL and returned rows.

General requests are routed to conversational chat and do not generate
dashboards. Data requests use the loaded table schema to generate DuckDB
`SELECT`/`WITH` queries. The application executes those queries locally against
the loaded data and displays the actual returned values. A separate answer step
uses the executed results to phrase a concise response. If analysis SQL fails,
the app makes one correction attempt.

## Load data

Use the sidebar's **Data source** selector.

### Upload files

The uploader accepts:

- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)
- JSON (`.json`)
- Parquet (`.parquet`)
- SQLite (`.db`, `.sqlite`, `.sqlite3`)

For Excel, every workbook sheet is loaded as its own table. For SQLite files,
each table is loaded. Table names are normalized to lowercase names with
underscores.

### Connect to a database

Choose **Database URL**, enter a SQLAlchemy connection URL, then select
**Connect**. For example, a PostgreSQL URL has this form:

```text
postgresql+psycopg2://username:password@hostname:5432/database_name
```

Use a database account with read-only permissions. The application imports
tables into memory for analysis; it does not write query results back to the
connected database.

## Data limits and accuracy

- Each table/file is limited to the first **200,000 rows** read by the app.
- For each message, the Gemini model receives the user's request and table
  names/column names/types to decide whether it is chat or data analysis.
- For data analysis, the generated query is checked and executed locally.
  Returned query results are then sent to Gemini to phrase the answer. Do not
  upload personal, health, financial, or other sensitive data unless you are
  authorized to use the configured Gemini service for that data.
- A result cannot be more complete than the data loaded into the app. Check the
  file/table row counts in the sidebar and the displayed SQL/data before relying
  on an answer.
- The model may still misunderstand a question or produce an incorrect query.
  Verify important results against the source data.

## Project files

```text
app.py             Streamlit UI, upload/connect logic, chat routing and analysis
check_models.py    Optional helper to test Gemini model availability
requirements.txt   Python dependencies
.env.example       Gemini configuration template
README.md          Setup and usage instructions
```

## Troubleshooting

### Gemini API key not found

Confirm `.env` is in the same folder as `app.py`, contains `GEMINI_API_KEY`,
and restart Streamlit after changing it.

### Package or command not found

Make sure the project virtual environment is activated and dependencies were
installed with `python -m pip install -r requirements.txt`. On Windows, use
`.\venv\Scripts\python.exe -m streamlit run app.py` if `streamlit` is not
recognized as a command.

### Database connection fails

Check the SQLAlchemy URL, network access, database name, credentials, and
installed database driver. Prefer a read-only database account.

### Analysis cannot answer a question

Check the loaded table and column names in the sidebar and preview. Rephrase
the question to refer to actual column names, and inspect the SQL/data shown
with the result.
