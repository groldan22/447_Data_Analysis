import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

# ---- set universal paths here ----
# read current working directory
# print(os.getcwd())
# create univeral path for current working directory.
path = Path(__file__).parent.absolute()
path = str(path)

# path to data, cleanData, and pngs folder here. 
data_path = str(path) + "/data/"
cleanData_folder = str(path) + "/cleanData/"
pngs_folder = str(path) + "/pngs/"

# set file paths to INGEST here.
state_stats_path = data_path + "State_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"

# --------------------

# ----- create data frames here -----
df = pd.read_csv(state_stats_path)

# --------------------


# ---- country wide manipulation ----
# !!!reformat so that all other states have their own data frame in similar format is needed!!!
# !!!print data frame df to see old vs "clean". They should look the same!!!
region_list = ["Maryland", "Virginia", "District of Columbia"]
# remove all states but Maryland Virginia and DC
df_state = df[df.RegionName.isin(region_list) == True]
#remove unecessary columns
df_state = df_state.drop(["RegionID"],1)
df_state = df_state.drop(["SizeRank"],1)

# transpose + clean 
df_state = df_state.T
df_state.reset_index(inplace=True, drop=False)
# update header to first row then delete un-needed rows. Make print statements between rows to see changes.
df_state = df_state.rename(columns=df_state.iloc[0])
df_state.drop(df_state.index[0], inplace = True)
df_state.drop(df_state.index[0], inplace = True)
df_state.drop(df_state.index[0], inplace = True)
df_state.rename(columns = {'RegionName':'Date'}, inplace = True)
df_state.reset_index(inplace=True, drop=True)

# --------------------

# ---- country wide plot and csv export ----
# modify plot and show
plt.xlabel("Year")
plt.ylabel("Price")
plt.plot(df_state["Maryland"], label = "MD")
plt.plot(df_state["Virginia"], label = "VA")
plt.plot(df_state["District of Columbia"], label = "DC")
plt.legend()
plt.savefig(pngs_folder + 'state_time_series.png')
plt.show()

# export table
df_state.to_csv(cleanData_folder + "regions_table.csv")

# --------------------

