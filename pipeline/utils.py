import vaex as vx
import numpy as np
import pandas as pd



# converting to hdf5 format will help us faster indexing and filtering
def convert_to_hdf5():
    # use pandas to read in the data
    # todo remove local read connect to s3 
    df_pandas = pd.read_csv('./data.csv')
    df_pandas.dropna(inplace=True)

    # convert dates to pandas datetime format
    df_pandas.Date = pd.to_datetime(df_pandas.Date, format='%m/%d/%Y %I:%M:%S %p')

    # setting the index to be the date will help us a lot later on
    df_pandas.index = pd.DatetimeIndex(df_pandas.Date)

    # convert pandas dataframe to vaex dataframe
    df_vaex = vx.from_pandas(df_pandas)

    # export the dataframe to a hdf5 file
    df_vaex.export('./processed.hdf5')


# function to aggreate groupby on districts

def compute_district_agg(crimes):
    # todo remove the data read will create a global object to the utilites and work on a local copy
    crimes = vx.open('./processed.hdf5')
    # group by district
    district_crime = crimes.groupby('District').agg({"District": "count"})
    # add geo tagged districts 
    return district_crime
    pass

# function to group crimes by ward     
# def compute_ward_agg(crimes):
      #pass

  

