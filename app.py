import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
from datetime import datetime

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

###List all routes that are available.

@app.route("/")
def surfs_up():
    return (
        f"Welcome to the climate app<br/>"
        f"Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

###Convert the query results to a dictionary using `date` as the key and `prcp` as the value.


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    start_date = dt.date(2016,8,23)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date > start_date).order_by(measurement.date).all()
    session.close()
    date_tobs = []                                                                   
    for row in results:
        dict = {}
        dict['date'] = row.date
        dict['tobs'] = row.tobs
        date_tobs.append(dict)
                                                                       
    return jsonify(date_tobs)

###Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(measurement.station, station.name).group_by(measurement.station).all()
    session.close()
    
    station_list = []
    for row in results:
        dict={}
        dict['name'] = row.name
        dict['station'] = row.station
        station_list.append(dict)

    return jsonify(station_list)

###Query the dates and temperature observations of the most active station for the last year of data.

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    start_date = dt.date(2016,8,23)
    results = session.query(measurement.date, measurement.tobs).filter(measurement.date > start_date).filter(Measurement.station == 'USC00519281').all()
    session.close()

    temp_tobs = []
    for date, temp in results:
        dict = {}
        dict["Date"] = date
        dict["Temperature"] = temp
        tobs.append(dict)

    return jsonify(temp_tobs)

###Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
###When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

@app.route("/api/v1.0/<start>")
def start():
    start_date = dt.date(2016,8,23)
    end_date = dt.date(2017,8,23)
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    temp_summ = []
    for min, avg, max in results:
        dict = {}
        dict["Minimum Temperature"] = min
        dict["Avgerage Temperature"] = avg
        dict["Maximum Temperature"] = max
        temp_summ.append(dict)
        
    return jsonify(temp_summ)

###When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.


@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end():
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date > start_date).filter(measurement.date < end_date).all()
    session.close()

    temp_summ2 = []
    for min, avg, max in results:
        dict = {}
        dict["Minimum Temperature"] = min
        dict["Avgerage Temperature"] = avg
        dict["Maximum Temperature"] = max
        temp_summ.append(dict)
        
    return jsonify(temp_summ2)
        
if __name__ == '__main__':
    app.run(debug=False)                                                           