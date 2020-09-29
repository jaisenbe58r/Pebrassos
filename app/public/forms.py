"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester  
<www.linkedin.com/in/jaisenbe>

License: MIT


FECHA DE CREACIÓN: 24/01/2019

"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    content = TextAreaField('Contenido', validators=[DataRequired(), ])
    submit = SubmitField('Comentar')
