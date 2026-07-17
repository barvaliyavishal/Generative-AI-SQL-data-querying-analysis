import importlib.util
from pathlib import Path
import sys

APP_PATH = Path(__file__).resolve().parents[1] / 'projects' / 'Data Querying' / 'app.py'
spec = importlib.util.spec_from_file_location('portfolio_app', str(APP_PATH))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

q = 'which customer spent most in march?'
print('create_query ->')
print(mod.create_query(q))
print('\nrun_query ->')
try:
    print(mod.run_query(mod.create_query(q)))
except Exception as e:
    print('run_query raised:', e)
