import plotly.express as px
import pandas as pd


df = pd.read_csv('asoiaf_nodes_prop.csv')
# print(df)
fig = px.scatter(df,
                 x = 'pagerank', # x axis
                 y= 'betweenness', # y axis
                 log_x=True, log_y=True, # log scale 
                 color_continuous_scale='Turbo', # color scale 
                 color = 'diversity',
                 size = 'pagerank', 
                 custom_data = ['name', 'degree','peel', 'diversity'], # custom data for tool tip
                 labels=dict( betweenness="betweeness centrality"), # axis labels dictonary 
                 )

# tooltip data 
fig.update_traces(hovertemplate = ( 'name: %{customdata[0]}<br>'
                                    'pagerank: %{x}, betweenness: %{y}<br>'
                                    'degree: %{customdata[1]:.2e}<br>'
                                    'peel: %{customdata[2]:.2e}'
                                    'diversity: %{customdata[1]:.2e}<br>'
                                    ))

fig.update_layout(
    xaxis=dict(
          rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="log"
    )
)                                    
config = dict({'scrollZoom': True})
fig.show(config=config)
fig.write_image("./fig1.png")