from collections import deque

import matplotlib.pyplot as plt
import numpy as np
from marche import Marche
from tqdm import tqdm


# Tous les jours, acheter un actif
# TOus les 3 jours vendre cet actif
def exo1():
    marche = Marche()
    marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_agent('human', 'Eddy', 100)
    marche.agents[0].add_strat(marche.agents[0].first_strat)
    marche.next_day()
    for time in range(1, 150):
        marche.agents[0].strat[0](marche.current_time, marche.actifs[0])
        marche.next_day()
    print(marche.agents[0].compte.historique)
    name = next(iter(marche.agents[0].compte.actifs))
    marche.agents[0].compte.sell_actif(name, marche.agents[0].compte.actifs[name], marche.actifs[0].price,
                                       marche.current_time)
    marche.agents[0].plot_compte()
    print(
        f"resultat de la strategie, on passe de {100} à {marche.agents[0].compte.get_credit()} euros en {150 - 1 + 1} jours soit {(marche.agents[0].compte.get_credit() - 100) / (150 - 1 + 1)} euros par jour moyenne")


# Utiliser la moyenne mobile pour determiner si on achete ou vend des actions
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
    print(f"resultat de la strategie, on passe de {100} à {marche.agents[0].compte.get_credit()} euros en {20-1+1} jours soit {(marche.agents[0].compte.get_credit() - 100)/(20-1+1)} euros par jour moyenne")
    return

# Creer une strategie Bull
def exo3():
    marche = Marche()
    # marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_actif('lvmh', 505000000, 734.70)
    marche.add_agent('human', 'Eddy', 6000)
    marche.agents[0].add_strat(marche.agents[0].third_strat)
    marche.next_day()
    for time in tqdm(range(1, 6000)):
        marche.agents[0].strat[0](marche.current_time, marche.actifs[0])
        marche.next_day()
    # print(marche.agents[0].compte.historique_obligation)
    # print(marche.agents[0].compte.actifs)
    # marche.agents[0].compte.sell_actif(marche.actifs[0].name, marche.agents[0].compte.actifs[marche.actifs[0].name],
    #                                    marche.actifs[0].price,
    #                                    marche.current_time)

    marche.agents[0].plot_compte(plot_obligation=False)
    plt.plot(list(marche.actifs[0].price_history.values()))
    plt.show()
    print(f"resultat de la strategie, on passe de {100} à {marche.agents[0].compte.get_credit()} euros en {6000 - 1 + 1} jours soit {(marche.agents[0].compte.get_credit() - 100) / (6000 - 1 + 1)} euros par jour moyenne")

    return

# Entrainer un permier agent à trouver les bons prix des bulls
def exo4():
    marche = Marche()
    # marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_actif('lvmh', 505000000, 734.70)
    marche.add_agent('bot', 'terminator', 100)
    marche.agents[0].add_strat(marche.agents[0].fourth_strat)
    periode = 1
    epochs = 50
    marche.agents[0].train(marche.actifs[0], 'bull', periode, epochs)  # On entraine notre agent
    marche.next_day()
    inputs = deque([marche.actifs[0].price] * 1000)
    for time in tqdm(range(1, 6000)):
        marche.agents[0].strat[0](marche.current_time, marche.actifs[0], np.array(inputs).reshape(1, 1000) / 740,
                                  periode)
        marche.next_day()
        inputs.append(marche.actifs[0].price)  # On ajoute le prix courant
        inputs.popleft()  # On retire le prix le plus ancien
    marche.agents[0].compte.sell_actif(marche.actifs[0].name, marche.agents[0].compte.actifs[marche.actifs[0].name],
                                       marche.actifs[0].price,
                                       marche.current_time)
    print(marche.agents[0].compte.historique_obligation)
    print(marche.agents[0].compte.actifs)
    marche.agents[0].plot_compte(plot_obligation=True)
    plt.plot(list(marche.actifs[0].price_history.values()))
    plt.show()
    print(
        f"resultat de la strategie, on passe de {100} à {marche.agents[0].compte.get_credit()} euros en {6000 - 1 + 1} jours soit {(marche.agents[0].compte.get_credit() - 100) / (6000 - 1 + 1)} euros par jour moyenne")

    return

# Entrainer un agent à determiner quelle strategie utiliser
# Entrainer un agent à faire des Bull et des Bear
# Mettre en oeuvre cette strategie
def exo5():
    marche = Marche()
    # marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_actif('lvmh', 505000000, 734.70)
    marche.add_agent('bot', 'terminator', 100)
    marche.agents[0].add_strat(marche.agents[0].fifth_strat)
    periode = 2
    epochs = 60
    marche.agents[0].train(marche.actifs[0], 'bear', periode, epochs)  # On entraine notre agent
    marche.agents[0].train(marche.actifs[0], 'bull', periode, epochs)  # On entraine notre agent

    marche.agents[0].train_strategy(marche.actifs[0], 'bull', periode, epochs)  # On entraine notre agent
    marche.next_day()
    inputs = deque([marche.actifs[0].price] * 1000)
    for time in tqdm(range(1, 6000)):
        marche.agents[0].strat[0](marche.current_time, marche.actifs[0], np.array(inputs).reshape(1, 1000) / 740,
                                  periode)
        marche.next_day()
        inputs.append(marche.actifs[0].price)  # On ajoute le prix courant
        inputs.popleft()  # On retire le prix le plus ancien
    print(marche.agents[0].compte.historique_obligation)
    print(marche.agents[0].compte.actifs)
    marche.agents[0].compte.sell_actif(marche.actifs[0].name, marche.agents[0].compte.actifs[marche.actifs[0].name],
                                       marche.actifs[0].price,
                                       marche.current_time)

    marche.agents[0].plot_compte(plot_obligation=True)
    plt.plot(list(marche.actifs[0].price_history.values()))
    plt.show()
    print(
        f"resultat de la strategie, on passe de {100} à {marche.agents[0].compte.get_credit()} euros en {6000 - 1 + 1} jours soit {(marche.agents[0].compte.get_credit() - 100) / (6000 - 1 + 1)} euros par jour moyenne")

    return


def main():
    exo1()
    exo2()
    exo3()
    exo4()
    exo5()


if __name__ == '__main__':
    main()
