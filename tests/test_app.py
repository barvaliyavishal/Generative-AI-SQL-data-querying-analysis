import importlib.util
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "projects" / "Data Querying" / "app.py"


class AppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("portfolio_app", APP_PATH)
        cls.app_module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.app_module
        spec.loader.exec_module(cls.app_module)

    def test_database_path_is_resolved_from_project_directory(self):
        self.assertTrue(self.app_module.DB_PATH.exists(), "Expected sample database to exist")

    def test_home_page_renders(self):
        client = self.app_module.app.test_client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Ask your data question", response.data)

    def test_fallback_query_generation_works_without_openai(self):
        question = "Which customers spent the most in March?"
        query = self.app_module.create_query(question)
        self.assertIn("SELECT", query.upper())
        self.assertIn("FROM", query.upper())


if __name__ == "__main__":
    unittest.main()
