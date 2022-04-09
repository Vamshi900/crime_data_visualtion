import vaex as vx

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
    def create_selection(self, years=[2001, 2002, 2003], types=[], districts=[], months=[]):
        df = self.original_data_frame.copy()
        selection = None
        if len(years) > 0:
            df = df[df.Year.isin(years)]
            print(df.count())
        if len(districts) > 0:
            df = df[df.District.isin(districts)]
            print(df.count())
        if len(months) > 0:
            df = df[df.Month.isin(months)]
            print(df.count())
        if len(types) > 0:
            df = df[df["Primary Type"].isin(types)]
            print(df.count())

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
        return tp_df

    def table_filter(self, data_frame=None):
        if data_frame is None:
            data_frame = self.data_frame
        tp_df = data_frame.copy()
        tp_df['District_Name'] = tp_df.District.map(
            self.get_police_districts())
        tp_df = tp_df.groupby([tp_df["District_Name"], tp_df["Primary Type"]], agg={
            'total_case': vx.agg.count('Primary Type')})
        tp_df = tp_df.sort(["District_Name", 'total_case'], ascending=False)
        return tp_df
