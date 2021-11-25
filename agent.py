import numpy as np

from actif import Actif
from compte import Compte
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


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
        if day % 3 == 0 and self.compte.can_sell(actif.name, 1):
            self.compte.sell_actif(actif.name, 1, actif.price, day)
        elif self.compte.can_buy(actif.price, 1):
            self.compte.buy_actif(actif.name, 1, actif.price, day)

    def second_strat(self, date: int, actif: Actif):
        total = 0
        count = 0
        for i in range(1, 6):
            try:
                total += actif.price_history[date - i]
                count += 1
            except:
                pass
        try:
            moyenne_mobile = total / count
        except:
            moyenne_mobile = actif.price
        if moyenne_mobile > actif.price and self.compte.can_buy(actif.price, 1):
            self.compte.buy_actif(actif.name, 1, actif.price, date)
        elif self.compte.can_sell(actif.name, 1):
            self.compte.sell_actif(actif.name, 1, actif.price, date)
        else:  # Au lieu de ne rien faire on achete
            if self.compte.can_buy(actif.price, 1):
                self.compte.buy_actif(actif.name, 1, actif.price, date)

    #Uniquement des bull, centrées en le prix actuel
    def third_strat(self,date: int, actif: Actif):
        periode = 3
        if date%periode == 0:
            self.compte.add_obligation(date, actif.name, 1, actif.price, date + periode)
            self.compte.add_obligation(date, actif.name, -1, actif.price * 1.5, date + periode)
        self.compte.resolve_obligation(date)
        print(actif.price)

    def plot_compte(self, plot_obligation=False):
        x = list(range(min(self.compte.historique), max(self.compte.historique)+1))
        # x = np.linspace(1, len(self.compte.historique)+1, len(self.compte.historique)+1)
        y = np.zeros_like(x)
        y1 = np.zeros_like(x)
        y2 = np.zeros_like(x)
        c = np.empty_like(x, dtype=str)
        for i, date in enumerate(x):
            try:
                y[i] = self.compte.historique_credit[date]
            except:
                pass
            if date in self.compte.historique:
                for actif in self.compte.historique[date].keys():
                    try:
                        y1[i] += self.compte.historique[date][actif][0]  # * self.compte.historique[date][actif][1]
                    except:
                        pass
            if date in self.compte.historique_obligation:
                for actif in self.compte.historique_obligation[date].keys():
                    try:
                        y2[i] += self.compte.historique[date][actif][0]
                    except:
                        pass
            if y1[i] > 0:
                c[i] = 'green'
            elif y1[i] < 0:
                c[i] = 'red'
            else:
                c[i] = 'yellow'
        # y = self.compte.historique_credit.values()
        fig, ax1 = plt.subplots()
        ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax1.set_xlim(xmin=0, xmax=max(x)+1)
        color = 'blue'
        ax1.set_xlabel('jours')
        ax1.set_ylabel('euros', color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.plot(x, y, color=color, label = 'portefeuille')
        ax2 = ax1.twinx()
        # color = 'orange'
        ax2.set_ylabel('vente')
        ax2.tick_params(axis='y')
        ax2.scatter(x, y1, marker='x', c=c, label='achats/ventes')
        if plot_obligation:
            ax2.scatter(x, y2, marker='1', c=c, label='obligation')

        fig.tight_layout()
        # todo faire de jolie plot, afficher ACHAT OU VENTE
        ax2.legend()
        ax1.legend()
        ax1.grid(visible=True, axis="y", linestyle='-')
        plt.show()
