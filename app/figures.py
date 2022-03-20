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