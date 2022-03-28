import pandas as pd
import networkx as nx
import pandas as pd
import numpy as np
import json
from utils import *
import matplotlib 

datasets = ['cit-Patents_1092_919138',
            'cit-Patents_7315_1037462', 'cit-Patents_103101_508033']


def compute_data_frame(id=0):
    df = pd.read_csv(f'./Dataset/{datasets[id]}.txt', header=None)

    df.columns=['source','target']
    df['source'] = df['source'].astype(str)
    df['target'] = df['target'].astype(str)
    g = nx.from_pandas_edgelist(df, source='source', target='target') 
    nx.draw(g)

    sources  = df['source'].unique()
    targets = df['target'].unique()
    dict(zip(targets, targets))
    a = [g.degree(club) for club in targets]
# print((a))
    degrees = { }
    for club in targets:
      if degrees.get(club)==None:
            degrees[club] = g.degree(club)

    print(len(df['source'].unique()))
    df['degree'] = df['target'].map(degrees)   
    print( len(df['degree'].unique()))
    return df



class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj) 

def compute_data(df, id=0):
    edges = df
    nodes = set()

    cy_edges = []
    cy_nodes = []

    for index, row in edges.iterrows():
        source, target,degree = row['source'], row['target'], row['degree']

        if source not in nodes:
            nodes.add(source)
            cy_nodes.append({"id": source, "label": source, "degree":degree})
        if target not in nodes:
            nodes.add(target)
            cy_nodes.append({"id": target, "label": target, "degree":degree})

        cy_edges.append({
            'source': source,
            'target': target
        })

    jsonStr = json.dumps(cy_nodes, cls=NpEncoder)
    with open(f'nodes_{id}.json', 'w') as f:
        # write jsonStr to file
        f.write(jsonStr)

    jsonStr = json.dumps(cy_edges, cls=NpEncoder)
    # print(jsonStr)
    with open(f'links{id}.json', 'w') as f:
        # write jsonStr to file
        f.write(jsonStr)    

    return 'done'
    pass


def compute_json_file():
    for i in range(len(datasets)):
        df = compute_data_frame(i)
        compute_data(df, i)
    return 'done'


def __main__():
    compute_json_file()
    print('done')

compute_json_file()