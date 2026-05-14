import pandas as pd
import requests
import logging
from datetime import datetime

# --- CONFIGURATION & LOGGING SETUP ---
# This creates a file named 'pipeline.log' to track the script's progress
logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_pipeline():
    logging.info("ETL Pipeline Started")
    print("🚀 Starting Bio-Signaling ETL Pipeline...")

    # 1. EXTRACT (Fetching Live Data)
    try:
        search_term = "gut microbiota signaling"
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {"db": "pubmed", "term": search_term, "retmode": "json", "retmax": 5}
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        paper_ids = response.json().get("esearchresult", {}).get("idlist", [])
        
        logging.info(f"Extract Successful: Found {len(paper_ids)} papers.")
    except Exception as e:
        logging.error(f"Extraction Failed: {e}")
        return

    # 2. TRANSFORM (Cleaning the Data)
    # We use mock data here for the demonstration of cleaning logic
    raw_data = [
        {"id": paper_ids[0] if paper_ids else "N/A", "title": "Microbiota Signaling", "impact": 8.5},
        {"id": "N/A", "title": "None", "impact": 5.0},
        {"id": "Manual-Entry", "title": "Protein Metabolism", "impact": None}
    ]
    
    try:
        df = pd.DataFrame(raw_data)
        df = df[df['title'] != "None"] # Remove bad data
        df['impact'] = df['impact'].fillna(df['impact'].mean()) # Fill missing values
        logging.info("Transform Successful: Data cleaned and validated.")
    except Exception as e:
        logging.error(f"Transformation Failed: {e}")
        return

    # 3. LOAD (Saving the Result)
    try:
        filename = f"microbiota_data_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        logging.info(f"Load Successful: Saved to {filename}")
        print(f"✅ Success! Data saved to {filename} and progress logged.")
    except Exception as e:
        logging.error(f"Loading Failed: {e}")

if __name__ == "__main__":
    run_pipeline()

