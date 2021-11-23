from actif import Actif
from agent import Agent
from marche import Marche

import numpy as np
import pandas as pd

import tensorflow as tf


class Solveur():
    def __init__(self, marche:Marche):
        self.marche = marche

    def end_day(self):
        for agent in self.marche.agents:
            for strategie in agent.strategies:
                return #todo





# FOnction pour creer un marche avec un actif et un agent qui s'appelle EDDY
def init_marche_un_actif():
    marche = Marche()
    marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
    marche.add_agent('human', 'Eddy', 1000000)
    return marche


def creat_random_fake_data(day: int):
    return pd.DataFrame(np.random.randint(0, day, size=(day, 4)), columns=['actif_prix', 'my_actif', 'my_banque', 'label'])

def create_model(actif: Actif, agent : Agent):
    # true method todo

    # fake method
    data_train = creat_random_fake_data(10000)
    label_train = data_train.iloc[:,3].to_numpy()
    data_train = data_train.iloc[:,0:3].to_numpy()

    data_validation = creat_random_fake_data(10000)
    label_validation = data_validation.iloc[:,3].to_numpy()
    data_validation = data_validation.iloc[:,0:3].to_numpy()

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



# create_model('toto', 'test')
