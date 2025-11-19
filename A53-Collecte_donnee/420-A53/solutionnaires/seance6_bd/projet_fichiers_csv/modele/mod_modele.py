class Article:
    def __init__(self, titre, qte, prix ):
        self.titre = titre
        self.qte = qte
        self.prix  = prix

    def __str__(self):
        return f'{self.titre}|{self.qte}|{self.prix} '

class RegistreArticle:
    def __init__(self):
        self.liste_articles = []

    def ajouter_article(self, article):
        self.liste_articles.append(article)

    def afficher_articles(self):
        for article in self.liste_articles:
            print(article)

