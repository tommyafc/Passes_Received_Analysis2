import streamlit as st
import soccerdata as sd
import pandas as pd

st.set_page_config(
    page_title="WhoScored Passes Analysis",
    layout="wide"
)

st.title("Analisi Passaggi Ricevuti – WhoScored")
st.markdown("Inserisci il **match_id** di WhoScored per vedere gli eventi del match.")

# Input
match_id = st.text_input("Match ID (es: 1485184)", "1485184")

if st.button("Carica dati") or match_id.strip():
    with st.spinner("Sto scaricando i dati da WhoScored... (può richiedere 10–40 secondi)"):
        try:
            # Inizializziamo WhoScored
            # Nota: mettiamo cache=True per velocizzare i prossimi caricamenti
            ws = sd.WhoScored(
                leagues="ENG-Premier League",   # ← puoi renderlo selezionabile dopo
                seasons=2025,                   # ← aggiorna all'anno corrente o fai input
                proxy=None,                     # se hai problemi di connessione
                no_cache=False,
                cache_dir="cache"
            )

            events = ws.read_events(match_id=match_id.strip())

            if events.empty:
                st.error("Nessun dato trovato per questo match_id 😔")
            else:
                st.success(f"Caricati {len(events):,} eventi!")

                # Mostriamo le prime righe
                st.subheader("Prime 10 righe del dataset")
                st.dataframe(events.head(10))

                # Info generali
                with st.expander("Informazioni sul dataset"):
                    st.write(events.info())

                # Esempio di statistiche base sui passaggi ricevuti
                if 'recipient' in events.columns and 'type' in events.columns:
                    passes_received = events[
                        (events['type'] == 'Pass') &
                        (events['outcome_type'].isna() | (events['outcome_type'] == 'Successful'))
                    ].groupby('recipient').size().sort_values(ascending=False)

                    st.subheader("Top 10 giocatori per passaggi ricevuti")
                    st.bar_chart(passes_received.head(10))

                # Mostra tutto il dataframe (opzione con toggle)
                if st.checkbox("Mostra tutto il dataframe (potrebbe essere lento)"):
                    st.dataframe(events)

        except Exception as e:
            st.error(f"Errore durante il caricamento:\n{str(e)}")
            st.info(
                "Possibili cause:\n"
                "• Match ID sbagliato\n"
                "• Partita non ancora disponibile su WhoScored\n"
                "• Problemi di connessione / scraping bloccato\n"
                "• Stagione non ancora supportata"
            )
