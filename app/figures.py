import plotly.express as px
import plotly.graph_objects as go
from filter_values import LoadFilterValues

class FiguresCreation:
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def create_sunburst(self):
        fil_obj = LoadFilterValues(self.data_frame)
        dist_name_map = fil_obj.get_police_districts()
        req_dist = self.data_frame["District"].unique()
        tp_df = self.data_frame
        tp_df["District_Name"] = tp_df["District"].map(dist_name_map)
        fig = px.sunburst(tp_df, path=['District_Name', 'Primary Type'], values='ID')
        fig2 =go.Figure(go.Sunburst(
                labels=fig['data'][0]['labels'].tolist(),
                parents=fig['data'][0]['parents'].tolist(),
                ids=fig['data'][0]['ids'].tolist())
                )
        fig2.update_layout(margin = dict(t=10, l=0, r=0, b=10))
        return fig2

    def create_ranking(self):
        fil_obj = LoadFilterValues(self.data_frame)
        dist_name_map = fil_obj.get_police_districts()
        tp_df = self.data_frame
        tp_df["District_Name"] = tp_df["District"].map(dist_name_map)
        tp_df = (tp_df[["District","Primary Type"]].groupby(["District","Primary Type"],as_index=False)
                 .agg(total_case=('Primary Type', 'count'))
                 .sort_values(["District",'total_case'], ascending=False))
        """
        last_district = None
        records = []
        for i, record in tp_df[['District', 'Primary Type', 'total_case']].iterrows():
            if record['District'] != last_district:
                last_district = record['District']
            else:
                record['District'] = ''  # don't repeat borough
        records.append(record)
        """
        return tp_df, data_bars(tp_df, 'total_case')

def data_bars(df, column):
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
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #96dbfa 0%,
                    #96dbfa {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'paddingBottom': 2,
            'paddingTop': 2
        })

    return styles