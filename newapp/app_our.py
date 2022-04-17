# importing the necessary modules
from dash import Dash
import dash_bootstrap_components as dbc
import vaex as vx
import pandas as pd



# defining the dash app to be used for development and deployment
app = Dash(__name__, suppress_callback_exceptions=True)

# specifying the port on which the app should run
port = 5059

orig_data_frame = vx.read_csv("dataset/sample.csv")


# orig_data_frame= vx.open("./data*.hdf5")