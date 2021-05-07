#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf


# In[3]:


df = pd.read_csv('pl.csv')


# In[25]:


df.info()


# In[26]:


df.isnull().sum()


# In[9]:


df = df[df['Age'].notna()]


# In[20]:


df = df[df['BodyweightKg'].notna()]


# In[21]:


df = df[df['WeightClassKg'].notna()]


# In[13]:


df = df.drop(['Division','Wilks','McCulloch','IPFPoints'],1)


# In[17]:


df = df.drop(['Squat4Kg','Bench4Kg','Deadlift4Kg','Glossbrenner'],1)


# In[24]:


df = df.drop(['Tested','Country','MeetCountry','MeetState'],1)


# In[33]:


df.iloc[2]['Squat3Kg']


# In[39]:


def fill_squat_values(row):
    if row[10].isnull():
        if row[9].isnull():
            if row[8].isnull():
                return True;
            else:
                row[9] = row[8]
                row[10] = row[8]
        else:
            row[10] = row[9]
                


# In[42]:


for row in df:
    print(row)


# In[103]:


df2=df


# In[ ]:





# In[104]:


df2.head


# In[105]:


df2.Squat1Kg = df2.Squat1Kg.fillna(df2.Squat2Kg)


# In[106]:


df2.isnull().sum()


# In[107]:


df2.Squat2Kg = df2.Squat2Kg.fillna(df2.Squat1Kg)


# In[108]:


df2.isnull().sum()


# In[109]:


df3 = df2[df2['Squat2Kg'].isnull()]


# In[110]:


df2.dropna()


# In[115]:


df2.info()


# In[112]:


df2 = df2.dropna()


# In[113]:


df2.isnull().sum()


# In[114]:


df2[df2['Sex'] == 'M'].count()


# In[116]:


df2 = df2.drop(['Place','Federation','Date','MeetName'],1)


# In[122]:


df2.info()


# In[121]:


df2 = df2.drop(['Name'],1)


# In[138]:


def sex_to_number(sex):
    if sex == 'F':
        return 0
    elif sex == 'M':
        return 1


# In[127]:


df3 = df2.copy(deep=True)


# In[128]:


df3['Sex'] = df3['Sex'].apply(lambda s: sex_to_number(s) )


# In[129]:


df3.head()


# In[130]:


df2.head(100)


# In[131]:


df3.head(100)


# In[136]:


df3.info()


# In[102]:


df2.head()


# In[137]:


df3.Equipment.value_counts()


# In[139]:


def equipment_to_number(equip):
    if equip == 'Raw':
        return 0
    elif equip == 'Single-ply':
        return 1
    elif equip == 'Wraps':
        return 2
    elif equip == 'Multi-ply':
        return 3


# In[140]:


df3['EquipFeat'] = df3['Equipment'].apply(lambda e: equipment_to_number(e) )


# In[142]:


df3.head(30)


# In[143]:


df3.EquipFeat.value_counts()


# In[144]:


df3.info()


# In[145]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf


# In[ ]:





# In[202]:


plt.figure(figsize=(12,8))
sns.histplot(data = df3, x = 'TotalKg', y = "Age", hue = 'Sex')


# In[155]:


plt.figure(figsize=(12,8))
sns.histplot(data = df3, x = 'Best3BenchKg', y = "Age", hue = 'Sex')


# In[156]:


plt.figure(figsize=(12,8))
sns.histplot(data = df3, x = 'Best3SquatKg', y = "Age", hue = 'Sex')


# In[157]:


plt.figure(figsize=(12,8))
sns.histplot(data = df3, x = 'Best3DeadliftKg', y = "Age", hue = 'Sex')


# In[160]:


plt.figure(figsize=(12,8))
sns.pairplot(df3)


# In[161]:


df3.columns


# In[244]:


X = df3.drop(['Equipment','Squat1Kg', 'Squat2Kg',
       'Squat3Kg',  'Bench1Kg', 'Bench2Kg', 'Bench3Kg', 'Deadlift1Kg', 'Deadlift2Kg', 'Deadlift3Kg','TotalKg','Best3BenchKg'],1)


# In[245]:


y = df3['Best3BenchKg']


# In[246]:


from sklearn.model_selection import train_test_split


# In[247]:


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)


# In[248]:


from sklearn.preprocessing import MinMaxScaler


# In[249]:


scaler = MinMaxScaler()


# In[250]:


X_train= scaler.fit_transform(X_train)


# In[251]:


X_test = scaler.transform(X_test)


# In[252]:


X_train.shape


# In[253]:


X_test.shape


# In[254]:


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam


# In[255]:


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


# In[256]:


model.fit(x=X_train,y=y_train.values,
          validation_data=(X_test,y_test.values),
          batch_size=128,epochs=400)


# In[257]:


losses = pd.DataFrame(model.history.history)


# In[258]:


losses.plot()


# In[259]:


from sklearn.metrics import mean_squared_error,mean_absolute_error,explained_variance_score


# In[260]:


X_test


# In[261]:


predictions = model.predict(X_test)


# In[262]:


mean_absolute_error(y_test,predictions)


# In[263]:


np.sqrt(mean_squared_error(y_test,predictions))


# In[264]:


explained_variance_score(y_test,predictions)


# In[265]:


plt.scatter(y_test,predictions)
plt.plot(y_test,y_test,'r')


# In[266]:


y_test


# In[267]:


errors = y_test.values.reshape(71697, 1) - predictions


# In[268]:


errors


# In[269]:


sns.histplot(errors)


# In[299]:


single_pred = df3.drop(['Equipment','Squat1Kg', 'Squat2Kg',
       'Squat3Kg',  'Bench1Kg', 'Bench2Kg', 'Bench3Kg', 'Deadlift1Kg', 'Deadlift2Kg', 'Deadlift3Kg','TotalKg','Best3BenchKg'],1).iloc[0]


# In[300]:


single_pred[0] = 1 


# In[301]:


single_pred[1] = 80


# In[302]:


single_pred[2] = 120


# In[237]:


single_pred[3] = 210


# In[238]:


single_pred[4] = 110


# In[239]:


single_pred[5] = 260


# In[240]:


single_pred[6] = 1


# In[303]:


single_pred


# In[304]:


single_pred = scaler.transform(single_pred.values.reshape(-1, 6))


# In[305]:


model.predict(single_pred)


# In[306]:


df3.iloc[0]


# In[307]:


df3


# In[317]:


newboxplot = sns.boxenplot(x='Equipment', y='TotalKg', data= df3)


# In[320]:


newregplot = sns.regplot(x='Age', y='TotalKg', data = df3, logx=True)


# In[322]:


df3.info()


# In[326]:


newheatmap = sns.heatmap(df3.drop(['Equipment','Squat1Kg', 'Squat2Kg',
       'Squat3Kg',  'Bench1Kg', 'Bench2Kg', 'Bench3Kg', 'Deadlift1Kg', 'Deadlift2Kg', 'Deadlift3Kg','TotalKg'],1), cmap="mako")


# In[ ]:




