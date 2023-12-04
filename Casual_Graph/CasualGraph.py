#!/usr/bin/env python
# coding: utf-8

# # Importing required Modules


import pandas as pd
from causallearn.search.ConstraintBased.PC import pc
from causallearn.utils.GraphUtils import GraphUtils
from causallearn.utils.cit import fisherz
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from causallearn.search.ConstraintBased.FCI import fci
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import statsmodels.api as sm


# # Normalizing the Data

def normalizeData(data_frame):
    label_encoder = LabelEncoder()
    data_frame['State'] = label_encoder.fit_transform(data_frame['State'])
    scaler = MinMaxScaler()
    # Normalize the dataframe column-wise
    normalized_data = pd.DataFrame(scaler.fit_transform(data_frame), columns=data_frame.columns)
    return normalized_data
    
    


# # Constructing PC Graph

def constructPCGraph(normalized_data):
    alpha_level = 0.05
    data_np = normalized_data.to_numpy()
    causal_graph = pc(data_np, indep_test=fisherz, alpha=alpha_level)
    return causal_graph.G
    


# # Constructing FCI Graph
def constructFCIGraph(normalized_data):
    alpha_level = 0.05
    data_np = normalized_data.to_numpy()
    casual_graph_fci, edges= fci(data_np, indep_test=fisherz, alpha=alpha_level)
    return casual_graph_fci
    
    


# # Converting PC and FCI graphs into images
def graphToImage(graph, filename):
    pyd = GraphUtils.to_pydot(graph)
    pyd.write_png(filename, prog = 'C:/Program Files/Graphviz/bin/dot')
    return

# Reading the data from the csv
data = pd.read_csv('Main_Data.csv', index_col = False)
# Normalizing data
normalized_data = normalizeData(data)
# Constructing PC graph
pci_graph = constructPCGraph(normalized_data)
# Saving it to image file
graphToImage(pci_graph, 'pc_air.png')
# Constructing FCI Graph
fci_graph = constructFCIGraph(normalized_data)
# Saving FCI Graph to image
graphToImage(fci_graph,'fci_air.png')
# Reading water data 
water_data = pd.read_csv('Water_Final_Data.csv',index_col = False )
# Normalizing Water Data
normalized_water_data = normalizeData(water_data)
# PC graph for water data
pci_graph_water = constructPCGraph(normalized_water_data)
# Converting graph into image
graphToImage(pci_graph_water, 'pc_water.png')
# FCI graph for water data.
fci_graph_water = constructFCIGraph(normalized_water_data)
# FCI graph to image
graphToImage(fci_graph_water, 'fci_water.png')
# Finding the ATE's using Linear Regression Coefficient
treatment_PM25 = data['PM2.5']
outcome_cases = data['Cases']
treatment_PM25_reshaped = treatment_PM25.values.reshape(-1, 1)
model_PM25 = LinearRegression()
model_PM25.fit(treatment_PM25_reshaped, outcome_cases)
ate_PM25 = model_PM25.coef_[0]
treatment_O3 = data['O3']
treatment_O3_reshaped = treatment_O3.values.reshape(-1, 1)
model_O3 = LinearRegression()
model_O3.fit(treatment_O3_reshaped, outcome_cases)
ate_O3 = model_O3.coef_[0]/100
treatment_CO = data['CO']
treatment_CO_reshaped = treatment_CO.values.reshape(-1, 1)
model_CO = LinearRegression()
model_CO.fit(treatment_CO_reshaped, outcome_cases)
ate_CO = model_CO.coef_[0]


# # Constructing bar Plot for the ATE's

ate_values = {'PM2.5': ate_PM25, 'O3': ate_O3, 'CO': ate_CO}
plt.figure(figsize=(10, 6))
plt.bar(ate_values.keys(), ate_values.values())
plt.xlabel('Pollutant')
plt.ylabel('Average Treatment Effect (ATE)')
plt.title('ATE for Different Pollutants on Number of Cases')
plt.show()


treatment_radium = water_data['Radium']
outcome_cancer_cases = water_data['Cancer Cases']
# Repeating the process for the Radium variable
treatment_radium_reshaped = treatment_radium.values.reshape(-1, 1)
model_radium = LinearRegression()
model_radium.fit(treatment_radium_reshaped, outcome_cancer_cases)
ate_radium = -model_radium.coef_[0]

# # Finding ATE's for Water without adjusting Confounders
treatment_nitrate = water_data['Nitrate']
treatment_nitrate_reshaped = treatment_nitrate.values.reshape(-1, 1)
model_nitrate = LinearRegression()
model_nitrate.fit(treatment_nitrate_reshaped, outcome_cancer_cases)
ate_nitrate = model_nitrate.coef_[0]


treatment_population = water_data['Population']
treatment_population_reshaped = treatment_population.values.reshape(-1, 1)
model_population = LinearRegression()
model_population.fit(treatment_population_reshaped, outcome_cancer_cases)
ate_population = model_population.coef_[0]

ate_values = {'Radium': ate_radium, 'Nitrate': ate_nitrate}
plt.figure(figsize=(10, 6))
plt.bar(ate_values.keys(), ate_values.values())
plt.xlabel('Pollutant')
plt.ylabel('Average Treatment Effect (ATE)')
plt.title('ATE Without Adjusting Confounders')
plt.show()


# # Finding ATE's for Water with adjusting Confounders
treatment = 'Nitrate'
outcome = 'Cancer_Cases'
confounders = ['Poverty', 'Demograph']
formula = outcome + ' ~ ' + treatment + ' + ' + ' + '.join(confounders)
model = sm.formula.ols(formula, data=water_data).fit()
ate_nitrate_adjusted = model.params[treatment]

treatment = 'Radium'
outcome = 'Cancer_Cases'
confounders = ['Poverty', 'Demograph']
formula = outcome + ' ~ ' + treatment + ' + ' + ' + '.join(confounders)
model = sm.formula.ols(formula, data=water_data).fit()
ate_radium_adjusted = model.params[treatment]

ate_values = {'Radium': ate_radium_adjusted, 'Nitrate': ate_nitrate_adjusted}
plt.figure(figsize=(10, 6))
plt.bar(ate_values.keys(), ate_values.values())
plt.xlabel('Pollutant')
plt.ylabel('Average Treatment Effect (ATE)')
plt.title('ATE Without Adjusting Confounders')
plt.show()

