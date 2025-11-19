from mod_utils import saisir_infos_contribuable, calculer_revenu, calculer_impot
from modele.mod_classes import RegistreContribuable





def main():
    #Creer l'objet de type RegistreContribuable
    listing = RegistreContribuable()

    #Demander les infos contribuable
    contribuable = saisir_infos_contribuable()

    #Calculer l'impot
    revenu_reel = calculer_revenu(contribuable)
    impot = calculer_impot(revenu_reel)

    #Afficher l'impot
    print(f"Impôt à payer: {impot:.2f}")
    #Ajouter dans le registre
    listing.ajouter_contribuable(contribuable)
    #Afficher le registre
    print('='*50)
    print("Registre des contribuables:")
    listing.afficher_contribuables()



if __name__ == '__main__':
    main()