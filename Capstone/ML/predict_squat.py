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


def load_create_sets():
    df4 = pd.read_csv('df4.csv')

    X = df4.drop(['Equipment', 'TotalKg', 'Best3SquatKg'], 1)

    y = df4['Best3SquatKg']

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

    return X_train, X_test, y_train, y_test

def train_create_model():

    X_train, X_test, y_train, y_test = load_create_sets()


    X_test = scaler.transform(X_test)

    model = Sequential()

    model.add(Dense(6,activation='relu'))
    model.add(Dense(6,activation='relu'))
    model.add(Dense(6,activation='relu'))
    model.add(Dense(6,activation='relu'))
    model.add(Dense(6,activation='relu'))
    model.add(Dense(6,activation='relu'))
    model.add(Dense(6,activation='relu'))
    model.add(Dense(1))

    model.compile(optimizer='adam',loss='mse')
    model.fit(x=X_train,y=y_train.values,
              validation_data=(X_test,y_test.values),
              batch_size=16,epochs=200)

    model.save('predict_squat.h5')

def fit_scalar(X_train):

    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)

    return scaler


def predict(result_list):
    scaler = fit_scalar()
    model = load_model('predict_deadlift.h5')
    result_list = np.array(result_list)
    result_list = scaler.transform(result_list.reshape(-1, 6))

    return model.predict(result_list)
