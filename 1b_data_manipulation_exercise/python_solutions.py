
#    Find the five worst delayed destinations (largest 
#    average arrival delay) for flights departing EWR. 
#    Include the number of flights and the average
#    arrival delay.

# Import modules and read flights data
import numpy as np
import pandas as pd

# Load the flights dataset
flights = pd.read_csv('data/flights/flights.csv')

# look at head
pd.set_option("display.html.table_schema", True)
flights.head(10)

# look at EWR flightst
flights.query('origin.isin(["EWR"])')

# find the most delayed destinations
flights \
  .query('origin.isin(["EWR"])') \
  .groupby(['dest']) \
  .agg({'arr_delay': ['count', 'mean']})['arr_delay']  \
  .reset_index() \
  .sort_values('mean', ascending=False) \
  .head(5)


#    Calculate the average air speed of each flight in 
#    units of miles per hour (`distance / air_time * 60`) 
#    rounded to the nearest integer. Return a result set
#    that includes the carrier, flight, origin, and dest
#    columns, as well as the new column giving the air 
#    speed, sorted in descending order of air speed. 
#    Remove records with missing distance or air_time.
#    What is the fastest flight in the data? The slowest?

# assign air speed of flights and select max
flights \
  .assign(
    air_speed = lambda x:
      np.round(60*x.distance/x.air_time, 0)
  ) \
  .filter(['carrier', 'flight', 'origin', 'dest', 'air_speed']) \
  .sort_values('air_speed', ascending=False) \
  .head(1)

# assign air speed of flights and select min
flights \
  .assign(
    air_speed = lambda x:
      np.round(60*x.distance/x.air_time, 0)
  ) \
  .filter(['carrier', 'flight', 'origin', 'dest', 'air_speed']) \
  .sort_values('air_speed', ascending=True) \
  .head(1)


#   Which airline's flights had the fastest average speed?

# assign air speed of flights and group by carrier
flights \
  .assign(
    air_speed = lambda x:
      np.round(60*x.distance/x.air_time, 0)
  ) \
  .filter(['carrier', 'air_speed']) \
  .groupby(['carrier']) \
  .agg({'air_speed': ['mean']})['air_speed'] \
  .reset_index() \
  .sort_values('mean', ascending=False) \
  .head(5)  


#    Which of the airlines that have at least 10,000
#    flights in the dataset had the fastest average speed?










