import plotly.express as px
import plotly.graph_objects as go
from filter_values.filter_values import LoadFilterValues
import vaex as vx
from dash import dcc


class CreateFigures:
    def __init__(self, data_frame):
        pass

    def create_sunburst(self, tp_df):
        fig = px.sunburst(
            tp_df, path=['District_Name', 'Primary Type'], values='total_case')
        fig2 = go.Figure(go.Sunburst(
            labels=fig['data'][0]['labels'].tolist(),
            parents=fig['data'][0]['parents'].tolist(),
            ids=fig['data'][0]['ids'].tolist())
        )
        fig2.update_layout(margin=dict(t=10, l=0, r=0, b=10))
        return fig2

    # function to create ranking table
    def create_ranking(self, tp_df):
        return self.data_bars(tp_df, 'total_case')

    def data_bars(self, df, column):
        n_bins = 100
        bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
        ranges = [
            ((df[column].max() - df[column].min()) * i) + df[column].min()
            for i in bounds
        ]
        styles = []
        for i in range(1, len(bounds)):
            min_bound = ranges[i - 1]
            max_bound = ranges[i]
            max_bound_percentage = bounds[i] * 100
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (
                            i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'background': (
                    """
                        linear-gradient(90deg,
                        # 96dbfa 0%,
                        # 96dbfa {max_bound_percentage}%,
                        white {max_bound_percentage}%,
                        white 100%)
                    """.format(max_bound_percentage=max_bound_percentage)
                ),
                'paddingBottom': 2,
                'paddingTop': 2
            })

        return styles

    # year range slider
    def range_selector(self, years, selector_type, count=0):
        range_vals = []
        min = 0
        max = 0
        if selector_type == "years":
            range_vals.extend(years)
            min = range_vals[0]
            max = range_vals[-1]

        create_slider = dcc.RangeSlider(
            min,
            max,
            step=1,
            dots=False,
            marks=None,
            value=[min, max],
            tooltip={'placement': 'bottom', 'always_visible': True},
            id="id_slider_"+selector_type
        )

        return create_slider

    # dropdown menu options
    def dropdown_filter(self, filter_type, filter_vals):
        options = []
        vals = []
        placeholder = ""
        if filter_type == "crime_type":
            vals = filter_vals.get_crime_types()
            for val in vals:
                options.append({"label": val.capitalize(),
                               "value": val.capitalize()})
            placeholder = "Select crime types..."
        elif filter_type == "days_of_week":
            vals = filter_vals.get_days_of_week()
            for val in vals:
                options.append({"label": val.capitalize(),
                               "value": val.capitalize()})
            placeholder = "Select days of week..."
        elif filter_type == "arrest":
            options.append({"label": "Arrested", "value": True})
            options.append({"label": "Not Arrested", "value": False})
            placeholder = "Choose arrest types..."
        elif filter_type == "domestic":
            options.append({"label": "Domestic Crime", "value": True})
            options.append({"label": "Non Domestic", "value": False})
            placeholder = "Choose domestic/non-domestic types..."
        elif filter_type == "months":
            vals = filter_vals.get_months()
            for num, name in vals.items():
                options.append({"label": name, "value": num})
            placeholder = "Select months..."
        elif filter_type == "districts":
            vals = filter_vals.get_police_districts()
            for num, name in vals.items():
                options.append({"label": name, "value": num})
            placeholder = "Choose districts..."

        create_filter = dcc.Dropdown(
            options=options,
            multi=True,
            searchable=True,
            placeholder=placeholder,
            value=[],
            id="id_dropdown_"+filter_type
        )

        return create_filter
