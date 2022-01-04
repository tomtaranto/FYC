from tqdm import tqdm

from actif import Actif
from agent import Agent
from marche import Marche

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf


class Solveur():
    def __init__(self, marche: Marche):
        self.marche = marche

    def end_day(self):
        for agent in self.marche.agents:
            for strategie in agent.strategies:
                return  # todo


# FOnction pour creer un marche avec un actif et un agent qui s'appelle EDDY
def init_marche_un_actif():
    marche = Marche()
    marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_agent('human', 'Eddy', 1000000)
    return marche


def creat_random_fake_data(day: int):
    return pd.DataFrame(np.random.randint(0, day, size=(day, 4)),
                        columns=['actif_prix', 'my_actif', 'my_banque', 'label'])


def create_model(actif: Actif, agent: Agent):
    # true method todo

    # fake method
    data_train = creat_random_fake_data(10000)
    label_train = data_train.iloc[:, 3].to_numpy()
    data_train = data_train.iloc[:, 0:3].to_numpy()

    data_validation = creat_random_fake_data(10000)
    label_validation = data_validation.iloc[:, 3].to_numpy()
    data_validation = data_validation.iloc[:, 0:3].to_numpy()

    model = model_dense()
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.MeanAbsoluteError(),
                  metrics=['accuracy'])

    model.fit(data_train, label_train,
              validation_data=(data_validation, label_validation),
              epochs=1000,
              batch_size=65,
              verbose=1)

    return 0


def model_dense():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(1000, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='relu'))
    return model

def create_model2():
    inputs = tf.keras.Input(shape = (1000,))
    x = tf.keras.layers.Dense(1000, activation='relu')(inputs)
    x = tf.keras.layers.Dropout(0.1)(x)
    x = tf.keras.layers.Dense(1000, activation='relu')(x)
    x1 = tf.keras.layers.Dense(1, activation='linear')(x)
    x2 = tf.keras.layers.Dense(1, activation='linear')(x)
    model = tf.keras.Model(inputs,[x1,x2])
    return model


# Fonctionne uniquement pour lvmh
def generate_true_data(filepath: str):
    assert filepath == 'lvmh.csv'
    df = pd.read_csv(filepath, sep=";", header=0)
    df = df.reindex(index=df.index[::-1])
    df.reset_index(inplace=True, drop=True)
    df['bull1x2'] = df['Close'].shift(-1)  # x2 pour un bull spread de T=1
    df['bull1x1'] = df['Close'].shift(-1) * 0.99  # x2 pour un bull spread de T=1

    df['bull2x2'] = df['Close'].shift(-2)
    df['bull2x1'] = df['Close'].shift(-2) * 0.99

    df['bull5x2'] = df['Close'].shift(-5)
    df['bull5x1'] = df['Close'].shift(-5) * 0.99

    df['bull10x2'] = df['Close'].shift(-10)
    df['bull10x1'] = df['Close'].shift(-10) * 0.99
    df.to_csv(filepath[:-4] + "_train.csv")
    return


def train(actif_name: str, strategie_type: str, maturity: int):
    df = pd.read_csv(actif_name + "_train.csv")# On charge les donnees d entrainement
    df = df[['Close',strategie_type + str(maturity) + 'x1',strategie_type + str(maturity) + 'x2']] # On ne garde que les colonnes qui nous interessent
    df.dropna(inplace=True) # On retire les jours sans données
    price = df['Close']
    x1 = df[strategie_type + str(maturity) + 'x1']
    x2 = df[strategie_type + str(maturity) + 'x2']
    X = np.zeros((len(x1), 1000))
    for i in tqdm(range(len(x1)),desc='Creation des donnees'):
        start_price = price[i]
        hist_len = min(999, i)
        hist_values = price[i - hist_len:i + 1]
        X[i, -len(hist_values):] = hist_values
        X[i,:][X[i,:]==0] = start_price
    X = X/np.max(X)
    model = create_model2()
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.MeanAbsoluteError(),
                  metrics=['MAPE'])

    history = model.fit(X, [x1,x2],
              epochs=15,
              batch_size=65,
              verbose=1, validation_split=0.1)
    print(history.history)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('training loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()
    return model


'''
# create_model('toto', 'test')
if __name__ == '__main__':
    #generate_true_data('lvmh.csv')
    train('lvmh', 'bull',1)
'''