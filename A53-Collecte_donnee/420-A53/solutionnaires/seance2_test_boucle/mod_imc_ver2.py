#Calcul IMC
poids = float(input("Entrez votre poids en kg : "))
taille = float(input("Entrez votre taille en m : "))
imc = poids / (taille ** 2)
print(f"Votre IMC est de :{imc:5.2f} ")


# #Utilisation des tests
if imc < 18.5:
    message = 'Accru'
elif imc < 25:
    message = 'Moindre'
elif imc < 30:
    message = 'Accru'
elif imc < 35:
    message = 'Élevé'
elif imc < 40:
    message = 'Très élevé'
else:
    message='Extrêmement élevé'

print(f"Votre risque: {message}")


