import streamlit as st
from whoscored.whoscored_events_data import load_whoscored_events_data
import subprocess
import sys

# Installa la libreria da GitHub solo se non è già presente
try:
    from whoscored.whoscored_events_data import load_whoscored_events_data
except ImportError:
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "git+https://github.com/sahil-gidwani/football-data-webscraping.git#subdirectory=whoscored"
    ])
    from whoscored.whoscored_events_data import load_whoscored_events_data
st.title("WhoScored Events")

url = st.text_input("Inserisci URL partita WhoScored", "...")
if st.button("Carica"):
    try:
        df = load_whoscored_events_data(url)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Errore: {e}")
