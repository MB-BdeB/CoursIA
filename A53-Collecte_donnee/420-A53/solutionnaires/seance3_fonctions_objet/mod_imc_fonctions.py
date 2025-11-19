risque =['Accru','Moindre','Accru','Élevé','Très élevé',
'Extrêmement élevé']
classification =['Poids insuffisant',
'Poids normal','Excès de poids','Obésité, classe I','Obésité, classe II',
'Obésité, classe III']

#Calcul IMC

def saisir_valeur(message:str)->float:
    valeur = 0
    while valeur <= 0:
        valeur = float(input(message))
    return valeur






def calculer_imc(poids, taille):
    return poids / (taille ** 2)


def afficher_resultat(imc):
    print(f"Votre IMC est de :{imc:5.2f} ")


def determiner_indice(imc):
    # #Utilisation des tests
    if imc < 18.5:
        indice = 0
    elif imc < 25:
        indice = 1
    elif imc < 30:
        indice = 2
    elif imc < 35:
        indice = 3
    elif imc < 40:
        indice = 4
    else:
        indice = 5
    return indice


def afficher_risque_classe(indice):
    print(f"Votre risque: {risque[indice]}")
    print(f"Votre classification: {classification[indice]}")


def main():
    #Saisie du poids
    poids = saisir_valeur("Entrez votre poids en kg : ")
    #Saisie de la taille
    taille = saisir_valeur("Entrez votre taille en m : ")
    #Calcul de l'IMC
    imc = calculer_imc(poids, taille)
    #Affichage du résultat
    afficher_resultat(imc)
    #Determination de l'indice de risque et de la classification
    indice = determiner_indice(imc)
    #Affichage du risque et de la classification
    afficher_risque_classe(indice)

if __name__ == '__main__':
    main()
