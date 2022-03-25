import pandas as pd

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto
import numpy as np

app = dash.Dash(__name__)
server = app.server



# prepare data
df = pd.read_csv('./Dataset/cit-Patents_1092_919138.txt', header=None)
df.columns = ['from', 'to']
df['weight'] = pd.Series(np.random.rand(len(df)))

# add random colors column to dataframe
# (to be used as node colors)
colors= ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'white']
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
        "selector": 'node', #For all nodes
        'style': {
            "opacity": 0.9,
            "label": "data(label)", #Label of node to display
            "background-color": "#07ABA0", #node color
            "color": "#008B80" #node label color
        }
    },
    {
        "selector": 'edge', #For all edges
        "style": {
            "target-arrow-color": "#C5D3E2", #Arrow color
            "target-arrow-shape": "triangle", #Arrow shape
            "line-color": "#C5D3E2", #edge color
            'arrow-scale': 2, #Arrow size
            'curve-style': 'bezier' #Default curve-If it is style, the arrow will not be displayed, so specify it
    }
}]

# define layout
app.layout = html.Div([
    html.H1('Diva hw3, Group: 4',style={'text-align': 'center'}),
    html.Hr(),
    html.Label('Choose dataset',style={'text-align': 'center'}),
    dcc.Dropdown(
        id='dataset',
        options=[
            {'label': 'cit-Patents_1092_919138', 'value': 'cit-Patents_1092_919138'},
            {'label': 'cit-Patents_7315_1037462', 'value': 'cit-Patents_7315_1037462'},
            {'label': 'cit-Patents_103101_508033', 'value': 'cit-Patents_103101_508033'},
        ],
        value='cit-Patents_1092_919138',
        style={'width': '50%', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}
    ),
    html.Label('Choose Graph style',style={'text-align': 'center'}),
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
                 'value': 'cose'}
            ], value='grid',
            style={'width': '50%', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}
        ),
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
    ])
])



@app.callback(Output('cytoscape', 'layout'),
              [Input('dropdown-layout', 'value'),
              Input('dataset', 'value')])
def update_cytoscape_layout(layout):
    return {'name': layout, 'animate': True}



@app.callback(Output('cytoscape', 'elements'),
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
                'source': source,
                'target': target
            }
        })
    return cy_edges + cy_nodes

if __name__ == '__main__':
    app.run_server(debug=False)
