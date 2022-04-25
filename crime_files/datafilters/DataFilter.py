import imp
import vaex as vx
import pandas as pd
import numpy as np


class DataFilter:
    def __init__(self, data_frame):
        self.original_data_frame = data_frame
        self.data_frame = data_frame

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
        months = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]
        return months

    # get police districts
    def get_police_districts(self):
        districts = self.data_frame["District_Name"].unique()
        return sorted(districts)

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
    
    # method to get district name with highest crime count
    def get_district_crime_high(self): 
        # get the data frame
        df = self.data_frame.copy()
        # get the district name
        district_name = df["District_Name"].value_counts().index[0]
        return district_name
    
    # method to get percentage of arrest done
    def get_percentage_arrest(self):
        # get the data frame
        df = self.data_frame.copy()
        # get the arrest count
        arrest_count = df["Arrest"].value_counts()[1]
        # get the total count
        total_count = df.count()
        # get the percentage
        percentage = (arrest_count / total_count) * 100
        return percentage
    
    # method to get percentage of domestic crimes
    def get_percentage_domestic(self):
        # get the data frame
        df = self.data_frame.copy()
        # get the domestic crimes count
        domestic_count = df["Domestic"].value_counts()[1]
        # get the total count
        total_count = df.count()
        # get the percentage
        percentage = (domestic_count / total_count) * 100
        return percentage

    # primary data selection filter
    def create_selection(self, years=[2006 , 2022], types=[], districts=[], months=[]):
        df = self.original_data_frame.copy()
        selection = None
        if len(years) > 0:
            # array of years given start and end
            filter_years = [yr for yr in range(years[0], years[1]+1)]
            df = df[df["Year"].isin(filter_years)]
        if len(districts) > 0:
            print(districts)
            df = df[df["District_Name"].isin(districts)]
        if len(months) > 0:
            df = df[df.Month.isin(months)]
        if len(types) > 0:
            # convert types to uppper case
            types = [x.upper() for x in types]
            df = df[df["Primary Type"].isin(types)]
        self.update_data_frame(df)
        return df

    # sunburst figure filter
    def sunburst_filter(self, data_frame=None):
        # check for none
        if data_frame is None:
            data_frame = self.data_frame

        temp_data_frame = data_frame.copy()
        temp_data_frame = temp_data_frame[["Primary Type", "District_Name"]]

        temp_data_frame = temp_data_frame.groupby([temp_data_frame["District_Name"], temp_data_frame["Primary Type"]],
                                                  agg={'total_case': vx.agg.count('Primary Type')}, sort=True)
        temp_data_frame = temp_data_frame.sort(
            ["District_Name", "total_case"], ascending=False)
        temp_data_frame = temp_data_frame.to_pandas_df()
        temp_data_frame = temp_data_frame.groupby(["District_Name"]).head(5)
        vals = np.array(temp_data_frame["total_case"].tolist())
        labels = np.array(temp_data_frame["District_Name"].tolist())
        parents = np.array(temp_data_frame['Primary Type'].tolist())

        # todo: fix this pandas bug
        new_data_frame = pd.DataFrame(
            {'labels': labels, 'parents': parents, 'value': vals})
        return new_data_frame

    # geo plot filter
    def geo_plot_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        tp_df = data_frame.copy()
        # tp_df = tp_df['Latitude', 'Longitude']
        if tp_df.count() > 20000:
            tp_df = tp_df.sample(20000)
        # tpf = tp_df.sample(n=2, random_state=42)
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
        temp_data_frame = temp_data_frame.to_pandas_df()
        temp_data_frame = temp_data_frame.groupby(["District_Name"]).head(5)
        return temp_data_frame

    # police arrest filter
    def effective_pd_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        temp_data_frame = data_frame.copy()

        temp_data_frame = data_frame[["Primary Type", "Arrest", "District_Name"]]

        td1 = temp_data_frame[temp_data_frame["Arrest"] == 'Yes']
        td2 = temp_data_frame[temp_data_frame["Arrest"] == 'No']

        td1 = td1.groupby([temp_data_frame["Primary Type"], temp_data_frame["Arrest"],temp_data_frame["District_Name"]], agg={
            'Count': vx.agg.count('Primary Type')}, sort=True)
        td2 = td2.groupby([temp_data_frame["Primary Type"], temp_data_frame["Arrest"],temp_data_frame["District_Name"]], agg={
            'Count': vx.agg.count('Primary Type')}, sort=True)

        return td1, td2

    # holiday filter
    def holiday_crime_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        temp_data_frame = data_frame.copy()
        
        temp_data_frame = data_frame[["Primary Type", "Month", "District_Name"]]
        temp_data_frame = temp_data_frame.groupby([temp_data_frame["Month"],temp_data_frame["District_Name"]], agg={
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
        temp_data_frame = temp_data_frame[["Time","District_Name"]]

        temp_data_frame["Time"] = temp_data_frame["Time"].apply(
            lambda x: x[:2])
        temp_data_frame = temp_data_frame.groupby([temp_data_frame["Time"],temp_data_frame["District_Name"]], agg={
            'Count': vx.agg.count('Time')}, sort=True)
        mean = temp_data_frame.mean("Count").tolist()
        return temp_data_frame, mean

    def abuse_crime_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        temp_data_frame = data_frame.copy()

        temp_data_frame = data_frame[[
            "Primary Type", "District_Name", "Domestic","Month"]]
        # slice for True domestic column
        temp_data_frame = temp_data_frame[temp_data_frame["Domestic"] == 'Yes']

        temp_data_frame = temp_data_frame.groupby([temp_data_frame["District_Name"], temp_data_frame["Domestic"],temp_data_frame["Month"],], agg={
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
