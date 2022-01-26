
import plotly.express as px
import pandas as pd



# load data frame
df = pd.read_csv('asoiaf_nodes_prop.csv')
# add root index 
df['id']="all"
# add id to all rows in the data frame
df['index'] = range(1, len(df)+1)

g_levels ={
  'all':'all'
}


# function to split into buckets based on specified columname,data
def genrate_buckets(data,colName):
    
    # compute mean
    mean = data[colName].mean()
    #compute std
    std = data[colName].std()
    
    # compute the mean_arr of the form mean+x*std
    mean_arr = [mean+x*std for x in range(-3,4,1)]
     
    # create the interval range for pandas to split the dataframe
    ir = pd.IntervalIndex.from_breaks(mean_arr)
    # print(ir)
    
    #store the buckets
    buckets =[]
    for i in range(1,len(mean_arr)):
        buckets.append(data[data[colName].between(mean_arr[i-1],mean_arr[i])])
        # print(buckets[len(buckets)-1].describe())
    
    # for each bucket append the id column it should be of the form all/degree+mean_arr[i]
    # here the value is computed of the form from mean arr
    count=0
    for bucket in buckets:
     count+=1
     val = colName+str(count)
     if(g_levels.get(val)==None):
       g_levels[val]=val

     for index, row in bucket.iterrows():
        row['id']+='/'+colName+str(count)
        mask = df['index'] == row['index']

        df.loc[(df.index == index),'id']+='/'+colName+str(count)
        df.loc[(df.index == index),colName]= df.loc[(df.index == index),'id']



        # each row would be appended as such id in the original data frame 
    
    return buckets

# fucntion to order split data as required 
def prep_data():
  levels =['all', 'degree', 'peel', 'pagerank','diversity','betweenness']
  buckets =[df]
  for level in levels[1:]:
    
    newbuckets =[]
    for bucket in buckets:
      genrated = genrate_buckets(bucket,level)
      for bck in genrated:
        newbuckets.append(bck)
    buckets=newbuckets  

print('creating data buckets....')
prep_data()

# genrate_buckets(df,'degree') # here in the genarate buckets we group by the id colum and split further based on the crieteria


depths= list(g_levels.values())

# df.to_pickle('test') 
# joblib.dump(depths,'./depths')

# visualisation
df2 = pd.read_csv('asoiaf_nodes_prop.csv')

# add root index 
df['values']=df2['diversity']

df = df[df['degree']!=0]
df = df[df['peel']!=0]
df = df[df['diversity']!=0]
df = df[df['pagerank']!=0]
df = df[df['betweenness']!=0]
df = df[df['values']!=0]
print('data ready')
# print(df)
fig = px.treemap(df, path=['degree', 'peel', 'pagerank','betweenness'], 
                 labels=depths,
                 values='values', color='values')
print('treemap genrated')
# fig.show()
fig.write_image('./Hw1_late_vs734_treemap.png')







