from typing import Dict, Tuple


class Actif():
    # history = [date : [buyer : (quantity, price)]]
    def __init__(self, name: str, quantity: float, price: float, history: Dict[str, Dict[str, Tuple[float, float]]]):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.history = history

    def get_price(self) -> float:
        return self.price

    # Achat avec quantity positif
    # Vente avec quantity negatif
    # Obligatoirement appeller can_buy() avant d'appeller cette fonction
    def update(self, quantity: float, date: str, buyer: str) -> None:
        self.quantity -= quantity
        self.history[date][buyer] = (quantity, self.price)

    def set_price(self, price: float) -> None:
        self.price = price

    # Obligatoirement appeller cette fonction avant d'appeller update
    def can_buy(self, quantity: float) -> bool:
        if self.quantity > quantity:
            return True
        return False

    # Populate history with data
    def load(self):
        pass
