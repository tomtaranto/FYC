from typing import Dict, Tuple
import pandas as pd
import numpy as np


class Actif():
    # history = [date : [buyer : (quantity, price)]]
    def __init__(self, name: str, quantity: float, price: float, history: Dict[str, Dict[str, Tuple[float, float]]]):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.history = history
        self.price_history = dict()  # date : prix
        self.real_data = None
        self.volatility = 0.01
        if 'shib' in name.lower():
            self.load('shib-usd-max.csv')  # TODO mettre le nom en parametre si on a plusieurs actifs
        else:
            print()
            self.load('lvmh.csv')

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
        if 'shib' in filepath:
            df = pd.read_csv(filepath)
            df = df[df.market_cap != 0.0].reset_index(drop=True)
        else:
            df = pd.read_csv(filepath, sep=";", header=0)
        self.real_data = df

    # Update price and quantity with today's data
    def update_from_date(self, date: int):
        if 'shib' in self.name.lower():
            self.quantity = self.quantity + self.real_data.iloc[date].total_volume - self.real_data.iloc[
                date - 1].total_volume
            self.price = float(self.real_data.iloc[date].market_cap / self.real_data.iloc[date].total_volume)
        else:
            self.quantity = 505000000
            self.price = self.real_data.loc[
                len(self.real_data.index) - self.real_data.index[date + 1], 'Close']  # TODO FIx IT EDDY !
        self.price_history[date] = self.price
        # self.volatility = np.std(list(self.price_history.values())[-50:])/self.price *np.sqrt(356)#/ self.price
        self.volatility = self.compute_volatility()

    def compute_volatility(self):
        l = []
        hist_prices = list(self.price_history.values())[-365:]
        if len(hist_prices)<2:
            return 0.001
        for i in range(1, len(hist_prices)):
            l.append(np.log(hist_prices[i - 1] / hist_prices[i]))
        return max(np.std(np.array(l)) * np.sqrt(365), 0.001)


def main():
    a = Actif('Shiba', 2255990535.605459, 7827138285.646066 / 2255990535.605459, dict())
    print(a.price, a.quantity, a.history, a.real_data)
    for i in range(1, 160):
        a.update_from_date(i)
    print(a.price, a.quantity, a.history)


if __name__ == '__main__':
    main()
