class Contribuable:
    pass

class RegistreContribuable:
    def __init__(self):
        self.contribuables = []

    def ajouter_contribuable(self, contribuable):
        self.contribuables.append(contribuable)

    def afficher_contribuables(self):
        for contribuable in self.contribuables:
            print(contribuable)