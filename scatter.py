import plotly.express as px
import pandas as pd

df = pd.read_csv('asoiaf_nodes_prop.csv')
# print(df)
fig = px.scatter(df, x = 'degree', y = 'peel', color = 'diversity',
                 size = 'pagerank', custom_data = ['name', 'diversity', 'pagerank'])

fig.update_traces(hovertemplate = ( 'name: %{customdata[0]}<br>'
                                    'degree: %{x}, peel: %{y}<br>'
                                    'diversity: %{customdata[1]:.2e}<br>'
                                    'pagerank: %{customdata[2]:.2e}'))

fig.write_image("fig1.png")