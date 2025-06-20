import pandas as pd
from sqlalchemy import create_engine

# Connexion à la base MariaDB
user = "root"
password = ""
host = "127.0.0.1"
port = 3307
database = "info_money"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# Liste des vues ou tables à extraire
views_or_tables = [
    "V_MOUVEMENT",
    "V_CATEGORIE",
    "Utilisateur",
    "Compte",
    "Tiers",
    "Virement",
    "Mouvement"
]

# Dossier de sortie pour les fichiers CSV
output_dir = "./exports_powerbi"

import os
os.makedirs(output_dir, exist_ok=True)

# Extraction + Transformation (optionnelle) + Chargement
for table in views_or_tables:
    df = pd.read_sql(f"SELECT * FROM {table}", engine)
    
    # Exemple de transformation simple : format date
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Sauvegarde en CSV
    df.to_csv(f"{output_dir}/{table}.csv", index=False)
    print(f"{table} exporté vers CSV")

print("✅ ETL terminé. Importez les fichiers dans Power BI.")
