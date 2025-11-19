import csv
import sqlite3

def lire_fichier_et_filtrer_colonnes(fichier_source, champs_a_conserver : list):

    
    with open(fichier_source, mode='r') as source:
        # remplacer pour ';'
        lecteur_csv = csv.reader(source, delimiter=';')
        
        # en-tête 
        en_tete = next(lecteur_csv)
        print(f"En-tête du fichier source : {en_tete}")
        
        # Nettoyer les espaces pour viteesse
        en_tete = [col.strip() for col in en_tete]
        
        # Trouver les indices pour les capter les valeurs de ligne
        indices_champs = []
        for champ in champs_a_conserver:
            if champ in en_tete:
                indices_champs.append(en_tete.index(champ))
        
        # Filtrer l'en-tête
        en_tete_filtre = [en_tete[i] for i in indices_champs]
        print(f"Indices des champs à conserver : {indices_champs}")
        print(f"En-tête originale : {en_tete}")
        
        # Filtrer les lignes
        lignes_filtrees = [
            [ligne[i] for i in indices_champs] for ligne in lecteur_csv
        ]
        
        return en_tete_filtre, lignes_filtrees
  

def ecrire_fichier(fichier_destination, en_tete, lignes):
    with open(fichier_destination, mode='w', newline='') as destination:
        writer = csv.writer(destination, delimiter=';')
        
        # Écrire l'en-tête
        writer.writerow(en_tete)
        
        # Écrire les lignes
        for ligne in lignes:
            writer.writerow(ligne)

def ecrire_fichier_sqlite(fichier_destination, fichier_source, en_tete):

    conn = sqlite3.connect(fichier_destination)
    cursor = conn.cursor()

    colonnes_sql = ", ".join([f"{col} TEXT" for col in en_tete])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS MANEGES ({colonnes_sql})")

    en_tete, lignes = lire_fichier_et_filtrer_colonnes(fichier_source, en_tete)
    print(f"En-tête pour SQLite : {en_tete}")

    for ligne in lignes:
        cursor.execute(f"INSERT INTO MANEGES ({', '.join(en_tete)}) VALUES ({', '.join(['?'] * len(en_tete))})", ligne)


    conn.commit()
    conn.close()