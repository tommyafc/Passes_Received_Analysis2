import streamlit as st
import soccerdata as sd
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="WhoScored Passes Analysis",
    layout="wide"
)

st.title("Analisi Passaggi Ricevuti – WhoScored")
st.markdown("Inserisci **lega**, **stagione** e **match_id** per visualizzare gli eventi della partita.")

# ────────────────────────────────────────────────
# Selettore Stagione
# ────────────────────────────────────────────────
available_seasons = [
    "25-26",    # stagione in corso (2025/26)
    "24-25",
    "23-24",
    "22-23",
    "21-22",
]

selected_season = st.selectbox(
    "Stagione",
    options=available_seasons,
    index=0,                    # di default la più recente
    help="Formato 'yy-yy' o 'yyyy' – WhoScored interpreta entrambi"
)

# ────────────────────────────────────────────────
# Input Lega (per ora fisso, poi puoi espandere)
# ────────────────────────────────────────────────
league = "ENG-Premier League"   # puoi trasformarlo in selectbox dopo

# ────────────────────────────────────────────────
# Input Match ID
# ────────────────────────────────────────────────
match_id_str = st.text_input(
    "Match ID (es: 1485184, 1734567, ...)",
    value="1485184",
    help="Trovi l'ID nell'URL della partita su whoscored.com"
)

if st.button("Carica dati") and match_id_str.strip():
    match_id = match_id_str.strip()

    with st.spinner(f"Scaricamento dati {league} {selected_season} – match {match_id} ... (10–60 secondi)"):
        try:
            ws = sd.WhoScored(
                leagues=league,
                seasons=selected_season,
                proxy=None,               # prova "tor" se hai Tor attivo
                no_cache=False,
                no_store=False,
                data_dir=Path("cache_whoscored"),
                headless=True,            # resta True, ma può causare blocchi WhoScored
            )

            events = ws.read_events(match_id=match_id)

            if events.empty:
                st.warning("Nessun evento trovato per questo match_id nella stagione selezionata.")
                st.info(
                    "Possibili motivi:\n"
                    "• ID partita errato\n"
                    "• Partita non ancora caricata su WhoScored\n"
                    "• Stagione sbagliata per quel match"
                )
            else:
                st.success(f"Caricati **{len(events):,}** eventi!")

                # Tabella base
                st.subheader("Anteprima dati (prime 10 righe)")
                st.dataframe(events.head(10))

                # Statistiche passaggi ricevuti
                if 'recipient' in events.columns and 'type' in events.columns:
                    successful_passes = events[
                        (events['type'] == 'Pass') &
                        (events['outcome_type'].isna() | (events['outcome_type'] == 'Successful'))
                    ]

                    received_count = (
                        successful_passes
                        .groupby('recipient')
                        .size()
                        .sort_values(ascending=False)
                        .head(12)
                        .reset_index(name='Passaggi ricevuti')
                    )

                    st.subheader("Top giocatori per passaggi ricevuti (match)")
                    st.dataframe(received_count.style.highlight_max(color='#d4edda'))

                    st.bar_chart(
                        received_count.set_index('recipient')['Passaggi ricevuti'],
                        use_container_width=True
                    )

                # Opzione per vedere tutto
                with st.expander("Mostra dataframe completo"):
                    st.dataframe(events)

                # Info aggiuntive
                with st.expander("Informazioni sul dataset"):
                    buf = events.memory_usage(deep=True).sum() / (1024 ** 2)
                    st.write(f"Dimensioni: {events.shape[0]} righe × {events.shape[1]} colonne")
                    st.write(f"Memoria approssimativa: {buf:.1f} MB")
                    st.write(events.dtypes)

        except Exception as e:
            st.error(f"Errore durante il caricamento:\n{str(e)}")
            st.info(
                "Possibili cause comuni:\n"
                "• Match non esiste in questa stagione\n"
                "• Problemi di rete / WhoScored blocca lo scraping\n"
                "• Problemi con ChromeDriver / Selenium su Cloud (permission denied uc_driver)\n"
                "   → Prova headless=False in locale per debug\n"
                "• Cache corrotta → cancella la cartella cache_whoscored/\n"
                "• Su Streamlit Cloud: controlla packages.txt con chromium + chromium-driver"
            )
