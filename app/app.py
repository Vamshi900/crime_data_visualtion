# importing the necessary modules
from dash import Dash
import dash_bootstrap_components as dbc
import vaex as vx
import pandas as pd

# defining our application style sheet
style_sheets = [dbc.themes.YETI]

# defining the dash app to be used for development and deployment
app = Dash(__name__, external_stylesheets=style_sheets, suppress_callback_exceptions=True)

# specifying the port on which the app should run
port = 5059

orig_data_frame = pd.read_csv("sample_data.csv") #vx.from_csv("sample_data.csv")