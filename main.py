from collections import deque

import matplotlib.pyplot as plt
import numpy as np
from marche import Marche
from tqdm import tqdm
from utils import init_marche_un_actif

# Tous les jours, acheter un actif
# TOus les 3 jours vendre cet actif
"""
def exo1_fake():
    # On creer notre marche ainsi qu'une strategie simple
    marche = init_marche_un_actif()
    strategie = Strategie()
    strategie.add_strat(strategie.first_strat)
    marche.next_day()
    # On fait avancer le marche de plusieurs jours
    # TODO automatiser cela via une fonction
    for time in range(1,20):
        strategie.strat[0](marche.current_time, marche.actifs[0], marche.agents[0])
        marche.next_day()

    print(marche.agents[0].compte.historique)"""


def exo1():
    marche = Marche()
    marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_agent('human', 'Eddy', 100)
    marche.agents[0].add_strat(marche.agents[0].first_strat)
    marche.next_day()
    for time in range(1, 20):
        marche.agents[0].strat[0](marche.current_time, marche.actifs[0])
        marche.next_day()
    print(marche.agents[0].compte.historique)
    name = next(iter(marche.agents[0].compte.actifs))
    marche.agents[0].compte.sell_actif(name, marche.agents[0].compte.actifs[name], marche.actifs[0].price,
                                       marche.current_time)
    marche.agents[0].plot_compte()


def exo2():
    marche = Marche()
    marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_agent('human', 'Eddy', 100)
    marche.agents[0].add_strat(marche.agents[0].second_strat)
    marche.next_day()
    for time in range(1, 20):
        marche.agents[0].strat[0](marche.current_time, marche.actifs[0])
        marche.next_day()
    marche.agents[0].compte.sell_actif(marche.actifs[0].name, marche.agents[0].compte.actifs[marche.actifs[0].name],
                                       marche.actifs[0].price,
                                       marche.current_time)
    marche.agents[0].plot_compte()
    return


def exo3():
    marche = Marche()
    # marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_actif('lvmh', 505000000, 734.70)

    marche.add_agent('human', 'Eddy', 100)
    marche.agents[0].add_strat(marche.agents[0].third_strat)
    marche.next_day()
    for time in range(1, 6000):
        marche.agents[0].strat[0](marche.current_time, marche.actifs[0])
        marche.next_day()
    marche.agents[0].compte.sell_actif(marche.actifs[0].name, marche.agents[0].compte.actifs[marche.actifs[0].name],
                                       marche.actifs[0].price,
                                       marche.current_time)
    # print(marche.agents[0].compte.historique_obligation)
    # print(marche.agents[0].compte.actifs)
    marche.agents[0].plot_compte(plot_obligation=True)
    plt.plot(list(marche.actifs[0].price_history.values()))
    plt.show()
    return


def exo4():
    marche = Marche()
    # marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_actif('lvmh', 505000000, 734.70)
    marche.add_agent('bot', 'terminator', 100)
    marche.agents[0].add_strat(marche.agents[0].fourth_strat)
    periode = 1
    epochs = 50
    marche.agents[0].train(marche.actifs[0], 'bull', periode, epochs) # On entraine notre agent
    marche.next_day()
    inputs = deque([marche.actifs[0].price]*1000)
    for time in tqdm(range(1, 60)):
        marche.agents[0].strat[0](marche.current_time, marche.actifs[0], np.array(inputs).reshape(1,1000)/740,periode)
        marche.next_day()
        inputs.append(marche.actifs[0].price) # On ajoute le prix courant
        inputs.popleft() # On retire le prix le plus ancien
    marche.agents[0].compte.sell_actif(marche.actifs[0].name, marche.agents[0].compte.actifs[marche.actifs[0].name],
                                       marche.actifs[0].price,
                                       marche.current_time)
    # print(marche.agents[0].compte.historique_obligation)
    # print(marche.agents[0].compte.actifs)
    marche.agents[0].plot_compte(plot_obligation=True)
    plt.plot(list(marche.actifs[0].price_history.values()))
    plt.show()
    return


def test():
    marche = Marche()
    # marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_actif('lvmh', 505000000, 734.70)
    marche.add_agent('bot', 'terminator', 100)
    marche.agents[0].add_strat(marche.agents[0].fifth_strat)
    periode = 10
    epochs = 60
    marche.agents[0].train(marche.actifs[0], 'bull', periode, epochs) # On entraine notre agent
    marche.agents[0].train_strategy(marche.actifs[0], 'bull', periode, epochs) # On entraine notre agent
    marche.next_day()
    inputs = deque([marche.actifs[0].price]*1000)
    for time in tqdm(range(1, 6000)):
        marche.agents[0].strat[0](marche.current_time, marche.actifs[0], np.array(inputs).reshape(1,1000)/740,periode)
        marche.next_day()
        inputs.append(marche.actifs[0].price) # On ajoute le prix courant
        inputs.popleft() # On retire le prix le plus ancien
    print(marche.agents[0].compte.historique_obligation)
    print(marche.agents[0].compte.actifs)
    marche.agents[0].compte.sell_actif(marche.actifs[0].name, marche.agents[0].compte.actifs[marche.actifs[0].name],
                                       marche.actifs[0].price,
                                       marche.current_time)

    marche.agents[0].plot_compte(plot_obligation=True)
    plt.plot(list(marche.actifs[0].price_history.values()))
    plt.show()
    return



def main():
    # exo1()
    # exo2()
    # exo3()
    test()


if __name__ == '__main__':
    main()
