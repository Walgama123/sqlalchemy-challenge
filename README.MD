# Analyze and Explore the Climate Data & Design a Climate App
In this project it is going to analyze climate changes of Honolulu, Hawaii island 
and design an app that would help you to plan a vacation trip in advance. 
## Project Scope
- Analyze and Explore the Climate Data
- Design the Climate App


## Methodology 
Using the Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database.
Then design an app using python Flask API to call the analyzed end-points.

## Tools and python libraries used
- SQLAlchemy ORM queries
- Pandas
- Matplotlib
- Flask API

## Process and steps of the analysis 
- Use the SQLAlchemy create_engine() function to connect to your SQLite database.
- Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.
- Link Python to the database by creating a SQLAlchemy session.
- Retrieve the data to the app using Flask API.

## Area of analyzed
1.	Find the most recent date in the dataset.
2.	Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
3.	Select only the "date" and "prcp" values.
4.	Load the query results into a Pandas DataFrame. Explicitly set the column names.
5.	Sort the DataFrame values by "date".
6.	Plot the results by using the DataFrame plot method, as the following image shows
7.	Use Pandas to print the summary statistics for the precipitation data.
8.	Design a query to calculate the total number of stations in the dataset.
9.	Details of the most active station (Min , Max and Avg Temperature) and plot the data.

## Routs of the app
- /api/v1.0/precipitation
 - Retrieve the temperature of the last twelve months.
- /api/v1.0/stations
 - Return a JSON list of stations from the dataset.
- /api/v1.0/tobs
 - Query the dates and temperature observations of the most-active station for the previous year of data.
- /api/v1.0/<start> and /api/v1.0/<start>/<end>
 - Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

## Folders and files
- SurfsUp folder (root folder).
  - climate_starter.ipynb (Analysis codes of the project)
  - app.py (Source code of the app)
- Resources folder. 
  - hawaii.sqlite (Temperature and Precipitation data of each stations)


