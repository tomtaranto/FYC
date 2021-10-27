class Compte():
    def __init__(self, credit: float, date_creation: int):
        self.credit = credit
        self.date_creation = date_creation
        self.actifs = dict()  # nom_actif : quantité
        self.historique = dict()  # date : crédit dépensé ou crédit reçu
        self.obligation = dict()  # nom_actif : quantité, prix date execution, date achat
        self.grecques = None

    def get_credit(self) -> float:
        return self.credit

    def add_credit(self, credit) -> None:
        self.credit += credit

    def lose_credit(self, credit) -> None:
        self.credit -= credit

    def get_date_creation(self) -> int:
        return self.date_creation

    def get_actifs(self) -> dict:
        return self.actifs

    # On ajoute un actif (on achete une 'quantite' d'actif 'nom' au prix 'prix' à la date 'date'
    def add_actif(self, nom: str, quantite: int, prix: float, date: int):
        # si le nom est déjà une clé du dict
        if nom in self.actifs:
            self.actifs[nom] += quantite
        else:  # sinon
            self.actifs[nom] = quantite

        # si la date de l'achat de l'actif est déjà une clé dans le dict
        if date in self.historique:
            self.historique[date].append(-(prix * quantite))  # on met dans l'historique l'achat effectuer
            self.lose_credit(prix * quantite)  # on met à jour nos crédits
        else:
            self.historique[date] = []
            self.historique[date].append(-(prix * quantite))
            self.lose_credit(prix * quantite)

    def sell_actif(self, nom: str, quantite: int, prix: float, date: int) -> None:
        if nom in self.actifs:
            if quantite <= self.actifs[nom]:
                self.actifs[nom] -= quantite
                # si la date de l'achat de l'actif est déjà une clé dans le dict
                if date in self.historique:
                    self.historique[date].append(prix * quantite)  # on met dans l'historique la vente effectuer
                    self.add_credit(prix * quantite)  # on met à jour nos crédits
                else:
                    self.historique[date] = []
                    self.historique[date].append(prix * quantite)
                    self.add_credit(prix * quantite)
            else:
                print("ERROR, tu possèdes " + str(self.actifs[nom]) + " actions " + str(
                    nom) + " mais tu veux vendre " + str(quantite) + " actions.")

        else:
            print("Tu ne possèdes pas d'actif :", nom)

    def get_historique(self) -> dict:
        return self.historique

    # On ajoute une obligation
    def add_obligation(self, date_achat: int, nom: str, quantite: int, prix: float, date_execution: int) -> None:
        # si le nom est deja une clé du dict
        if nom in self.obligation:
            self.historique[nom].append([quantite, prix, date_achat, date_execution])
        else:
            self.historique[nom] = []
            self.historique[nom].append([quantite, prix, date_achat, date_execution])

    def get_obligation(self) -> dict:
        return self.obligation

    def get_grecques(self) -> dict:
        return self.grecques
