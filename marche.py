from actif import Actif
from agent import Agent


class Marche():
    def __init__(self):
        self.current_time = 0
        self.actifs = []
        self.agents = []

    # Ajouter un actif
    def add_actif(self, name: str, quantity: float, price: float):
        self.actifs.append(Actif(name, quantity, price, dict()))

    # Ajouter un agent
    def add_agent(self, agent_type: str, agent_name: str, wallet: float):
        self.agents.append(Agent(agent_name, agent_type, wallet))

    # Passer au jour suivant
    def next_day(self):
        self.current_time += 1
        for actif in self.actifs:
            actif.update_from_date(self.current_time)
        # TODO pour chaque agent, cloturer les positions sur obligation
