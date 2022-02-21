import json
import logging
import os


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff


# app intialisation 
app = Dash(__name__)

# cache setup 
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

# time out 
CACHE_TIMEOUT = int(os.environ.get('DASH_CACHE_TIMEOUT', '60'))



df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")


def create_geomap():
    scope = ['Oregon']
    df_sample = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/minoritymajority.csv')
    df_sample_r = df_sample[df_sample['STNAME'].isin(scope)]

    values = df_sample_r['TOT_POP'].tolist()
    fips = df_sample_r['FIPS'].tolist()

    colorscale = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                  "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                  "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
                  "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                  "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                  "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
                  "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
                  "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
                  "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"]

    fig = ff.create_choropleth(
        fips=fips,
        values=values,
        scope=scope,
        colorscale=colorscale,
        round_legend_values=True,
        simplify_county=0,
        simplify_state=0,
        county_outline={'color': 'rgb(15, 15, 55)', 'width': 0.5},
        state_outline={'width': 1},
        legend_title='pop. per county',
        title='Illinois')

    fig.layout.template = None
    return fig


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
            value=[2001, 2010],
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

    ], style={'padding': 10, 'flex': 1}),

    html.Div(children=[
        dcc.Graph(id='geomap_figure',
                  figure=create_geomap(),
                  )
    ])


], style={'display': 'flex', 'flex-direction': 'column'})


# run the the server
if __name__ == '__main__':
    app.run_server(debug=True)
