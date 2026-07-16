# Data Querying & Analysis (GenAI)

This small demo showcases converting natural-language questions into SQL, running them against a sample SQLite database, and using a generative model to interpret results into concise answers.

What this demo shows
- NL  SQL: prompts generate SQLite queries from a simple schema.
- Execution: the generated queries run against `example.db` (SQLite).
- Interpretation: model summarizes query results and answers the original question.

Files of interest
- `app.py`  Flask app that accepts a question, generates a query, runs it, and returns an answer.
- `templates/index.html`  simple web UI to enter questions and view answers.
- `example.db`  optional sample SQLite DB (create or populate as needed).

Setup
1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies from the repository root:

```powershell
pip install -r requirements.txt
```

3. Set your OpenAI API key in the environment (required):

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

Run the demo
1. From the repository root or this folder, run:

```powershell
# from repo root
python projects\"Data Querying"\app.py

# or from this folder
python app.py
```

2. Open http://localhost:5000 and type a question like:
- "Which customers spent the most in March?"
- "Show total sales by product for 2023."

Notes & customization
- The app expects a simple schema defined in `app.py`. Replace or extend it to match your dataset.
- If you don't have `example.db`, create it and populate `customer` and `sales` tables, or modify `run_query` to point to a different DB.
- For local demos, keep `debug=True` off in production.

Presentation tips
- Record a short screencast showing the question  generated SQL  answer flow.
- Include the SQL output and a brief note on prompt design and safety checks (e.g., validate generated SQL before running on production data).

If you'd like, I can create a sample `example.db` with toy data and add a screenshot or GIF for the README.
