import subprocess
import sys
import importlib.util

# Check if whoscored is already importable
if importlib.util.find_spec("whoscored") is None:
    st.info("Installing whoscored scraper from GitHub... (one-time, may take 20–60s)")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "--no-cache-dir",
        "git+https://github.com/sahil-gidwani/football-data-webscraping.git#subdirectory=whoscored"
    ])
    st.success("Installation done. Refresh the page if needed.")

# Now safe to import
from whoscored.whoscored_events_data import load_whoscored_events_data
