from matplotlib.pyplot import title
import pydeck as pdk
import dash_deck
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


class CreateFigures:
    def __init__(self, data_frame):
        self.data_frame = data_frame
        self.lat = 41.769448846
        self.lon = -87.594177051
        self.zoom = 10.1
        self.mapbox_api_token = "pk.eyJ1IjoidmFtc2hpOTYiLCJhIjoiY2wwZnRwNG1uMHUyYjNqb2lhbGRjbTMydCJ9.BveaAINhSJscgd_FiC9Ihw"
        # self.mapbox_api_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

    def range_selector_fig(self, selector_type, years=[2006, 2022], count=0):
        min = years[0]
        max = years[-1]
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

    def dropdown_filter_fig(self, filter_type, filter_obj, isMulti=True, default_value=[]):
        options = []
        vals = []
        placeholder = ""
        if filter_type.startswith("crime_type"):
            vals = filter_obj.get_crime_types()
            for val in vals:
                options.append({"label": val.capitalize(),
                               "value": val.capitalize()})
            placeholder = "Select crime types..."
        elif filter_type == "days_of_week":
            vals = filter_obj.get_days_of_week()
            for val in vals:
                options.append({"label": val.capitalize(),
                               "value": val.capitalize()})
            placeholder = "Select days of week..."
        elif filter_type.startswith("months"):
            vals = filter_obj.get_months()
            for val in vals:
                options.append({"label": val,
                               "value": val})
            placeholder = "Select months..."
        elif filter_type.startswith("districts"):
            vals = filter_obj.get_police_districts()
            for val in vals:
                options.append({"label": val,
                               "value": val})
            placeholder = "Choose districts..."
        elif filter_type == "year_frame":
            vals = ["2006-2010", "2011-2015", "2016-2020", "2021-2022"]
            for val in vals:
                options.append({"label": val, "value": val})
            placeholder = "Choose Years..."
        create_filter = dcc.Dropdown(
            options=options,
            multi=isMulti,
            searchable=True,
            placeholder=placeholder,
            value=default_value,
            id="id_dropdown_"+filter_type
        )

        return create_filter

    def pydeck_elevation_fig(self, data_frame):
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
        tooltip = {
            'html': '<b>Total Cases:</b> {elevationValue}',
            'style': {
                'color': 'white'
            }
        }
        deck_component = dash_deck.DeckGL(map_plot.to_json(
        ), tooltip=tooltip, mapboxKey=self.mapbox_api_token)
        return deck_component

    def pydeck_scatter_fig(self, data_frame):
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
                    data=data_frame,
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
        tooltip = {
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
                    <td>{District_Name}</td>
                </tr>
            </table>
            """,
            'style': {
                'color': 'white',
            }
        }
        deck_component = dash_deck.DeckGL(map_plot.to_json(
        ), tooltip=tooltip, mapboxKey=self.mapbox_api_token)
        return deck_component

    def effective_pd_fig(self, data_frame_1, data_frame_2):

        # data_frame_1
        # x_axis = df_train.evaluate(df_train['Census_ProcessorClass'], selection = True)
        # color_axis = df_train.evaluate(df_train['HasDetections'], selection = True)
        pd_df_1 = data_frame_1.to_pandas_df()
        pd_df_2 = data_frame_2.to_pandas_df()
        fig3 = px.bar(pd_df_1, x="Count", y="Primary Type",
                      color="District_Name", title="Crime Type Arrested by District ", text_auto='.2s')
        fig4 = px.bar(pd_df_2, x="Count", y="Primary Type",
                      color="District_Name", title="Crime Type Not Arrested by District",   text_auto='.2s')

      
        return fig3, fig4

    def holiday_crime_fig(self, data_frame, mean):
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]

        pd_df_1 = data_frame.to_pandas_df()
        fig3 = px.line(pd_df_1, x="Month", y="Count",
                      color="District_Name", title="Number of Criminal Offences",text="Count")
        
        fig3.add_trace(go.Scatter(x=months, y=[mean for v in range(12)], name="Average Crimes",
        ))
        return fig3          
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=np.array(data_frame["Count"].tolist()), name="Total Crimes", text=np.array(data_frame["Count"].tolist()), textposition="top center",
                                 mode="lines+markers+text", line=dict(color='royalblue', width=3)))
        fig.update_traces(marker_size=10)
        fig.add_trace(go.Scatter(x=months, y=[mean for v in range(12)], name="Average Crimes",
                                 line=dict(color='firebrick', width=1, dash="dash")))
        fig.update_layout(yaxis=dict(
            title_text="Number of Criminal Offences",
        ),
            xaxis=dict(
            title_text="Time of the Year",
        ),
            title="Number of Crimes During the Holidays",
            title_x=0.5,
            height=600,
            margin=dict(
            l=10,
            r=10,
            b=10,
            t=50,
            pad=4
        ),)
        return fig

    def weekday_crime_fig(self, data_frame, mean):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=np.array(data_frame["Day"].tolist()),
                                 y=np.array(
                                     data_frame["District_Name"].tolist()),
                                 text=np.array(data_frame["Count"].tolist()),
                                 mode="markers",
                                 marker=dict(
            sizemode='diameter',
            sizeref=mean/12,
            size=np.array(data_frame["Count"].tolist()),
            color="red"
        )))
        fig.update_layout(yaxis=dict(
            title_text="District_Name",
        ),
            xaxis=dict(
            title_text="Day of week",
        ),
            title="Crime Count by Day of the Week",
            title_x=0.5,
            height=600,
            margin=dict(
            l=10,
            r=20,
            b=10,
            t=50,
            pad=4
        ),)
        return fig

    def daytime_crime_fig(self, data_frame, mean):

        pd_df_1 = data_frame.to_pandas_df()
        fig3 = px.line(pd_df_1, x="Time", y="Count",
                      color="District_Name", title="Number of Criminal Offences",text="Count")
        
        fig3.add_trace(go.Scatter(x=np.array(data_frame["Time"].tolist()), y=[mean for v in range(24)], name="Average Crimes",
        ))
        return fig3

        # fig = go.Figure()

        # fig.add_trace(go.Scatter(x=np.array(data_frame["Time"].tolist()), y=np.array(data_frame["Count"].tolist()), name="Total Crimes", text=np.array(data_frame["Count"].tolist()), textposition="top center",
        #                          mode="lines+markers+text", line=dict(color='royalblue', width=3)))
        # fig.update_traces(marker_size=10)
        # fig.add_trace(go.Scatter(x=np.array(data_frame["Time"].tolist()), y=[mean for v in range(24)], name="Average Crimes",
        #                          line=dict(color='firebrick', width=1, dash="dash")))
        # fig.update_layout(yaxis=dict(
        #     title_text="Number of Criminal Offences",
        # ),
        #     xaxis=dict(
        #     title_text="Time of the Day",
        #     tickmode="linear"
        # ),
        #     title="Number of Crimes by Time of the Day",
        #     title_x=0.5,
        #     height=600,
        #     margin=dict(
        #     l=10,
        #     r=10,
        #     b=10,
        #     t=50,
        #     pad=4
        # ),)
        # return fig

    def abuse_crime_fig(self, data_frame):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=np.array(data_frame["District_Name"].tolist()),
            x=np.array(data_frame["Count"].tolist()),
            name='Domestic',
            orientation='h',
            marker=dict(
                color='#347FC2'
            )
        ))
        fig.update_layout(barmode='stack',
                          height=600,
                          yaxis=dict(
                              title_text="District_Name",
                          ),
                          xaxis=dict(
                              title_text="Number of Domestic Offences",
                          ),
                          title="Domestic Offences",
                          title_x=0.5,
                          margin=dict(
                              l=10,
                              r=10,
                              b=10,
                              t=50,
                              pad=4
                          ),)
        return fig

    def state_crime_fig(self, data_frame):
        fig = go.Figure()
        X = np.array(data_frame["Year"].tolist())
        Y = np.array(data_frame["Count"].tolist())
        fig.add_trace(go.Bar(x=X, y=Y, opacity=.6, marker=dict(
            color='#BEBEBE'), width=[.2, .2, .2, .2, .2]))
        fig.add_trace(go.Scatter(x=X, y=Y,
                                 mode='markers+text', opacity=1, textposition='middle center', text=Y,
                                 textfont=dict(
                                     family="sans serif",
                                     size=12,
                                     color="white"
                                 ),
                                 marker=dict(size=[100, 100, 100, 100, 100], color='#0047AB')))
        fig.update_layout(showlegend=False,
                          height=600,
                          yaxis=dict(
                              title_text="Number of Offences",
                          ),
                          xaxis=dict(
                              title_text="Years",
                          ),
                          title="Number of Offences by Year",
                          title_x=0.5,
                          margin=dict(
                              l=10,
                              r=10,
                              b=10,
                              t=50,
                              pad=4
                          ),)
        return fig

    def sunburst_fig(self, data_frame):
        fig = px.sunburst(data_frame, path=[
                          'labels', 'parents'], values='value')
        fig1 = go.Figure(go.Sunburst(
            labels=fig['data'][0]['labels'].tolist(),
            parents=fig['data'][0]['parents'].tolist(),
            ids=fig['data'][0]['ids'].tolist(),
            values=fig['data'][0]['values'].tolist(),
        ))
        fig1.update_layout(margin=dict(t=10, l=0, r=0, b=10))
        return fig1

    def convert_to_pandas(self, data_frame):
        return data_frame.to_pandas_df()

    def create_ranking_fig(self, data_frame):
        #data_frame = self.convert_to_pandas(data_frame)
        return data_frame, self.data_bars(data_frame, 'total_case')

    def data_bars(self, data_frame, column):
        n_bins = 100
        bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
        ranges = [
            ((data_frame[column].max() - data_frame[column].min())
             * i) + data_frame[column].min()
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
                        #96dbfa 0%,
                        #96dbfa {max_bound_percentage}%,
                        white {max_bound_percentage}%,
                        white 100%)
                    """.format(max_bound_percentage=max_bound_percentage)
                ),
                'paddingBottom': 2,
                'paddingTop': 2
            })
        return styles
