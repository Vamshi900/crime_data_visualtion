import imp
import vaex as vx
import pandas as pd
import numpy as np

class DataFilter:
    def __init__(self, data_frame):
        self.data_frame = data_frame
        self.original_data_frame = data_frame
    
    def update_data_frame(self, data_frame):
        self.data_frame = data_frame
    
    def reset_data_frame(self):
        self.data_frame = self.original_data_frame.copy()
    
    def get_days_of_week(self):
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        return days

    def get_months(self):
        months_map = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June",
                      7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
        return months_map
    
    def get_police_districts(self):
        district_map = {1  : "Central", 2  : "Wentworth", 3  : "Grand Crossing", 4  : "South Chicago", 5  : "Calumet",
                        6  : "Gresham", 7  : "Englewood", 8  : "Chicago Lawn", 9  : "Deering", 10  : "Ogden",
                        11  : "Harrison", 12  : "Near West", 14  : "Shakespeare", 15  : "Austin", 16  : "Jefferson Park",
                        17  : "Albany Park", 18  : "Near North", 19  : "Town Hall", 20  : "Lincoln", 22  : "Morgan Park",
                        24  : "Rogers Park", 25  : "Grand Central"}
        return district_map
    
    def get_years(self):
        years = self.data_frame["Year"].unique()
        return sorted(years)
    
    def get_crime_types(self):
        types = self.data_frame["Primary Type"].unique()
        return sorted(types)    
    
    def create_selection(self, years=[2001, 2022], types=[], districts=[], months=[]):
        temp_data_frame = self.original_data_frame.copy()
        if len(years) > 0:
            temp_data_frame = temp_data_frame[temp_data_frame["Year"].isin([year for year in range(years[0], years[1]+1)])]
        if len(types) > 0:
            temp_data_frame = temp_data_frame[temp_data_frame["Primary Type"].isin(type.upper() for type in types)]
        if len(districts) > 0:
            temp_data_frame = temp_data_frame[temp_data_frame["District"].isin(districts)]
        if len(months) > 0:
            temp_data_frame = temp_data_frame[temp_data_frame["Month"].isin(months)]
        return temp_data_frame
    
    def sunburst_filter(self, data_frame):
        temp_data_frame = data_frame.copy()
        temp_data_frame["District_Name"] = temp_data_frame["District"].map(self.get_police_districts())
        # temp_data_frame = temp_data_frame.groupby([temp_data_frame["District_Name"],temp_data_frame["Primary Type"]],
        #                    agg={'total_case': vx.agg.count('Primary Type')})
        # temp_data_frame = temp_data_frame.sort(["District_Name","total_case"], ascending=False)
        temp_data_frame = (temp_data_frame[["District_Name","Primary Type"]].groupby(["District_Name","Primary Type"],as_index=False)
                 .agg(total_case=('Primary Type', 'count'))
                 .sort_values(["District_Name",'total_case'], ascending=False))
        temp_data_frame = temp_data_frame.groupby(["District_Name"]).head(5)
        vals = np.array(temp_data_frame["total_case"].tolist())
        labels = np.array(temp_data_frame["District_Name"].tolist())
        parents = np.array(temp_data_frame['Primary Type'].tolist())
        new_data_frame = pd.DataFrame({'labels': labels, 'parents': parents, 'values': vals})
        return new_data_frame
    
    def pydeck_plot_filter(self, data_frame):
        temp_data_frame = data_frame.copy()
        new_temp_df = temp_data_frame.replace({"District":self.get_police_districts()})
        true_false_map = {True:"Yes", False:"No"}
        new_temp_df.replace({"Arrest":true_false_map}, inplace=True)
        new_temp_df.replace({"Domestic":true_false_map}, inplace=True)
        return new_temp_df
    
    def effective_pd_filter(self, data_frame):
        temp_data_frame = data_frame[["ID","Year","Primary Type","Arrest"]]
        temp_data_frame_1 = temp_data_frame.groupby(["Primary Type","Arrest"]).size().to_frame(name="Count").reset_index()
        temp_data_frame_2 = temp_data_frame_1[temp_data_frame_1["Arrest"]==True]
        temp_data_frame_3 = temp_data_frame_1[temp_data_frame_1["Arrest"]==False]
        return temp_data_frame_2, temp_data_frame_3
    
    def holiday_crime_filter(self, data_frame):
        temp_data_frame = data_frame[["ID", "Primary Type", "Month"]]
        temp_data_frame_1 = temp_data_frame.groupby(["Month"]).size().to_frame(name="Count").reset_index()
        mean = temp_data_frame_1["Count"].mean()
        return temp_data_frame_1, mean
    
    def weekday_crime_filter(self, data_frame):
        temp_data_frame = data_frame[["Primary Type","District","Day"]]
        temp_data_frame_1 = temp_data_frame.groupby(["District","Day"]).size().to_frame(name="Count").reset_index()
        day_category = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        temp_data_frame_1["Day"] = pd.Categorical(temp_data_frame_1["Day"], categories = day_category)
        temp_data_frame_1 = temp_data_frame_1.sort_values(by="Day")
        temp_data_frame_1.replace({"District":self.get_police_districts()}, inplace=True)
        mean = temp_data_frame_1["Count"].mean()
        return temp_data_frame_1, mean
    
    def daytime_crime_filter(self, data_frame):
        temp_data_frame = data_frame[["Time","Primary Type"]]
        temp_data_frame_1 = temp_data_frame["Time"].groupby(pd.to_datetime(temp_data_frame["Time"]).dt.hour).count()
        temp_data_frame_2 = pd.DataFrame({'hour': temp_data_frame_1.index, 'Count': temp_data_frame_1.values})
        mean = temp_data_frame_2["Count"].mean()
        return temp_data_frame_2, mean
    
    def abuse_crime_filter(self, data_frame):
        temp_data_frame = data_frame[["Primary Type","District","Domestic"]]
        temp_data_frame.replace({"District":self.get_police_districts()}, inplace=True)
        temp_data_frame_1 = temp_data_frame.groupby(["District","Domestic"]).size().to_frame(name="Count").reset_index()
        temp_data_frame_2 = temp_data_frame_1[temp_data_frame_1["Domestic"]==True]
        return temp_data_frame_2
    
    def state_crime_filter(self, data_frame):
        temp_data_frame = data_frame[["ID","Year"]]
        temp_data_frame_1 = temp_data_frame.groupby(["Year"]).size().to_frame(name="Count").reset_index()
        return temp_data_frame_1
    
    def create_ranking_filter(self, data_frame):
        temp_data_frame = data_frame[["District","Primary Type"]]
        temp_data_frame["District_Name"] = temp_data_frame["District"].map(self.get_police_districts())
        # temp_data_frame = temp_data_frame.groupby([temp_data_frame["District_Name"], temp_data_frame["Primary Type"]], agg={
        #     'total_case': vx.agg.count('Primary Type')})
        # temp_data_frame = temp_data_frame.sort(["District_Name", 'total_case'], ascending=False)
        temp_data_frame = (temp_data_frame[["District_Name","Primary Type"]].groupby(["District_Name","Primary Type"],as_index=False)
                 .agg(total_case=('Primary Type', 'count'))
                 .sort_values(["District_Name",'total_case'], ascending=False))
        temp_data_frame = temp_data_frame.groupby(["District_Name"]).head(5)
        return temp_data_frame

