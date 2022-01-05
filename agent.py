import numpy as np
import numpy.linalg

from actif import Actif
from compte import Compte
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
from tqdm import tqdm

import tensorflow as tf


class Agent:
    def __init__(self, name: str, agent_type: str, start_credit: float):
        assert agent_type in ["human", "bot"]
        self.name = name
        self.agent_type = agent_type
        self.compte = Compte(start_credit, 0)
        self.age = 0
        self.strat = []
        self.model=None
        self.model_strat = None

    def train(self, actif: Actif, strategie_type:str, maturity:int, epochs:int):
        if self.agent_type != 'bot':
            print("You are not a bot, use your brain to train")
            return
        if 'lvmh' not in actif.name:
            print("Actif not supported \n only lvmh supported yet")
            return
        df = pd.read_csv(actif.name + "_train.csv")  # On charge les donnees d entrainement
        df = df[['Close', strategie_type + str(maturity) + 'x1',
                 strategie_type + str(maturity) + 'x2']]  # On ne garde que les colonnes qui nous interessent
        df.dropna(inplace=True)  # On retire les jours sans données
        price = df['Close']
        x1 = df[strategie_type + str(maturity) + 'x1']
        x2 = df[strategie_type + str(maturity) + 'x2']
        X = np.zeros((len(x1), 1000))
        for i in tqdm(range(len(x1)), desc='Creation des donnees'):
            start_price = price[i] # Valeur pour fill si on a pas assez de donnees
            hist_len = min(999, i)
            hist_values = price[i - hist_len:i + 1] # Les valeurs à ajouter sont les 1000 dernieres ( ou le maximum) a partir de i
            X[i, -len(hist_values):] = hist_values # On place ces valeurs dans notre input
            X[i, :][X[i, :] == 0] = start_price # On remplace les 0 par le prix de depart
        X = X / 740 # On normalise nos données
        model = self.create_model3() # On créé le modele
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
                      #loss=tf.keras.losses.MeanAbsoluteError(),
                      loss = tf.keras.losses.MeanAbsolutePercentageError(), # Utilisation d'une erreur en pourcentage
                      metrics=['MAPE']) # On le compile

        history = model.fit(X, [x1, x2],
                            epochs=epochs,
                            batch_size=500,
                            verbose=1, validation_split=0.1) # On fit nos données
        print(history.history)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('training loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper left')
        plt.show() # On affiche le resultat de l'entrainement
        self.model=model # On enregistre notre modele pour l agent

    # Ajout d'une strategie
    def add_strat(self, strategie):
        self.strat.append(strategie)

    # Strategie attendue pour l'exercice 1
    def first_strat(self, day: int, actif: Actif):
        if day % 3 == 0 and self.compte.can_sell(actif.name, 1):
            self.compte.sell_actif(actif.name, 1, actif.price, day)
        elif self.compte.can_buy(actif.price, 1):
            self.compte.buy_actif(actif.name, 1, actif.price, day)

    def second_strat(self, date: int, actif: Actif):
        total = 0
        count = 0
        for i in range(1, 6):
            try:
                total += actif.price_history[date - i]
                count += 1
            except:
                pass
        try:
            moyenne_mobile = total / count
        except:
            moyenne_mobile = actif.price
        if moyenne_mobile > actif.price and self.compte.can_buy(actif.price, 1):
            self.compte.buy_actif(actif.name, 1, actif.price, date)
        elif self.compte.can_sell(actif.name, 1):
            self.compte.sell_actif(actif.name, 1, actif.price, date)
        else:  # Au lieu de ne rien faire on achete
            if self.compte.can_buy(actif.price, 1):
                self.compte.buy_actif(actif.name, 1, actif.price, date)

    # Uniquement des bull, centrées en le prix actuel
    def third_strat(self, date: int, actif: Actif):
        periode = 2
        if date % periode == 0:
            self.compte.add_obligation(date, actif, 10, actif.price * 0.8, date + periode)
            self.compte.add_obligation(date, actif, -10, actif.price * 1.5, date + periode)
        else:
            self.compte.do_nothing(date)
        self.compte.resolve_obligation(date)

    def fourth_strat(self, date: int, actif: Actif,inputs, periode):
        assert self.model is not None # On s assure que le train aie deja ete effectue
        x1,x2 = self.model(inputs) # On calcule le prix des options
        #print("actif price : ",actif.price, " x1 : ",x1, " x2 : ",x2, " inputs : ", inputs[:30])
        if date % periode == 0:
            self.compte.add_obligation(date, actif, 10, x1, date + periode)
            self.compte.add_obligation(date, actif, -10, x2, date + periode)
        else:
            self.compte.do_nothing(date)
        self.compte.resolve_obligation(date)

    def train_strategy(self, actif: Actif, strategie_type:str, maturity:int, epochs:int):
        if self.agent_type != 'bot':
            print("You are not a bot, use your brain to train")
            return
        if 'lvmh' not in actif.name:
            print("Actif not supported \n only lvmh supported yet")
            return
        df = pd.read_csv(actif.name + "_train.csv")  # On charge les donnees d entrainement
        df = df[['Close', 'best_strat' + str(maturity) ]]  # On ne garde que les colonnes qui nous interessent
        df.dropna(inplace=True)  # On retire les jours sans données
        price = df['Close']
        #Y = tf.keras.utils.to_categorical(df['best_strat' + str(maturity)])
        Y = df['best_strat' + str(maturity)]
        X = np.zeros((len(Y), 1000))
        for i in tqdm(range(len(Y)), desc='Creation des donnees'):
            start_price = price[i]  # Valeur pour fill si on a pas assez de donnees
            hist_len = min(999, i)
            hist_values = price[
                          i - hist_len:i + 1]  # Les valeurs à ajouter sont les 1000 dernieres ( ou le maximum) a partir de i
            X[i, -len(hist_values):] = hist_values  # On place ces valeurs dans notre input
            X[i, :][X[i, :] == 0] = start_price  # On remplace les 0 par le prix de depart
        X = X / 740  # On normalise nos données

        split = 0.7
        chosen_train_idx = np.random.choice(list(range(len(Y))), int(len(Y)*split),replace=False)
        chosen_test_idx = [x for x in range(len(Y)) if x not in chosen_train_idx]

        X_train = np.array(X[chosen_train_idx])
        X_test = np.array(X[chosen_test_idx])
        Y = tf.keras.utils.to_categorical(Y,num_classes=2)
        Y_train = np.array(Y[chosen_train_idx])
        Y_test = np.array(Y[chosen_test_idx])
        print("shape start = ",X_train.shape,Y_train.shape, X_test.shape, Y_test.shape)
        print(np.sum(Y_test)/len(Y_test))

        def predict(x,win,wout):
            a = np.dot(x, win)  # Passage dans le reseau
            a = np.maximum(a, 0, a)
            y = np.dot(a, wout)
            return y

        INPUT_LENGHT = X_train.shape[1]  # 6800 et quelques
        HIDDEN_UNITS = 50
        Win = np.random.normal(size=[INPUT_LENGHT, HIDDEN_UNITS]) # Initialisation aléatoire des poids
        for epoch in tqdm(range(1)): # Boucle d'apprentissage
            a = np.dot(X_train, Win)  # Passage dans le reseau
            X = np.maximum(a, 0, a) # Relu activation
            Xt = np.transpose(X)
            # On utilise la formule de mise a jour des poids :
            # (Xt X)-1 * Xt Y
            Wout = np.dot(np.linalg.pinv(np.dot(Xt, X)), np.dot(Xt, Y_train))
            # On monitor l'entrainement:
            y = predict(X_test,Win, Wout)
            correct = 0
            total = y.shape[0]
            for i in range(total):
                #print("predictions : ", y[i])
                predicted = np.argmax(y[i])
                #predicted = np.round(y[i])
                test = np.argmax(Y_test[i])
                #test = Y_test[i]
                #print("test : ",test, "vs predicted : ",predicted, " result : ", predicted==test)
                correct = correct + (1 if predicted == test else 0)
            print('Accuracy: {:f}'.format(correct / total))



        '''
        model = self.create_model4()  # On créé le modele
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
                      # loss=tf.keras.losses.MeanAbsoluteError(),
                      loss=tf.keras.losses.BinaryCrossentropy(),  # Utilisation d'une erreur en pourcentage
                      metrics=[tf.keras.metrics.BinaryAccuracy()])  # On le compile


        history = model.fit(X, Y,
                            epochs=epochs,
                            batch_size=500,
                            verbose=1, validation_split=0.1)  # On fit nos données
        print(history.history)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('training loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper left')
        plt.show()  # On affiche le resultat de l'entrainement
        self.model = model  # On enregistre notre modele pour l agent
        '''


    def plot_compte(self, plot_obligation=False):
        x = list(range(min(self.compte.historique), max(self.compte.historique) + 1))
        # x = np.linspace(1, len(self.compte.historique)+1, len(self.compte.historique)+1)
        y = np.zeros_like(x)
        y1 = np.zeros_like(x)
        y2 = np.zeros_like(x)
        c = np.empty_like(x, dtype=str)
        for i, date in enumerate(x):
            try:
                y[i] = self.compte.historique_credit[date]
            except:
                pass
            if date in self.compte.historique:
                for actif in self.compte.historique[date].keys():
                    try:
                        y1[i] += self.compte.historique[date][actif][0]  # * self.compte.historique[date][actif][1]
                    except:
                        pass
            if date in self.compte.historique_obligation:
                for actif in self.compte.historique_obligation[date].keys():
                    try:
                        y2[i] += self.compte.historique[date][actif][0]
                    except:
                        pass
            if y1[i] > 0:
                c[i] = 'green'
            elif y1[i] < 0:
                c[i] = 'red'
            else:
                c[i] = 'yellow'
        # y = self.compte.historique_credit.values()
        fig, ax1 = plt.subplots()
        ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax1.set_xlim(xmin=0, xmax=max(x) + 1)
        color = 'blue'
        ax1.set_xlabel('jours')
        ax1.set_ylabel('euros', color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.plot(x, y, color=color, label='portefeuille')
        ax2 = ax1.twinx()
        # color = 'orange'
        ax2.set_ylabel('vente')
        ax2.tick_params(axis='y')
        ax2.scatter(x, y1, marker='x', c=c, label='achats/ventes')
        if plot_obligation:
            ax2.scatter(x, y2, marker='1', c=c, label='obligation')

        fig.tight_layout()
        # todo faire de jolie plot, afficher ACHAT OU VENTE
        ax2.legend()
        ax1.legend()
        ax1.grid(visible=True, axis="y", linestyle='-')
        plt.show()

    def create_model2(self):
        inputs = tf.keras.Input(shape = (1000,))
        x = tf.keras.layers.Reshape((1000,1))(inputs)
        lstm = tf.keras.layers.LSTM(16)
        x = lstm(x)
        x = tf.keras.layers.Flatten()(x)
        x = tf.keras.layers.Dense(1000, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.1)(x)
        x = tf.keras.layers.Dense(1000, activation='relu')(x)
        x1 = tf.keras.layers.Dense(1, activation='linear')(x)
        x2 = tf.keras.layers.Dense(1, activation='linear')(x)
        model = tf.keras.Model(inputs,[x1,x2])
        return model


    def create_model3(self):
        inputs = tf.keras.Input(shape = (1000,))
        x = tf.keras.layers.Dense(1000, activation='relu')(inputs)
        for _ in range(5):
            x = tf.keras.layers.Dropout(0.1)(x)
            x = tf.keras.layers.Dense(1000, activation='relu')(x)
        x1 = tf.keras.layers.Dense(1, activation='linear')(x)
        x2 = tf.keras.layers.Dense(1, activation='linear')(x)
        model = tf.keras.Model(inputs,[x1,x2])
        return model

    def create_model4(self):
        inputs = tf.keras.Input(shape = (1000,))
        x = tf.keras.layers.Dense(1000, activation='relu')(inputs)
        for _ in range(5):
            x = tf.keras.layers.Dropout(0.1)(x)
            x = tf.keras.layers.Dense(1000, activation='relu')(x)
        x1 = tf.keras.layers.Dense(2, activation='softmax')(x)
        model = tf.keras.Model(inputs,x1)
        return model