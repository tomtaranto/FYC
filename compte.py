class Compte():
    def __init__(self, credit: float, date_creation: int):
        self.credit = credit
        self.date_creation = date_creation
        self.actifs = dict()  # nom_actif : quantité
        self.historique = dict()  # date : nom_actif : quantite, prix
        self.historique_credit = {date_creation: credit}  # date : credit
        self.obligation = dict()  # nom_actif : quantité, prix, date execution, date achat
        self.historique_obligation = dict()  # date achat : nom_actif : list(quantite, prix, date execution)
        self.grecques = None

    def get_credit(self) -> float:
        return self.credit

    def change_credit(self, credit) -> None:
        self.credit += credit

    def get_date_creation(self) -> int:
        return self.date_creation

    def get_actifs(self) -> dict:
        return self.actifs

    # On ajoute un actif (on achete une 'quantite' d'actif 'nom' au prix unitaire 'prix' à la date 'date')
    def buy_actif(self, nom: str, quantite: int, prix: float, date: int):
        # si le nom est déjà une clé du dict
        if nom in self.actifs:
            self.actifs[nom] += quantite
        else:  # sinon
            self.actifs[nom] = quantite

        # on ajoute dans l'historique l'achat effectuer
        if date in self.historique:
            self.historique[date][nom] = [quantite, prix]
        else:
            self.historique[date] = dict()
            self.historique[date][nom] = [quantite, prix]

        self.change_credit(-(prix * quantite))

        self.historique_credit[date] = self.credit


    # On supprime un actif (on vend une 'quantite' d'actif 'nom' au prix unitaire 'prix' à la date 'date')
    # quantite > 0
    def sell_actif(self, nom: str, quantite: int, prix: float, date: int) -> None:
        if nom in self.actifs:
            self.actifs[nom] -= quantite

        # on ajoute dans l'historique la vente effectuer
        if date in self.historique:
            self.historique[date][nom] = [-quantite, prix]
        else:
            self.historique[date] = dict()
            self.historique[date][nom] = [-quantite, prix]

        self.change_credit(prix * quantite)
        self.historique_credit[date] = self.credit

    # APPELEZ OBLIGATOIREMENT POUR CHAQUE ACHAT (check si on peut acheter)
    def can_buy(self, prix: float, quantite: int):
        return abs(self.get_credit()) >= abs(prix * quantite)

    # APPELEZ OBLIGATOIREMENT POUR CHAQUE VENTE (check si on peut vendre)
    def can_sell(self, nom: str, quantite: int):
        if nom in self.actifs:
            if self.actifs[nom] >= quantite:
                return True
        return False

    def get_historique(self) -> dict:  # todo changer le type de retour
        return self.historique

    # On ajoute une obligation
    def add_obligation(self, date_achat: int, nom: str, quantite: int, prix: float, date_execution: int) -> None:
        # si le nom est deja une clé du dict
        if nom in self.obligation:
            self.obligation[nom].append([quantite, prix, date_achat, date_execution])
        else:
            self.obligation[nom] = []
            self.obligation[nom].append([quantite, prix, date_achat, date_execution])

        if date_achat in self.historique_obligation:
            if nom in self.historique_obligation[date_achat]:
                self.historique_obligation[date_achat][nom].append([quantite, prix, date_execution])
            else:
                self.historique_obligation[date_achat][nom] = []
                self.historique_obligation[date_achat][nom].append([quantite, prix, date_execution])
        else:
            self.historique_obligation[date_achat] = dict()
            self.historique_obligation[date_achat][nom] = []
            self.historique_obligation[date_achat][nom].append([quantite, prix, date_execution])

    def get_obligation(self) -> dict:
        return self.obligation

    def get_grecques(self) -> dict:
        return self.grecques
