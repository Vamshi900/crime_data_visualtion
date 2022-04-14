from dash import html, dcc
from navbar import Navbar
from app import app, port
import dash_bootstrap_components as dbc

nav = Navbar()

buttons = html.Div([
    dbc.Button("Is crime rate declining?", color="secondary", className="me-1", style=dict(width=150,height=60)),
    dbc.Button("Yes it should!!", color="secondary", className="me-1", style=dict(width=150,height=60)),
    dbc.Button("How effective is Chicago PD?", color="secondary", className="me-1", style=dict(width=150,height=60)),
    dbc.Button("Streets are not safe...", color="secondary", className="me-1", style=dict(width=150,height=60)),
    dbc.Button("Criminals also sleep at night...", color="secondary", className="me-1", style=dict(width=150,height=60)),
    dbc.Button("Criminals on a holiday!!", color="secondary", className="me-1", style=dict(width=150,height=60)),
    dbc.Button("Careful on Saturdays!!", color="secondary", className="me-1", style=dict(width=150,height=60)),
    dbc.Button("Sensitive Crimes", color="secondary", className="me-1", style=dict(width=150,height=60)),
    html.Br(),
    html.Br(),
])

chicago_pd_effect = html.div([
    html.Div(
        className = "row", children = [
            html.Div(className="Element", children = [
                html.Label("Select Years"),
                filters.range_selector("years")
            ], style=dict(width="30%",background="#F9F9F9",marginLeft="40px",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Crime Type"),
                filters.dropdown_filter("crime_type")
            ], style=dict(width="20%",background="#F9F9F9",padding="15px")),
            html.Div(className="Element", id="filter_district", children = [
                html.Label("Select Districts"),
                filters.dropdown_filter("districts")
            ], style=dict(width="20%",background="#F9F9F9",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Month"),
                filters.dropdown_filter("months")
            ], style=dict(width="20%",background="#F9F9F9",padding="15px"))
        ], style=dict(display='flex',)
    ),
])

body = html.Div(
    className = "container scalable",
    children = [
        html.Br(),
        html.H1("Our view on the Crime Story"),
        buttons,
        chicago_pd_effect
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