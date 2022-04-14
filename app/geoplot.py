import pydeck as pdk
import pandas as pd
import dash_deck

class GeoPlot:
    def __init__(self, data_frame):
        self.lat=41.769448846
        self.lon=-87.594177051
        self.zoom=10.1
        self.mapbox_api_token = "pk.eyJ1IjoidmFtc2hpOTYiLCJhIjoiY2wwZnRwNG1uMHUyYjNqb2lhbGRjbTMydCJ9.BveaAINhSJscgd_FiC9Ihw"
        self.data = self.preprocess_data_frame(data_frame)
    
    def preprocess_data_frame(self,data_frame):
        district_map = {1  : "Central", 2  : "Wentworth", 3  : "Grand Crossing", 4  : "South Chicago", 5  : "Calumet",
                        6  : "Gresham", 7  : "Englewood", 8  : "Chicago Lawn", 9  : "Deering", 10  : "Ogden",
                        11  : "Harrison", 12  : "Near West", 14  : "Shakespeare", 15  : "Austin", 16  : "Jefferson Park",
                        17  : "Albany Park", 18  : "Near North", 19  : "Town Hall", 20  : "Lincoln", 22  : "Morgan Park",
                        24  : "Rogers Park", 25  : "Grand Central"}
        new_df = data_frame.replace({"District":district_map})
        
        true_false_map = {True:"Yes", False:"No"}
        new_df.replace({"Arrest":true_false_map}, inplace=True)
        new_df.replace({"Domestic":true_false_map}, inplace=True)

        return new_df

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
    
    def get_geoScatterPlot(self):
        map_plot = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state={
                "latitude": self.lat,
                "longitude": self.lon,
                "zoom": self.zoom,
                "pitch": 30,
            },
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=self.data,
                    get_position=["Longitude", "Latitude"],
                    radius=100,
                    auto_highlight=True,
                    pickable=True,
                    opacity=0.9,
                    stroked=True,
                    filled=True,
                    radius_scale=6,
                    radius_min_pixels=2,
                    radius_max_pixels=100,
                    line_width_min_pixels=0.5,
                    get_fill_color=[255, 140, 0],
                    get_line_color=[0, 0, 0],
                ),
            ]
        )
        tooltip={
            'html': """
            <style>
                table {
                    font-family: arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                }

                td, th {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }
            </style>
            <table>
                <tr>
                    <td>Year</td>
                    <td>{Year}</td>
                </tr>
                <tr>
                    <td>Date/Time</td>
                    <td>{Date}</td>
                </tr>
                <tr>
                    <td>Day Of Week</td>
                    <td>{Day}</td>
                </tr>
                <tr>
                    <td>Crime Type</td>
                    <td>{Primary Type}</td>
                </tr>
                <tr>
                    <td>Block</td>
                    <td>{Block}</td>
                </tr>
                <tr>
                    <td>Arrest</td>
                    <td>{Arrest}</td>
                </tr>
                <tr>
                    <td>Domestic</td>
                    <td>{Domestic}</td>
                </tr>
                <tr>
                    <td>District</td>
                    <td>{District}</td>
                </tr>
            </table>
            """,
            'style': {
                'color': 'white',
            }
        }
        deck_component = dash_deck.DeckGL(map_plot.to_json(), id="deck-gl", tooltip=tooltip, mapboxKey=self.mapbox_api_token)
        
        return deck_component