# fin = open('toto.txt')
# for ligne in fin:
#     print(ligne)
# fin.close()
from modele.mod_classes import Employe, RegistreEmployes

registre = RegistreEmployes() # liste d'employes
with open('toto.txt') as fin:
        for ligne in fin:
            token = ligne.split()# token[0] code et token[1] nom
            emp = Employe(token[0], token[1])
            registre.ajouter(emp)
print("=" * 50)
registre.afficher()
#Ecrire le contenu du registre dans le fichier de sortie
with open('sortie.txt', 'w') as fout:
    for tmp in registre.liste:
        fout.write(str(tmp.nom.upper()) +';'+emp.code+ "\n")
