# Import required libraries
import pickle
import copy
import pathlib
import urllib.request
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import vaex as vx


from datafilters.DataFilter import DataFilter
from figures.Figures import CreateFigures

data_frame = vx.read_csv("dataset/sample.csv")


filters = DataFilter(data_frame)

figures = CreateFigures(data_frame)

# Create controls
# year range slider
year_slider = figures.range_selector_fig("years")
# districts dropdown
district_dd = figures.dropdown_filter_fig("districts", filters)
# crime type dropdown
crime_type_dd = figures.dropdown_filter_fig("crime_type", filters)
# month dropdown
month_dd = figures.dropdown_filter_fig("months", filters)


app = dash.Dash(
    __name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width"}],
)
app.title = "Crimilnalytics"
server = app.server

# Load data

# Create global chart template
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url(
                                        "detective_logo.png"),
                                    id="plotly-image2",
                                    style={
                                        "height": "60px",
                                        "width": "auto",
                                        "margin-bottom": "-25px",
                                    },
                                ),
                                html.H3(
                                    "Criminalytics",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Crime Data Insights", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="two-thirds column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="https://plot.ly/dash/pricing/",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "5px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Filter by construction date (or select range in histogram):",
                            className="control_label",
                        ),
                        year_slider,
                        html.P("Filter by crime type:",
                               className="control_label"),
                        crime_type_dd,
                        html.P("Filter by districts:",
                               className="control_label"),
                        district_dd,
                        html.P("Filter by month:", className="control_label"),
                        month_dd,
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="well_text"),
                                     html.P("No. of Wells")],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="crimes_count"),
                                     html.P(f"No. of Crimes : {data_frame.count()} ")],
                                    id="crimes_count_text",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [
                                # dcc.Graph(id="count_graph")
                                # figures.pydeck_elevation_fig(filters.geo_plot_filter())

                            ],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="ten columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        # dcc.Graph(id="main_graph")
                        figures.pydeck_elevation_fig(filters.geo_plot_filter())
                    ],
                    id="elevation_deck",
                    className="pretty_container twleve columns",
                ),
                # html.Div(
                #     [dcc.Graph(id="individual_graph")],
                #     className="pretty_container five columns",
                # ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        # dcc.Graph(id="pie_graph")
                        # figures.sunburst_fig(filters.sunburst_filter()),
                        dcc.Graph(id='sunburst_plot', figure=figures.sunburst_fig(
                filters.sunburst_filter()))

                    ],
                    id="sunburst_deck",
                    className="pretty_container five columns",
                ),
                html.Div(
                    [dcc.Graph(id="aggregate_graph")],
                    className="pretty_container seven columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


# callback for count display change when
# dropdown filter is changed
@app.callback(
    [Output("count_display", "children"),
     Output("pydeck_map", "children"),
     Output("pydeck_map_1", "children"),
     Output("sunburst_plot", "figure")],
    [Input("id_dropdown_crime_type", "value"),
        Input("id_slider_years", "value"),
        Input("filter_district", "value"),
        Input("id_dropdown_months", "value")]
)
def filter_count_display(types, years, districts, months):
    print(' i am in filter_count_display')
    if years is None:
        years = []
    if types is None:
        types = []
    if districts is None:
        districts = []
    if months is None:
        months = []

    # print old data frame count
    print("old data frame count: ", filters.data_frame.count())
    # filter data
    print('input selected years', years)
    print('input selected types', types)
    print('input selected districts', districts)
    print('input selected months', months)

    new_data_frame = filters.create_selection(years, types, districts, months)

    print('new_data_frame count', new_data_frame.count())

    # count display
    changed_count = "**Total Cases: {}**".format(str(new_data_frame.count()))

    # pydeck maps data and figures
    pydeck_data_frame = filters.geo_plot_filter(new_data_frame)
    pydeck_fig = figures.pydeck_elevation_fig(pydeck_data_frame)
    pydeck_fig_1 = figures.pydeck_scatter_fig(pydeck_data_frame)

    # sunburst data and figures
    sunburst_data_frame = filters.sunburst_filter(new_data_frame)
    sunburst_fig = figures.sunburst_fig(sunburst_data_frame)

    # ranking table data and figures
    ranking_data_frame = filters.create_ranking_filter(new_data_frame)
    ranking_table_records, ranking_table_style = figures.create_ranking_fig(
        ranking_data_frame)

    return [changed_count, pydeck_fig, pydeck_fig_1, sunburst_fig]
    return [changed_count]


# Main
if __name__ == "__main__":
    app.run_server(debug=True)
