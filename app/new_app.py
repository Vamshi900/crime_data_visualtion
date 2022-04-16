import pydeck as pdk
import pandas as pd
import dash_deck
import dash
import dash_html_components as html

import vaex as vx

lat = 41.769448846
lon = -87.594177051
zoom = 10.1
mapbox_api_token = "pk.eyJ1IjoidmFtc2hpOTYiLCJhIjoiY2wwZnRwNG1uMHUyYjNqb2lhbGRjbTMydCJ9.BveaAINhSJscgd_FiC9Ihw"
df = vx.open('./dataset/h_d.hdf5')
df = df['Longitude', 'Latitude']
print(df.head(5))
pd_df = df.to_pandas_df(['Longitude', 'Latitude'])


def get_geoplot(data):
    map_plot = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v10",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 55,
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
                auto_highlight=True,
                filled=True,
                coverage=1
            ),
        ]
    )
    tooltip = {
        'html': '<b>Total Cases:</b> {elevationValue}',
        'style': {
            'color': 'white'
        }
    }
    deck_component = dash_deck.DeckGL(map_plot.to_json(
    ), id="deck-gl", tooltip=tooltip, mapboxKey=mapbox_api_token)

    return deck_component


r = get_geoplot(pd_df)
app = dash.Dash(__name__)


app.layout = html.Div(
    r
)


if __name__ == "__main__":
    app.run_server(debug=True)
