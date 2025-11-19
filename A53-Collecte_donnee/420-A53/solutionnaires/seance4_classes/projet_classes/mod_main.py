from modele.mod_classes import Etudiant, Professeur


def main():
    #Creation objet
    objE = Etudiant('Flouflou','Alain',0.0)
    objP = Professeur('Flouclair','Annie',0.0)
    print('Avant collaboration')
    print(objE)
    print(objP)
    print('=='*50)
    objP.connecter_zoom('Professeur')
    objE.connecter_zoom('Student')
    objP.enseigner()
    objE.ecouter()
    objP.donner_examen()
    objE.faire_examen()
    print('Apres collaboration')
    print(objE)
    print(objP)

if __name__ == '__main__':
    main()