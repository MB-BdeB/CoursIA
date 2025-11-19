class Professeur:
    def __init__(self, nom, prenom,indice):
        self.nom = nom
        self.prenom = prenom
        self.indice = indice

    def __str__(self):
        return f'Nom: {self.nom}, Prenom: {self.prenom}, Indice satisfaction: {self.indice}'

    def connecter_zoom(self, message):
        print(f'Je suis {self.prenom} {self.nom}, je me connecte à Zoom. {message}')


    def enseigner(self) :
        print(f'{self.prenom} {self.nom} donne le cours.')
        self.indice += 10

    def donner_examen(self):
        print(f'{self.prenom} {self.nom} donner l\'examen.')
        self.indice += 30



class Etudiant:
    def __init__(self, nom, prenom,note_finale):
        self.nom = nom
        self.prenom = prenom
        self.note_finale = note_finale

    def __str__(self):
        return f'Nom: {self.nom}, Prenom: {self.prenom}, Note finale: {self.note_finale}'

    def connecter_zoom(self, message):
        print(f'Je suis {self.prenom} {self.nom}, je me connecte à Zoom. {message}')
        self.note_finale += 5

    def ecouter(self) :
        print(f'{self.prenom} {self.nom} écoute le cours.')
        self.note_finale += 10

    def faire_examen(self):
        print(f'{self.prenom} {self.nom} fait l\'examen.')
        self.note_finale += 20

