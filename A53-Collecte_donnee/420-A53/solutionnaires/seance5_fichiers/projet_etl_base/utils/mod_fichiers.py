from modele.mod_classes import Employe


def lire_data(fichier, registre):
    with open(fichier) as fin:
        for ligne in fin:
            token = ligne.split()  # token[0] code et token[1] nom
            emp = Employe(token[0], token[1])
            registre.ajouter(emp)

def ecrire_data(fichier, registre):
    with open(fichier, 'a') as fout:
        for tmp in registre.liste:
            fout.write(str(tmp.nom) + ';' + tmp.code + "\n")