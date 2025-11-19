class Toto:
    def __init__(self, titre, note):
        self.titre = titre
        self.note = note

obj = Toto("flouflou", 90)
print(vars(obj))
import json
with open('sortie.json', 'w') as file:
    json.dump(vars(obj), file, indent=4)
