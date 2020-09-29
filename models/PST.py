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
// Functionality: ejemplo de un modelo de ML basándonos en el ejercicio de 
// Pronóstico de Series Temporales que hace un pronóstico de ventas con redes 
// neuronales con Embeddings
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