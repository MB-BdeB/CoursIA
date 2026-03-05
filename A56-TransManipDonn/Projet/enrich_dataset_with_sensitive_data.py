"""
Script pour enrichir le dataset avec des données sensibles (noms, prénoms, NAS, dates de naissance)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import math

# Listes de noms et prénoms courants
FIRST_NAMES = ['Jean', 'Marie', 'Pierre', 'Sophie', 'Luc', 'Anne', 'Marc', 'Julie', 'Paul', 'Claire',
               'Jacques', 'Nathalie', 'Christian', 'Véronique', 'Philippe', 'Isabelle', 'François', 'Martine',
               'Joseph', 'Monique', 'Michel', 'Sylvie', 'André', 'Michèle', 'Georges', 'Danielle',
               'Alain', 'Catherine', 'Etienne', 'Stéphanie', 'Didier', 'Valérie', 'Christophe', 'Laure',
               'Olivier', 'Sandrine', 'Laurent', 'Fabienne', 'Serge', 'Virginie', 'Thierry', 'Dominique']

LAST_NAMES = ['Martin', 'Bernard', 'Dubois', 'Durand', 'Legrand', 'Garnier', 'Fontaine', 'Lefevre',
             'Lemaire', 'Demay', 'Mercier', 'Renaud', 'Gillet', 'Gillet', 'Leroy', 'Moreau',
             'Meunier', 'Deschamps', 'Masson', 'Renouard', 'Thiebault', 'Marechal', 'Leconte', 'Delatour',
             'Roux', 'Olivier', 'Lafrance', 'Couderc', 'Renault', 'Guedon', 'Bonnet', 'Lemoine',
             'Beaumont', 'Lebesgue', 'Lefebvre', 'Bouvier', 'Noël', 'Rousseau', 'Brun', 'Hubbard']

# Charger le dataset original
print("Chargement du dataset original...")
df = pd.read_csv("default_of_credit_card_clients.csv")

print(f"Dataset chargé: {df.shape[0]} lignes")

# Ajouter les colonnes sensibles
np.random.seed(42)
n_rows = len(df)

# Générer les prénoms et noms
df['FIRST_NAME'] = np.random.choice(FIRST_NAMES, size=n_rows)
df['LAST_NAME'] = np.random.choice(LAST_NAMES, size=n_rows)

# Générer les dates de naissance (cohérentes avec l'AGE existant)
# L'AGE dans le dataset semble être entre 21 et 79 ans
# We'll generate DOB based on the age and current date
base_date = datetime(2005, 9, 30)  # Date de référence du dataset

def generate_dob(age):
    """Générer une date de naissance approximative basée sur l'âge"""
    # Gérer les valeurs NaN
    try:
        if math.isnan(float(age)):
            age = np.random.randint(21, 79)
    except (ValueError, TypeError):
        age = np.random.randint(21, 79)
    
    age = int(age)
    dob = base_date - timedelta(days=age * 365 + np.random.randint(-30, 30))
    return dob.date()

df['DATE_OF_BIRTH'] = df['AGE'].apply(generate_dob)

# Générer les NAS (Numéro d'Assurance Sociale) - format fictif XXX-XXX-XXX
def generate_nas():
    """Générer un NAS fictif au format XXX-XXX-XXX"""
    part1 = np.random.randint(100, 999)
    part2 = np.random.randint(100, 999)
    part3 = np.random.randint(100, 999)
    return f"{part1}-{part2}-{part3}"

df['NAS'] = [generate_nas() for _ in range(n_rows)]

# Réorganiser les colonnes pour mettre les données sensibles en premier
cols = df.columns.tolist()
sensitive_cols = ['FIRST_NAME', 'LAST_NAME', 'DATE_OF_BIRTH', 'NAS']
other_cols = [col for col in cols if col not in sensitive_cols]
df = df[sensitive_cols + other_cols]

# Sauvegarder le dataset enrichi
output_file = "default_of_credit_card_clients_with_sensitive_data.csv"
df.to_csv(output_file, index=False)
print(f"\nDataset enrichi sauvegardé dans: {output_file}")
print(f"Colonnes sensibles ajoutées: {sensitive_cols}")
print(f"\nApperçu des données sensibles:")
print(df[['ID', 'FIRST_NAME', 'LAST_NAME', 'DATE_OF_BIRTH', 'NAS', 'AGE']].head(10))
