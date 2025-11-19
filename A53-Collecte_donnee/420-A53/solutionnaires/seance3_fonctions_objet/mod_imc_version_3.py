risque =['Accru','Moindre','Accru','Élevé','Très élevé',
'Extrêmement élevé']
classification =['Poids insuffisant',
'Poids normal','Excès de poids','Obésité, classe I','Obésité, classe II',
'Obésité, classe III']

#Calcul IMC
poids = 0
while poids <= 0:
    poids = float(input("Entrez votre poids en kg : "))

taille = 0
while taille <= 0:
    taille = float(input("Entrez votre taille en m : "))

imc = poids / (taille ** 2)

print(f"Votre IMC est de :{imc:5.2f} ")


# #Utilisation des tests
if imc < 18.5:
    indice = 0
elif imc < 25:
    indice = 1
elif imc < 30:
    indice = 2
elif imc < 35:
    indice = 3
elif imc < 40:
    indice = 4
else:
    indice = 5

print(f"Votre risque: {risque[indice]}")
print(f"Votre classification: {classification[indice]}")


