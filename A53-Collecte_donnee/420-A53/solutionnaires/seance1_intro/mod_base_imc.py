#Calcul IMC
poids = float(input("Entrez votre poids en kg : "))
taille = float(input("Entrez votre taille en m : "))
imc = poids / (taille ** 2)
print("Votre IMC est de : ", imc)
print(f"Votre IMC est de :{imc:5.2f} ")
