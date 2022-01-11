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
        for agent in self.agents:
            credit = agent.compte.get_credit()
            print("credit avant solve : ", credit)
            self.resolve_obligation(agent, self.current_time)
            print("revenu de l operation : ", agent.compte.get_credit() - credit)
        self.current_time += 1
        for actif in self.actifs:
            actif.update_from_date(self.current_time)
        # TODO pour chaque agent, cloturer les positions sur obligation

    def resolve_obligation(self, agent: Agent, current_date: int):
        # nom_actif : [quantité, prix, date execution, date achat, type]
        # print(agent.compte.obligation)
        for actif_name in agent.compte.obligation:
            # On cherche la correspondance entre l actif de l obligation et l actif reel
            idx_actif = 0
            for i, actif in enumerate(self.actifs):
                if actif.name == actif_name:
                    idx_actif = i
                    break
            for i in range(len(agent.compte.obligation[actif_name])):
                if agent.compte.obligation[actif_name][i][
                    2] == current_date:  # Si la date d'execution est la date du jour
                    if agent.compte.obligation[actif_name][i][0] > 0:  # Si c'est un ordre d'achat
                        # Si utiliser l option est interessant
                        if agent.compte.obligation[actif_name][i][1] < self.actifs[idx_actif].price:
                            print("l option est utilisee")
                            if agent.compte.obligation[actif_name][i][4] == 'achat':  # J'ai achete une option d acheter
                                print("resolution offre achat call")
                                agent.compte.buy_actif(actif_name, agent.compte.obligation[actif_name][i][0],
                                                       agent.compte.obligation[actif_name][i][1],
                                                       current_date)

                            if agent.compte.obligation[actif_name][i][4] == 'vente':  # J'ai vendu l option d'acheter
                                print("resolution offre vente call")
                                # On ne fait pas le check de si on peut vendre
                                agent.compte.sell_actif(actif_name, agent.compte.obligation[actif_name][i][0],
                                                        agent.compte.obligation[actif_name][i][1], current_date)
                        else: # Utiliser l option n est pas interessant
                            agent.compte.do_nothing(current_date)


                    else:
                        # Si utiliser l option est interessant
                        if agent.compte.obligation[actif_name][i][1] > self.actifs[idx_actif].price:
                            if agent.compte.obligation[actif_name][i][4] == 'achat':  # J'ai achete une option de vente
                                agent.compte.sell_actif(actif_name, -agent.compte.obligation[actif_name][i][0],
                                                        agent.compte.obligation[actif_name][i][1], current_date)
                            if agent.compte.obligation[actif_name][i][4] == 'vente':  # J'ai vendu une option de vente
                                agent.compte.buy_actif(actif_name, agent.compte.obligation[actif_name][i][0],
                                                       agent.compte.obligation[actif_name][i][1],
                                                       current_date)
                        else:
                            agent.compte.do_nothing(current_date)
        return
