class Contribuable:
    def __init__(self, nom, prenom, montant, retrait):
        self.nom = nom
        self.prenom = prenom
        self.montant = montant
        self.retrait = retrait
        self.impot = 0

    def __str__(self):
        return f"{self.nom} {self.prenom} - Montant: {self.montant}, Retrait: {self.retrait}, Impôt: {self.impot:.2f}"

class RegistreContribuable:
    def __init__(self):
        self.contribuables = []

    def ajouter_contribuable(self, contribuable):
        self.contribuables.append(contribuable)

    def afficher_contribuables(self):
        for contribuable in self.contribuables:
            print(contribuable)