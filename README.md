# Data Querying & Analysis — GenAI Portfolio Project
Hey — I built this little GenAI demo to show how I turn plain English questions into safe SQL and explain the results.

What it does (in plain terms)
- You type a question like "Which customers spent the most in March?"
- The app uses a model (or a simple fallback) to build a safe SQLite `SELECT` query
- It runs the query against a small sample DB and shows a short, readable answer

Why I made it
- To demonstrate prompt design, safe model/database integration, and a short demo you can run locally in under a minute.

Quick demo (run locally)
1. Create a virtual environment and activate it (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install the deps:

```powershell
pip install -r requirements.txt
```

3. Create the sample DB (this will create `projects/Data Querying/example.db`):

```powershell
python projects\"Data Querying"\create_example_db.py
```

4. (Optional) If you want the model to generate SQL, set your OpenAI key:

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

5. Run the app:

```powershell
python projects\"Data Querying"\app.py
```

6. Open http://localhost:5000 and try a few questions. The UI is already wired up — I recommend trying:
- "Which customers spent the most in March?"
- "Show total sales by product."

Screenshot / GIF
If you drop a GIF or PNG named `demo.gif` into `projects/Data Querying/assets/` it will be automatically embedded below in this README so visitors see the demo flow.

Safety notes (short)
- The app only runs read-only `SELECT` queries and blocks multiple statements. Don’t point it at production data without adding auth and audit logs.

Tests
- Run the tiny test suite:

```powershell
python -m unittest discover -s tests -v
```

If you want, I can add a GitHub Actions workflow to run the tests on every push, and I can add the GIF you mentioned inside `projects/Data Querying/assets/demo.gif`.

— [Your Name]

![Demo screenshot](projects/Data%20Querying/assets/demo.gif)
