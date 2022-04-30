import pandas as pd
import plotly.graph_objects as go
import vaex as vx
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.ticker as ticker

class CreateStatFigures:
    def __init__(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        self.data_frame = data_frame
    
    def load_daily(self):
        df = pd.read_csv('dataset/daily_cases.csv')
        df = df.set_index('Date')
        df = df.sort_index()
        return df['Count']

    def load_monthly(self):
        df = pd.read_csv('dataset/monthly_cases.csv')
        df = df.set_index('Date')
        df = df.sort_index()
        return df['Count']

    def load_prediction(self):
        df = pd.read_csv('dataset/prediction.csv', header=None)
        df = df.set_index(0)
        return df[1]

    def load_m_prediction(self):
        df = pd.read_csv('dataset/monthly_prediction.csv', header=None)
        df = df.set_index(0)
        return df[1]
    
    def plot_daily_prediction(self):
        df_daily = self.load_daily()
        df_daily = df_daily[-396:]
        prediction = self.load_prediction()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            name="Original",
            mode="lines", x=df_daily.index, y=df_daily
        ))
        fig.add_trace(go.Scatter(
            name="Prediction",
            mode="lines", x=prediction.index, y=prediction
        ))
        fig.update_layout(title='Daily Crime Cases Prediction in 2022',
                        xaxis_title='Date',
                        yaxis_title='Daily Cases')
        return fig

    def plot_monthly_prediction(self):
        df_monthly = self.load_monthly()
        df_monthly = df_monthly[-25:]
        prediction = self.load_m_prediction()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            name="Original",
            mode="lines", x=df_monthly.index, y=df_monthly
        ))
        fig.add_trace(go.Scatter(
            name="Prediction",
            mode="lines", x=prediction.index, y=prediction
        ))
        fig.update_layout(title='Monthly Crime Cases Prediction in next 3 years',
                        xaxis_title='Month',
                        yaxis_title='Monthly Cases')
        return fig
    
    def chart_1(self):
        crime_types = self.data_frame[['Primary Type']]
        temp_data_frame = crime_types.groupby(crime_types["Primary Type"],
                                                  agg={'total_case': vx.agg.count('Primary Type')}, sort=True)
        temp_data_frame = temp_data_frame.sort(
                    ["total_case"], ascending=False)
        temp_data_frame = temp_data_frame.head(15)
        temp_data_frame = temp_data_frame.sort(
                    ["total_case"], ascending=True)
        temp_data_frame = temp_data_frame.to_pandas_df()
        fig = px.bar(temp_data_frame, y="Primary Type", x="total_case", orientation="h", title="Top Chicago Crimes by Type (2006-Present)")
        fig.update_layout(title_x=0.5, height=600, width=670, xaxis_title="Crime Count", yaxis_title="Crime Type")
        return fig
    
    def chart_2(self):
        narcotics = self.data_frame[self.data_frame['Primary Type']=='NARCOTICS']
        temp_data_frame = narcotics.groupby([narcotics["Primary Type"],narcotics["Description"]],
                                                  agg={'total_case': vx.agg.count('Primary Type')}, sort=True)
        temp_data_frame = temp_data_frame.sort(
                    ["total_case"], ascending=False)
        temp_data_frame = temp_data_frame.head(15)
        temp_data_frame = temp_data_frame.sort(
                    ["total_case"], ascending=True)
        temp_data_frame = temp_data_frame.to_pandas_df()
        fig = px.bar(temp_data_frame, y="Description", x="total_case", orientation="h", title="Top Chicago Narcotics Crimes (2006-Present)")
        fig.update_layout(title_x=0.5, height=600, width=670, xaxis_title="Crime Count", yaxis_title="Narcotics Crime")
        return fig
    
    def chart_3(self):
        narcotics = self.data_frame[self.data_frame['Primary Type']=='OTHER OFFENSE']
        temp_data_frame = narcotics.groupby([narcotics["Primary Type"],narcotics["Description"]],
                                                        agg={'total_case': vx.agg.count('Primary Type')}, sort=True)
        temp_data_frame = temp_data_frame.sort(
                    ["total_case"], ascending=False)
        temp_data_frame = temp_data_frame.head(15)
        temp_data_frame = temp_data_frame.sort(
                    ["total_case"], ascending=True)
        temp_data_frame = temp_data_frame.to_pandas_df()
        fig = px.bar(temp_data_frame, y="Description", x="total_case", orientation="h", title="Top Chicago Other Offense Crimes (2006-Present)")
        fig.update_layout(title_x=0.5, height=600, width=670, xaxis_title="Crime Count", yaxis_title="Other Offense Crime")
        return fig
    
    def chart_4(self):
        temp_data_frame = self.data_frame.groupby(self.data_frame["Day"],agg={'total_case': vx.agg.count('Day')}, sort=True)
        temp_data_frame = temp_data_frame.sort(
                    ["total_case"], ascending=True)
        temp_data_frame = temp_data_frame.to_pandas_df()
        fig = px.bar(temp_data_frame, y="Day", x="total_case", orientation="h", title="All Chicago Crimes by Day of the Week (2006-Present)")
        fig.update_layout(title_x=0.5, height=600, width=670, xaxis_title="Crime Count", yaxis_title="Week Day")
        return fig
    
    def chart_5(self):
        temp_data_frame = self.data_frame.groupby(self.data_frame["Month"],agg={'total_case': vx.agg.count('Month')}, sort=True)
        temp_data_frame = temp_data_frame.sort(["total_case"], ascending=True)
        temp_data_frame = temp_data_frame.to_pandas_df()
        fig = px.bar(temp_data_frame, y="Month", x="total_case", orientation="h", title="All Chicago Crimes by Month of the Year (2006-Present)")
        fig.update_layout(title_x=0.5, height=600, width=670, xaxis_title="Crime Count", yaxis_title="Month of the year")
        return fig
    
    def chart_6(self):
        temp_data_frame = self.data_frame.groupby(self.data_frame["Location Description"],agg={'total_case': vx.agg.count('Month')}, sort=True)
        temp_data_frame = temp_data_frame.sort(
                    ["total_case"], ascending=False)
        temp_data_frame = temp_data_frame.head(15)
        temp_data_frame = temp_data_frame.sort(
                    ["total_case"], ascending=True)
        temp_data_frame = temp_data_frame.to_pandas_df()
        fig = px.bar(temp_data_frame, y="Location Description", x="total_case", orientation="h", title="Top 15 Chicago Crime Locations (2006-Present)")
        fig.update_layout(title_x=0.5, height=600, width=670, xaxis_title="Crime Count", yaxis_title="Location")
        return fig
    
    def chart_7(self):
        temp_data_frame = self.data_frame[self.data_frame["Primary Type"]=='PROSTITUTION']
        temp_data_frame = temp_data_frame.groupby(temp_data_frame["Location Description"],agg={'total_case': vx.agg.count('Location Description')}, sort=True)
        temp_data_frame = temp_data_frame.sort(
                    ["total_case"], ascending=False)
        temp_data_frame = temp_data_frame.head(15)
        temp_data_frame = temp_data_frame.sort(
                    ["total_case"], ascending=True)
        temp_data_frame = temp_data_frame.to_pandas_df()
        fig = px.bar(temp_data_frame, y="Location Description", x="total_case", orientation="h", title="Top 15 Chicago Prostitution Locations (2006-Present)")
        fig.update_layout(title_x=0.5, height=600, width=670, xaxis_title="Crime Count", yaxis_title="Location")
        return fig

    def chart_8(self):
        temp_data_frame = self.data_frame[self.data_frame["Primary Type"]=='PROSTITUTION']
        temp_data_frame = temp_data_frame.groupby(temp_data_frame["Year"],agg={'total_case': vx.agg.count('Year')}, sort=True)
        temp_data_frame = temp_data_frame.to_pandas_df()
        fig = px.line(temp_data_frame, y="total_case", x="Year", orientation="h", title="Chicago Prostitution Situation (2006-Present)")
        fig.update_layout(title_x=0.5, height=600, width=670, xaxis_title="Year", yaxis_title="Crime Count")
        return fig