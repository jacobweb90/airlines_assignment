#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 13:19:45 2024

@author: jacobming
"""

### Importing files
import pandas as pd

flights = pd.read_csv('Manipulation-assignment/flights.csv')
planes= pd.read_csv('Manipulation-assignment/planes.csv')
airlines= pd.read_csv('Manipulation-assignment/airlines.csv')
airports = pd.read_csv('Manipulation-assignment/airports.csv')

### Inspecting the data
flights.columns
flights.dep_time
flights.dep_delay

planes.head()
planes.columns

airlines

airports

##### Questions

####### 1. What is the most popular destination city from NewYork?
flights.columns

## Steps:
# Calculate the total flights of each airport, then sort it from the highest to the lowest
table1=flights.groupby('dest').agg(counts=('dest','count')).sort_values(by='counts',ascending=False).reset_index()

# Left join the table to find the airport name
pd.merge(table1,airports[['faa','name']],how='left',left_on='dest',right_on='faa')

## Answer : ORD Chicago Ohare International

####### 2. Which month is the busiest of the year?
flights.columns

## Step
# value counts of the months
flights['month'].value_counts()

## Answer : July 29425 flights

####### 3. Which airline is the most punctual?

### checking average of departure delay vs arrival delay (positive = delay; negative = no delay)
## Steps
# 1. Calculate total delay
flights['total_delay']= flights['arr_delay']+flights['dep_delay']

# 2.Get average total delay per carrier
table1=flights.groupby('carrier').agg(mean_delay= ('total_delay','mean')).sort_values(by='mean_delay').reset_index()
airlines
# 3. Join the tables to find the airline
pd.merge(table1,airlines,how='left')

## Answer : HA Hawaiian Airlines (-2.01, closer to 0, least deviation)

####### 4. Which airlines is the worst in term of delays?

flights['total_delay']= flights['arr_delay']+flights['dep_delay']
table1=flights.groupby('carrier').agg(mean_delay= ('total_delay','mean')).sort_values(by='mean_delay').reset_index()
pd.merge(table1,airlines,how='left')

## Answer : F9 Frontier Airlines (42.12)

####### 5. Which destination has the longest duration?

flights.air_time.describe()

## Step
# 1. Calculate the average air time, then sort from the highest to lowest
table1= flights.groupby(['origin','dest']).agg(average_air_time=
                                       ('air_time','mean')).reset_index().sort_values(by='average_air_time',ascending=False)

# 2. Left join the table to find out the origin and dest airports
pd.merge(table1,airports[['faa','name']],how='left',left_on='dest',right_on='faa')

## Answer : HNL Honolyly International

####### 6. Which airlines has the most capacity of seats?
airlines

planes.columns
flights.columns

## Common key: tailnum
## other keys: carrier, seats

## Steps

# 1. Get the carrier and tailnum (Subsetting the data of flights)
# 2. Drop duplicates because each carrier can fly multiple times
carrier_tailnum= flights[['carrier','tailnum']].drop_duplicates()

# 3. Join the tables
seats=pd.merge(carrier_tailnum,planes[['tailnum','seats']],how='left').groupby('carrier').agg(total_seats=('seats','sum')).sort_values(by='total_seats',ascending=False).reset_index()

pd.merge(seats,airlines,how='left')

## Answer: UA United Air Lines (116252 seats)

####### 7. Which airplane model is the highest in use and from which manufacturer? 

airplanes_use=flights.groupby('tailnum').agg(count=('tailnum','count')).reset_index()

pd.merge(planes[['tailnum','model','manufacturer']],airplanes_use).groupby(['model','manufacturer']).agg(total_flights=('count','sum')).sort_values(by='total_flights',ascending=False)

## Answer: A320-232 AIRBUS (31278 flights)