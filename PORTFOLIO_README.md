# Data Querying & Analysis — GenAI Portfolio Demo

This repository presents a polished Gen AI portfolio project that demonstrates a practical NL-to-SQL workflow: a user asks a question in natural language, the app generates a safe SQLite query, runs it against a sample database, and summarizes the results in plain English.

## What this project shows
- Natural-language to SQL generation with a generative model
- Safe execution of read-only SELECT statements against a local sample database
- A simple Flask web interface suitable for demos and portfolio walkthroughs
- A clean, reproducible setup for local development and GitHub sharing

## Quick start
1. Create and activate a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Create the sample database: `python projects/"Data Querying"/create_example_db.py`
4. Run the demo: `python projects/"Data Querying"/app.py`
5. Open http://localhost:5000 and try questions such as “Which customers spent the most in March?”

## Portfolio angle
This is a strong Gen AI demo because it highlights prompt engineering, LLM + database integration, safe execution, and a simple end-to-end user experience.
