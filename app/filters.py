import pandas as pd
import numpy as np

#Load dataset
csv_crime = r"E:\Lectures\526DATA INT VIS ANALYT\P\Crimes_-_2001_to_Present.csv"
df = pd.read_csv(csv_crime)

#Drop rows where Location is missing
df.dropna(subset=["Location"], axis=0, inplace=True)

#Parsing Date Time
df['Datetime'] = pd.to_datetime(df['Date'])
df['Day'] = df['Datetime'].dt.day_name()
df['Time'] = [d.time() for d in df['Datetime']]
df['Date'] = [d.date() for d in df['Datetime']]
df['Month'] = df['Datetime'].apply(lambda x: x.month)
df['Year'] = df['Datetime'].apply(lambda x: x.year)

#Save to csv
df.to_csv(r'E:\Lectures\526DATA INT VIS ANALYT\P\Crimes_2_19.csv')

#Load csv
df = pd.read_csv(r'E:\Lectures\526DATA INT VIS ANALYT\P\Crimes_2_19.csv')
df = df.set_index('Datetime')

#Total crimes for each year
df['Year'].value_counts()

#Total crimes for each month by year
query_year = 2017
df[df['Year']==query_year].groupby("Month")["Month"].count()

#Total crimes by primary type
df.groupby("Primary Type")["Primary Type"].count().sort_values(ascending=False)

#Crime trend yearly
df.groupby("Year")["Year"].count().sort_values()

#Dangerous block
df.groupby("Block")["Block"].count().sort_values(ascending=False)

#Saftest date by year
query_year = 2019
df[df['Year']==query_year].groupby("Date")["Date"].count().sort_values()
