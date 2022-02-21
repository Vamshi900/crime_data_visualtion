
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div([
    html.Div(children=[
        html.Br(),
        html.Label('District Dropdown'),
        dcc.Dropdown(['1', '2', '3', '4', '5'],
                     ['1', '3'],
                     multi=True),
    ], style={'padding': 10, 'flex': 1}),

    # auto compute theft types

    # html.Div(children=[
    #     html.Br(),
    #     html.Label('District Dropdown'),
    #     dcc.Dropdown(df_vaex.unique('Primary Type'),
    #                  ['Theft'],
    #                  multi=True),
    # ], style={'padding': 10, 'flex': 1})

    html.Div(children=[
        html.Br(),
        html.Label('Slider'),
        dcc.RangeSlider(
            2001,
            2022,
            1,
            marks={i: f'{i}' for i in range(2001, 2022, 5)},
            value=[2001,2010],
            tooltip={"placement": "bottom", "always_visible": True}
        ),

        # autumatic year slider

        # dcc.RangeSlider(
        #     df['year'].min(),
        #     df['year'].max(),
        #     step=None,
        #     value=df['year'].min(),
        #     marks={str(year): str(year) for year in df['year'].unique()},
        #     id='year-slider'
        # )

    ], style={'padding': 10, 'flex': 1})
], style={'display': 'flex', 'flex-direction': 'row'})


# run the the server
if __name__ == '__main__':
    app.run_server(debug=True)
