from typing import Dict, Tuple
import pandas as pd


class Actif():
    # history = [date : [buyer : (quantity, price)]]
    def __init__(self, name: str, quantity: float, price: float, history: Dict[str, Dict[str, Tuple[float, float]]]):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.history = history
        self.price_history = dict()  # date : prix
        self.real_data = None
        self.load('shib-usd-max.csv')  # TODO mettre le nom en parametre si on a plusieurs actifs

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
        if self.quantity >= quantity:
            return True
        return False

    # Populate history with data
    def load(self, filepath):
        df = pd.read_csv(filepath)
        df = df[df.market_cap != 0.0].reset_index(drop=True)
        self.real_data = df

    # Update price and quantity with today's data
    def update_from_date(self, date: int):
        self.quantity = self.quantity + self.real_data.iloc[date].total_volume - self.real_data.iloc[
            date - 1].total_volume
        self.price = float(self.real_data.iloc[date].market_cap / self.real_data.iloc[date].total_volume)
        self.price_history[date] = self.price



def main():
    a = Actif('Shiba', 2255990535.605459, 7827138285.646066/2255990535.605459, dict())
    print(a.price, a.quantity, a.history, a.real_data)
    for i in range(1,160):
        a.update_from_date(i)
    print(a.price, a.quantity, a.history)

if __name__ == '__main__':
    main()

