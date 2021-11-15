from strategie import Strategie
from utils import init_marche_un_actif


# Tous les jours, acheter un actif
# TOus les 3 jours vendre cet actif
def exo1():
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

    print(marche.agents[0].compte.historique)


def main():
    exo1()


if __name__ == '__main__':
    main()
