import plotly.express as px
import pandas as pd



df = pd.read_csv('asoiaf_nodes_prop.csv')



# print(df)
fig = px.scatter(df,
                 x = 'pagerank', # x axis
                 y= 'betweenness', # y axis
                 log_x=True, log_y=True, # log scale 
                 color_continuous_scale='Turbo', # color scale 
                 color = 'peel',
                 size = 'degree', 
                 custom_data = ['name', 'degree','peel', 'diversity'], # custom data for tool tip
                 labels=dict( betweenness="betweeness centrality"), # axis labels dictonary 
                 )

# calculate size ref
sizeref = 2*max(df['degree'])/(1000)

print('size ref',sizeref)
                                    
# tooltip data 
fig.update_traces(hovertemplate = ( 'name: %{customdata[0]}<br>'
                                    'pagerank: %{x}, betweenness: %{y}<br>'
                                    'degree: %{customdata[1]:.2e}<br>'
                                    'peel: %{customdata[2]:.2e}'
                                    'diversity: %{customdata[1]:.2e}<br>'
                                    ),
                                    mode='markers', marker=dict(sizemode='area',    
                                              sizeref=0.2, line_width=2)
                                    )
# range slider and dragmode config 
fig.update_layout(
    xaxis=dict(
        rangeslider=dict(
            visible=True
        ),
        type="log"
    ),
    dragmode="pan",
) 
  
# zoom configuration
config = dict({'scrollZoom': True})
fig.show(config=config)
fig.write_image("./HW1_vs734_scatter.png")