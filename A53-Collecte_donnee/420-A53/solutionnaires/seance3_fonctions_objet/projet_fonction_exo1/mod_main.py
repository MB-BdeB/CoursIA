def choisir_option_menu():
    # 1 Kg vers livre
    # 2 Livre vers Kg
    # 3 Quitter
    pass


def saisir_valeur(param):
    pass


def convertir_poids(poids, option):
    pass


def afficher_resultat(poids, poids_converti, option):
    pass


def main():
    print('Bienvenue dans le convertisseur de poids !')
    # Demander à l'utilisateur de choisir le type de conversion
    option = choisir_option_menu()
    # Type de conversion
    while option in [1,2]:
        #Saisie du poids
        poids = saisir_valeur("Entrez le poids à convertir : ")
        #Conversion du poids
        poids_converti = convertir_poids(poids, option)
        #Affichage
        afficher_resultat(poids, poids_converti, option)
        option = choisir_option_menu()

    print('Merci d\'avoir utilisé le convertisseur de poids !')

if __name__ == '__main__':
    main()