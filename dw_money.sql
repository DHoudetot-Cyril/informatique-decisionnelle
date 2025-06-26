CREATE DATABASE IF NOT EXISTS dw_money;
USE dw_money;

-- Dimension Compte
CREATE TABLE DimCompte (
    idCompteDim INT PRIMARY KEY,
    descriptionCompte VARCHAR(50) NOT NULL,
    nomBanque VARCHAR(50) NOT NULL
);

-- Dimension Tiers
CREATE TABLE DimTiers (
    idTiersDim INT PRIMARY KEY,
    nomTiers VARCHAR(50) NOT NULL
);

-- Dimension Catégorie + SousCatégorie
CREATE TABLE DimCategorie (
    idCategorieDim INT PRIMARY KEY,
    nomCategorie VARCHAR(50) NOT NULL,
    nomSousCategorie VARCHAR(50) NULL
);

-- Dimension Temps
CREATE TABLE DimTemps (
    idTemps INT PRIMARY KEY,
    dateMouvement DATE NOT NULL,
    annee INT NOT NULL,
    mois INT NOT NULL,
    jour INT NOT NULL
);

-- Table de faits Mouvements
CREATE TABLE FaitsMouvements (
    idMouvement INT PRIMARY KEY,
    montant DECIMAL(10,2) NOT NULL,
    idCompteDim INT NOT NULL,
    idTiersDim INT NOT NULL,
    idCategorieDim INT NOT NULL,
    idTemps INT NOT NULL,
    CONSTRAINT fk_faits_compte FOREIGN KEY (idCompteDim) REFERENCES DimCompte(idCompteDim),
    CONSTRAINT fk_faits_tiers FOREIGN KEY (idTiersDim) REFERENCES DimTiers(idTiersDim),
    CONSTRAINT fk_faits_categorie FOREIGN KEY (idCategorieDim) REFERENCES DimCategorie(idCategorieDim),
    CONSTRAINT fk_faits_temps FOREIGN KEY (idTemps) REFERENCES DimTemps(idTemps)
);
