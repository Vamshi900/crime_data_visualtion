from dash import html, dcc
from navbar import Navbar
from app import app, port


nav = Navbar()

body = html.Div(
    className = "container scalable",
    children = [
        html.Br(),
        html.H1("Future Crime Predictions")
])

def Predictor():
    pred_layout = html.Div([
        nav,
        body
    ])
    return pred_layout

app.layout = Predictor()

if __name__ == "__main__":
    app.run_server("0.0.0.0",port=port, debug=False)