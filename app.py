import streamlit as st
import pandas as pd
from whoscored.whoscored_events_data import load_whoscored_events_data
import re  # per mostrare match_id estratto

st.set_page_config(page_title="WhoScored Events (soccerdata)", layout="wide")

st.title("WhoScored Match Events Viewer ⚽📊 [via soccerdata]")

st.markdown("""
Inserisci l'URL completo del **Match Centre** o **Match Report** di WhoScored.  
Esempi validi (2025/26):  
• https://www.whoscored.com/Matches/1903117/Live/England-Premier-League-2025-2026-Liverpool-Bournemouth  
• https://www.whoscored.com/Matches/1901138/MatchReport/Italy-Serie-A-2025-2026-Como-Atalanta  
""")

match_url = st.text_input(
    "URL Match Centre / Match Report",
    placeholder="https://www.whoscored.com/Matches/1901138/MatchReport/...",
    help="Copia l'URL dalla barra del browser nella pagina della partita"
)

if st.button("Carica eventi", type="primary", disabled=not match_url.strip()):
    if not match_url.strip():
        st.warning("Inserisci un URL valido.")
    else:
        # Debug 1: mostra l'URL inserito
        st.info(f"URL inserito: {match_url}")

        # Debug 2: prova a estrarre match_id (utile per capire se la regex funziona)
        match_id_match = re.search(r'/Matches/(\d+)', match_url, re.IGNORECASE)
        if match_id_match:
            match_id = match_id_match.group(1)
            st.info(f"Match ID estratto: **{match_id}**")
        else:
            st.error("Non riesco a estrarre il match_id dall'URL (cerca '/Matches/NUMERO/')")
            st.stop()

        with st.spinner("Caricamento dati da WhoScored via soccerdata..."):
            df = load_whoscored_events_data(match_url)

        # Debug 3: controllo esplicito dopo la chiamata
        if df is None:
            st.error("La funzione ha restituito None → nessun dato caricato")
        elif df.empty:
            st.warning("DataFrame caricato ma vuoto (0 righe)")
        else:
            st.success(f"Dati caricati correttamente → {len(df)} eventi")

        # Debug 4: stampa informazioni sul DataFrame
        if df is not None:
            st.subheader("Debug DataFrame")
            st.write("Tipo oggetto:", type(df))
            st.write("Shape:", df.shape if hasattr(df, 'shape') else "Non ha shape")
            st.write("Prime colonne:", list(df.columns)[:10] if hasattr(df, 'columns') else "Nessuna colonna")
            
            # Mostra prime righe se esiste qualcosa
            if not df.empty:
                st.subheader("Prime 5 righe del DataFrame")
                st.dataframe(df.head(5))
            else:
                st.info("Nessuna riga da mostrare")
        else:
            st.info("df è None → controlla i log runtime o aggiungi print nella funzione loader")

else:
    st.info("Inserisci l'URL della partita e premi 'Carica eventi'.")
