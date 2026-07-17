## Data Querying & Analysis — personal demo

Hi — I'm a data engineer and I built this compact demo to show how I convert plain-English questions into safe SQL, execute them against a local SQLite database, and produce concise, human-readable answers using a generative model.

What this project demonstrates
- Natural-language → SQL generation (OpenAI-backed, with deterministic fallbacks).
- Safe, read-only execution on a local `example.db` SQLite database.
- Optional model-based summarization of query results for clearer answers.

Primary files
- `app.py`: Flask app and the main pipeline (query generation, validation, execution, summarization).
- `create_example_db.py`: script to create and seed `example.db` with `customer` and `sales` tables.
- `templates/index.html`: minimal UI to enter questions and view answers.

Sample schema
- `customer(customer_id, name, email, join_date)`
- `sales(sale_id, customer_id, product, amount, sale_date)`

Quick start (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies from the repository root:

```powershell
pip install -r requirements.txt
```

3. Create the example database (from this folder):

```powershell
python create_example_db.py
```

4. (Optional) Set your OpenAI key to enable model-driven SQL generation and summarization:

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

Running the demo

```powershell
# from repo root
python projects\"Data Querying"\app.py

# or from this folder
python app.py
```

Open http://localhost:5000 and try questions like:
- "Which customers spent the most in March?"
- "Show total sales by product for 2023."

Safety & limitations
- The app enforces read-only `SELECT` queries and blocks mutation tokens (`insert`, `update`, `delete`, `drop`, `alter`, `create`, `pragma`).
- Multiple-statement queries and overly long inputs are rejected; validation lives in `run_query()` inside `app.py`.
- This demo has no authentication or audit logging — do not use it against production data without hardening.

How I present this project
- I demonstrate the full flow: question → generated SQL (or fallback) → query results → concise model summary.
- I highlight the prompt design, SQL validation, and fallback logic when the API key is missing.

Next steps I can do for you
- Add an embedded `demo.gif` or screenshot to this README.
- Add a GitHub Actions workflow to run tests and format checks.
- Extend the schema and add example queries and expected outputs in a separate `examples.md` file.

If you'd like a more formal or shorter description suitable for a portfolio page, tell me the tone and I'll adapt the README.
