class Contribuable:
    def __init__(self, nom, prenom, montant, retrait):
        self.nom = nom
        self.prenom = prenom
        self.montant = montant
        self.retrait = retrait

    def __str__(self):
        return f"Contribuable: {self.nom} {self.prenom}, Montant: {self.montant}, Retrait: {self.retrait}"

class RegistreContribuable:
    def __init__(self):
        self.contribuables = []

    def ajouter_contribuable(self, contribuable):
        self.contribuables.append(contribuable)

    def afficher_contribuables(self):
        for contribuable in self.contribuables:
            print(contribuable)