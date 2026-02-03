# app.py
from .whoscored_events_data import load_whoscored_events_data
import pandas as pd
from pathlib import Path
import time
import random

# -------------------------------
# CONFIG
# -------------------------------
MATCH_URLS = [
    "https://www.whoscored.com/Matches/1821545/Live/Italy-Serie-A-2025-2026-Juventus-Inter",   # ← cambia con match reali!
    "https://www.whoscored.com/Matches/1821550/Live/Italy-Serie-A-2025-2026-Napoli-Milan",
    # aggiungi altri match qui (trovi l'URL aprendo la partita su WhoScored)
]

OUTPUT_FOLDER = Path("data/raw/whoscored_events")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

DELAY_MIN = 8
DELAY_MAX = 18
# -------------------------------

def main():
    print("Inizio scraping WhoScored events...\n")

    for i, url in enumerate(MATCH_URLS, 1):
        print(f"[{i}/{len(MATCH_URLS)}] {url}")
        
        try:
            df = load_whoscored_events_data(url)
            
            if df is None or df.empty:
                print(" → Nessun dato trovato / errore")
                continue
                
            # Nome file significativo
            match_id = url.split('/Matches/')[1].split('/')[0]
            teams = url.split('/')[-1].replace('-', ' vs ')
            filename = f"{match_id}_{teams.replace(' ', '_')}.csv"
            filepath = OUTPUT_FOLDER / filename
            
            df.to_csv(filepath, index=False)
            print(f" → Salvato: {filepath}  ({len(df)} eventi)")
            
        except Exception as e:
            print(f" → ERRORE: {e}")
        
        # Anti-ban: attesa random
        if i < len(MATCH_URLS):
            wait = random.uniform(DELAY_MIN, DELAY_MAX)
            print(f"Attesa {wait:.1f} secondi...\n")
            time.sleep(wait)

    print("\nScraping terminato!")

if __name__ == "__main__":
    main()
