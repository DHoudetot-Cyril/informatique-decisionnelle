import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# Configuration des connexions
source_config = {
    'host': "127.0.0.1",
    'port': 3307,
    'user': 'root',
    'password': '',
    'database': 'money'
}

target_config = {
    'host': "127.0.0.1",
    'port': 3307,
    'user': 'root',
    'password': '',
    'database': 'dw_money'
}

# Connexion source/destination
source_conn = mysql.connector.connect(**source_config)
target_engine = create_engine(f"mysql+mysqlconnector://{target_config['user']}:{target_config['password']}@{target_config['host']}:{target_config['port']}/{target_config['database']}")

# Extraction des données 
df_mouvements = pd.read_sql("SELECT * FROM V_MOUVEMENT", source_conn)



## DimCompte
dim_compte = df_mouvements[['descriptionCompte', 'nomBanque']].drop_duplicates().reset_index(drop=True)
dim_compte['idCompteDim'] = dim_compte.index + 1

## DimTiers
dim_tiers = df_mouvements[['nomTiers']].drop_duplicates().reset_index(drop=True)
dim_tiers['idTiersDim'] = dim_tiers.index + 1

## DimCategorie
dim_categorie = df_mouvements[['nomCategorie', 'nomSousCategorie']].drop_duplicates().reset_index(drop=True)
dim_categorie['idCategorieDim'] = dim_categorie.index + 1

## DimTemps
dim_temps = df_mouvements[['dateMouvement']].drop_duplicates().reset_index(drop=True)
dim_temps['idTemps'] = dim_temps.index + 1
dim_temps['annee'] = pd.to_datetime(dim_temps['dateMouvement']).dt.year
dim_temps['mois'] = pd.to_datetime(dim_temps['dateMouvement']).dt.month
dim_temps['jour'] = pd.to_datetime(dim_temps['dateMouvement']).dt.day

# Création de la table de faits
df_faits = df_mouvements.copy()

# Jointures pour les ID des dimensions
df_faits = df_faits.merge(dim_compte, on=['descriptionCompte', 'nomBanque'], how='left')
df_faits = df_faits.merge(dim_tiers, on='nomTiers', how='left')
df_faits = df_faits.merge(dim_categorie, on=['nomCategorie', 'nomSousCategorie'], how='left')
df_faits = df_faits.merge(dim_temps, on='dateMouvement', how='left')

# Table de faits finale
fact_mouvements = df_faits[[
    'idMouvement', 'montant',
    'idCompteDim', 'idTiersDim', 'idCategorieDim', 'idTemps'
]]

# insertion dans la base cible
dim_compte.to_sql('DimCompte', con=target_engine, if_exists='replace', index=False)
dim_tiers.to_sql('DimTiers', con=target_engine, if_exists='replace', index=False)
dim_categorie.to_sql('DimCategorie', con=target_engine, if_exists='replace', index=False)
dim_temps.to_sql('DimTemps', con=target_engine, if_exists='replace', index=False)
fact_mouvements.to_sql('FaitsMouvements', con=target_engine, if_exists='replace', index=False)

print(" ETL terminé.")
