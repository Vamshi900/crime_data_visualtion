from filter_values import LoadFilterValues
from dash import dcc

class FilterCreation:
    def __init__(self, data_frame):
        self.filter_vals = LoadFilterValues(data_frame)

    def dropdown_filter(self, filter_type):
        options = []
        vals = []
        placeholder = ""
        if filter_type == "crime_type":
            vals = self.filter_vals.get_crime_types()
            for val in vals:
                options.append({"label":val.capitalize(), "value": val.capitalize()})
            placeholder = "Select crime types..."
        elif filter_type == "days_of_week":
            vals = self.filter_vals.get_days_of_week()
            for val in vals:
                options.append({"label":val.capitalize(), "value": val.capitalize()})
            placeholder = "Select days of week..."
        elif filter_type == "arrest":
            options.append({"label":"Arrested", "value":True})
            options.append({"label":"Not Arrested", "value":False})
            placeholder = "Choose arrest types..."
        elif filter_type == "domestic":
            options.append({"label":"Domestic Crime", "value":True})
            options.append({"label":"Non Domestic", "value":False})
            placeholder = "Choose domestic/non-domestic types..."
        elif filter_type == "months":
            vals = self.filter_vals.get_months()
            for num, name in vals.items():
                options.append({"label":name, "value":num})
            placeholder = "Select months..."
        elif filter_type == "districts":
            vals = self.filter_vals.get_police_districts()
            for num, name in vals.items():
                options.append({"label": name, "value": num})
            placeholder = "Choose districts..."
        
        create_filter = dcc.Dropdown(
            options = options,
            multi = True,
            searchable = True,
            placeholder = placeholder,
            value = [],
            id = "id_dropdown_"+filter_type
        )

        return create_filter

    def range_selector(self, selector_type, count=0):
        range_vals = []
        min = 0
        max = 0
        if selector_type == "years":
            range_vals.extend(self.filter_vals.get_years())
            min = range_vals[0]
            max = range_vals[-1]
        
        create_slider = dcc.RangeSlider(
            min,
            max,
            step=1,
            dots=False,
            marks=None,
            value = [min, max],
            tooltip = {'placement':'bottom', 'always_visible':True},
            id = "id_slider_"+selector_type
        )

        return create_slider