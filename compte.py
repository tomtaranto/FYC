from scipy.integrate import quad
from scipy import stats
import numpy as np

from actif import Actif


# TODO On a fait uniquement ACHETER des options d'achat et de vente
# TODO OR !!!!
# TODO les strategies se basent sur le fait qu'on puisse VENDRE en meme temps des options d'achat et de vente
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

    def get_historique(self) -> dict:  # todo changer le type de retour
        return self.historique

    # On ajoute une obligation
    # TODO Ajouter le type (achat/vente)
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
        # TODO refaire en gerant le type achat vente
        '''
        if quantite > 0:  # Option achat/Call
            price: float = max(0.0, actif.price - prix)
        else:  # Option de vente / Put
            price = self.compute_price_obligation(actif.price, date_execution, prix, 0.0001, actif.volatility, date_achat)
        self.change_credit(-abs(price))
        self.historique_credit[date_achat] = self.credit
        '''
        # Prix unitaire de l'option
        if quantite > 0:
            price: float = self.compute_price_obligation(actif.price, date_execution, prix, 0.000001, actif.volatility,
                                                         date_achat)
        else:
            price: float = self.compute_price_obligation(actif.price, date_execution, prix, 0.000001, actif.volatility,
                                                         date_achat)
        # On mutliplie le prix par la quantite d action que l on souhaite
        price = price * quantite
        print("prix : ", price, "type : ", type)
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

    # TODO ajouter deux conditions pour vérifier si il est interessant d exercer l option
    # def resolve_obligation(self, current_date: int):
    #     # nom_actif : [quantité, prix, date execution, date achat, type]
    #     for actif_name in self.obligation:
    #         for i in range(len(self.obligation[actif_name])):
    #             if self.obligation[actif_name][i][2] == current_date:  # SI la date d'execution est la date du jour
    #                 """
    #                 if self.obligation[actif_name][i][0] > 0:  # Si c'est un ordre d'achat
    #                     self.buy_actif(actif_name, self.obligation[actif_name][i][0], self.obligation[actif_name][i][1],
    #                                    current_date)
    #                 else:
    #                     self.sell_actif(actif_name, -self.obligation[actif_name][i][0],
    #                                     self.obligation[actif_name][i][1], current_date)
    #                 """
    #                 if self.obligation[actif_name][i][0] > 0:  # Si c'est un ordre d'achat
    #                     if self.obligation[actif_name][i][4]=='achat': # J'ai achete une option d acheter
    #                         # Ajouter un check pour verifier si l obligation est interessant par rapport au prix reel de l actif
    #                         pass
    #                     if self.obligation[actif_name][i][4]=='vente': # J'ai vendu l option d'acheter
    #                         # On check si le vendeur a interet a acheter
    #                         pass
    #
    #                     self.buy_actif(actif_name, self.obligation[actif_name][i][0], self.obligation[actif_name][i][1],
    #                                    current_date)
    #                 else:
    #                     if self.obligation[actif_name][i][4] == 'achat':  # J'ai achete une option de vente
    #                         # On check si le vendre au prix est plus interessant que le vendre au prix du marche
    #                         pass
    #                     if self.obligation[actif_name][i][4] == 'vete':  # J'ai vendu une option de vente
    #                         # On check si le vendre au prix est plus interessant que le vendre au prix du marche
    #                         pass
    #                     self.sell_actif(actif_name, -self.obligation[actif_name][i][0],
    #                                     self.obligation[actif_name][i][1], current_date)
    #     return

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
