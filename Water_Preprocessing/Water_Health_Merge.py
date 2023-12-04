#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt


# # Joining the water Health Data

df = pd.read_csv("poverty.csv")
df1 = pd.read_csv("income.csv")
df2  =  pd.read_csv("demograph.csv")
result_df = pd.merge(df, df1, on=['State','Year'], how='inner')
result_df = pd.merge(result_df, df2, on = ['State', 'Year'], how = 'inner')

water = pd.read_csv("Water.csv")
final = pd.merge(result_df,water,on = ['Year', 'State'], how = 'inner')


water_data = pd.read_csv("Water_data.csv")
cancer_data = pd.read_csv("cancer.csv")
water_cancer = pd.merge(water_data,cancer_data, on = ['Year', 'State'], how = 'inner')
water_cancer.drop(columns = ['Unnamed: 0'], inplace = True)
water_cancer.rename(columns = {'Data Value':'Population', 'Cases': 'Cancer Cases'}, inplace = True)
final_data = pd.merge(final,water_cancer, on = ['Year', 'State'], how = 'inner')
final_data.to_csv('Water_Final_Data.csv')

