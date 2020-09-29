
import json
import requests
import pandas as pd
import pickle
from Helpers import utils
 
header = {'Content-Type': 'application/json', \
                  'Accept': 'application/json'}
 
# creamos un dataset de pruebas
df = pd.DataFrame({"unidades": [289,288,260,240,290,255,270,300], 
					"weekday": [5,0,1,2,3,4,5,0], 
					"month":   [4,4,4,4,4,4,4,4]})
 
loaded_scaler = utils.load_object('Model/Modelo_Series_temporales.pkl')
 
reframed = utils.transformar(df, loaded_scaler)
 
reordenado=reframed[['weekday','month','var1(t-7)','var1(t-6)','var1(t-5)','var1(t-4)','var1(t-3)','var1(t-2)','var1(t-1)'] ]
reordenado.dropna(inplace=True)
 
"""Converting Pandas Dataframe to json
"""
data = reordenado.to_json(orient='records')
 
print('JSON para enviar en POST', data)
 
"""POST &lt;url>/predict
"""
resp = requests.post("http://localhost:5002/predict", \
                    data = json.dumps(data),\
                    headers= header)
                    
print('status',resp.status_code)
 
 
"""The final response we get is as follows:
"""
print('Respuesta de Servidor')
print(resp.json())
 


# [{"weekday":5,
# "month":4,
# "var1(t-7)":0.6333341599,
# "var1(t-6)":0.6000003815
# ,"var1(t-5)":-0.3333330154
# ,"var1(t-4)":-1.0,
# "var1(t-3)":0.6666669846,
# "var1(t-2)":-0.5,
# "var1(t-1)":0.0}]