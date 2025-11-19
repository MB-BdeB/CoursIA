import csv

from modele.mod_modele import Article


def lire_data (fichier, listing):
    with open(fichier, 'r') as f:
        for ligne in f:
            # Suppression des espaces et séparation par la virgule
            ligne = ligne.strip().split()
            # Ajout de chaque élément à la liste
            # Création d'un objet Article
            art = Article(ligne[0], int(ligne[1]), float(ligne[2]))
            listing.ajouter_article(art)

def ecrire_data (fichier, listing):
    with open(fichier, 'w', newline='\n') as fout:
        for tmp in listing.liste_articles:
            fout.write(f'{tmp.titre}|{tmp.qte}|{tmp.prix}\n')

def ecrire_data_csv(fichier, listing):
    with open(fichier, 'w', newline='\n') as fout:
        ecriteur = csv.writer(fout, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        for tmp in listing.liste_articles:
            ecriteur.writerow( (tmp.titre,tmp.qte,tmp.prix)  )

