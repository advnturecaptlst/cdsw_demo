# 

# # Read data from a Hive table into an R data frame

# ## Using odbc and DBI

# Load packages
library(odbc)
library(DBI)

# Connect to Impala with ODBC
impala <- dbConnect(
  drv = odbc(),
  dsn = "Impala DSN"
)

# Read data into a data frame
games <- dbGetQuery(impala, "SELECT * FROM games")

# Disconnect
dbDisconnect(impala)

# View the data as a data frame
games

# View the data as a tibble
library(tibble)
as.tibble(games)
