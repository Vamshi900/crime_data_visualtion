import vaex as vx
import numpy as np
import pandas as pd





# use pandas to read in the data
df_pandas = pd.read_csv('./data.csv')

# convert pandas dataframe to vaex dataframe
df_vaex = vx.from_pandas(df_pandas)

print(' dat loadaded')
# export the dataframe to a hdf5 file
df_vaex.export_hdf5(path=f'./crimes.hdf5', overwrite=True,progress=True)

del df_pandas,df_vaex
