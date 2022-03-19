import pydeck as pdk
import pandas as pd

class geoMap:
    def __init__(self):
        self.district_data = pd.read_csv("dist_20.csv")
    
    def get_map(self):
        layer = pdk.Layer(
            'HexagonLayer',  # `type` positional argument is here
            self.district_data,
            get_position=['long', 'lat'],
            auto_highlight=True,
            elevation_scale=50,
            pickable=True,
            elevation_range=[0, 3000],
            extruded=True,
            coverage=1)

        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=-87.74597835776501,
            latitude=41.90235233193659,
            zoom=6,
            min_zoom=5,
            max_zoom=15,
            pitch=40.5,
            bearing=-27.36)

        map = pdk.Deck(layers=[layer], initial_view_state=view_state)
        map.to_html('district.html')