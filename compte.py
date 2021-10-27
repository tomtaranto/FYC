class Compte():
    def __init__(self, credit, date_creation):
        self.credit = credit
        self.date_creation = date_creation
        self.actifs = dict()  # nom_actif : quantité
        self.historique = dict()  # date : crédit dépensé ou crédit reçu
        self.obligation = dict()  # date : nom_actif, quantité, prix
        self.grecques = None

    def get_credit(self):
        return self.credit

    def add_credit(self, credit):
        self.credit += credit

    def lose_credit(self, credit):
        self.credit -= credit

    def get_date_creation(self):
        return self.date_creation

    def get_actifs(self):
        return self.actifs

    def add_actif(self, nom, quantite, prix, date):
        # si le nom est déjà une clé dans le dict
        if nom in self.actifs:
            self.actifs[nom] += quantite
        else:  # sinon
            self.actifs[nom] = quantite

        # si la date de l'achat de l'actif est déjà une clé dans le dict
        if date in self.historique:
            self.historique[date].append(prix)
        else:
            self.historique[date] = []
            self.historique[date].append(prix)

    def get_historique(self):
        return self.historique

    def get_obligation(self):
        return self.obligation

    def get_grecques(self):
        return self.grecques
