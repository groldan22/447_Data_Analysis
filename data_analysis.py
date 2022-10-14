import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

# read current working directory
print(os.getcwd())
# create base univeral path for importing of CSVs. add CSVs below as needed using
# the main path variable created below
path = Path(__file__).parent.absolute()
path = str(path)

# store data path here
data_path = str(path) + "/data"

# store cleanData path here
clean_data_path = str(path) + "/cleanData/"

# set path names here
state_stats_path = data_path + "/State_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"

# ----- create data frames here -----
df = pd.read_csv(state_stats_path)

# ---- end of data frame creation ---


# ---- country wide analysis ----
# !!!reformat so that all other states have their own data frame in similar format is needed!!!
# !!!print data frame df to see old vs "clean". They should look the same!!!
region_list = ["Maryland", "Virginia", "District of Columbia"]
# remove all states but Maryland Virginia and DC
df_regions = df[df.RegionName.isin(region_list) == True]
#remove unecessary columns
df_regions = df_regions.drop(["RegionID"],1)
df_regions = df_regions.drop(["SizeRank"],1)

# transpose + clean 
df_regions = df_regions.T
df_regions.reset_index(inplace=True, drop=False)
# update header to first row then delete un-needed rows. Make print statements between rows to see changes.
df_regions = df_regions.rename(columns=df_regions.iloc[0])
df_regions.drop(df_regions.index[0], inplace = True)
df_regions.drop(df_regions.index[0], inplace = True)
df_regions.drop(df_regions.index[0], inplace = True)
df_regions.rename(columns = {'RegionName':'Date'}, inplace = True)
df_regions.reset_index(inplace=True, drop=True)

# plot 



plt.xlabel("Year")
plt.ylabel("Price")
plt.plot(df_regions["Maryland"], label = "MD")
plt.plot(df_regions["Virginia"], label = "VA")
plt.plot(df_regions["District of Columbia"], label = "DC")
plt.legend()
# plt.show()
# export table
print(os.getcwd())
print(path)
df_regions.to_csv(clean_data_path + " regions_table.csv")
