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
city_rental_path = data_path + "City_zori_sm_month.csv"
zip_home_value_path = data_path + \
    "Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"

# --------------------

# ----- create data frames for the Homevalue here -----
df = pd.read_csv(state_stats_path)
# print(df)
# Create data frames for Rental -----
df_rental = pd.read_csv(city_rental_path)
# print(df_rental)
# Create data frames for Home value by zipcode
df_home_value_zip = pd.read_csv(zip_home_value_path)
# print(df_home_value_zip)
# --------------------


# ---- country wide manipulation ----
# !!!reformat so that all other states have their own data frame in similar format is needed!!!
# !!!print data frame df to see old vs "clean". They should look the same!!!
region_list = ["Maryland", "Virginia", "District of Columbia"]
region_list2 = ["MD", "VA", "DC"]
# # remove all states but Maryland Virginia and DC
df_state = df[df.RegionName.isin(region_list) == True]
df_rental = df_rental[df_rental.State.isin(region_list2) == True]
# #remove unecessary columns
df_state = df_state.drop(["RegionID"], 1)
df_state = df_state.drop(["SizeRank"], 1)

# # transpose + clean
df_state = df_state.T
df_state.reset_index(inplace=True, drop=False)
# update header to first row then delete un-needed rows. Make print statements between rows to see changes.
df_state = df_state.rename(columns=df_state.iloc[0])
df_state.drop(df_state.index[0], inplace=True)
df_state.drop(df_state.index[0], inplace=True)
df_state.drop(df_state.index[0], inplace=True)
df_state.rename(columns={'RegionName': 'Date'}, inplace=True)
df_state.reset_index(inplace=True, drop=True)

# Dropping the rows that are unnecessary
df_rental2 = df_rental.drop(
    ['RegionID', 'SizeRank', 'RegionType', 'StateName', 'Metro'], axis=1)
# print(df_rental2)

# --------------------
# modify plot and show
"""---------------------------"""
# TO DO: Create a data visualization that shows the top 10 counties from Maryland based on the price values - Viphu
# Removing the NaN with 0 values
df_rental2 = df_rental2.fillna(0)
maryland = df_rental2[df_rental2['State'] == 'MD']
# Remove the column for city name
maryland = maryland.drop(['RegionName'], axis=1)
# print(maryland)
# print(maryland.dtypes)

# maryland = maryland['CountyName'].nlargest(10)

# Create category counts for the Counties variable
maryland_counties = maryland.groupby(['CountyName'], sort=False).size().sort_values(ascending=False)

# maryland_counties = (maryland_counties.set_index(["State", "CountyName"])
#          .stack()
#          .reset_index(name='Value')
#          .rename(columns={'level_2':'Date'}))
# print(maryland_counties)

# Merge all of the date columns to rows
maryland2 = maryland.melt(id_vars=['State', 'CountyName'],
              var_name='Date',
              value_name='Value')
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)
# print(maryland2)

maryland3 = maryland2.groupby(['CountyName', 'Date', 'Value']).size().sort_values(ascending=False)
# print(maryland3)

# Export to CSV
maryland3.to_csv('TestB.csv')

# To display a graph of price per county
# plt.title("Price Per County")
# plt.xlabel("County")
# plt.ylabel("Price Values")
# xlabel = maryland['CountyName']
# ylabel = maryland['']
# plt.xticks(xlabel)
# plt.yticks()
# plt.plot(xlabel, )
# # plt.savefig(pngs_folder + 'county_.png')
# plt.show()
"""---------------------------"""

# ---- country wide plot and csv export ----
# modify plot and show
plt.xlabel("Year")
plt.ylabel("Price")
plt.plot(df_state["Maryland"], label="MD")
plt.plot(df_state["Virginia"], label="VA")
plt.plot(df_state["District of Columbia"], label="DC")
plt.legend()
plt.savefig(pngs_folder + 'state_time_series.png')
# plt.show()

# export table
# df_state.to_csv(cleanData_folder + "regions_table.csv")
# df_rental.to_csv(cleanData_folder + "ingested_rental.csv")
# df_home_value_zip.to_csv(cleanData_folder + "ingested_zip_home_value.csv")

# --------------------
