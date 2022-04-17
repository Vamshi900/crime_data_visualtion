from dash import html, dcc, Input, Output, callback_context
from app_our import app, port, orig_data_frame
import dash_bootstrap_components as dbc
import pandas as pd

from datafilters.DataFilter import DataFilter
from figures.Figures import CreateFigures
from screens.navbar import Navbar

data_frame = orig_data_frame

filters = DataFilter(data_frame)

figures = CreateFigures(data_frame)

nav = Navbar()

buttons = html.Div([
    dbc.Button("Where we are?", id="btn-str-1", n_clicks=0, color="secondary", className="me-1", style=dict(width=150,height=60)),
    dbc.Button("How effective is Chicago PD?", id="btn-str-2", n_clicks=0, color="secondary", className="me-1", style=dict(width=150,height=60)),
    dbc.Button("Criminals also sleep at night...", id="btn-str-3", n_clicks=0, color="secondary", className="me-1", style=dict(width=150,height=60)),
    dbc.Button("Criminals on a holiday!!", id="btn-str-4", n_clicks=0, color="secondary", className="me-1", style=dict(width=150,height=60)),
    dbc.Button("Careful on Weekends!!", id="btn-str-5", n_clicks=0, color="secondary", className="me-1", style=dict(width=150,height=60)),
    dbc.Button("Say to no Domestic Abuse...", id="btn-str-6", n_clicks=0, color="secondary", className="me-1", style=dict(width=150,height=60)),
    html.Br()
])

effective_pd_block = html.Div([
    html.Div(
        className = "row", children = [
            html.Div(className="Element", children = [
                html.Label("Select Years"),
                figures.range_selector_fig("years")
            ], style=dict(width="33.3%",marginLeft="20px",padding="15px")),
            html.Div(className="Element", id="filter_district", children = [
                html.Label("Select Districts"),
                figures.dropdown_filter_fig("districts", filters)
            ], style=dict(width="33.3%",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Month"),
                figures.dropdown_filter_fig("months", filters)
            ], style=dict(width="25%",padding="15px"))
        ], style=dict(display='flex',)
    ),
    html.Div(
        className = "EffectivePD", children = [
            dcc.Graph(id="effective_pd", figure={}, style=dict(width="1200px"))
        ], style=dict(display='flex',)
    )
])

holiday_crime_block = html.Div([
    html.Div(
        className = "row", children = [
            html.Div(className="Element", children = [
                html.Label("Select Years"),
                figures.range_selector_fig("years")
            ], style=dict(width="33.3%",marginLeft="20px",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Crime Type"),
                figures.dropdown_filter_fig("crime_type",filters)
            ], style=dict(width="33.3%",padding="15px")),
            html.Div(className="Element", id="filter_district", children = [
                html.Label("Select Districts"),
                figures.dropdown_filter_fig("districts", filters)
            ], style=dict(width="25%",padding="15px"))
        ], style=dict(display='flex',)
    ),
    html.Div(
        className = "HolidayCrime", children = [
            dcc.Graph(id="holiday_crime", figure={}, style=dict(width="1200px"))
        ], style=dict(display='flex',)
    )
])

weekday_crime_block = html.Div([
    html.Div(
        className = "row", children = [
            html.Div(className="Element", children = [
                html.Label("Select Years"),
                figures.range_selector_fig("years")
            ], style=dict(width="33.3%",marginLeft="20px",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Crime Type"),
                figures.dropdown_filter_fig("crime_type",filters)
            ], style=dict(width="33.3%",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Month"),
                figures.dropdown_filter_fig("months", filters)
            ], style=dict(width="25%",padding="15px"))
        ], style=dict(display='flex',)
    ),
    html.Div(
        className = "CrimeDay", children = [
            dcc.Graph(id="weekday_crime", figure={}, style=dict(width="1200px"))
        ], style=dict(display='flex',)
    )
])

daytime_crime_block = html.Div([
    html.Div(
        className = "row", children = [
            html.Div(className="Element", children = [
                html.Label("Select Years"),
                figures.range_selector_fig("years")
            ], style=dict(width="30%",marginLeft="20px",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Crime Type"),
                figures.dropdown_filter_fig("crime_type", filters)
            ], style=dict(width="20%",padding="15px")),
            html.Div(className="Element", id="filter_district", children = [
                html.Label("Select Districts"),
                figures.dropdown_filter_fig("districts",filters)
            ], style=dict(width="20%",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Month"),
                figures.dropdown_filter_fig("months", filters)
            ], style=dict(width="20%",padding="15px"))
        ], style=dict(display='flex',)
    ),
    html.Div(
        className = "CrimeDaytime", children = [
            dcc.Graph(id="daytime_crime", figure={}, style=dict(width="1200px"))
        ], style=dict(display='flex',)
    )
])

