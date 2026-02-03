# app.py
import streamlit as st
import pandas as pd
try:
    from whoscored.whoscored_events_data import load_whoscored_events_data
except ImportError:
    st.error("Libreria whoscored non trovata. Installala da github:")
    st.code("pip install git+https://github.com/sahil-gidwani/football-data-webscraping.git#subdirectory=whoscored")
    st.stop()

st.title("WhoScored Event Data Viewer ⚽")

match_url = st.text_input(
    "Inserisci URL partita WhoScored",
    value="https://www.whoscored.com/Matches/1729476/Live/England-Premier-League-2023-2024-Manchester-City-Everton",
    help="Esempio: https://www.whoscored.com/Matches/XXXXXXX/Live/..."
)

if st.button("Carica eventi") and match_url:
    with st.spinner("Scraping in corso da WhoScored (può richiedere 5–20 secondi)..."):
        try:
            events = load_whoscored_events_data(match_url)
            
            if isinstance(events, pd.DataFrame):
                st.success(f"Trovati {len(events)} eventi!")
                
                # Filtri utili
                col1, col2, col3 = st.columns(3)
                team = col1.selectbox("Squadra", ["Tutte"] + sorted(events['team'].unique()))
                event_type = col2.selectbox("Tipo evento", ["Tutti"] + sorted(events['event_type'].unique()))
                period = col3.selectbox("Periodo", ["Tutti", "1", "2"])
                
                df_show = events.copy()
                if team != "Tutte":
                    df_show = df_show[df_show['team'] == team]
                if event_type != "Tutti":
                    df_show = df_show[df_show['event_type'] == event_type]
                if period != "Tutti":
                    df_show = df_show[df_show['period'] == int(period)]
                
                st.dataframe(df_show.style.background_gradient(cmap='Blues', subset=['x','y']), use_container_width=True)
                
                # Statistiche veloci
                st.subheader("Statistiche rapide")
                st.write(events['event_type'].value_counts().head(10))
                
                # Heatmap xG / passaggi (se hai le coordinate x,y)
                if 'x' in events.columns and 'y' in events.columns:
                    st.subheader("Heatmap eventi (tiri/passi)")
                    # qui potresti aggiungere uno scatter o hexbin con matplotlib/seaborn
            else:
                st.json(events)  # se restituisce dict/json raw
                
        except Exception as e:
            st.error(f"Errore durante il caricamento:\n{e}")
            st.info("Controlla che l'URL sia corretto e che WhoScored non abbia cambiato struttura HTML.")
