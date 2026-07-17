import json
import os
import sqlite3
from pathlib import Path

from flask import Flask, render_template, request
from openai import OpenAI, OpenAIError

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "example.db"

app = Flask(__name__)


def ensure_sample_database() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            join_date TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product TEXT,
            amount REAL,
            sale_date TEXT,
            FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
        )
        """
    )

    customers = [
        (1, "Asha Sharma", "asha@example.com", "2023-01-15"),
        (2, "Rahul Verma", "rahul@example.com", "2022-11-03"),
        (3, "Priya Singh", "priya@example.com", "2023-03-22"),
    ]
    sales = [
        (1, 1, "Laptop", 1200.0, "2023-03-05"),
        (2, 2, "Monitor", 300.0, "2023-03-12"),
        (3, 1, "Mouse", 25.0, "2023-03-15"),
        (4, 3, "Keyboard", 45.0, "2023-04-02"),
        (5, 2, "Laptop", 1100.0, "2023-05-20"),
    ]

    cursor.executemany("INSERT OR IGNORE INTO customer VALUES (?,?,?,?)", customers)
    cursor.executemany("INSERT OR IGNORE INTO sales VALUES (?,?,?,?,?)", sales)

    conn.commit()
    conn.close()


ensure_sample_database()


def get_openai_client():
    # IMPORTANT: do NOT hardcode API keys. Read from environment instead.
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        return OpenAI(api_key=api_key)
    except OpenAIError:
        return None


def clean(dict_variable):
    return next(iter(dict_variable.values()))


def build_fallback_query(question: str) -> str:
    lowered = question.lower()
    if "product" in lowered and "sales" in lowered:
        return "SELECT product, SUM(amount) AS total_sales FROM sales GROUP BY product ORDER BY total_sales DESC"
    if "customer" in lowered and ("spend" in lowered or "spent" in lowered or "amount" in lowered):
        return "SELECT c.name, SUM(s.amount) AS total_spent FROM customer c JOIN sales s ON c.customer_id = s.customer_id GROUP BY c.customer_id, c.name ORDER BY total_spent DESC"
    if "customer" in lowered:
        return "SELECT customer_id, name, email FROM customer ORDER BY customer_id"
    return "SELECT * FROM sales ORDER BY sale_date LIMIT 10"


def create_query(question):
    schema = """
    customer (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        join_date TEXT
    )

    sales (
        sale_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product TEXT,
        amount REAL,
        sale_date TEXT,
        FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
    )
    """

    prompt = f"""Given the schema below, create a safe SQLite query to answer the question.
Output only the query in JSON with a single key named 'query'.

Schema:
{schema}

Question:
{question}
"""

    client = get_openai_client()
    if client is None:
        return build_fallback_query(question)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        payload = json.loads(response.choices[0].message.content or "{}")
        return clean(payload)
    except (OpenAIError, TypeError, ValueError, json.JSONDecodeError):
        return build_fallback_query(question)


def run_query(query):
    # Normalize whitespace and strip trailing semicolons
    cleaned = query.strip()
    # Remove any trailing semicolons that models sometimes append
    while cleaned.endswith(";"):
        cleaned = cleaned[:-1].rstrip()

    lowered = cleaned.lower()

    forbidden = ["insert", "update", "delete", "drop", "alter", "create", "attach", "detach", "pragma", "replace"]
    # Disallow semicolons in the middle of the query (multiple statements)
    if ";" in lowered:
        raise ValueError("Only simple SELECT queries are allowed.")
    if any(token in lowered for token in forbidden):
        raise ValueError("Only simple SELECT queries are allowed.")

    if not lowered.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    if len(cleaned) > 2000:
        raise ValueError("Query too long.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(cleaned)
    rows = cursor.fetchall()
    output = json.dumps(rows, default=str)
    conn.close()

    return output


def interpret_results(question, results):
    client = get_openai_client()
    if client is None:
        return "OpenAI API key not set, so the app is using a safe fallback summary based on the database output."

    prompt = f"""Given the database results below, answer the user's question concisely.

Results:
{results}

User's question:
{question}
"""

    try:
        response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content
    except OpenAIError:
        return "The model could not summarize the results right now, but the query executed successfully."


def get_question_and_return_answer(question):
    query = create_query(question)
    results = run_query(query)
    answer = interpret_results(question, results)
    return answer


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    question = ""
    if request.method == "POST":
        question = request.form.get("text", "").strip()
        if question:
            try:
                result = get_question_and_return_answer(question)
            except Exception as exc:
                result = f"Unable to process the request: {exc}"
        else:
            result = "Please enter a question to explore the database."

    return render_template("index.html", result=result, question=question)


if __name__ == "__main__":
    app.run(debug=True)


