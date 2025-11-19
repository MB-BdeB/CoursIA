def mettre_maj(registre):
    """
    Met à jour les noms des employés dans le registre en les mettant en majuscules.
    """
    for emp in registre.liste:
        emp.nom = emp.nom.upper()