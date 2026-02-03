import streamlit as st
from whoscored.whoscored_events_data import load_whoscored_events_data

st.title("WhoScored Events")

url = st.text_input("Inserisci URL partita WhoScored", "...")
if st.button("Carica"):
    try:
        df = load_whoscored_events_data(url)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Errore: {e}")
