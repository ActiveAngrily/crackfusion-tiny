"""Root entrypoint for Streamlit Community Cloud and local execution."""

import runpy
from pathlib import Path

webapp_app = Path(__file__).resolve().parent / "webapp" / "app.py"
runpy.run_path(str(webapp_app), run_name="__main__")
