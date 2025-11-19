#DDL creation table USagers
import sqlite3

cde_ddl ='''
CREATE TABLE if not exists Usagers(
    ID INTeger PRIMARY KEY AUTOINCREMENT,
    Nom TEXT,
    Age INTeger
)'''

#Créer la connexion à la base de données
con = sqlite3.connect('ma_base.db')
#Créer le curseur
curseur = con.cursor()
#Créer la table USagers
curseur.execute(cde_ddl)

#Insertion dans la table USagers
cde_ins = '''insert into usagers (Nom, Age) values (?, ?)'''
nom = input("Entrez le nom de l'usager : ")
age = int(input("Entrez l'âge de l'usager : "))
curseur.execute(cde_ins, (nom, age))
con.commit()

print('='*50)
#Select de la table USagers
requete = '''select id, nom, age from usagers'''
curseur.execute(requete)
for rec in curseur:
    print(f'{rec[0]}  {rec[1]}  {rec[2]}')
con.close()