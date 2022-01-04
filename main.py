import matplotlib.pyplot as plt

from marche import Marche
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
    marche.agents[0].compte.sell_actif(name, marche.agents[0].compte.actifs[name], marche.actifs[0].price, marche.current_time)
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
    marche.agents[0].compte.sell_actif(marche.actifs[0].name, marche.agents[0].compte.actifs[marche.actifs[0].name], marche.actifs[0].price,
                                       marche.current_time)
    marche.agents[0].plot_compte()
    return

def exo3():
    marche = Marche()
    #marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
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
    #print(marche.agents[0].compte.historique_obligation)
    #print(marche.agents[0].compte.actifs)
    marche.agents[0].plot_compte(plot_obligation=True)
    plt.plot(list(marche.actifs[0].price_history.values()))
    plt.show()
    return


def main():
    #exo1()
    #exo2()
    exo3()


if __name__ == '__main__':
    main()
