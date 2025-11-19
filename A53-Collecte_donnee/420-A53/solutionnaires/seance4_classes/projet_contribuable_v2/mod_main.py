from mod_utils import saisir_infos_contribuable, calculer_revenu, calculer_impot, afficher_menu
from modele.mod_classes import RegistreContribuable

def main():
    #Creer l'objet de type RegistreContribuable
    listing = RegistreContribuable()
    #Afficher le menu
    option = afficher_menu()
    while option in [1,2]:
        if option == 1:#contribuable saisie et impot
            # Demander les infos contribuable
            contribuable = saisir_infos_contribuable()

            # Calculer l'impot
            revenu_reel = calculer_revenu(contribuable)
            contribuable.impot = calculer_impot(revenu_reel)

            # Afficher l'impot
            print(f"Impôt à payer: {contribuable.impot:.2f}")
            # Ajouter dans le registre
            listing.ajouter_contribuable(contribuable)


        elif option == 2:#Affichage de tous les contribuables
            # Afficher le registre
            print('=' * 40)
            print("Registre des contribuables:")
            listing.afficher_contribuables()

        option = afficher_menu()




if __name__ == '__main__':
    main()