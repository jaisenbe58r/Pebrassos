"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester
<www.linkedin.com/in/jaisenbe>

License: MIT


FECHA DE CREACIÓN: 24/01/2019

"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, DateField, TextAreaField, BooleanField, SelectField, IntegerField, FloatField)
from wtforms.validators import DataRequired, Length, Optional


class StationWeatherForm(FlaskForm):
    station_id = StringField('Estación Metereológica', validators=[DataRequired(), Length(max=8)])
    municipio = StringField('Municipio', validators=[DataRequired(), Length(max=80)])
    provincia = StringField('Provincia', validators=[DataRequired(), Length(max=80)])
    altura = IntegerField('Altura', validators=[DataRequired()])
    latitud = FloatField('Latitud')
    latitud_gd = FloatField('Latitud GD', validators=[DataRequired()])
    longitud = FloatField('Longitud', validators=[Length(max=8)])
    longitud_gd = FloatField('Longitud GD', validators=[DataRequired()])

    submit = SubmitField('Guardar')
