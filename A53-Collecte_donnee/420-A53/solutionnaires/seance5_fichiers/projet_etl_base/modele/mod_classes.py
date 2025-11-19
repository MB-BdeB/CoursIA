class Employe:
    def __init__(self, code, nom):
        self.nom = nom
        self.code = code

    def __str__(self):
        return f"Employe {self.code} : {self.nom}"

class RegistreEmployes:
    def __init__(self):
        self.liste = []

    def ajouter(self, emp):
        self.liste.append(emp)

    def afficher(self):
        for emp in self.liste:
            print(emp)