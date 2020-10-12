"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester  
<www.linkedin.com/in/jaisenbe>

License: MIT


FECHA DE CREACIÓN: 24/05/2019

"""

from flask import Blueprint

meteo_bp = Blueprint('meteo', __name__, template_folder='templates')

from . import routes
from . import api_meteo
