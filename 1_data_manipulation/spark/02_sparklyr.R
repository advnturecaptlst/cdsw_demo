# 

# # sparklyr example with dplyr verbs

# Load required packages
library(sparklyr)
library(dplyr)

# Start a Spark session
spark <- spark_connect(master = "local")

# Load the data
flights <- tbl(spark, "flights")

# Use dplyr verbs to perform operations on the Spark
# DataFrame and return a pointer to the result DataFrame
flights %>%
  filter(dest == "LAS") %>%
  group_by(origin) %>%
  summarise(
    num_departures = n(),
    avg_dep_delay = mean(dep_delay, na.rm = TRUE)
  ) %>%
  arrange(avg_dep_delay)

# In this case, the full result DataFrame is printed to the
# screen because it's so small

# End the Spark session
spark_disconnect(spark)
