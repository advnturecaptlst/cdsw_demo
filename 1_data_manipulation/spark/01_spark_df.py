# 

# ## Spark DataFrame API example (with PySpark)

# Import the required modules
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, count, mean

# Start a Spark session
spark = SparkSession.builder.master('local').getOrCreate()

# Load the data
flights = spark.table('flights')

# Display a subset of rows from the Spark DataFrame
flights

# Use Spark DataFrame methods to perform operations on the
# DataFrame and return a pointer to the result DataFrame
flights \
  .filter(col('dest') == lit('LAS')) \
  .groupBy('origin') \
  .agg( \
       count('*').alias('num_departures'), \
       mean('dep_delay').alias('avg_dep_delay') \
  ) \
  .orderBy('avg_dep_delay') \
  .show()

# In this case, the full result DataFrame is printed to the
# screen because it's so small

# End the Spark session
spark.stop()
