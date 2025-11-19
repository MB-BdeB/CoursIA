import sqlite3
#DDL  creation de la table usagers

cde_ddl='''
create table if not exists usagers (
    id integer primary key autoincrement,
    nom text not null,
    age integer not null
)'''

#creer la connexion a la bd
con = sqlite3.connect('ma_table.db')
curseur = con.cursor()

#creer la table
curseur.execute(cde_ddl)

#inserer des donnees dans la table
cde_ins ='''insert into usagers (nom, age) values (?,?)'''
nom = input("Entrez le nom de usager:\n")
age = int(input("Entrez l'age de lusager:"))
curseur.execute(cde_ins, (nom, age))
con.commit()
#requeter les donnees de la table
#modifier une donnee dans la table
con.close()


#DDL  creation de la table etudiant

cde_ddl='''
create table if not exists etudiant (
    id integer primary key autoincrement,
    nom text not null,
    age integer not null
)'''

#creer la connexion a la bd
con = sqlite3.connect('school.db')
curseur = con.cursor()

#creer la table
curseur.execute(cde_ddl)

#inserer des donnees dans la table
cde_ins ='''insert into etudiant (nom. age) values (?,?)'''
nom = input("Entrez le nom de etudiant:\n")
age = int(input("Entrez l'age de etudiant:"))
curseur.execute(cde_ins, (nom, age))
con.commit()
#requeter les donnees de la table

#modifier une donnee dans la table
con.close()