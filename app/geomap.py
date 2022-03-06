import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import json
import plotly.io as pio
import plotly.graph_objects as go

#change default render to browser
pio.renderers.default='browser'

#Load csv
df = pd.read_csv(r'E:\Lectures\526DATA INT VIS ANALYT\P\Crimes_2_19.csv')

#Load geojson
districts_json = r'D:\workshop\CS526\diva536\app\geodata\Boundaries_districts.geojson'

with open(districts_json) as dj:
    districts = json.load(dj)


df_2018 = df[df['Year']==2018].groupby("District")["District"].count().reset_index(name ='Total_Count')


fig = go.Figure(go.Choroplethmapbox(geojson=districts, locations=df_2018.District, z=df_2018.Total_Count,
                                    colorscale="Viridis",
                                    marker_opacity=0.5, marker_line_width=1, featureidkey='properties.area_numbe'))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=12, mapbox_center = {"lat": 41.8151, "lon": -87.67})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()



