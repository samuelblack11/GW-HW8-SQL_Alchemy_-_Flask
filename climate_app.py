import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify
import json

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/global_warming")
def global_warming():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate Flask App."

    )

@app.route("/rain_check")
def dates():
    dates_query = session.query(Measurement.date).all()
    prcp_query = session.query(Measurement.prcp).all()
    rain_dates = list(np.ravel(dates_query))
    rain_prcp = list(np.ravel(prcp_query))
    rain_dict = dict(zip(rain_dates, rain_prcp))
    #rain_dates_dict=(rain_dates)
    return jsonify(rain_dict)

@app.route("/codes")
def alpha():
    station_query = session.query(Station.station).all()
    station_list = list(np.ravel(station_query))
    #rain_dates_dict=(rain_dates)
    return jsonify(station_list)


# query for the dates and temperature observations from a year from the last data point.
@app.route("/temps_dates")
def temperatures():
    query_date = dt.date(2016,8,23) - dt.timedelta(days=365)
    print("Query Date: ", query_date)
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=query_date).all()
    return jsonify(temps)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/metrics")
def measurements():
    query_date_2 = dt.date(2016,8,23) - dt.timedelta(days=365)
    print("Query Date: ", query_date_2)
    measure = session.query(func.max(Measurement.tobs).label('max temp'),\
                      func.min(Measurement.tobs).label('min temp'),\
                      func.avg(Measurement.tobs).label('avg temp')).filter(Measurement.date>=query_date_2).all()
    return jsonify(measure)

# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/metrics_2")
def measurements_2():
    query_date_3 = dt.date(2016,8,23) - dt.timedelta(days=365)
    end_date = dt.date(2016,8,23)
    print("Query Date: ", query_date_3)
    measure_2 = session.query(func.max(Measurement.tobs).label('max temp'),\
                      func.min(Measurement.tobs).label('min temp'),\
                      func.avg(Measurement.tobs).label('avg temp')).filter(Measurement.date>=query_date_3).filter(Measurement.date<=end_date).all()
    return jsonify(measure_2)


if __name__ == '__main__':
    app.run(debug=True)
