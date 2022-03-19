import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import json
import plotly.io as pio
import plotly.graph_objects as go

# change default render to browser
pio.renderers.default = 'browser'


# Load csv
csv_file = "./geodata/processed_crimes_sample.csv"


def get_geomap_districts(csv_file):
    df = pd.read_csv(csv_file)

    # Load geojson
    districts_json = "./geodata/chicago_districts.geojson"

    # Load GeoJSON file
    with open(districts_json) as dj:
        districts = json.load(dj)

    # compute the total number of crimes per district
    df_computed = df.groupby("District")[
        "District"].count().reset_index(name='Total_Count')

    fig = go.Figure(go.Choroplethmapbox(geojson=districts, locations=df_computed.District, z=df_computed.Total_Count,
                                        colorscale="Viridis",
                                        marker_opacity=0.5, marker_line_width=1, featureidkey='properties.area_numbe'))
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=12, mapbox_center={"lat": 41.8151, "lon": -87.67})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


def get_geomap_crimes_pydeck(csv_file):
    
    pass


get_geomap_districts(csv_file)
