import random
from datetime import datetime, timedelta

# === CONFIGURATION ===
n_utilisateurs = 5
n_comptes = 3
n_mouvements = 3000
banques = ["Banque A", "Banque B", "Banque C"]

# === DONNÉES DE BASE ===
categories = [
    ("Alimentation", ["Carrefour", "Auchan", "Lidl", "Intermarché"], (30, 200)),
    ("Salaire", ["Entreprise A", "Entreprise B", "Entreprise C"], (2000, 3000)),
    ("Loisir", ["Netflix", "Spotify", "Cinéma", "Bowling"], (10, 100)),
    ("Transport", ["SNCF", "Uber", "Blablacar"], (5, 80)),
    ("Santé", ["Pharmacie", "Doctolib", "Hôpital"], (15, 150)),
    ("Logement", ["EDF", "Engie", "Loyer"], (300, 900)),
    ("Internet", ["Orange", "Free", "SFR"], (20, 60)),
    ("Téléphone", ["Bouygues", "SFR", "Orange"], (10, 50)),
    ("Cadeau", ["Amazon", "Fnac", "Zalando"], (20, 200)),
    ("Vacances", ["Airbnb", "Booking", "Expedia"], (100, 1200)),
    ("Impôts", ["Impôts", "URSSAF"], (200, 2000)),
    ("Assurance", ["MAIF", "AXA", "Allianz"], (20, 120)),
    ("Remboursement", ["Mutuelle", "CPAM"], (10, 300)),
    ("Épargne", ["Livret A", "PEL"], (50, 500)),
    ("Animaux", ["Truffaut", "Animalis"], (10, 100)),
    ("Vêtements", ["Zara", "H&M", "Uniqlo"], (15, 250)),
    ("Frais bancaires", ["Banque Postale", "Crédit Agricole"], (2, 20)),
    ("Enfants", ["JouetClub", "Orchestra"], (10, 150)),
    ("Divers", ["Divers"], (5, 100)),
    ("Retrait", ["DAB"], (20, 300)),
]

users = [
    ("Dupont", "Alice", "alice", "Paris", "75000"),
    ("Martin", "Bob", "bob", "Lyon", "69000"),
    ("Durand", "Charlie", "charlie", "Marseille", "13000"),
    ("Petit", "David", "david", "Lille", "59000"),
    ("Lefevre", "Eve", "eve", "Toulouse", "31000"),
]

start_date = datetime.now() - timedelta(days=3 * 365)
end_date = datetime.now()

def random_date():
    delta = end_date - start_date
    return (start_date + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")

with open("mouvements_test.sql", "w", encoding="utf-8") as f:
    # === CATEGORIES ===
    for idx, (nom_cat, _, _) in enumerate(categories, 1):
        f.write(f"INSERT INTO categorie (idCategorie, nomCategorie) VALUES ({idx}, '{nom_cat}');\n")
    f.write("\n")

    # === UTILISATEURS ===
    for idx, (nom, prenom, login, ville, cp) in enumerate(users, 1):
        mdp = "test1234"
        f.write(
            f"INSERT INTO utilisateur (idUtilisateur, nomUtilisateur, prenomUtilisateur, login, mdp, ville, codePostal) "
            f"VALUES ({idx}, '{nom}', '{prenom}', '{login}', '{mdp}', '{ville}', '{cp}');\n"
        )
    f.write("\n")

    # === COMPTES ===
    for idx in range(1, n_comptes + 1):
        idUtilisateur = random.randint(1, n_utilisateurs)
        description = f"Compte {idx}"
        banque = random.choice(banques)
        date_creation = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        montant = round(random.uniform(500, 5000), 2)
        f.write(
            f"INSERT INTO compte (idCompte, descriptionCompte, nomBanque, idUtilisateur, "
            f"dateHeureCreation, dateHeureMAJ, montantInitial, dernierMontantCalculé) VALUES "
            f"({idx}, '{description}', '{banque}', {idUtilisateur}, "
            f"'{date_creation}', '{date_creation}', {montant}, {montant});\n"
        )
    f.write("\n")

    # === TIERS ===
    idTiers_global = 1
    tiers_map = {}
    for cat_idx, (_, tiers_list, _) in enumerate(categories, 1):
        for nom in tiers_list:
            idUtilisateur = random.randint(1, n_utilisateurs)
            tiers_map[(cat_idx, nom)] = idTiers_global
            f.write(f"INSERT INTO tiers (idTiers, nomTiers, idUtilisateur) VALUES ({idTiers_global}, '{nom}', {idUtilisateur});\n")
            idTiers_global += 1
    f.write("\n")

    # === MOUVEMENTS ===
    for _ in range(n_mouvements):
        cat_idx = random.randint(0, len(categories) - 1)
        cat_name, tiers_list, (min_m, max_m) = categories[cat_idx]
        montant = round(random.uniform(min_m, max_m), 2)
        type_mouvement = 'C' if cat_name in ["Salaire", "Remboursement", "Épargne"] else 'D'
        if type_mouvement == 'D':
            montant = -abs(montant)
        idCategorie = cat_idx + 1
        idCompte = random.randint(1, n_comptes)
        tiers_nom = random.choice(tiers_list)
        idTiers = tiers_map[(idCategorie, tiers_nom)]
        dateMouvement = random_date()
        f.write(
            f"INSERT INTO mouvement (dateMouvement, idCompte, idTiers, idCategorie, montant, typeMouvement) "
            f"VALUES ('{dateMouvement}', {idCompte}, {idTiers}, {idCategorie}, {montant}, '{type_mouvement}');\n"
        )