abuse_crime_block = html.Div([
    html.Div(
        className = "row", children = [
            html.Div(className="Element", children = [
                html.Label("Select Years"),
                figures.range_selector_fig("years")
            ], style=dict(width="33.3%",marginLeft="20px",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Month"),
                figures.dropdown_filter_fig("months", filters)
            ], style=dict(width="25%",padding="15px"))
        ], style=dict(display='flex',)
    ),
    html.Div(
        className = "CrimeAbuse", children = [
            dcc.Graph(id="abuse_crime", figure={}, style=dict(width="1200px"))
        ], style=dict(display='flex',)
    )
])

state_crime_block = html.Div([
    html.Div(
        className = "row", children = [
            html.Div(className="Element", children = [
                html.Label("Select Years"),
                figures.dropdown_filter_fig("year_frame",filters,False)
            ], style=dict(width="25%",padding="15px")),
        ], style=dict(display='flex',)
    ),
    html.Div(
        className = "WhereWe", children = [
            dcc.Graph(id="state_crime", figure={}, style=dict(width="1200px"))
        ], style=dict(display='flex',) 
    )
])

@app.callback(
    [Output("effective_pd","figure"),],
    [Input("id_slider_years", "value"),
     Input("id_dropdown_districts", "value"),
     Input("id_dropdown_months", "value")]
)
def effective_pd_filter(years, districts, months):
    if years is None:
        years = []
    if districts is None:
        districts = []
    if months is None:
        months = []
    new_data_frame = filters.create_selection(years=years, types=[], districts=districts, months=months)
    data_frame_1, data_frame_2 = filters.effective_pd_filter(new_data_frame)
    return (figures.effective_pd_fig(data_frame_1, data_frame_2),)


@app.callback(
    [Output("holiday_crime","figure"),],
    [Input("id_slider_years", "value"),
     Input("id_dropdown_crime_type", "value"),
     Input("id_dropdown_districts", "value")]
)
def holiday_crime_filter(years, types, districts):
    if years is None:
        years = []
    if types is None:
        types = []
    if districts is None:
        districts = []
    new_data_frame = filters.create_selection(years=years, types=types, districts=districts, months=[])
    data_frame_1, mean = filters.holiday_crime_filter(new_data_frame)
    return (figures.holiday_crime_fig(data_frame_1,mean),)

@app.callback(
    [Output("weekday_crime","figure"),],
    [Input("id_slider_years", "value"),
     Input("id_dropdown_crime_type", "value"),
     Input("id_dropdown_months", "value")]
)
def crime_during_weekday_filter(years, types, months):
    if years is None:
        years = []
    if types is None:
        types = []
    if months is None:
        months = []
    new_data_frame = filters.create_selection(years=years, types=types, districts=[], months=months)
    data_frame_1, mean = filters.weekday_crime_filter(new_data_frame)
    return (figures.weekday_crime_fig(data_frame_1,mean),)

@app.callback(
    [Output("daytime_crime","figure"),],
    [Input("id_slider_years", "value"),
     Input("id_dropdown_crime_type", "value"),
     Input("id_dropdown_districts", "value"),
     Input("id_dropdown_months", "value")]
)
def crime_daytime_filter(years, types, districts, months):
    if years is None:
        years = []
    if types is None:
        types = []
    if districts is None:
        districts = []
    if months is None:
        months = []
    new_data_frame = filters.create_selection(years=years, types=types, districts=districts, months=months)
    data_frame_1, mean = filters.daytime_crime_filter(new_data_frame)
    return (figures.daytime_crime_fig(data_frame_1,mean),)

@app.callback(
    [Output("abuse_crime","figure"),],
    [Input("id_slider_years", "value"),
     Input("id_dropdown_months", "value")]
)
def crime_abuse_filter(years,months):
    if years is None:
        years = []
    if months is None:
        months = []
    new_data_frame = filters.create_selection(years=years, types=[], districts=[], months=months)
    data_frame_1 = filters.abuse_crime_filter(new_data_frame)
    return (figures.abuse_crime_fig(data_frame_1),)

@app.callback(
    [Output("state_crime","figure"),],
    [Input("id_dropdown_year_frame", "value"),]
)
def where_we_at_filter(years):
    if years is None or years==[]:
        years = [2016, 2020]
    else:
        years = list(map(int,years.split("-")))
    new_data_frame = filters.create_selection(years=years, types=[], districts=[], months=[])
    data_frame_1 = filters.state_crime_filter(new_data_frame)
    return (figures.state_crime_fig(data_frame_1),)

@app.callback(
    [Output("conatiner_charts","children"),],
    [Input('btn-str-1','n_clicks'),
    Input('btn-str-2','n_clicks'),
    Input('btn-str-3','n_clicks'),
    Input('btn-str-4','n_clicks'),
    Input('btn-str-5','n_clicks'),
    Input('btn-str-6','n_clicks'),]
)
def button_change(btn1,btn2,btn3,btn4,btn5,btn6):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    print(changed_id)
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

body = html.Div(
    className = "container scalable",
    children = [
        html.Br(),
        buttons,
        html.Div(id='conatiner_charts', children=[state_crime_block])
])

def StoryLine():
    story_layout = html.Div([
        nav,
        body
    ])
    return story_layout

app.layout = StoryLine()

if __name__ == "__main__":
    app.run_server("0.0.0.0",port=port, debug=False)

