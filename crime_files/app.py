# Import required libraries
import dash
from dash import dcc, html, Input, Output, dash_table, callback_context
import vaex as vx
import dash_bootstrap_components as dbc

# importing helper components
from datafilters.DataFilter import DataFilter
from figures.Figures import CreateFigures
from figures.StatFigures import CreateStatFigures

data_frame = vx.open("dataset/cleaned_2006.hdf5")

filters = DataFilter(data_frame)

figures = CreateFigures(data_frame)

stat_figures = CreateStatFigures(data_frame)

# Create controls
# year range slider
year_slider = figures.range_selector_fig("years")
# districts dropdown
district_dd = figures.dropdown_filter_fig("districts", filters)
# crime type dropdown
crime_type_dd = figures.dropdown_filter_fig("crime_type", filters)
# month dropdown
month_dd = figures.dropdown_filter_fig("months", filters)

# initial district with highest crime count
init_district_name = "District with highest Crime : {}".format(
    filters.get_district_crime_high())
# initial count of total crimes
init_crime_count = "Total Offences : {}".format(filters.get_total_cases())
# initial arrest percentage
init_arrest_percentage = "Arrest Done : {:.2f}%".format(
    filters.get_percentage_arrest())
# initial domestic violence percentage
init_domestic_percentage = "Domestic Abuse : {:.2f}%".format(
    filters.get_percentage_domestic())

# initial data_table content
temp_data_frame = filters.create_ranking_filter(data_frame)
table_records_intitial, table_style_initial = figures.create_ranking_fig(
    temp_data_frame)

# storyline buttons definition
story_buttons = html.Div([
    dbc.Button("Where we are?", id="btn-str-1", n_clicks=0,
               color="secondary", className="me-1 four columns",),
    dbc.Button("Effective Chicago PD?", id="btn-str-2", n_clicks=0,
               color="secondary", className="me-1 five columns",),
    dbc.Button("Criminals sleep at night...", id="btn-str-3",
               n_clicks=0, color="secondary", className="me-1 six columns",),
    dbc.Button("Criminals on a holiday!!", id="btn-str-4", n_clicks=0,
               color="secondary", className="me-1 five columns",),
    dbc.Button("Careful on Weekends!!", id="btn-str-5", n_clicks=0,
               color="secondary", className="me-1 five columns",),
    dbc.Button("Say to no Domestic Abuse...", id="btn-str-6",
               n_clicks=0, color="secondary", className="me-1 five columns",),
    html.Br()
], className="row flex-display", style={"width": "560px"})

effective_pd_block = html.Div([
    html.Div(
        className="row", children=[
            html.Div(className="Element", children=[
                html.Label("Select Years"),
                figures.range_selector_fig("years_1")
            ], style=dict(width="33.3%", marginLeft="20px", padding="15px")),
            html.Div(className="Element", id="filter_district", children=[
                html.Label("Select Districts"),
                figures.dropdown_filter_fig(
                    "districts_1", filters, True, "Central")
            ], style=dict(width="33.3%", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Month"),
                figures.dropdown_filter_fig(
                    "months_1", filters, False, "January")
            ], style=dict(width="25%", padding="15px"))
        ], style=dict(display='flex', width="1370px")
    ),
    html.Div(
        className="EffectivePD", children=[
            dcc.Graph(id="effective_pd_1", figure={},
                      style=dict(width="1350px"))
        ], style=dict(display='flex', width="1370px")
    ),
    html.Br(),
    html.Div(
        className="EffectivePD", children=[
            dcc.Graph(id="effective_pd_2", figure={},
                      style=dict(width="1350px"))
        ], style=dict(display='flex',)
    )
])

holiday_crime_block = html.Div([
    html.Div(
        className="row", children=[
            html.Div(className="Element", children=[
                html.Label("Select Years"),
                figures.range_selector_fig("years_1")
            ], style=dict(width="33.3%", marginLeft="20px", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Crime Type"),
                figures.dropdown_filter_fig(
                    "crime_type_1", filters, False, "Arson")
            ], style=dict(width="33.3%", padding="15px")),
            html.Div(className="Element", id="filter_district", children=[
                html.Label("Select Districts"),
                figures.dropdown_filter_fig(
                    "districts_1", filters, True, "Central")
            ], style=dict(width="25%", padding="15px"))
        ], style=dict(display='flex', width="1370px")
    ),
    html.Div(
        className="HolidayCrime", children=[
            dcc.Graph(id="holiday_crime_1", figure={},
                      style=dict(width="1350px"))
        ], style=dict(display='flex',)
    ),
    html.Br()

])

