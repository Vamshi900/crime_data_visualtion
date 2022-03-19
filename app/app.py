"""import json
import logging
import os


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff


# app intialisation 
app = Dash(__name__)

# # cache setup 
# cache = Cache(app.server, config={
#     'CACHE_TYPE': 'filesyste',
#     'CACHE_DIR': 'cache-directory'
# })

# # time out 
# CACHE_TIMEOUT = int(os.environ.get('DASH_CACHE_TIMEOUT', '60'))

# figure functions start

# import from figures.py
#---- figure functions end

# filter options 

#

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
    app.run_server(host='0.0.0.0', port=8080, debug=True)
    # app.run_server(debug=True)

"""

from dash import Dash, html, dcc
from filters import FilterCreation

app = Dash(__name__)

filters = FilterCreation()

# dashboard layout code
app.layout = html.Div([
    html.H1('Criminalytics: A visual tool for crime analysis',
            style={
                'textAlign':'center',
                'paddingTop': '10px'
            }
    ),

    html.Div(
        className = "row", children = [
            html.Div(className="Element", children = [
                html.Label("Displayed Crimes")
            ], style=dict(width="25%",background="white",margin="10px",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Years"),
                filters.range_selector("years")
            ], style=dict(width="25%",background="white",margin="10px",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Crime Type"),
                filters.dropdown_filter("crime_type")
            ], style=dict(width="25%",background="white",margin="10px",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Month"),
                filters.dropdown_filter("months")
            ], style=dict(width="25%",background="white",margin="10px",padding="15px"))
        ], style=dict(display='flex')
    ),

    dcc.Tabs(id="tabs", value='tab-1-visualization', children=[
        dcc.Tab(label='Visualization', value='tab-1-visualization'),
        dcc.Tab(label='Prediction', value='tab-2-prediction'),
    ], style=dict(padding="15px")),

    html.Div(className="Maps", children = [
        html.Div(className="MainMap", id="main_map", children = [
            html.Label("Dem")
            #html.Iframe(src="./district.html", style={'width':"40%", 'height':"380px"})
        ], style=dict(width="40%", height="380px",background="white",margin="10px",padding="15px")),
        html.Div(className="Element", id="filter_district", children = [
            html.Label("Select Districts"),
            filters.dropdown_filter("districts")
        ], style=dict(width="200px",margin_bottom="150px")),
        html.Div(className="MinMap", id="min_map", children = [
            html.Div(className="MinMap", id="min_map1", children = [
                html.Label("Map2")
            ], style=dict(width="20%", height="380px",background="white",margin="10px",padding="15px")),
            html.Div(className="MinMap", id="min_map2", children = [
                html.Label("Map3")
            ], style=dict(width="20%", height="380px",background="white",margin="10px",padding="15px")),
            html.Div(className="MinMap", id="min_map3", children = [
                html.Label("Map4")
            ], style=dict(width="20%", height="380px",background="white",margin="10px",padding="15px"))
        ],style=dict(display='flex'))
    ],style=dict(display='flex')),

    html.Div(className = "charts_table", children=[
        html.Div(className="Element", children = [
            html.Label("District Sunburst")
        ], style=dict(width="40%", height="400px",background="white",margin="10px",padding="15px")),
        html.Div(className="Element", children = [
            html.Label("District Tabular"),
        ], style=dict(width="60%", height="500px",background="white",margin="10px",padding="15px")),
    ], style=dict(display='flex'))


], style = {'background': '#F2F2F2'})


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8044,debug=True)


