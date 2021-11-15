from actif import Actif
from compte import Compte


# from strategie import Strategie


class Agent:
    def __init__(self, name: str, agent_type: str, start_credit: float, strat: Strategie):
        assert agent_type in ["human", "bot"]
        self.name = name
        self.agent_type = agent_type
        self.compte = Compte(start_credit, 0)
        self.age = 0
        self.strategies = [strat]


# Classe contenant les strategies
class Strategie():
    def __init__(self):
        self.first_stategie = self.first_strat
        self.strat = []

    # Ajout d'une strategie
    def add_strat(self, strategie):
        self.strat.append(strategie)

    # Strategie attendue pour l'exercice 1
    def first_strat(self, day: int, actif: Actif, agent: Agent):
        agent.compte.add_actif(actif.name, 1, actif.price, day)
        if day % 3 == 0:
            agent.compte.sell_actif(actif.name, 1, actif.price, day)


def main():
    strat = Strategie()


if __name__ == '__main__':
    main()
