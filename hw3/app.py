import pandas as pd
import math

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto
import numpy as np
import plotly.express as px


app = dash.Dash(__name__)
server = app.server


# prepare data
df = pd.read_csv('./Dataset/cit-Patents_1092_919138.txt', header=None)
df.columns = ['from', 'to']
df['weight'] = pd.Series(np.random.rand(len(df)))

# add random colors column to dataframe
# (to be used as node colors)
colors = ['red', 'blue', 'green', 'yellow',
          'orange', 'purple', 'pink', 'brown', 'white']
df['color'] = pd.Series(np.random.choice(colors, len(df)))

edges = df
nodes = set()

cy_edges = []
cy_nodes = []

for index, row in edges.iterrows():
    source, target = row['from'], row['to']

    if source not in nodes:
        nodes.add(source)
        cy_nodes.append({"data": {"id": source, "label": source}})
    if target not in nodes:
        nodes.add(target)
        cy_nodes.append({"data": {"id": target, "label": target}})

    cy_edges.append({
        'data': {
            'source': source,
            'target': target
        }
    })

# define stylesheet
stylesheet = [
    {
        "selector": 'node',  # For all nodes
        'style': {
            "opacity": 0.9,
            "label": "data(label)",  # Label of node to display
            # "background-color": "#07ABA0", #node color
            # "color": "#008B80" #node label color
        }
    },
    {
        "selector": 'edge',  # For all edges
        "style": {
            "target-arrow-color": "#C5D3E2",  # Arrow color
            "target-arrow-shape": "triangle",  # Arrow shape
            "line-color": "#C5D3E2",  # edge color
            'arrow-scale': 2,  # Arrow size
            # Default curve-If it is style, the arrow will not be displayed, so specify it
            'curve-style': 'bezier'
        }
    }]

col_swatch = px.colors.qualitative.Dark24


edge_count = len(cy_edges)
node_count = len(cy_nodes)
stylesheet += [
    {
        "selector": "." + str(i),
        "style": {"background-color": col_swatch[i % 5], "line-color": col_swatch[i % 5]},
    }
    for i in range(node_count)
]

# define layout
app.layout = html.Div([
    html.H1('Diva hw3, Group: 4', style={'text-align': 'center'}),
    html.Hr(),
    html.Label('Choose dataset', style={'text-align': 'center'}),
    dcc.Dropdown(
        id='dataset',
        options=[
            {'label': 'cit-Patents_1092_919138',
                'value': 'cit-Patents_1092_919138'},
            {'label': 'cit-Patents_7315_1037462',
                'value': 'cit-Patents_7315_1037462'},
            {'label': 'cit-Patents_103101_508033',
                'value': 'cit-Patents_103101_508033'},
        ],
        value='cit-Patents_1092_919138',
        style={'width': '50%', 'display': 'block',
               'margin-left': 'auto', 'margin-right': 'auto'}
    ),
    html.Label('Choose Graph style', style={'text-align': 'center'}),

    dcc.Dropdown(
        id='dropdown-layout',
        options=[
            {'label': 'random',
             'value': 'random'},
            {'label': 'grid',
             'value': 'grid'},
            {'label': 'circle',
             'value': 'circle'},
            {'label': 'concentric',
             'value': 'concentric'},
            {'label': 'breadthfirst',
             'value': 'breadthfirst'},
            {'label': 'cose',
             'value': 'cose'},

        ], value='grid',
        style={'width': '50%', 'display': 'block',
               'margin-left': 'auto', 'margin-right': 'auto'}
    ),

    html.Label(f'Number of edges ', style={'text-align': 'center'}),
    # display count of edges as text
    html.Div(id='edge-count',
             style={'text-align': 'left'}, children=f'{edge_count}'),


    html.Label(f'Number of Nodes s :', style={'text-align': 'Center'}),
    # display count of nodes as text
    html.Div(id='node-count',
             style={'text-align': 'left'}, children=f'{node_count}'),


    html.Div(children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=cy_edges + cy_nodes,
            style={
                'height': '95vh',
                'width': '100%'
            },
            stylesheet=stylesheet
        )
    ], style={'margin-left': '50px', 'width': '90%', 'margin-right': '50px', 'border': '3px solid red'})
])

layout_options = {
    'cose': {
        'name': 'klay',
        # 'minNodeSize': 5,
        # 'maxNodeSize': 10,
        # 'nodeOverlap': 20,
        # 'idealEdgeLength': 100,
        # 'edgeElasticity': 100,
        # 'minEdgeSize': 100,
    }
}


@app.callback(Output('cytoscape', 'layout'),
              [Input('dropdown-layout', 'value')])
def update_cytoscape_layout(layout):
    return {'name': layout}


@app.callback([Output('cytoscape', 'elements'), Output('edge-count', 'children'), Output('node-count', 'children')],
              [Input('dataset', 'value')])
def update_dataset(dataset):
    edges = pd.read_csv('./Dataset/'+dataset+'.txt', header=None)
    edges.columns = ['from', 'to']
    edges['weight'] = pd.Series(np.random.rand(len(edges)))
    edges['color'] = pd.Series(np.random.choice(colors, len(edges)))
    cy_edges = []
    cy_nodes = []
    nodes = set()
    for index, row in edges.iterrows():
        source, target = row['from'], row['to']

        if source not in nodes:
            nodes.add(source)
            cy_nodes.append({"data": {"id": source, "label": source}})
        if target not in nodes:
            nodes.add(target)
            cy_nodes.append({"data": {"id": target, "label": target}})

        cy_edges.append({
            'data': {
                "id": str(index),
                'source': source,
                'target': target
            }
        })
    return ((cy_edges + cy_nodes), f'{len(cy_edges)} ~ 2** {math.log2(len(cy_edges)) }', len(cy_nodes))


if __name__ == '__main__':
    app.run_server(debug=False)
