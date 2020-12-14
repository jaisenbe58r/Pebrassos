"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester  
<www.linkedin.com/in/jaisenbe>

License: MIT


FECHA DE CREACIÓN: 08/07/2019

"""

import os
from .default import *


SECRET_KEY = '5e04a4955d8878191923e86fe6a0dfb24edb226c87d6c7787f35ba4698afc86e95cae409aebd47f7'
DEBUG = True  # Quitar

APP_ENV = APP_ENV_PRODUCTION

USER = os.environ["MYSQL_USER"]
PASSWORD = os.environ["MYSQL_PASSWORD"]
HOST = os.environ["MYSQL_HOST"]
DATABASE = os.environ["MYSQL_DATABASE"]
PORT = os.environ["MYSQL_PORT"]

# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:1234@localhost:3307/Pebrassos'
SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'