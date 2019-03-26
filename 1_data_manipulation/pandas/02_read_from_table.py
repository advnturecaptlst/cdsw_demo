# 

# # Read data from a Hive table into a pandas DataFrame

# Import modules
import numpy as np
import pandas as pd


# ## Using impyla

import impala.dbapi
con = impala.dbapi.connect(host='worker-1', port=21050)
sql = 'SELECT * FROM games'
games = pd.read_sql(sql, con)
games


# ## Using pyodbc

import pyodbc
con = pyodbc.connect('DSN=Impala DSN', autocommit=True)
sql = 'SELECT * FROM games'
games = pd.read_sql(sql, con)
games
