import streamlit as st
import pandas as pd
from whoscored.whoscored_events_data import load_whoscored_events_data

st.set_page_config(page_title="WhoScored Events (soccerdata)", layout="wide")

st.title("WhoScored Match Events Viewer ⚽📊 [via soccerdata]")

st.markdown("""
Inserisci l'URL completo del **Match Centre** o **Match Report** di WhoScored.  
Esempi validi (2025/26):  
• https://it.whoscored.com/matches/1903264/live/inghilterra-premier-league-2025-2026-brighton-everton
""")

match_url = st.text_input(
    "URL Match Centre / Match Report",
    placeholder="https://www.whoscored.com/...",
    help="Copia l'URL dalla barra del browser nella pagina della partita"
)

if st.button("Carica eventi", type="primary", disabled=not match_url.strip()):
    if not match_url.strip():
        st.warning("Inserisci un URL valido.")
    else:
        df = load_whoscored_events_data(match_url)
else:
    st.info("Inserisci l'URL della partita e premi 'Carica eventi'.")