weekday_crime_block = html.Div([
    html.Div(
        className="row", children=[
            html.Div(className="Element", children=[
                html.Label("Select Years"),
                figures.range_selector_fig("years_1")
            ], style=dict(width="33.3%", marginLeft="20px", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Crime Type"),
                figures.dropdown_filter_fig(
                    "crime_type_1", filters, False, "Assault")
            ], style=dict(width="33.3%", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Month"),
                figures.dropdown_filter_fig(
                    "months_1", filters, False, "January")
            ], style=dict(width="25%", padding="15px"))
        ], style=dict(display='flex', width="1370px")
    ),
    html.Div(
        className="CrimeDay", children=[
            dcc.Graph(id="weekday_crime_1", figure={},
                      style=dict(width="1350px"))
        ], style=dict(display='flex',)
    ),
    html.Br(),
    html.Div(
        className="row", children=[
            html.Div(className="Element", children=[
                html.Label("Select Years"),
                figures.range_selector_fig("years_2")
            ], style=dict(width="33.3%", marginLeft="20px", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Crime Type"),
                figures.dropdown_filter_fig(
                    "crime_type_2", filters, False, "Arson")
            ], style=dict(width="33.3%", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Month"),
                figures.dropdown_filter_fig(
                    "months_2", filters, False, "January")
            ], style=dict(width="25%", padding="15px"))
        ], style=dict(display='flex', width="1370px")
    ),
    html.Div(
        className="CrimeDay", children=[
            dcc.Graph(id="weekday_crime_2", figure={},
                      style=dict(width="1350px"))
        ], style=dict(display='flex',)
    )
])

daytime_crime_block = html.Div([
    html.Div(
        className="row", children=[
            html.Div(className="Element", children=[
                html.Label("Select Years"),
                figures.range_selector_fig("years_1")
            ], style=dict(width="30%", marginLeft="20px", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Crime Type"),
                figures.dropdown_filter_fig(
                    "crime_type_1", filters, False, "Assault")
            ], style=dict(width="20%", padding="15px")),
            html.Div(className="Element", id="filter_district", children=[
                html.Label("Select Districts"),
                figures.dropdown_filter_fig(
                    "districts_1", filters, True, "Central")
            ], style=dict(width="20%", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Month"),
                figures.dropdown_filter_fig(
                    "months_1", filters, False, "January")
            ], style=dict(width="20%", padding="15px"))
        ], style=dict(display='flex', width="1370px")
    ),
    html.Div(
        className="CrimeDaytime", children=[
            dcc.Graph(id="daytime_crime_1", figure={},
                      style=dict(width="1350px"))
        ], style=dict(display='flex',)
    ),
    html.Br()
])

abuse_crime_block = html.Div([
    html.Div(
        className="row", children=[
            html.Div(className="Element", children=[
                html.Label("Select Years"),
                figures.range_selector_fig("years_1")
            ], style=dict(width="33.3%", marginLeft="20px", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Month"),
                figures.dropdown_filter_fig(
                    "months_1", filters, True, "January")
            ], style=dict(width="25%", padding="15px"))
        ], style=dict(display='flex', width="1370px")
    ),
    html.Div(
        className="CrimeAbuse", children=[
            dcc.Graph(id="abuse_crime_1", figure={},
                      style=dict(width="1350px"))
        ], style=dict(display='flex',)
    )
])

state_crime_block = html.Div([
    html.Div(
        className="row", children=[
            html.Div(className="Element", children=[
                html.Label("Select Years"),
                figures.dropdown_filter_fig("year_frame", filters, False)
            ], style=dict(width="25%", padding="15px")),
        ], style=dict(display='flex', width="1370px")
    ),
    html.Div(
        className="WhereWe", children=[
            dcc.Graph(id="state_crime", figure={}, style=dict(width="1350px"))
        ], style=dict(display='flex',)
    )
])

app = dash.Dash(
    __name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width"}],
)
app.title = "Crimilnalytics"
server = app.server

