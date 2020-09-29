"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester  
<www.linkedin.com/in/jaisenbe>

License: MIT
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
 
from Helpers import utils
from Model import Embed, Checkpoint
 
 
EPOCHS=80
PASOS=7
 
# Carga de datos para el entrenamiento
scaler, training_data, target_data, valid_data, valid_target, continuas, valid_continuas = utils.load_data(PASOS)
 
# Modelo a utilizar
model = Embed.crear_modeloEmbeddings(PASOS)
  
 #Entrenamiento
history = model.fit([training_data['weekday'],training_data['month'],continuas], target_data, epochs=EPOCHS,
                 validation_data=([valid_data['weekday'],valid_data['month'],valid_continuas],valid_target))
 
# Guardamos Checkpoint del modelo
Checkpoint.save_model(model, scaler)


# Predicción de resultados
results = model.predict([valid_data['weekday'],valid_data['month'],valid_continuas])
 

print( 'Resultados escalados',results )
inverted = scaler.inverse_transform(results)
print( 'Resultados',inverted )