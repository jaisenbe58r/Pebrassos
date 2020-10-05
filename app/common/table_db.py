"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester
<www.linkedin.com/in/jaisenbe>

License: MIT


FECHA DE CREACIÓN: 20/09/2020

"""

from flask_table import Table, Col


class Hist_meteo(Table):
    id = Col('Id', show=False)
    reception_time = Col('reception_time')
    Location_name = Col('Location_name')
    country = Col('country')
    sunset_time = Col('sunset_time')
    sunrise_time = Col('sunrise_time')
    clouds = Col('clouds')
    wind_speed = Col('wind_speed')
    wind_deg = Col('wind_deg')
    humidity = Col('humidity')
    pressure = Col('pressure')
    temp_max = Col('temp_max')
    temp_min = Col('temp_min')
    temp = Col('temp')
    status = Col('status')
    detailed_status = Col('detailed_status')
