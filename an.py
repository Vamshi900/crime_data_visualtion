import plotly.express as px
import pandas as pd
import joblib
# df = px.data.tips()
# print(df)


df2 = pd.read_csv('asoiaf_nodes_prop.csv')
# df_plot = df[df['degree']!=0]
# df_plot = df[df['peel']!=0]
# df_plot = df[df['diversity']!=0]

df = pd.read_pickle("./test") 
print(df)
depths = joblib.load('./depths')
print(depths)

# add root index 
df['id']="all"
df['values']=df2['peel']

df = df[df['degree']!=0]
df = df[df['peel']!=0]
df = df[df['diversity']!=0]
df = df[df['pagerank']!=0]
df = df[df['betweenness']!=0]
df = df[df['values']!=0]
# print(df)


fig = px.treemap(df, path=['degree', 'peel', 'pagerank','betweenness'], 
                 labels=depths,
                 values='values', color='values')
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
fig.show()
fig.write_image('./treemap.png')
