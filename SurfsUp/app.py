import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
mes = Base.classes.measurement
sta = Base.classes.station


app = Flask(__name__)




@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"To conduct a report of the average, higest, and lowest temperatures in relation to a set of dates you can use the link formats below replacing 'start' and 'end' with dates in the format of 'yyyy-mm-dd'.<br/>"
        f"You may encounter issues if the date ranges are outside of the dataset.<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_data = session.query(mes.date, mes.prcp).filter(mes.date >= '2016-08-23').all()
    session.close()
    prcp_j = []
    for row in prcp_data:
        prcp = row._asdict()
        prcp_dict = {(prcp["date"]):(prcp["prcp"])}
        prcp_j.append(prcp_dict)
    return jsonify(prcp_j)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sta_lst = session.query(sta.id, sta.station, sta.name, sta.latitude, sta.longitude, sta.elevation).distinct().all()
    session.close()
    station_j = []
    for row in sta_lst:
        station_r = list(np.ravel(row))
        station_j.append(station_r)
    return jsonify(station_j)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_data = session.query(mes.date, mes.tobs).filter(mes.date >= '2016-08-23', mes.station == 'USC00519281').all()
    session.close()
    tobs_j = []
    for row in tobs_data:
        tobs = row._asdict()
        tobs_dict = {(tobs["date"]):(tobs["tobs"])}
        tobs_j.append(tobs_dict)
    return jsonify(tobs_j)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    tmax = session.query(func.max(mes.tobs)).filter(mes.date >= start).first()
    tmin = session.query(func.min(mes.tobs)).filter(mes.date >= start).first()
    tavg = session.query(func.avg(mes.tobs)).filter(mes.date >= start).first()
    return {"Highest Temperature":tmax[0], "Lowest Temperature":tmin[0], "Average Temperature":tavg[0]}

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    session = Session(engine)
    tmax = session.query(func.max(mes.tobs)).filter(mes.date >= start, mes.date <= end).first()
    tmin = session.query(func.min(mes.tobs)).filter(mes.date >= start, mes.date <= end).first()
    tavg = session.query(func.avg(mes.tobs)).filter(mes.date >= start, mes.date <= end).first()
    return {"Highest Temperature":tmax[0], "Lowest Temperature":tmin[0], "Average Temperature":tavg[0]}



if __name__ == '__main__':
    app.run(debug=True)