# dashboard layout
dashboard_layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
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
                                        "margin-bottom": "-15px",
                                        "margin-left": "-25px",
                                    },
                                )
                            ],
                            className="three columns",
                        ),
                        html.Div(
                            [
                                html.H3(
                                    "Criminalytics: Crime Data Insights",
                                    style={"margin-bottom": "0px",
                                           "margin-top": "5px", "margin-left": "-230px"},
                                )
                            ],
                            className="nine columns",
                        ),
                    ],
                    className="one-thirds column",
                    id="title",
                ),
                html.Div(
                    [
                        dbc.Button("Dashboard", n_clicks=0, id="layout_btn_1"),
                        dbc.Button("StoryLine", n_clicks=0, id="layout_btn_2"),
                        dbc.Button("Insights", n_clicks=0, id="layout_btn_3"),
                        dbc.Button("Predictor", n_clicks=0, id="layout_btn_4"),
                    ],
                    className="two-third column",
                    id="button_layout_div",
                    style={"padding-top": "5px"}
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "5px"},
        ),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Filter by year:",
                            className="control_label",
                        ),
                        year_slider,
                        html.Br(),
                        html.P("Filter by crime type:",
                               className="control_label"),
                        crime_type_dd,
                        html.Br(),
                        html.P("Filter by districts:",
                               className="control_label"),
                        district_dd,
                        html.Br(),
                        html.P("Filter by month:", className="control_label"),
                        month_dd,
                        html.Br(),
                        html.P("City view:", className="control_label"),
                        dcc.RadioItems(options=[
                            {'label': 'Elevation', 'value': 'elevate'},
                            {'label': 'Scatter', 'value': 'scatter'},
                        ],
                            value='elevate', id="map_choice")
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(id="crimes_info"),
                                        html.P(init_crime_count, id="total_crimes_text")],
                                    id="crimes_info_div",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="district_info"),
                                     html.P(init_district_name, id="district_info_text")],
                                    id="district_info_div",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="arrest_info"),
                                     html.P(init_arrest_percentage, id="arrest_info_text")],
                                    id="arrest_info_div",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="domestic_info"),
                                     html.P(init_domestic_percentage, id="domestic_info_text")],
                                    id="domestic_info_div",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(children=[
                            dcc.Graph(id="main_graph"),
                            html.Div(children=[figures.pydeck_elevation_fig(
                                filters.geo_plot_filter())], id="map_graph"),
                        ],
                            className="pretty_container eleven columns",
                        ),
                    ],
                    id="right-column",
                    className="nine columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='sunburst_plot', figure=figures.sunburst_fig(
                            filters.sunburst_filter()))

                    ],
                    id="sunburst_deck",
                    className="pretty_container five columns",
                ),
                html.Div(children=[
                    dash_table.DataTable(id='table1', columns=[
                        {'name': 'District', 'id': 'District_Name'},
                        {'name': 'Primary Type', 'id': 'Primary Type'},
                        {'name': 'Number of Cases', 'id': 'total_case'},
                    ],
                        data=table_records_intitial.to_dict('records'),
                        style_data_conditional=table_style_initial,
                        style_as_list_view=True,
                        style_header={
                        'border': '1px solid lightgrey',
                            'fontWeight': 'bold'
                    },
                        style_data={
                        'border': '1px solid lightgrey',
                    },
                        page_size=20,
                        style_table={'height': '500px', 'overflowY': 'auto'}
                    )
                ],
                    className="pretty_container seven columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# storyline layout
story_line_layout = html.Div(children=[
    dcc.Store(id="aggregate_data"),
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
                                    "margin-left": "-25px",
                                },
                            )
                        ],
                        className="three columns",
                    ),
                    html.Div(
                        [
                            html.H3(
                                "Criminalytics: Crime Data Insights",
                                style={"margin-bottom": "0px",
                                       "margin-top": "5px", "margin-left": "-230px"},
                            )
                        ],
                        className="nine columns",
                    ),
                ],
                className="one-thirds column",
                id="title",
            ),
            html.Div(
                [
                    dbc.Button("Dashboard", n_clicks=0, id="layout_btn_1"),
                    dbc.Button("StoryLine", n_clicks=0, id="layout_btn_2"),
                    dbc.Button("Insights", n_clicks=0, id="layout_btn_3"),
                    dbc.Button("Predictor", n_clicks=0, id="layout_btn_4"),
                ],
                className="two-third column",
                id="button_layout_div",
                style={"padding-top": "5px"}
            ),
        ],
        id="header",
        className="row flex-display",
        style={"margin-bottom": "5px"},
    ),
    html.Br(),
    story_buttons,
    html.Div(id='conatiner_charts', children=[state_crime_block])
])

