def transf_maj(listing):
    for art in listing.liste_articles:
        art.titre = art.titre.upper()

def transf_rabais(listing,qte_min, rabais):
    for art in listing.liste_articles:
        if art.qte < qte_min:
            art.prix = round(art.prix - (art.prix * rabais / 100),2)