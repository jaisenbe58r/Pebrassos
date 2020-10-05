"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester
<www.linkedin.com/in/jaisenbe>

License: MIT


FECHA DE CREACIÓN: 24/05/2019

"""

import logging
import os
import pandas as pd

from flask import render_template, redirect, url_for, request, abort, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.auth.decorators import admin_required
from app.auth.models import User
from app.models import WeatherStation
from . import meteo_bp
from .forms import StationWeatherForm

logger = logging.getLogger(__name__)


@meteo_bp.route("/meteo/")
@login_required
def index():
    return render_template("meteo/index.html")


@meteo_bp.route("/meteo/stations/")
@login_required
def list_weather_stations():
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    meteo_pagination = WeatherStation.all_paginated(page, per_page)
    logger.info(meteo_pagination)
    logger.info(page)
    logger.info(per_page)
    return render_template("meteo/weatherstations.html", meteo_pagination=meteo_pagination)


@meteo_bp.route("/meteo/p/<string:slug>/", methods=['GET', 'POST'])
def show_meteo_station(slug):
    logger.info('Mostrando un post')
    logger.debug(f'Slug: {slug}')
    post = WeatherStation.get_by_slug(slug)
    if not post:
        logger.info(f'La estación {slug} no existe')
        abort(404)
    return render_template("meteo/weatherstations.html", post=post)


@meteo_bp.route("/meteo/station/", methods=['GET', 'POST'])
@login_required
@admin_required
def station_form():
    """Crea una nueva estación meterológica"""
    form = StationWeatherForm()
    if form.validate_on_submit():
        station_id = form.station_id.data
        municipio = form.municipio.data
        provincia = form.provincia.data
        altura = form.altura.data
        latitud = form.latitud.data
        latitud_gd = form.latitud_gd.data
        longitud = form.longitud.data
        longitud_gd = form.longitud_gd.data

        weather_station = WeatherStation(
            station_id=station_id,
            municipio=municipio,
            provincia=provincia,
            altura=altura,
            latitud=latitud,
            latitud_gd=latitud_gd,
            longitud=longitud,
            longitud_gd=longitud_gd,
            )
        weather_station.save()
        logger.info(f'Guardada la nueva estación metereológica {station_id}:{municipio}')
        return redirect(url_for('meteo.list_weather_stations'))
    return render_template("meteo/weatherstation_form.html", form=form)


@meteo_bp.route("/meteo/station/getauto", methods=['GET', 'POST'])
@login_required
@admin_required
def station_form_auto():
    """Crea ula estaciones meterológicas automaticamente"""
    data = pd.read_csv("data/ListadoEStaciones_CSV_v04.csv", sep=";")

    stations = WeatherStation()
    stations_ids = [r.station_id for r in stations.query.distinct()]

    for i, row in data.iterrows():
        if row["ID"] in stations_ids:
            logger.info(f'{row["ID"]}:{row["MUNICIPIO"]} ya existe en la DB')
        else:
            weather_station = WeatherStation(
                station_id=row["ID"],
                municipio=row["MUNICIPIO"],
                provincia=row["PROVINCIA"],
                altura=row["ALTURA"],
                latitud=row["LATITUD"],
                latitud_gd=row["LATITUD GD"],
                longitud=row["LONGITUD"],
                longitud_gd=row["LONGITUD GD"],
                )
            weather_station.save()
            logger.info(f'Guardada la nueva estación metereológica {row["ID"]}:{row["MUNICIPIO"]}')

    return redirect(url_for('meteo.list_weather_stations'))


@meteo_bp.route("/meteo/station/<string:station_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
def update_station_form(station_id):
    """Actualiza una estación existente"""
    station = WeatherStation.get_by_station(station_id)
    if station is None:
        logger.info(f'La estación {station_id} no existe')
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del post.
    form = StationWeatherForm(obj=station)
    if form.validate_on_submit():
        # Actualiza los campos del post existente
        station.station_id = form.station_id.data
        station.municipio = form.municipio.data
        station.provincia = form.provincia.data
        station.altura = form.altura.data
        station.latitud = form.latitud.data
        station.latitud_gd = form.latitud_gd.data
        station.longitud = form.longitud.data
        station.longitud_gd = form.longitud_gd.data

        station.save()
        logger.info(f'Guardanda la estación metereológica {station_id}:{station.municipio}')
        return redirect(url_for('meteo.list_weather_stations'))
    return render_template("meteo/weatherstation_form.html", form=form, station=station)


@meteo_bp.route("/meteo/stations/delete/<string:station_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_station(station_id):
    logger.info(f'Se va a eliminar la estación metereológica {station_id}')
    station = WeatherStation.get_by_station(station_id)
    if station is None:
        logger.info(f'La estación metereológica {station_id} no existe')
        abort(404)
    station.delete()
    logger.info(f'L aestación meterológica {station_id} ha sido eliminada')
    return redirect(url_for('meteo.list_weather_stations'))
