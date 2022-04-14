import dash_bootstrap_components as dbc
from dash import html

def Navbar():
    
    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(dbc.NavbarBrand("Criminalytics: A visual tool for crime analysis", className="ms-4")),
                        ],
                        align="center"
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink("Storyline", href="/story")),
                        dbc.NavItem(dbc.NavLink("Predictions", href="/pred"))
                    ],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse2",
                    navbar=True,
                ),
            ]
        ),
        color="dark",
        dark=True,
    )
    return navbar