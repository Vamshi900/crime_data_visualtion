# loading necessary modules
from dash import html, dcc
from dash.dependencies import Input, Output

# loading application component/webpages
from app import app, port
from storyline import StoryLine
from predictor import Predictor
from dashboard import Dashboard


app.layout = html.Div([
    dcc.Location(id = 'url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'), 
    Input('url', 'pathname')
)
def visiting_page(path):
    if path == "/story":
        return StoryLine()
    elif  path=="/pred":
        return Predictor()
    else:
        return Dashboard()

if __name__ == "__main__":
    app.run_server("0.0.0.0",port=port, debug=False)