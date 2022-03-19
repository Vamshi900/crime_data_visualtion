
import pydeck as pdk
import pandas as pd
import dash
import dash_deck
from dash import html

lat=40.7
lon=-74
zoom=10
mapbox_api_token = "pk.eyJ1IjoidmFtc2hpOTYiLCJhIjoiY2wwZnRwNG1uMHUyYjNqb2lhbGRjbTMydCJ9.BveaAINhSJscgd_FiC9Ihw"
data = pd.read_csv('./geodata/processed_crimes_sample.csv')


map_plot = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": lat,
        "longitude": lon,
        "zoom": zoom,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data,
            get_position=["Longitude", "Latitude"],
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
)

deck_component = dash_deck.DeckGL(map_plot.to_json(), id="deck-gl",mapboxKey=mapbox_api_token)

app = dash.Dash(__name__)
app.layout = html.Div(deck_component)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8084,debug=True)

# map_plot.to_html("geojson_layer.html")