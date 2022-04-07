import pandas as pd

class LoadFilterValues:
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def get_crime_types(self):
        types = self.data_frame["Primary Type"].unique()
        return sorted(types)
    
    def get_days_of_week(self):
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        return days

    def get_months(self):
        months_map = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June",
                      7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
        return months_map
    
    def get_years(self):
        years = self.data_frame["Year"].unique()
        return sorted(years)

    
    def get_police_districts(self):
        district_map = {1  : "Central", 2  : "Wentworth", 3  : "Grand Crossing", 4  : "South Chicago", 5  : "Calumet",
                        6  : "Gresham", 7  : "Englewood", 8  : "Chicago Lawn", 9  : "Deering", 10  : "Ogden",
                        11  : "Harrison", 12  : "Near West", 14  : "Shakespeare", 15  : "Austin", 16  : "Jefferson Park",
                        17  : "Albany Park", 18  : "Near North", 19  : "Town Hall", 20  : "Lincoln", 22  : "Morgan Park",
                        24  : "Rogers Park", 25  : "Grand Central"}
        return district_map
    
    def create_selection(self, years=[2001, 2022], types=[], districts=[], months=[]):
        temp_data_frame = self.data_frame
        if len(years) > 0:
            temp_data_frame = temp_data_frame.loc[temp_data_frame["Year"].isin(year for year in range(years[0], years[1]+1))]
        if len(districts) > 0:
            temp_data_frame = temp_data_frame.loc[temp_data_frame["District"].isin(districts)]
        if len(months) > 0:
            temp_data_frame = temp_data_frame.loc[temp_data_frame["Month"].isin(months)]
        if len(types) > 0:
            temp_data_frame = temp_data_frame.loc[temp_data_frame["Primary Type"].isin(type.upper() for type in types)]
        return temp_data_frame