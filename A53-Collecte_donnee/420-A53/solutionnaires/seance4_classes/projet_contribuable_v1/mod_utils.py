from modele.mod_classes import Contribuable


def calculer_taux(revenu_reel):
    #voir la regle de calcul
    if revenu_reel < 10000:
        return 0.15
    elif revenu_reel < 30000:
        return 0.25
    elif revenu_reel <= 100000:
        return 0.35
    else:
        return 0.55


def calculer_impot(revenu_reel):
    taux = calculer_taux(revenu_reel)
    return revenu_reel * taux

def saisir_infos_contribuable():
    nom = input("Nom: ")
    prenom = input("Prénom: ")
    montant = float(input("Montant: "))
    retrait = float(input("Retrait: "))
    return Contribuable(nom, prenom, montant, retrait)

def calculer_revenu(contribuable):
    return contribuable.montant*.85 - contribuable.retrait