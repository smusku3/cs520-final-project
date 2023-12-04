#!/usr/bin/env python
# coding: utf-8

# # Importing modules

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from causallearn.search.ConstraintBased.PC import pc
from causallearn.search.ConstraintBased.FCI import fci


# # Merging the csv Files
df = pd.read_csv("annual_conc_by_monitor_2020.csv")
main_data = df[df['Parameter Name'].isin(['Ozone','PM2.5 - Local Conditions','Carbon monoxide'])]
main_data = main_data[['Year', 'State Name' , 'County Name', 'Parameter Name', '50th Percentile']]
years = list(range(2000,2020))
for year in years:
    df1 = pd.read_csv(f"annual_conc_by_monitor_{year}.csv")
    temp = df1[df1['Parameter Name'].isin(['Ozone','PM2.5 - Local Conditions','Carbon monoxide'])]
    temp = temp[['Year', 'State Name' , 'County Name', 'Parameter Name', '50th Percentile']]
    main_data = pd.concat([main_data , temp], axis = 0)

# # Preprocessing Data
main_data_c = main_data.drop('County Name', axis = 1)
grouped_df = main_data_c.groupby(['Year', 'State Name','Parameter Name']).mean()
grouped_df = grouped_df.reset_index()
df_pivot = grouped_df.pivot_table(index=['Year', 'State Name'], columns='Parameter Name', values='50th Percentile')
df_pivot = df_pivot.reset_index()
df_pivot.rename(columns={'PM2.5 - Local Conditions': 'PM2.5', 'Carbon monoxide' : 'CO', 'Ozone' : 'O3'}, inplace=True)
df_reset = df_pivot.reset_index(drop=True)
df_reset.rename(columns = {'State Name': 'State'}, inplace = True)

df_reset['Year'].unique()
df_reset['CO'].fillna(df_reset['CO'].mean(),inplace = True)
df_reset['O3'].fillna(df_reset['O3'].mean(),inplace = True)
df_reset['PM2.5'].fillna(df_reset['PM2.5'].mean(),inplace = True)

# # Reading the health data related to AIR
d = pd.read_csv('Health_Air.csv')
final_data = pd.merge(d, df_reset, on  = ['Year', 'State'], how = 'left')
final_copy = final_data.copy()
final_copy.to_csv('Final_original_merged.csv')
final_copy['CO'].fillna(final_copy['CO'].mean(),inplace = True)
final_copy['O3'].fillna(final_copy['O3'].mean(),inplace = True)
final_copy['PM2.5'].fillna(final_copy['PM2.5'].mean(),inplace = True)
final_copy.rename(columns = {'Cases': 'Asthma_Cases'} , inplace = True)
final_copy.drop('COPD',axis = 1,inplace = True)
final_copy = final_copy[(final_copy['Asthma_Cases'] != float(8965.707259953162))]
final_copy.to_csv("Main_Data_Air.csv")




