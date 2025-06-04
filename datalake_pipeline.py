import os
import requests
import pandas as pd
import sqlite3

BRONZE_DIR = os.path.join('datalake', 'bronze')
SILVER_DIR = os.path.join('datalake', 'silver')
GOLD_DIR = os.path.join('datalake', 'gold')
DB_PATH = os.path.join('datalake', 'datalake.db')


def ensure_dirs():
    """Create datalake directories if they do not exist."""
    for directory in [BRONZE_DIR, SILVER_DIR, GOLD_DIR]:
        os.makedirs(directory, exist_ok=True)


def ingest_csv(csv_path):
    """Copy a CSV file into the bronze layer."""
    ensure_dirs()
    dest = os.path.join(BRONZE_DIR, os.path.basename(csv_path))
    df = pd.read_csv(csv_path)
    df.to_csv(dest, index=False)
    return dest


def fetch_api(url, filename):
    """Fetch JSON data from an API and store it in the bronze layer."""
    ensure_dirs()
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    dest = os.path.join(BRONZE_DIR, filename)
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(response.text)
    return dest


def clean_to_silver():
    """Simple cleaning: remove rows with missing values from CSV files."""
    ensure_dirs()
    for file in os.listdir(BRONZE_DIR):
        if file.lower().endswith('.csv'):
            df = pd.read_csv(os.path.join(BRONZE_DIR, file))
            df = df.dropna()
            df.to_csv(os.path.join(SILVER_DIR, file), index=False)


def aggregate_to_gold():
    """Combine all silver CSV files into a single CSV in the gold layer."""
    ensure_dirs()
    frames = []
    for file in os.listdir(SILVER_DIR):
        if file.lower().endswith('.csv'):
            frames.append(pd.read_csv(os.path.join(SILVER_DIR, file)))
    if frames:
        combined = pd.concat(frames, ignore_index=True)
        gold_path = os.path.join(GOLD_DIR, 'all_data.csv')
        combined.to_csv(gold_path, index=False)
        return gold_path
    return None


def load_gold_to_db(table_name='gold_data'):
    """Load the aggregated gold data into a SQLite database."""
    gold_file = os.path.join(GOLD_DIR, 'all_data.csv')
    if not os.path.exists(gold_file):
        return
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_csv(gold_file)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()


if __name__ == '__main__':
    ensure_dirs()
    # Exemplos de uso:
    # ingest_csv('caminho/para/dados.csv')
    # fetch_api('https://api.exemplo.com/dados', 'api_data.json')
    clean_to_silver()
    aggregate_to_gold()
    load_gold_to_db()
