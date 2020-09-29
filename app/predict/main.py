"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester  
<www.linkedin.com/in/jaisenbe>

License: MIT
"""

"""Filename: server.py
"""
import pandas as pd
from sklearn.externals import joblib
from flask import Flask, jsonify, request

from Helpers import utils
from Model import Embed

PASOS = 7

app = Flask(__name__)

@app.route('/test', methods=['POST', 'GET'])
def hello_world():
    return("Hola Mundo")

@app.route('/autor', methods=['POST', 'GET'])
def Autor():
    return("Jaime Sendra")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
	"""API request
	"""
	try:
		req_json = request.get_json()
		input = pd.read_json(req_json, orient='records')

	except Exception as e:
		raise e

	if input.empty:
		return(print("empty"))
	else:
		#Load the saved model
		print("Cargar el modelo...")
		loaded_model = cargarModeloSiEsNecesario()

		print("Hacer Pronosticos")
		continuas = input[['var1(t-7)','var1(t-6)','var1(t-5)','var1(t-4)','var1(t-3)','var1(t-2)','var1(t-1)']]
		predictions = loaded_model.predict([input['weekday'], input['month'], continuas])

		print("Transformando datos")
		loaded_scaler = utils.load_object('Model/Modelo_Series_temporales.pkl')
		inverted = loaded_scaler.inverse_transform(predictions)
		inverted = inverted.astype('int32')

		final_predictions = pd.DataFrame(inverted)
		final_predictions.columns = ['ventas']
		
		print("Enviar respuesta")
		responses = jsonify(predictions=final_predictions.to_json(orient="records"))
		responses.status_code = 200
		print("Fin de Peticion")
		
		return (responses)

global_model = None

def cargarModeloSiEsNecesario():
    global global_model
    if global_model is not None:
        print('Modelo YA cargado')
        return global_model
    else:
        global_model = Embed.crear_modeloEmbeddings(PASOS)
        global_model.load_weights("Model/pesos.h5")
        print('Modelo Cargado')
        return global_model