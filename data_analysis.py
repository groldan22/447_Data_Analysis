import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import numpy as np

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


#------------------------------Rental Analysis-----------------------------------------------------------

# Drop the columns are not unnecessary
df_rental.columns
df_rental.drop(['RegionID', 'SizeRank', 'RegionType', 'StateName', 'Metro'], axis =1, inplace = True)
df_rental.columns

# Get the State only in the DMV
stateList = ['VA', 'MD', 'DC']
df_DMV = df_rental[df_rental['State'].isin(stateList) == True]
print(df_DMV)

# Drop NaN drow in data frame
df_DMV= df_DMV.dropna()

# Get to know the data
df_DMV.dtypes

# Analyze the rental for each state

# rental for VA
rental_VA = df_DMV[df_DMV['State'] == 'VA']
print(rental_VA)
rental_VA.drop(['State', 'CountyName'], axis =1, inplace = True)
rental_VA = rental_VA.T
rental_VA.reset_index(inplace = True, drop = False)
rental_VA = rental_VA.rename(columns=rental_VA.iloc[0])
rental_VA.drop(rental_VA.index[0], inplace = True)
rental_VA.rename(columns = {'RegionName': 'Date'}, inplace = True)
rental_VA.reset_index(inplace=True, drop=True)

# Find the maximum and the minimum of the rental price in VA
mean_VA = rental_VA.mean(axis=0)
mean_VA
mean_VA.min()
mean_VA.max()


# rental for MD
rental_MD = df_DMV[df_DMV['State'] == 'MD']
print(rental_MD)
rental_MD.drop(['State', 'CountyName'], axis =1, inplace = True)
rental_MD = rental_MD.T
rental_MD.reset_index(inplace = True, drop = False)
rental_MD = rental_MD.rename(columns=rental_MD.iloc[0])
rental_MD.drop(rental_MD.index[0], inplace = True)
rental_MD.rename(columns = {'RegionName': 'Date'}, inplace = True)

# Find the maximum and the minimum of the rental price in MD
mean_MD = rental_MD.mean(axis=0)
mean_MD
mean_MD.min()
mean_MD.max()
mean_MD.mean()

# rental for DC
rental_DC = df_DMV[df_DMV['State'] == 'DC']
print(rental_DC)
rental_DC.drop(['State', 'CountyName'], axis =1, inplace = True)
rental_DC = rental_DC.T
rental_DC.reset_index(inplace = True, drop = False)
rental_DC = rental_DC.rename(columns=rental_DC.iloc[0])
rental_DC.drop(rental_DC.index[0], inplace = True)
rental_DC.rename(columns = {'RegionName': 'Date'}, inplace = True)

# Find the maximum and the minimum of the rental price in DC
mean_DC = rental_DC.mean(axis=0)


# Visualization

# Plot the rental price between state
df = pd.DataFrame({'County':['MD', 'VA', 'DC'], 'Rental Price':[mean_MD.mean(), mean_VA.mean(), mean_DC.mean() ]})
ax = df.plot.bar(x='County', y='Rental Price', rot=0)
plt.savefig(pngs_folder + 'rental_price')

# Plot rental VA
rental_VA.plot(subplots = True, layout = (8,5), figsize = (20,10))
plt.savefig(pngs_folder + 'Rental_VA')
# Plot rental MD
rental_MD.plot(subplots = True, layout = (8,5), figsize = (20,10))
plt.savefig(pngs_folder + 'Rental_MD')
# Plot rental DC
rental_DC.plot(subplots = True)
plt.savefig(pngs_folder + 'Rental_DC')


# ---------------------------------------------------------------------------------------------------------------------
# modify plot and show
"""---------------------------"""
# TO DO: Create a data visualization that shows the top 10 counties from Maryland based on the price values - Viphu
# Removing the NaN with 0 values
df_rental2 = df_rental2.fillna(0)
maryland = df_rental2[df_rental2['State'] == 'MD']
# Remove the column for city name
maryland = maryland.drop(['RegionName'], axis=1)

# Merge all of the date columns to rows
maryland2 = maryland.melt(id_vars=['State', 'CountyName'],
                          var_name='Date',
                          value_name='Value')
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)

maryland3 = maryland2.groupby(
    ['CountyName', 'Date', 'Value']).size().sort_values(ascending=False)

# Export to CSV
# maryland3.to_csv(data_path + 'maryland_raw_county_data.csv')

# Ingest the file
maryland4 = data_path + 'maryland_raw_county_data.csv'
md = pd.read_csv(maryland4)

# Drop all of the rows with zero values
md = md.loc[~((md['Value'] == 0))]

md['Value'] = md['Value'].apply(np.ceil)
md['Value'] = md['Value'].astype(np.int64)

# Drop the column with unnecessary values
md.drop('0', axis=1, inplace=True)

# print(md.head())

# Export to CSV
# md.to_csv(cleanData_folder + 'maryland_county_data.csv')

# To display a graph of price per county
md['Value'].plot(kind='bar')
plt.xticks(rotation=30, horizontalalignment='center')
plt.title("Price Per County")
plt.xlabel("County")
plt.ylabel("Price Values")
plt.show()
"""---------------------------"""

# ---- country wide plot and csv export ----
# gerson test commit here
# modify plot and show
# plt.xlabel("Year")
# plt.ylabel("Price")
# plt.plot(df_state["Maryland"], label="MD")
# plt.plot(df_state["Virginia"], label="VA")
# plt.plot(df_state["District of Columbia"], label="DC")
# plt.legend()
# plt.savefig(pngs_folder + 'state_time_series.png')
# plt.show()

# export table
# df_state.to_csv(cleanData_folder + "regions_table.csv")
# df_rental.to_csv(cleanData_folder + "ingested_rental.csv")
# df_home_value_zip.to_csv(cleanData_folder + "ingested_zip_home_value.csv")

# --------------------
