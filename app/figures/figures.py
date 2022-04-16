from cProfile import label
import imp
import plotly.express as px
import plotly.graph_objects as go
import vaex as vx
from dash import dcc
import pydeck as pdk
import dash_deck
import numpy as np
import pandas as pd

fig_layout_defaults = dict(
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
)

class CreateFigures:
    def __init__(self, data_frame):
        self.data_frame = data_frame
        self.lat = 41.769448846
        self.lon = -87.594177051
        self.zoom = 10.1
        self.mapbox_api_token = "pk.eyJ1IjoidmFtc2hpOTYiLCJhIjoiY2wwZnRwNG1uMHUyYjNqb2lhbGRjbTMydCJ9.BveaAINhSJscgd_FiC9Ihw"

    # update the data frame for fallback
    def update_data_frame(self, data_frame):
        self.data_frame = data_frame

    def create_sunburst(self, df=None):
        # if df == None:
        #     df = self.data_frame
        fig = px.sunburst(
            df, path=['labels', 'parents'], values='values',
            color_continuous_scale=px.colors.sequential.Plasma,
            color_continuous_midpoint=np.average(df['values']),
        )
        fig.update_layout(**fig_layout_defaults)
        return fig
          
    def convert_to_pandas(self, df):
        # convert to pandas dataframe
        return df.to_pandas_df(df)

    # function to create ranking table
    def create_ranking(self, tp_df=None):
        if tp_df is None:
            tp_df = self.data_frame
        print(tp_df.head(5))
        tp_df = self.convert_to_pandas(tp_df)
        return self.data_bars(tp_df, 'total_case')

    def data_bars(self, df, column):
        if df is None:
            df = self.data_frame
        n_bins = 100
        bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
        ranges = [
            ((df[column].max() - df[column].min()) * i) + df[column].min()
            for i in bounds
        ]
        styles = []
        for i in range(1, len(bounds)):
            min_bound = ranges[i - 1]
            max_bound = ranges[i]
            max_bound_percentage = bounds[i] * 100
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (
                            i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'background': (
                    """
                        linear-gradient(90deg,
                        # 96dbfa 0%,
                        # 96dbfa {max_bound_percentage}%,
                        white {max_bound_percentage}%,
                        white 100%)
                    """.format(max_bound_percentage=max_bound_percentage)
                ),
                'paddingBottom': 2,
                'paddingTop': 2
            })

        return styles

    # year range slider
    def range_selector(self, selector_type, years, count=0):
        range_vals = []
        min = 0
        max = 0
        if selector_type == "years":
            range_vals.extend(years)
            min = range_vals[0]
            max = range_vals[-1]

        create_slider = dcc.RangeSlider(
            min,
            max,
            step=1,
            dots=False,
            marks=None,
            value=[min, max],
            tooltip={'placement': 'bottom', 'always_visible': True},
            id="id_slider_"+selector_type
        )

        return create_slider

    # dropdown menu options
    def dropdown_filter(self, filter_type, filter_vals):
        options = []
        vals = []
        placeholder = ""
        if filter_type == "crime_type":
            vals = filter_vals.get_crime_types()
            for val in vals:
                options.append({"label": val.capitalize(),
                               "value": val.capitalize()})
            placeholder = "Select crime types..."
        elif filter_type == "days_of_week":
            vals = filter_vals.get_days_of_week()
            for val in vals:
                options.append({"label": val.capitalize(),
                               "value": val.capitalize()})
            placeholder = "Select days of week..."
        elif filter_type == "arrest":
            options.append({"label": "Arrested", "value": True})
            options.append({"label": "Not Arrested", "value": False})
            placeholder = "Choose arrest types..."
        elif filter_type == "domestic":
            options.append({"label": "Domestic Crime", "value": True})
            options.append({"label": "Non Domestic", "value": False})
            placeholder = "Choose domestic/non-domestic types..."
        elif filter_type == "months":
            vals = filter_vals.get_months()
            for num, name in vals.items():
                options.append({"label": name, "value": num})
            placeholder = "Select months..."
        elif filter_type == "districts":
            vals = filter_vals.get_police_districts()
            for num, name in vals.items():
                options.append({"label": name, "value": num})
            placeholder = "Choose districts..."

        create_filter = dcc.Dropdown(
            options=options,
            multi=True,
            searchable=True,
            placeholder=placeholder,
            value=[],
            id="id_dropdown_"+filter_type
        )

        return create_filter

    # function to create the pydeck map
    def create_geoplot(self, data_frame):
        if data_frame is None:
            return 'No data'
            # data_frame = self.data_frame
        # data_frame = data_frame.copy()  
        # df_copy = data_frame.copy()
       
        # data_frame = data_frame.to_pandas_df(data_frame)
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
                    data=data_frame,
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
        # tooltip = {
        #     'html': '<b>Total Cases:</b> {elevationValue}',
        #     'style': {
        #         'color': 'white'
            # }
        # }
        deck_component = dash_deck.DeckGL(map_plot.to_json(
        ), id="deck-gl", mapboxKey=self.mapbox_api_token)

        return deck_component
