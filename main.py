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
    marche.add_agent('human', 'Eddy', 1000000)
    marche.agents[0].add_strat(marche.agents[0].first_strat)
    marche.next_day()
    for time in range(1, 20):
        marche.agents[0].strat[0](marche.current_time, marche.actifs[0])
        marche.next_day()
    print(marche.agents[0].compte.historique)
    marche.agents[0].compte.sell_actif('Shiba', marche.agents[0].compte.actifs['Shiba'], marche.actifs[0].price,  marche.current_time)
    marche.agents[0].plot_compte()

def exo2():
    marche = Marche()
    marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_agent('human', 'Eddy', 10000)
    marche.agents[0].add_strat(marche.agents[0].second_strat)
    marche.next_day()
    for time in range(1, 20):
        marche.agents[0].strat[0](marche.current_time, marche.actifs[0])
        marche.next_day()
    print(marche.agents[0].compte.historique)
    marche.agents[0].compte.sell_actif('Shiba', marche.agents[0].compte.actifs['Shiba'], marche.actifs[0].price,
                                       marche.current_time)
    marche.agents[0].plot_compte()
    return


def main():
    exo1()
    exo2()


if __name__ == '__main__':
    main()
