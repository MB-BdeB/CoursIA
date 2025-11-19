#ETL de base
from iofichiers.mod_fichiers import lire_data, ecrire_data, ecrire_data_csv
from modele.mod_modele import RegistreArticle
from utils.mod_transformation import transf_maj, transf_rabais

def saisir_parametre():
    qte_min = int(input('Quantité minimum : '))
    rabais = float(input('Rabais : '))
    return qte_min, rabais


listing = RegistreArticle()
#Lecture de fichier
lire_data ('c:\\temp\\data.csv', listing)
print('='*50)
print('Extraction')
print('='*50)
listing.afficher_articles( )
#transformation majuscule
transf_maj(listing)
#transformation de rabais
qte_min, rabais = saisir_parametre()
transf_rabais(listing, qte_min, rabais)
print('='*50)
print('Transformation')
print('='*50)
listing.afficher_articles( )

#ecriture
print('='*50)
print('Loading vers fichier')
print('='*50)
# ecrire_data ('c:\\temp\\data2.csv', listing)
ecrire_data_csv ('c:\\temp\\data2.csv', listing)
#TODO vers table BD