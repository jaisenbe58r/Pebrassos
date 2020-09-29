"""
//===========================================================================
// JAIME SENDRA BERENGUER
// TECH TRAININGS - MACHINE LEARNING
//-----------------------------------------------------------------------------
// Autor: JS 
// Revisado: JS 
//-----------------------------------------------------------------------------
// Library:       -
// Tested with:   CPU CORE i7 16Gb
// Engineering:   -
// Restrictions:  -
// Requirements:  Python 3.8
// Functionality: Utils
// 
//-----------------------------------------------------------------------------
// Change log table:
//
// Version Date           In charge       Changes applied
// 01.00.00 22/09/2020     JS              First released version
//
//===========================================================================
"""
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Activation,Flatten
from sklearn.preprocessing import MinMaxScaler

import pickle

EPOCHS=40
PASOS=7

def save_object(filename, object):
	with open(''+filename, 'wb') as file:
		pickle.dump(object, file)

def load_object(filename):
	with open(''+filename ,'rb') as f:
		loaded = pickle.load(f)
	return loaded

# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


def load_data(PASOS):

    df = pd.read_csv('time_series.csv',  parse_dates=[0], header=None,index_col=0, names=['fecha','unidades'])
    df['weekday']=[x.weekday() for x in df.index]
    df['month']=[x.month for x in df.index]

    values = df['unidades'].values

    # ensure all data is float
    values = values.astype('float32')
    # normalize features
    scaler = MinMaxScaler(feature_range=(-1, 1))

    values=values.reshape(-1, 1) # esto lo hacemos porque tenemos 1 sola dimension

    scaled = scaler.fit_transform(values)

    reframed = series_to_supervised(scaled, PASOS, 1)
    reframed.reset_index(inplace=True, drop=True)

    contador=0
    reframed['weekday']=df['weekday']
    reframed['month']=df['month']

    for i in range(reframed.index[0],reframed.index[-1]):
        reframed['weekday'].loc[contador]=df['weekday'][i+8]
        reframed['month'].loc[contador]=df['month'][i+8]
        contador=contador+1
        reframed.head()

    reordenado=reframed[ ['weekday','month','var1(t-7)','var1(t-6)','var1(t-5)','var1(t-4)','var1(t-3)','var1(t-2)','var1(t-1)','var1(t)'] ]
    reordenado.dropna(inplace=True)
    
    training_data = reordenado.drop('var1(t)', axis=1)
    target_data=reordenado['var1(t)']
    cant = len(df.index)
    valid_data = training_data[cant-30:cant]
    valid_target=target_data[cant-30:cant]
    
    training_data = training_data[0:cant]
    target_data=target_data[0:cant]

    continuas = training_data[['var1(t-7)','var1(t-6)','var1(t-5)','var1(t-4)','var1(t-3)','var1(t-2)','var1(t-1)']]
    valid_continuas = valid_data[['var1(t-7)','var1(t-6)','var1(t-5)','var1(t-4)','var1(t-3)','var1(t-2)','var1(t-1)']]
 

    return scaler, training_data, target_data, valid_data, valid_target, continuas, valid_continuas


def transformar(df, scaler):
	# cargar valpres
	values = df['unidades'].values
	# pasar a tipo float
	values = values.astype('float32')
	# normalizar features
	values = values.reshape(-1, 1) # esto lo hacemos porque tenemos 1 sola dimension
	scaled = scaler.fit_transform(values)

	reframed = series_to_supervised(scaled, PASOS, 1)
	reframed.reset_index(inplace=True, drop=True)

	contador=0
	reframed['weekday']=df['weekday']
	reframed['month']=df['month']

	for i in range(reframed.index[0], reframed.index[-1]):
		reframed['weekday'].loc[contador]=df['weekday'][i+8]
		reframed['month'].loc[contador]=df['month'][i+8]
		contador=contador+1
	#print(reframed.head())
	return reframed