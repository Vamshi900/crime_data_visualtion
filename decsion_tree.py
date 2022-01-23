import plotly.express as px
import pandas as pd


df = pd.read_csv('asoiaf_nodes_prop.csv')

def genrate_buckets(colName):
    print(df[colName].describe())
    mean = df[colName].mean()
    std = df[colName].std()
    print('mean',mean,'std',std)
    mean_arr = [mean+x*std for x in range(-3,4,1)]
    ir = pd.IntervalIndex.from_breaks(mean_arr)
    print(ir)
    # df2=  pd.cut(df, bins=ir)
    # print(df2.describe())
    buckets =[]
    for i in range(1,len(mean_arr)):
        buckets.append(df[df[colName].between(mean_arr[i-1],mean_arr[i])])
        print(buckets[len(buckets)-1].describe())

    print(buckets[0].describe())

    pass

sizeref = max(df['degree'])/(1000)
print(sizeref)
# genrate_buckets('degree')