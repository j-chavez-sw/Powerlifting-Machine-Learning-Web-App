import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler


class predict_bench():

    X_train, X_test, y_train, y_test = "", "", "", ""
    scaler = MinMaxScaler()

    def __init__(self):
        self.X_train, self.X_test, self.y_train, self.y_test = self.load_create_sets()
        self.fit_scaler()


    def load_create_sets(self):

        df4 = pd.read_csv('df4.csv')

        X = df4.drop(['Equipment', 'TotalKg', 'Best3BenchKg'], 1)
        print(df4.columns)

        y = df4['Best3BenchKg']

        from sklearn.model_selection import train_test_split

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

        return X_train, X_test, y_train, y_test


    def train_create_model(self):

        self.X_test = self.scaler.transform(self.X_test)

        model = Sequential()

        model.add(Dense(6,activation='relu'))
        model.add(Dense(6,activation='relu'))
        model.add(Dense(6,activation='relu'))
        model.add(Dense(6,activation='relu'))
        model.add(Dense(6,activation='relu'))
        model.add(Dense(6,activation='relu'))
        model.add(Dense(6,activation='relu'))
        model.add(Dense(1))

        model.compile(optimizer='adam', loss='mse')
        model.fit(x=self.X_train, y=self.y_train.values,
                  validation_data=(self.X_test, self.y_test.values),
                  batch_size=16, epochs=200)

        model.save('predict_bench.h5')


    def fit_scaler(self):

        self.scaler.fit(self.X_train)


    def predict(self, result_list):
        model = load_model('predict_bench.h5')
        result_list = np.array(result_list)
        result_list = self.scaler.transform(result_list.reshape(-1, 6))

        return model.predict(result_list)
