#!/usr/bin/env python3
"""Copyright (c) 2020 Jaime Sendra Berenguer & Carlos Mahiques Ballester

Pebrassos - Machine Learning Library Extensions

Author:Jaime Sendra Berenguer & Carlos Mahiques Ballester  
<www.linkedin.com/in/jaisenbe>

License: MIT


FECHA DE CREACIÓN: 05/10/2020

"""

import logging

import os
import pyowm
import json
import pandas as pd
from datetime import datetime
from flask import render_template, redirect, url_for, abort, current_app

from sqlalchemy import desc

from . import meteo_bp
from app.models import HistWeatherStatiion
from app.models import WeatherStation
from app.common.table_db import Hist_meteo


logger = logging.getLogger(__name__)

KEY = os.environ['KEY_OWM']
owm = pyowm.OWM(KEY)


def get_data(obs):
    data = json.loads(obs.to_JSON())

    return {
    "reception_time": datetime.fromtimestamp(data["reception_time"]),
    "Location_name": data["Location"]["name"],
    "Location_lon": data["Location"]["coordinates"]["lon"],
    "Location_lat": data["Location"]["coordinates"]["lat"],
    "ID": data["Location"]["ID"], 
    "country": data["Location"]["country"],

    "reference_time": datetime.fromtimestamp(data["Weather"]["reference_time"]),
    "sunset_time": datetime.fromtimestamp(data["Weather"]["sunset_time"]),
    "sunrise_time": datetime.fromtimestamp(data["Weather"]["sunrise_time"]),

    "clouds": data["Weather"]["clouds"],
    "rain": data["Weather"]["rain"],

    "wind_speed": data["Weather"]["wind"]["speed"],
    "wind_deg": data["Weather"]["wind"]["deg"],

    "humidity": data["Weather"]["humidity"],

    "pressure": data["Weather"]["pressure"]["press"],
    "sea_level": data["Weather"]["pressure"]["sea_level"],

    "temp": data["Weather"]["temperature"]["temp"],
    "temp_kf": data["Weather"]["temperature"]["temp_kf"],
    "temp_max": data["Weather"]["temperature"]["temp_max"],
    "temp_min": data["Weather"]["temperature"]["temp_min"],

    "status": data["Weather"]["status"],
    "detailed_status": data["Weather"]["detailed_status"],
    "weather_code": data["Weather"]["weather_code"],
    "weather_icon_name": data["Weather"]["weather_icon_name"],

    "visibility_distance": data["Weather"]["visibility_distance"],
    "dewpoint": data["Weather"]["dewpoint"],
    "humidex": data["Weather"]["humidex"],
    "heat_index": data["Weather"]["heat_index"]
    }


@meteo_bp.route("/meteo/actual/<string:station_id>/")
def database_station(station_id):

    stations = WeatherStation()
    _station = stations.get_by_station(station_id)
    if _station is None:
        logger.info(f'La estación {station_id} no existe')
        abort(404)
    _municipio = _station.municipio
    try:
        obs = owm.weather_at_place(f'{_municipio}, ES')
    except:
        logger.info(f'La estación {_municipio} no existe')
        abort(404)
    logger.info(_municipio)

    return render_template("meteo/weatherstation.html", station_id=station_id, data=get_data(obs))


@meteo_bp.route("/meteo/hist/<string:station_id>/")
def database_hist_station(station_id):
    results = []
    logger.info(station_id)
    station = HistWeatherStatiion()
    results = station.query.filter_by(station_id=station_id).order_by(HistWeatherStatiion.reception_time.desc())

    if results is None:
        logger.info(f'La estación {station_id} no existe en la DB')
        abort(404)

    table = Hist_meteo(results)
    table.border = True

    return render_template("meteo/weatherstation_hist.html", station_id=station_id, table=table)


@meteo_bp.route("/meteo/savedb")
def database():
    scheduler_db()
    return {"response": "OK"}


def scheduler_db():
    stations = WeatherStation()
    logger.info("---------")
    logger.info(stations.query.distinct())
    stations_ids = [r.station_id for r in stations.query.distinct()]
    logger.info(stations_ids)

    if stations_ids is None:
        logger.info('No existen estaciones dadas de alta')
        abort(404)

    for station_id in stations_ids:
        station = stations.get_by_station(station_id)
        _municipio = station.municipio
        try:
            obs = owm.weather_at_place(f'{_municipio}, ES')
            logger.info(_municipio)
            data_to_db(get_data(obs), station_id)
        except:
            logger.info(f'Pyowm no envuentra el municipio {_municipio}')


def data_to_db(data, station_id):
    """Insertar datos en DB de la estación meterológica"""

    weather_data = HistWeatherStatiion(
        station_id=station_id,
        reception_time=data["reception_time"],
        Location_name=data["Location_name"],
        Location_lon=data["Location_lon"],
        Location_lat=data["Location_lat"],
        id_loc=data["ID"],
        country=data["country"],
        reference_time=data["reference_time"],
        sunset_time=data["sunset_time"],
        sunrise_time=data["sunrise_time"],
        clouds=data["clouds"],
        # rain=data["rain"],
        wind_speed=data["wind_speed"],
        wind_deg=data["wind_deg"],
        humidity=data["humidity"],
        pressure=data["pressure"],
        sea_level=data["sea_level"],
        temp=data["temp"],
        temp_kf=data["temp_kf"],
        temp_max=data["temp_max"],
        temp_min=data["temp_min"],
        status=data["status"],
        detailed_status=data["detailed_status"],
        weather_code=data["weather_code"],
        weather_icon_name=data["weather_icon_name"],
        visibility_distance=data["visibility_distance"],
        dewpoint=data["dewpoint"],
        humidex=data["humidex"],
        heat_index=data["heat_index"],
        )
    try:
        weather_data.save()
        logger.info(f'\nGuardados los datos de la estación metereológica {weather_data.station_id}:{weather_data.Location_name}')
    except:
        logger.info(f'\nExcepción durante el guardado en db {weather_data.station_id}:{weather_data.Location_name}')
