import imp
import vaex as vx
import pandas as pd
import numpy as np


class DataFilter:
    def __init__(self, data_frame):
        self.original_data_frame = data_frame

        post_processed = self.pre_process(data_frame)
        self.data_frame = post_processed
        self.original_data_frame = post_processed

    # one time filter for adding district name to dataframe
    def pre_process(self, df):
        police_districts = self.get_police_districts()
        df["District_Name"] = df["District"].map(
            police_districts)
        # drop null value rows
        df = df.dropna()
        df = self.create_selection()

        return df

    # update data frame
    def update_data_frame(self, data_frame):
        self.data_frame = data_frame

    # reset data frame
    def reset_data_frame(self):
        self.data_frame = self.original_data_frame.copy()

    # get day of week
    def get_days_of_week(self):
        days = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
        return days

    # get month
    def get_months(self):
        months_map = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                      7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
        return months_map

    # get police districts
    def get_police_districts(self):
        district_map = {1: "Central", 2: "Wentworth", 3: "Grand Crossing", 4: "South Chicago", 5: "Calumet",
                        6: "Gresham", 7: "Englewood", 8: "Chicago Lawn", 9: "Deering", 10: "Ogden",
                        11: "Harrison", 12: "Near West", 14: "Shakespeare", 15: "Austin", 16: "Jefferson Park",
                        17: "Albany Park", 18: "Near North", 19: "Town Hall", 20: "Lincoln", 22: "Morgan Park",
                        24: "Rogers Park", 25: "Grand Central", 21: "missing North Center", 31: "missing Washington Park"}
        return district_map

    # unique years
    def get_years(self):
        years = self.data_frame["Year"].unique()
        return sorted(years)

    # unique primary crime types
    def get_crime_types(self):
        types = self.data_frame["Primary Type"].unique()
        return sorted(types)

    # filter to get the cases count display
    def get_total_cases(self):
        return self.data_frame.count()

    # primary data selection filter
    def create_selection(self, years=[2001, 2022], types=[], districts=[], months=[]):
        df = self.original_data_frame.copy()
        # print('before filter df ', df.count())
        selection = None
        if len(years) > 0:
            # array of years given start and end
            filter_years = [yr for yr in range(years[0], years[1]+1)]
            # print(filter_years)
            df = df[df["Year"].isin(filter_years)]
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

    # sunburst figure filter
    def sunburst_filter(self, data_frame=None):
        # check for none
        if data_frame is None:
            data_frame = self.data_frame

        temp_data_frame = data_frame.copy()
        temp_data_frame = temp_data_frame[["Primary Type", "District_Name"]]

        # temp_data_frame["District_Name"] = temp_data_frame["District"].map(self.get_police_districts())
        temp_data_frame = temp_data_frame.groupby([temp_data_frame["District_Name"], temp_data_frame["Primary Type"]],
                                                  agg={'total_case': vx.agg.count('Primary Type')}, sort=True)
        temp_data_frame = temp_data_frame.sort(
            ["District_Name", "total_case"], ascending=False)

        vals = np.array(temp_data_frame["total_case"].tolist())
        labels = np.array(temp_data_frame["District_Name"].tolist())
        parents = np.array(temp_data_frame['Primary Type'].tolist())

        # todo: fix this pandas bug
        new_data_frame = pd.DataFrame(
            {'labels': labels, 'parents': parents, 'values': vals})
        return new_data_frame

    # geo plot filter
    def geo_plot_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        tp_df = data_frame.copy()
        # print(tp_df.head(5))
        # tp_df = tp_df['Latitude', 'Longitude']
        if tp_df.count() > 2000000:
            tp_df = tp_df.sample(200000)
        # tpf = tp_df.sample(n=2, random_state=42)
        # print('geo plot sampled filter count', tp_df.count())
        df_pandas = tp_df.to_pandas_df()
        return df_pandas

    # ranking table filter
    def create_ranking_filter(self, data_frame):
        temp_data_frame = data_frame[[
            "District", "Primary Type", "District_Name"]]

        temp_data_frame = temp_data_frame.groupby([temp_data_frame["District_Name"], temp_data_frame["Primary Type"]], agg={
            'total_case': vx.agg.count('Primary Type')}, sort=True)
        temp_data_frame = temp_data_frame.sort(
            ["District_Name", 'total_case'], ascending=False)

        # print (temp_data_frame.head(5))
        # temp_data_frame = temp_data_frame.groupby(["District_Name"]).head(5)
        return temp_data_frame.head(5)

    # police arrest filter
    def effective_pd_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        temp_data_frame = data_frame.copy()

        temp_data_frame = data_frame[["Primary Type", "Arrest"]]

        td1 = temp_data_frame[temp_data_frame["Arrest"] == True]
        td2 = temp_data_frame[temp_data_frame["Arrest"] == False]

        td1 = td1.groupby([temp_data_frame["Primary Type"], temp_data_frame["Arrest"]], agg={
            'Count': vx.agg.count('Primary Type')}, sort=True)
        td2 = td2.groupby([temp_data_frame["Primary Type"], temp_data_frame["Arrest"]], agg={
            'Count': vx.agg.count('Primary Type')}, sort=True)

        return td1, td2

    # holiday filter
    def holiday_crime_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        temp_data_frame = data_frame.copy()
        temp_data_frame = data_frame[["Primary Type", "Month"]]
        temp_data_frame = temp_data_frame.groupby([temp_data_frame["Month"]], agg={
            'Count': vx.agg.count('Month')}, sort=True)

        mean = temp_data_frame.mean("Count").tolist()
        return temp_data_frame, mean

    # weekday filter
    def weekday_crime_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        temp_data_frame = data_frame.copy()
        temp_data_frame = temp_data_frame[[
            "Primary Type", "District", "Day", "District_Name"]]

        temp_data_frame = temp_data_frame.groupby([temp_data_frame["Day"], temp_data_frame["District_Name"]], agg={
            'Count': vx.agg.count('Day')}, sort=True)

        # temp_data_frame = temp_data_frame.sort(
        #     ["Day"], ascending=False)

        mean = temp_data_frame.mean("Count").tolist()

        return temp_data_frame, mean

    def daytime_crime_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        temp_data_frame = data_frame.copy()
        temp_data_frame = temp_data_frame[["Time"]]

        temp_data_frame["Time"] = temp_data_frame["Time"].apply(
            lambda x: x[:2])
        temp_data_frame = temp_data_frame.groupby([temp_data_frame["Time"]], agg={
            'Count': vx.agg.count('Time')}, sort=True)
        mean = temp_data_frame.mean("Count").tolist()
        return temp_data_frame, mean

    def abuse_crime_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        temp_data_frame = data_frame.copy()

        temp_data_frame = data_frame[[
            "Primary Type", "District_Name", "Domestic"]]
        # slice for True domestic column
        temp_data_frame = temp_data_frame[temp_data_frame["Domestic"] == True]

        temp_data_frame = temp_data_frame.groupby([temp_data_frame["District_Name"], temp_data_frame["Domestic"]], agg={
            'Count': vx.agg.count('Domestic')}, sort=True)

        return temp_data_frame

    def state_crime_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        temp_data_frame = data_frame.copy()
        temp_data_frame = temp_data_frame[["Year"]]

        temp_data_frame = temp_data_frame.groupby([temp_data_frame["Year"]], agg={
            'Count': vx.agg.count('Year')})

        return temp_data_frame
