"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester  
<www.linkedin.com/in/jaisenbe>

License: MIT
"""

from keras.layers import Input, Embedding, Dense, Flatten, Dropout, concatenate, LSTM
from keras.layers import BatchNormalization, SpatialDropout1D
from keras.callbacks import Callback
from keras.models import Model
from keras.optimizers import Adam
from keras.models import Sequential

from keras.models import load_model

def crear_modeloEmbeddings(PASOS):

	emb_dias = 2 #tamaño profundidad de embeddings
	emb_meses = 4

	in_dias = Input(shape=[1,], name = 'dias')
	emb_dias = Embedding(7+1, emb_dias)(in_dias)
	in_meses = Input(shape=[1,], name = 'meses')
	emb_meses = Embedding(12+1, emb_meses)(in_meses)
	in_cli = Input(shape=[PASOS,], name = 'cli')
	fe = concatenate([(emb_dias), (emb_meses)])
	x = Flatten()(fe)
	x = Dense(PASOS,activation='tanh')(x)
	outp = Dense(1,activation='tanh')(x)
	model = Model(inputs=[in_dias,in_meses,in_cli], outputs=outp)
	model.compile(loss='mean_absolute_error', 
				optimizer='adam',
				metrics=['MSE'])
	return model