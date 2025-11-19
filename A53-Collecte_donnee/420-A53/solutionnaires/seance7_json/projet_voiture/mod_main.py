import json
class Voiture:
    def __init__(self, marque, modele, transmission, couleur,accessoires={},
                 porte=4 ):
        self.marque = marque
        self.modele = modele
        self.transmission = transmission
        self.couleur = couleur
        self.porte = porte
        self.accessoires = accessoires

#instancier une voiture
voit = Voiture("Nissan", "Versa", "Automatique",
               "Orange", {"toit_ouvrant": True})
#afficher les attributs de la voiture
print(vars(voit))
#Sauvegarder la voiture dans un fichier
with open("objVoiture.json", "w") as f :
    json.dump(vars(voit), f, indent=3)
