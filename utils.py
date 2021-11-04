from marche import Marche


class Solveur():
    pass

# FOnction pour creer un marche avec un actif et un agent qui s'appelle EDDY
def init_marche_un_actif():
    marche = Marche()
    marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_agent('human', 'Eddy', 1000000)
    return marche
