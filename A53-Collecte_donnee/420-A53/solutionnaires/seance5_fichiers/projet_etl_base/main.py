
from modele.mod_classes import Employe, RegistreEmployes
from utils.mod_fichiers import lire_data, ecrire_data
from utils.mod_tranformation import mettre_maj

#LEcture du fichier d'entree
registre = RegistreEmployes() # liste d'employes
lire_data('toto.txt', registre)

#Appliquer des transformations
mettre_maj(registre)
print("=" * 50)
registre.afficher()

#Ecrire le contenu du registre dans le fichier de sortie
ecrire_data('sortie.txt', registre)
