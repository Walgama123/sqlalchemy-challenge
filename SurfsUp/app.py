#!/usr/bin/env python
# coding: utf-8

# Import the dependencies.
import numpy as np
import datetime as dt
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect,desc

from flask import Flask, jsonify

# Ignore SQLITE warnings related to Decimal numbers in the hawaii database
import warnings
warnings.filterwarnings('ignore')

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#Create data points
#most_recent_date=dt.date(2017,8,23)
most_recent_date=session.query(Measurement.date).order_by(desc(Measurement.date)).first()
most_recent_date=most_recent_date[0]
most_recent_date=datetime.strptime(most_recent_date, '%Y-%m-%d').date()
# Calculate the date one year from the last date in data set.
previous_year_date=most_recent_date - dt.timedelta(days=365)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-01-01<br/>"
        f"/api/v1.0/2016-01-01/2016-12-31<br/>"
    )
#Return all from precipitation_dict(date and the precipitation )
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create an empty dictionary 
    precipitation_dict={}
    # Perform a query to retrieve the data and precipitation scores
    prcpresult =session.query(Measurement.date,Measurement.prcp)\
                .where(Measurement.date.between(previous_year_date, most_recent_date))\
                .order_by(desc(Measurement.date)) 
    for prcp in prcpresult:
        precipitation_dict[prcp.date]=prcp.prcp

    return jsonify(precipitation_dict)

#Return the station list 
@app.route("/api/v1.0/stations")
def station():
    #Create station dictionary
    station_dict=[row[0] for row in session.query(Station.station).all()]
    return jsonify(station_dict)

#Return the temprature of the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    #Create a dictionary for the temprature of the most active station
    # List the stations and their counts in descending order.
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)) \
                        .group_by(Measurement.station) \
                        .order_by(func.count(Measurement.station).desc()) \
                        .first()

    most_active_station=most_active_station[0]
    most_active_station_temp={}
    temperature=session.query(Measurement.date,Measurement.tobs)\
                       .where(Measurement.station==most_active_station)\
                       .where(Measurement.date.between(previous_year_date, most_recent_date))
    #append data to the dictionary
    for temp in temperature:
        most_active_station_temp[temp.date]=temp.tobs

    return jsonify(most_active_station_temp)
#Return min,max and avg temprature after a given date
@app.route("/api/v1.0/<start_date>")
def temp_details_after_start_date(start_date):
    temp_details=session.query(func.min(Measurement.tobs),\
                  func.max(Measurement.tobs),\
                  func.avg(Measurement.tobs))\
                 .where(Measurement.date>=start_date)
    
    if temp_details[0][0] is not None:
        temp_dict={"Min":temp_details[0][0],
                   "Max":temp_details[0][1],
                   "Avg":round(temp_details[0][2],2)
                }
        return jsonify(temp_dict)
    else:
         return("No data found after the given date")
   
#Return min,max and avg temprature for a  given date range
@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_details_date_range(start_date,end_date):
    temp_details_range=session.query(func.min(Measurement.tobs),\
                  func.max(Measurement.tobs),\
                  func.avg(Measurement.tobs))\
                 .where(Measurement.date.between(start_date, end_date))
    
    if temp_details_range[0][0] is not None:
        temp_dict_range={"Min":temp_details_range[0][0],
                        "Max":temp_details_range[0][1],
                        "Avg":round(temp_details_range[0][2],2)
                        }
        return jsonify(temp_dict_range)
    else:
        return("No data found for the given date range")
    
#closing the session    
session.close()
if __name__ == '__main__':
    app.run(debug=True)