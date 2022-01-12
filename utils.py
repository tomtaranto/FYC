from tqdm import tqdm

#
# from marche import Marche

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf


# # FOnction pour creer un marche avec un actif et un agent qui s'appelle EDDY
# def init_marche_un_actif():
#     marche = Marche()
#     marche.add_actif('Shiba', 2255990535.605459, (7827138285.646066 / 2255990535.605459))
#     marche.add_agent('human', 'Eddy', 1000000)
#     return marche


def model_dense():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(1000, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='relu'))
    return model


def create_model2():
    inputs = tf.keras.Input(shape=(1000,))
    x = tf.keras.layers.Dense(1000, activation='relu')(inputs)
    x = tf.keras.layers.Dropout(0.1)(x)
    x = tf.keras.layers.Dense(1000, activation='relu')(x)
    x1 = tf.keras.layers.Dense(1, activation='linear')(x)
    x2 = tf.keras.layers.Dense(1, activation='linear')(x)
    model = tf.keras.Model(inputs, [x1, x2])
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

    df['bear1x2'] = df['Close'].shift(1)  # x2 pour un bull spread de T=1
    df['bear1x1'] = df['Close'].shift(1) * 0.99  # x2 pour un bull spread de T=1

    df['bear2x2'] = df['Close'].shift(2)
    df['bear2x1'] = df['Close'].shift(2) * 0.99

    df['bear5x2'] = df['Close'].shift(5)
    df['bear5x1'] = df['Close'].shift(5) * 0.99

    df['bear10x2'] = df['Close'].shift(10)
    df['bear10x1'] = df['Close'].shift(10) * 0.99

    # On cherche a savoir si le marche monte ou descend
    # Les valuers calculées valent -1 ou 1
    #
    df['best_strat1'] = np.sign((df['bull1x1'] - df['Close']))
    df['best_strat2'] = np.sign((df['bull2x1'] - df['Close']))
    df['best_strat5'] = np.sign((df['bull5x1'] - df['Close']))
    df['best_strat10'] = np.sign((df['bull10x1'] - df['Close']))

    # -1 si le marche baisse se transforme en 0
    # 1 si le marche monte se transforme en 1
    df.loc[df['best_strat1'] < 0, 'best_strat1'] = 0
    df.loc[df['best_strat2'] < 0, 'best_strat2'] = 0
    df.loc[df['best_strat5'] < 0, 'best_strat5'] = 0
    df.loc[df['best_strat10'] < 0, 'best_strat10'] = 0
    print(df)
    df.to_csv(filepath[:-4] + "_train.csv")
    return


def train(actif_name: str, strategie_type: str, maturity: int):
    df = pd.read_csv(actif_name + "_train.csv")  # On charge les donnees d entrainement
    df = df[['Close', strategie_type + str(maturity) + 'x1',
             strategie_type + str(maturity) + 'x2']]  # On ne garde que les colonnes qui nous interessent
    df.dropna(inplace=True)  # On retire les jours sans données
    price = df['Close']
    x1 = df[strategie_type + str(maturity) + 'x1']
    x2 = df[strategie_type + str(maturity) + 'x2']
    X = np.zeros((len(x1), 1000))
    for i in tqdm(range(len(x1)), desc='Creation des donnees'):
        start_price = price[i]
        hist_len = min(999, i)
        hist_values = price[i - hist_len:i + 1]
        X[i, -len(hist_values):] = hist_values
        X[i, :][X[i, :] == 0] = start_price
    X = X / np.max(X)
    model = create_model2()
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.MeanAbsoluteError(),
                  metrics=['MAPE'])

    history = model.fit(X, [x1, x2],
                        epochs=15,
                        batch_size=65,
                        verbose=1, validation_split=0.1)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('training loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()
    return model


# create_model('toto', 'test')
if __name__ == '__main__':
    generate_true_data('lvmh.csv')
    # train('lvmh', 'bull',1)