# insights layout
insights_layout = html.Div(children=[
    dcc.Store(id="aggregate_data"),
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
                                    "margin-left": "-25px",
                                },
                            )
                        ],
                        className="three columns",
                    ),
                    html.Div(
                        [
                            html.H3(
                                "Criminalytics: Crime Data Insights",
                                style={"margin-bottom": "0px",
                                       "margin-top": "5px", "margin-left": "-230px"},
                            )
                        ],
                        className="nine columns",
                    ),
                ],
                className="one-thirds column",
                id="title",
            ),
            html.Div(
                [
                    dbc.Button("Dashboard", n_clicks=0, id="layout_btn_1"),
                    dbc.Button("StoryLine", n_clicks=0, id="layout_btn_2"),
                    dbc.Button("Insights", n_clicks=0, id="layout_btn_3"),
                    dbc.Button("Predictor", n_clicks=0, id="layout_btn_4"),
                ],
                className="two-third column",
                id="button_layout_div",
                style={"padding-top": "5px"}
            ),
        ],
        id="header",
        className="row flex-display",
        style={"margin-bottom": "5px"},
    ),
    html.Br(),
    html.H1("Key Data Insigts"),
    html.Br(),
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id='chart_1', figure=stat_figures.chart_1()),
                ],
                id="div_chart_1",
                className="pretty_container six columns",
            ),
            html.Div(
                [
                    dcc.Graph(id='chart_2', figure=stat_figures.chart_2()),
                ],
                id="div_chart_2",
                className="pretty_container six columns",
            ),
        ],
        className="row flex-display",
    ),
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id='chart_3', figure=stat_figures.chart_3()),
                ],
                id="div_chart_3",
                className="pretty_container six columns",
            ),
            html.Div(
                [
                    dcc.Graph(id='chart_4', figure=stat_figures.chart_4()),
                ],
                id="div_chart_4",
                className="pretty_container six columns",
            ),
        ],
        className="row flex-display",
    ),
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id='chart_5', figure=stat_figures.chart_5()),
                ],
                id="div_chart_5",
                className="pretty_container six columns",
            ),
            html.Div(
                [
                    dcc.Graph(id='chart_6', figure=stat_figures.chart_6()),
                ],
                id="div_chart_6",
                className="pretty_container six columns",
            ),
        ],
        className="row flex-display",
    ),
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id='chart_7', figure=stat_figures.chart_7()),
                ],
                id="div_chart_7",
                className="pretty_container six columns",
            ),
            html.Div(
                [
                    dcc.Graph(id='chart_8', figure=stat_figures.chart_8()),
                ],
                id="div_chart_8",
                className="pretty_container six columns",
            ),
        ],
        className="row flex-display",
    ),
])

# predictor layout
predictor_layout = html.Div(children=[
    dcc.Store(id="aggregate_data"),
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
                                    "margin-left": "-25px",
                                },
                            )
                        ],
                        className="three columns",
                    ),
                    html.Div(
                        [
                            html.H3(
                                "Criminalytics: Crime Data Insights",
                                style={"margin-bottom": "0px",
                                       "margin-top": "5px", "margin-left": "-230px"},
                            )
                        ],
                        className="nine columns",
                    ),
                ],
                className="one-thirds column",
                id="title",
            ),
            html.Div(
                [
                    dbc.Button("Dashboard", n_clicks=0, id="layout_btn_1"),
                    dbc.Button("StoryLine", n_clicks=0, id="layout_btn_2"),
                    dbc.Button("Insights", n_clicks=0, id="layout_btn_3"),
                    dbc.Button("Predictor", n_clicks=0, id="layout_btn_4"),
                ],
                className="two-third column",
                id="button_layout_div",
                style={"padding-top": "5px"}
            ),
        ],
        id="header",
        className="row flex-display",
        style={"margin-bottom": "5px"},
    ),
    html.Br(),
    html.H1("Future Crime Predictions"),
    html.Br(),
    html.Div(id='predictor_charts', children=[
        dcc.Graph(id='predictor_graph_1',
                  figure=stat_figures.plot_daily_prediction()),
        dcc.Graph(id='predictor_graph_2',
                  figure=stat_figures.plot_monthly_prediction()),
    ], className="pretty_container eleven columns"),
]
)

# Create app layout
app.layout = html.Div(children=[dashboard_layout], id="app_container")

# callback for changing layout


