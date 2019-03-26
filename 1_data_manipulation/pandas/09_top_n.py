# 

# # Getting the rows with the top _n_ values in a column of a pandas DataFrame

# Import modules and read inventory data
import numpy as np
import pandas as pd
inventory = pd.read_table('data/inventory/data.txt', sep="\t")
inventory

# Example: What's the least expensive game in each shop?

inventory \
  .sort_values('price', ascending=True) \
  .groupby('shop') \
  .head(1)

# To return find the _most_ expensive game in each shop,
# set `ascending=False`.
  
# Optional:
# Add `.sort_values('shop')` to arrange by shop
# Add `.reset_index(drop=True)` to reset the indices
