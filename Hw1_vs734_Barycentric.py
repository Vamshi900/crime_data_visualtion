import plotly.express as px
import pandas as pd

df = pd.read_csv('asoiaf_nodes_prop.csv')

def normalise_properties(df):
    # make a copy of the exisitng data 
    newdata = df.copy()
    # loop through each colum 
    for column in df.columns:
        # condition to skip name colum since no max value
        if(column=='name'):
            continue
        # extract max value
        max_value = df[column].max()
        # extract min value
        min_value = df[column].min()
        # normalise and store in new data frame
        newdata[column] = (df[column] - min_value) / (max_value - min_value)

    return newdata # return normalised data

# normalise data
newdata = normalise_properties(df)

# barcyenctric data plot
fig = px.scatter_ternary(newdata,
    a="degree", b="peel", c="diversity", # axes data 
    color="betweenness",  # color
    size="pagerank",  # point size
    color_discrete_map = {"degree": "blue", "peel": "green", "diversity":"red"} # color definitions for the data
     )

fig.show()

# save png output
fig.write_image("./HW1_vs734_Barycentric.png")