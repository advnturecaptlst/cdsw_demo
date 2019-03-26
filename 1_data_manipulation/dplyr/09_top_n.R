# 

# # Getting the rows with the top _n_ values in a column of an R data frame

# Load packages and read inventory data
library(readr)
library(dplyr)
inventory <- read_tsv("data/inventory/data.txt")
inventory

# Example: What's the least expensive game in each shop?

inventory %>%
  group_by(shop) %>%
  top_n(1, price)

# To return the _most_ expensive game in each shop, set
# -1 as the `n` argument to `top_n()`

# It is also possible to achieve this using dplyr's
# [windowed rank functions](https://dplyr.tidyverse.org/reference/ranking.html)