@app.callback(
    [Output("app_container", "children"), ],
    [Input('layout_btn_1', 'n_clicks'),
     Input('layout_btn_2', 'n_clicks'),
     Input('layout_btn_3', 'n_clicks'),
     Input('layout_btn_4', 'n_clicks')]
)
def layout_change(btn1, btn2, btn3, btn4):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    layout_mode = dashboard_layout
    if changed_id == "layout_btn_1.n_clicks":
        layout_mode = dashboard_layout
    elif changed_id == "layout_btn_2.n_clicks":
        layout_mode = story_line_layout
    elif changed_id == "layout_btn_3.n_clicks":
        layout_mode = insights_layout
    elif changed_id == "layout_btn_4.n_clicks":
        layout_mode = predictor_layout
    return (layout_mode,)


# callback method for the dashboard plots
@app.callback(
    [Output("total_crimes_text", "children"),
     Output("district_info_text", "children"),
     Output("arrest_info_text", "children"),
     Output("domestic_info_text", "children"),
     Output("map_graph", "children"),
     Output("sunburst_plot", "figure"),
     Output("table1", "data"),
     Output("table1", "style_data_conditional")],
    [Input("id_dropdown_crime_type", "value"),
        Input("id_slider_years", "value"),
        Input("id_dropdown_districts", "value"),
        Input("id_dropdown_months", "value"),
        Input("map_choice", "value")]
)
def filter_count_display(types, years, districts, months, map_view):
    if years is None:
        years = []
    if types is None:
        types = []
    if districts is None:
        districts = []
    if months is None:
        months = []

    new_data_frame = filters.create_selection(years, types, districts, months)

    # count display
    changed_count = "Total Offenses : {}".format(filters.get_total_cases())
    # district with highest crime
    district_name = "District with highest Crime : {}".format(
        filters.get_district_crime_high())
    # arrest percentage
    arrest_percentage = "Arrest Done : {:.2f}%".format(
        filters.get_percentage_arrest())
    # domestic percentage
    domestic_percentage = "Domestic Abuse : {:.2f}%".format(
        filters.get_percentage_domestic())

    # pydeck maps data and figures
    pydeck_data_frame = filters.geo_plot_filter(new_data_frame)
    pydeck_fig = figures.pydeck_elevation_fig(
        pydeck_data_frame) if map_view == "elevate" else figures.pydeck_scatter_fig(pydeck_data_frame)

    # sunburst data and figures
    sunburst_data_frame = filters.sunburst_filter(new_data_frame)
    sunburst_fig = figures.sunburst_fig(sunburst_data_frame)

    # table data and style
    ranking_data_frame = filters.create_ranking_filter(new_data_frame)
    table_data, table_style = figures.create_ranking_fig(ranking_data_frame)

    return [changed_count, district_name, arrest_percentage, domestic_percentage, pydeck_fig, sunburst_fig, table_data.to_dict("records"), table_style]

# callback method for the story line plots


@app.callback(
    [Output("effective_pd_1", "figure"),
     Output("effective_pd_2", "figure"), ],
    [Input("id_slider_years_1", "value"),
     Input("id_dropdown_districts_1", "value"),
     Input("id_dropdown_months_1", "value"),
     ]
)
def effective_pd_filter(years1, districts1, months1):
    if years1 is None:
        years1 = []
    # districts1 = [districts1] if districts1 is not None else []
    # if district1 is of type string, convert to list
    if isinstance(districts1, str):
        districts1 = [districts1]
    months1 = [months1] if months1 is not None else []
    print('districts1', districts1)
    new_data_frame1 = filters.create_selection(
        years=years1, types=[], districts=districts1, months=months1)
    data_frame_1, data_frame_2 = filters.effective_pd_filter(new_data_frame1)
    fig_yes, fig_no = figures.effective_pd_fig(data_frame_1, data_frame_2)
    return (fig_yes, fig_no)


@app.callback(
    [Output("holiday_crime_1", "figure")],
    [Input("id_slider_years_1", "value"),
     Input("id_dropdown_crime_type_1", "value"),
     Input("id_dropdown_districts_1", "value")]
)
def holiday_crime_filter(years1, types1, districts1):
    if years1 is None:
        years1 = []

    if isinstance(districts1, str):
        districts1 = [districts1]
    types1 = [types1] if types1 is not None else []
    new_data_frame1 = filters.create_selection(
        years=years1, types=types1, districts=districts1, months=[])

    data_frame_1, mean1 = filters.holiday_crime_filter(new_data_frame1)
    fig33 = figures.holiday_crime_fig(data_frame_1, mean1)
    return [fig33]


