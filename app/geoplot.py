import pydeck as pdk
import pandas as pd
import dash_deck

class GeoPlot:
    def __init__(self, data_frame):
        self.lat=41.769448846
        self.lon=-87.594177051
        self.zoom=10.1
        self.mapbox_api_token = "pk.eyJ1IjoidmFtc2hpOTYiLCJhIjoiY2wwZnRwNG1uMHUyYjNqb2lhbGRjbTMydCJ9.BveaAINhSJscgd_FiC9Ihw"
        self.data = data_frame

    def get_geoplot(self):
        map_plot = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state={
                "latitude": self.lat,
                "longitude": self.lon,
                "zoom": self.zoom,
                "pitch": 55,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=self.data,
                    get_position=["Longitude", "Latitude"],
                    radius=100,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                    auto_highlight=True,
                    filled=True,
                    coverage=1
                ),
            ]
        )
        tooltip={
            'html': '<b>Total Cases:</b> {elevationValue}',
            'style': {
                'color': 'white'
            }
        }
        deck_component = dash_deck.DeckGL(map_plot.to_json(), id="deck-gl", tooltip=tooltip, mapboxKey=self.mapbox_api_token)
        
        return deck_component