from scipy.integrate import quad
from scipy import stats
import numpy as np

from actif import Actif

class Compte():
    def __init__(self, credit: float, date_creation: int):
        self.credit = credit
        self.date_creation = date_creation
        self.actifs = dict()  # nom_actif : quantité
        self.historique = dict()  # date : nom_actif : quantite, prix
        self.historique_credit = {date_creation: credit}  # date : credit
        self.obligation = dict()  # nom_actif : list(quantité, prix, date execution, date achat, type achat vente)
        self.historique_obligation = dict()  # date achat : nom_actif : list(quantite, prix, date execution, type)
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
        else:
            self.actifs[nom] = -quantite

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

    def get_historique(self) -> dict:
        return self.historique

    # On ajoute une obligation
    def add_obligation(self, date_achat: int, actif: Actif, quantite: int, prix: float, date_execution: int,
                       type: str) -> None:
        assert type in ['achat', 'vente']
        # si le nom est deja une clé du dict
        nom = actif.name
        if nom in self.obligation:
            self.obligation[nom].append([quantite, prix, date_achat, date_execution, type])
        else:
            self.obligation[nom] = []
            self.obligation[nom].append([quantite, prix, date_achat, date_execution, type])

        if date_achat in self.historique_obligation:
            if nom in self.historique_obligation[date_achat]:
                self.historique_obligation[date_achat][nom].append([quantite, prix, date_execution, type])
            else:
                self.historique_obligation[date_achat][nom] = []
                self.historique_obligation[date_achat][nom].append([quantite, prix, date_execution, type])
        else:
            self.historique_obligation[date_achat] = dict()
            self.historique_obligation[date_achat][nom] = []
            self.historique_obligation[date_achat][nom].append([quantite, prix, date_execution, type])
        # Prix unitaire de l'option
        if quantite > 0:
            price: float = self.compute_price_obligation(actif.price, date_execution, prix, 0.000001, actif.volatility,
                                                         date_achat)
        else:
            price: float = self.compute_price_obligation(actif.price, date_execution, prix, 0.000001, actif.volatility,
                                                         date_achat)
        # On mutliplie le prix par la quantite d action que l on souhaite
        price = price * quantite
        # Si on achete une option d achat ou de vente, on perd des sous
        if type == 'achat':
            self.change_credit(-abs(price))
        # Si on vend une option d achat ou de vente, on gagne des sous
        elif type == 'vente':
            self.change_credit(abs(price))
        self.historique_credit[date_achat] = self.credit
        return

    def get_obligation(self) -> dict:
        return self.obligation

    def get_grecques(self) -> dict:
        return self.grecques


    def do_nothing(self, date: int):
        self.historique_credit[date] = self.credit

    """
    :param
    sigma : volatilite
    r : taux interet sans risque
    K prix d exerice
    T temps avant echeance
    S prix du sous jacent
    """

    def compute_price_obligation(self, S: float, execution_date: int, K: float, r: float, sigma: float,
                                 current_date: int):
        T = (execution_date - current_date) / 365
        d1: float = (np.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * np.sqrt(T))
        d2: float = d1 - sigma * np.sqrt(T)
        # price = -S * quad(norm, -np.inf, d1)[0] + K * np.exp(-r * T) * quad(norm, -np.inf, d2)[0]
        price = -S * stats.norm.cdf(-d1) + K * np.exp(-r * T) * stats.norm.cdf(-d2)
        return price


def norm(x: float):
    return np.exp(-0.5 * (x ** 2)) / (np.sqrt(2 * np.pi))
