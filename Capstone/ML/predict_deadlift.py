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


df4 = pd.read_csv('df4.csv')
# df4.reset_index(drop=True, inplace=True)
# print(df4.info())
# df4.drop(['Unnamed: 0','Unnamed: 0.1'],1,inplace=True)
# df4.to_csv('df4.csv',index=False,)


X = df4.drop(['Equipment', 'TotalKg', 'Best3DeadliftKg'],1)

y = df4['Best3DeadliftKg']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)


scaler = MinMaxScaler()

X_train= scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

X_train.shape

X_test.shape

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

from sklearn.metrics import mean_squared_error,mean_absolute_error,explained_variance_score
X_test
predictions = model.predict(X_test)
mean_absolute_error(y_test,predictions)
np.sqrt(mean_squared_error(y_test,predictions))
explained_variance_score(y_test,predictions)

# model = load_model('predict_deadlift.h5')

single_pred = df4.drop(['Equipment', 'TotalKg', 'Best3DeadliftKg'],1).iloc[0]
print(single_pred)
single_pred = scaler.transform(single_pred.values.reshape(-1, 6))

print(model.predict(single_pred))
model.save('predict_deadlift.h5')