@app.callback(
    [Output("weekday_crime_1", "figure"),
     Output("weekday_crime_2", "figure"), ],
    [Input("id_slider_years_1", "value"),
     Input("id_slider_years_2", "value"),
     Input("id_dropdown_crime_type_1", "value"),
     Input("id_dropdown_crime_type_2", "value"),
     Input("id_dropdown_months_1", "value"),
     Input("id_dropdown_months_2", "value")]
)
def crime_during_weekday_filter(years1, years2, types1, types2, months1, months2):
    if years1 is None:
        years1 = []
    if years2 is None:
        years2 = []

    types1 = [types1] if types1 is not None else []
    types2 = [types2] if types2 is not None else []
    months1 = [months1] if months1 is not None else []
    months2 = [months2] if months2 is not None else []
    new_data_frame1 = filters.create_selection(
        years=years1, types=types1, districts=[], months=months1)
    new_data_frame2 = filters.create_selection(
        years=years2, types=types2, districts=[], months=months2)
    data_frame_1, mean1 = filters.weekday_crime_filter(new_data_frame1)
    data_frame_2, mean2 = filters.weekday_crime_filter(new_data_frame2)
    return (figures.weekday_crime_fig(data_frame_1, mean1), figures.weekday_crime_fig(data_frame_2, mean2))


@app.callback(
    [Output("daytime_crime_1", "figure")],
    [Input("id_slider_years_1", "value"),
     Input("id_dropdown_crime_type_1", "value"),
     Input("id_dropdown_districts_1", "value"),
     Input("id_dropdown_months_1", "value")
     ]
)
def crime_daytime_filter(years1, types1, districts1, months1):
    if years1 is None:
        years1 = []
    if isinstance(districts1, str):
        districts1 = [districts1]
    types1 = [types1] if types1 is not None else []
    months1 = [months1] if months1 is not None else []
    new_data_frame1 = filters.create_selection(
        years=years1, types=types1, districts=districts1, months=months1)

    data_frame_1, mean1 = filters.daytime_crime_filter(new_data_frame1)
    fig_yes = figures.daytime_crime_fig(data_frame_1, mean1)
    return [fig_yes]


@app.callback(
    [Output("abuse_crime_1", "figure")],
    [Input("id_slider_years_1", "value"),

     Input("id_dropdown_months_1", "value")],

)
def crime_abuse_filter(years1, months1):
    if years1 is None:
        years1 = []
    if isinstance(months1, str):
        months1 = [months1]
    # months1 = [months1] if months1 is not None else []
    new_data_frame1 = filters.create_selection(
        years=years1, types=[], districts=[], months=months1)

    data_frame_1 = filters.abuse_crime_filter(new_data_frame1)
    return [figures.abuse_crime_fig(data_frame_1)]


@app.callback(
    [Output("state_crime", "figure"), ],
    [Input("id_dropdown_year_frame", "value"), ]
)
def where_we_at_filter(years):
    if years is None or years == []:
        years = [2016, 2020]
    else:
        years = list(map(int, years.split("-")))
    new_data_frame = filters.create_selection(
        years=years, types=[], districts=[], months=[])
    data_frame_1 = filters.state_crime_filter(new_data_frame)
    return (figures.state_crime_fig(data_frame_1),)


@app.callback(
    [Output("conatiner_charts", "children"), ],
    [Input('btn-str-1', 'n_clicks'),
     Input('btn-str-2', 'n_clicks'),
     Input('btn-str-3', 'n_clicks'),
     Input('btn-str-4', 'n_clicks'),
     Input('btn-str-5', 'n_clicks'),
     Input('btn-str-6', 'n_clicks'), ]
)
def button_change(btn1, btn2, btn3, btn4, btn5, btn6):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    div_con = state_crime_block
    if changed_id == "btn-str-1.n_clicks":
        div_con = state_crime_block
    elif changed_id == "btn-str-2.n_clicks":
        div_con = effective_pd_block
    elif changed_id == "btn-str-3.n_clicks":
        div_con = daytime_crime_block
    elif changed_id == "btn-str-4.n_clicks":
        div_con = holiday_crime_block
    elif changed_id == "btn-str-5.n_clicks":
        div_con = weekday_crime_block
    elif changed_id == "btn-str-6.n_clicks":
        div_con = abuse_crime_block
    return (div_con,)


# Main
if __name__ == "__main__":
    app.run_server(debug=False, port=5000)
