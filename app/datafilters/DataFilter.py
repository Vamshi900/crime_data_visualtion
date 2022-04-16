import imp
import vaex as vx
import pandas as pd
import numpy as np


class DataFilter:
    def __init__(self, data_frame):
        self.data_frame = data_frame  # update data frame based on primary filters
        self.original_data_frame = data_frame  # backup of original data frame

    # static method to get days
    def get_days_of_week(self):
        days = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
        return days

    # static method to get months
    def get_months(self):
        months_map = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                      7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
        return months_map

     # static method to get police districts
    def get_police_districts(self):
        district_map = {1: "Central", 2: "Wentworth", 3: "Grand Crossing", 4: "South Chicago", 5: "Calumet",
                        6: "Gresham", 7: "Englewood", 8: "Chicago Lawn", 9: "Deering", 10: "Ogden",
                        11: "Harrison", 12: "Near West", 14: "Shakespeare", 15: "Austin", 16: "Jefferson Park",
                        17: "Albany Park", 18: "Near North", 19: "Town Hall", 20: "Lincoln", 21: "Lincoln1", 22: "Morgan Park",
                        24: "Rogers Park", 25: "Grand Central", 31: "Distr31"}
        return district_map
    #

    def get_years(self):
        years = self.data_frame["Year"].unique()
        return sorted(years)

    # update data frame based on primary filters
    def update_data_frame(self, data_frame):
        self.data_frame = data_frame

    def reset_data_frame(self):
        self.data_frame = self.original_data_frame.copy()

    # get crime type count sorted

    def get_crime_types(self):
        types = self.data_frame["Primary Type"].unique()
        return sorted(types)

    # filter to get the cases count display
    def get_total_cases(self):
        return self.data_frame.count()

    # primary filter to cut the data frame
    # always use the original data frame
    def create_selection(self, years=[2001, 2002, 2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022], types=[], districts=[], months=[]):
        df = self.original_data_frame.copy()
        print('before filter df ', df.count())
        selection = None
        # if len(years) > 0:
        #     df = df[df.Year.isin(years)]
        #     print('year selection', df.count())
        if len(districts) > 0:
            df = df[df.District.isin(districts)]
            print('disctricts slection', df.count())
        if len(months) > 0:
            df = df[df.Month.isin(months)]
            print('months slection', df.count())
        if len(types) > 0:
            # convert types to uppper case
            types = [x.upper() for x in types]
            df = df[df["Primary Type"].isin(types)]
            print('types slection', df.count())
        
        print('after filter selection', df.count())
        self.update_data_frame(df)
        return df

    def sunburst_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        tp_df = data_frame.copy()
        tp_df['District_Name'] = tp_df.District.map(
            self.get_police_districts())
        tp_df = tp_df.groupby([tp_df["District_Name"], tp_df["Primary Type"]], agg={
            'total_case': vx.agg.count('Primary Type')})
        tp_df = tp_df.sort(["District_Name", 'total_case'], ascending=False)
        # print('sunburst filter ', tp_df.total_case.unique())

        vals = np.array(tp_df.total_case.tolist())
        labels = np.array(tp_df["District_Name"].tolist())
        parents = np.array(tp_df['Primary Type'].tolist())
        # print(len(labels), len(parents), 'labels, parents', len(vals))
        new_df = pd.DataFrame(
            {'labels': labels, 'parents': parents, 'values': vals})
        return new_df

    def table_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        tp_df = data_frame.copy()
        tp_df['District_Name'] = tp_df.District.map(
            self.get_police_districts())
        tp_df = tp_df.groupby([tp_df["District_Name"], tp_df["Primary Type"]], agg={
            'total_case': vx.agg.count('Primary Type')})
        tp_df = tp_df.sort(["District_Name", 'total_case'], ascending=False)

        # vals = np.array(tp_df.total_case.tolist())
        # labels = np.array(tp_df["District_Name"].tolist())
        # parents = np.array(tp_df['Primary Type'].tolist())
        # print(len(labels), len(parents), 'labels, parents', len(vals))
        # new_df = pd.DataFrame(
        #     {'labels': labels, 'parents': parents, 'values': vals})
        # return new_df
        # return tp_df
    
    # geo plot filter
    def geo_plot_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        tp_df = data_frame.copy()
        # print(tp_df.head(5))
        tp_df = tp_df['Latitude', 'Longitude']
        if tp_df.count() > 2000000:
            tp_df = tp_df.sample(200000)
        # tpf = tp_df.sample(n=2, random_state=42)
        print('geo plot sampled filter count', tp_df.count())
        df_pandas = tp_df.to_pandas_df(["Longitude", "Latitude"])
        return df_pandas