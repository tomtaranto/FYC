import numpy as np

from actif import Actif
from compte import Compte
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, name: str, agent_type: str, start_credit: float):
        assert agent_type in ["human", "bot"]
        self.name = name
        self.agent_type = agent_type
        self.compte = Compte(start_credit, 0)
        self.age = 0
        self.strat = []

    # Ajout d'une strategie
    def add_strat(self, strategie):
        self.strat.append(strategie)

    # Strategie attendue pour l'exercice 1
    def first_strat(self, day: int, actif: Actif):
        if day % 3 == 0:
            self.compte.sell_actif(actif.name, 1, actif.price, day)
        else:
            self.compte.buy_actif(actif.name, 1, actif.price, day)


    def second_strat(self, date: int, actif: Actif):
        total = 0
        count = 0
        for i in range(1, 6):
            try:
                total += actif.price_history[date-i]
                count += 1
            except:
                pass
        try:
            moyenne_mobile = total / count
        except:
            moyenne_mobile = actif.price
        if moyenne_mobile > actif.price:
            self.compte.buy_actif(actif.name, 1, actif.price, date)
        else:
            self.compte.sell_actif(actif.name, 1, actif.price, date)




    def plot_compte(self):
        x = np.linspace(1, len(self.compte.historique)+1, len(self.compte.historique)+1)
        y = self.compte.historique_credit.values()
        plt.plot(x,y,marker='o')
        #todo faire de jolie plot, afficher ACHAT OU VENTE
        plt.show()

