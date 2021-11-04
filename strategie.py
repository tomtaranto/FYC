from actif import Actif
from agent import Agent


class Strategie():
    def __init__(self):
        self.first_stategie = self.first_strat

    # Strategie attendue pour l'exercice 1
    def first_strat(self, day: int, actif: Actif, agent: Agent):
        agent.compte.add_actif(actif.name, 1, actif.price, day)
        if day % 3 == 0:
            agent.compte.sell_actif(actif.name, 1, actif.price, day)
