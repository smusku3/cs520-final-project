#!/usr/bin/env python
# coding: utf-8

# # Importing Modules

# In[1]:


import pandas as pd


# # Convert the text into csv

# In[7]:


def creatingCSV(source_file, dest_file):
    with open(source_file, 'r') as input_file, open(dest_file, 'w') as output_file:
        # Read the input file line by line
        for line in input_file:
            # Replace horizontal tabs with commas and write to the output file
            line = line.replace(',','')
            modified_line = line.replace('\t', ',')
            output_file.write(modified_line)


# In[9]:


years = list(range(2000,2015))
for year in years:
    input_file = f'{year}.txt'
    output_file = f'{year}_Water.csv'
    creatingCSV(input_file, output_file)


# In[ ]:





# # Merging all the CSV Files

# In[10]:


main_df = pd.read_csv('2000.csv')


# In[11]:


for year in range(2001,2015):
    df = pd.read_csv(f'{year}.csv')
    main_df = pd.concat([main_df, df])


# In[12]:


main_df.drop(columns= ['PWS Name', 'PWS Id', 'Population Served', 'Maximum Contaminant Level'], axis =0, inplace = True)


# In[13]:


main_df.drop(columns = ['County'], axis = 0, inplace = True)


# In[17]:


result = main_df.groupby(['Year','State']).mean()


# In[18]:


result = result.reset_index()


# In[21]:


radium['Year'].dtype


# In[20]:


radium = pd.read_csv('radium.csv')


# In[22]:


radium = radium[0:346]


# In[23]:


radium['Year'] = radium['Year'].astype(int)


# In[24]:


result_df = pd.merge(result,radium, on = ['Year','State'], how = 'inner')


# In[25]:


result_df.to_csv('Water.csv')


# In[26]:


water_data = pd.read_csv('2001_Water.csv')


# In[27]:


for year in range(2002,2015):
    df = pd.read_csv(f'{year}_Water.csv')
    water_data = pd.concat([water_data,df])


# In[28]:


water_data.to_csv('Water_data.csv')


# In[29]:


water_data

