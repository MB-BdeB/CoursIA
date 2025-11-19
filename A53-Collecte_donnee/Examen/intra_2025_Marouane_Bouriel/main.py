from utils.utils import*

def main():
    
    print("Bienvenue dans le programme de transformation des données du manège !")

    fichier_source = "fichiers_donnees/maneges.csv"
    fichier_destination = "fichiers_donnees/maneges_filetered.csv"

    champs_a_conserver = ["Parc", "Type", "Ouvert", "Vitesse"]

    # Lire le fichier source 
    en_tete_filtre, lignes_filtrees = lire_fichier_et_filtrer_colonnes(fichier_source, champs_a_conserver)


    if en_tete_filtre and lignes_filtrees:
        print(f"Écriture dans le fichier : {fichier_destination}")
        ecrire_fichier(fichier_destination, en_tete_filtre, lignes_filtrees)
        print(f"Transformation terminée ! {len(lignes_filtrees)+1} lignes ont été traitées.")
    else:
        print("Aucune donnée n'a été traitée.")

    ecrire_fichier_sqlite("fichiers_donnees/maneges.db", fichier_destination, champs_a_conserver)

# Appeler la fonction principale
if __name__ == "__main__":
    main()