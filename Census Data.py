# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 12:20:04 2019

@author: Robert Schuldt
@email: rfschuldt@uams.edu

This is a practice on connecting to US Census data using the API provided by 
census.gov. Eventually this will be a test for creating a binary classifier
for proof of concept. 
"""
import census
import us
import requests
import pandas as pd
import json

from census import Census
from us import states
#Identify the columns that we are going to be interested in

#columns = ['COUNTY','STATE','B11001_001E','B18135_001E','B25110_006E']

columns = ['CP02_2011_001E','CP02_2012_015E','CP03_2015_069E','CP04_2015_058E','CP03_2015_097E',  ]

#Connecting to Census data with API key
print('Requesting data from the American Communities Survey')

acs = requests.get("https://api.census.gov/data/2015/acs/acs1/cprofile?get=CP02_2011_001E,CP02_2012_015E,CP03_2015_069E,CP04_2015_058E,CP03_2015_098E,CP03_2015_097E,CP04_2011_048E,CP04_2011_049E&for=county:*&key=62ede8de563355b8af858c6589ba30156de41404")

if (acs.status_code != 200):
    print('Error detected receiving (status code: ' + str(acs.status_code) + ')' )
    quit()

print('Sucessful request from American Communities Survey')

print(acs.text)

content = acs.json()

print(content)
#Make the data pulled from the ACS into a pandas dataframe
dataset= pd.DataFrame(content)
dataset.columns= dataset.iloc[0]

#remove the row I do not need that lists the variable names

dataset = dataset.drop([0])

#Need to concat the FIPS state and county codes to get useful number. 
dataset['FIPS'] = dataset['state'].str.cat(dataset['county'])


#Now for our tests for regression let's grab some data on the economic
#activity for the FIPS state and counties. This is also good practice
#for merging data together

columns2 = ['ST','COUNTY','PAYANN','LFO','ESTAB','EMP','CD115']

print('Requesting data from the 2015 County Business Patterns file')
	
cbp = requests.get("https://api.census.gov/data/2015/cbp?get=ST,COUNTY,PAYANN,LFO,ESTAB,EMP,CD115&for=county:*&key=62ede8de563355b8af858c6589ba30156de41404")

if (cbp.status_code != 200):
    print('Error detected receiving' + str(cbp.status_code)+ ')')
    quit()
    
print('Sucessful request from County Business Patterns file')

cbp_content = cbp.json()

print(cbp_content)