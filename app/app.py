# libaries
from dash import Dash, html, dcc, Input, Output, dash_table
# custom filters
from filters.filters import FilterCreation
# from filter_values.filter_values import LoadFilterValues
from filter_values.vaex_filtes import DataFilter
# geo plots
from figures.geoplot import GeoPlot
from figures.figures import CreateFigures
import vaex as vx
# figues import

# app init
app = Dash(__name__)

# intial data load
# data_frame = pd.read_csv("./dataset/processed_crimes_sample_5000.csv")
# read data frame using vaex
data_frame = vx.from_csv("./dataset/processed_crimes_sample_5000.csv")

filters = DataFilter(data_frame)

# safe update the data frame in the filters
DataFilter.update_data_frame(data_frame)


df_slice_obj = DataFilter.create_selection(data_frame)

figur
geo_plot = GeoPlot(data_frame)


# initilize ranking table
# table_records_intitial, table_style_initial = figures.create_ranking()

# dashboard layout code
app.layout = html.Div([
    html.H1('Criminalytics: A visual tool for crime analysis',
            style={
                'textAlign': 'center',
                'paddingTop': '10px',
                'color': '#323232'
            }
            ),

    dcc.Tabs(id="tabs", value='tab-1-visualization', children=[
        dcc.Tab(label='Crime Visualization in Chicago',
                value='tab-1-visualization'),
        dcc.Tab(label='Crime Prediction in Chicago', value='tab-2-prediction'),
    ], style=dict(padding="15px")),

    html.Div(
        className="row", children=[
            html.Div(className="Element", children=[
                html.Label("Select Years"),
                filters.range_selector("years")
            ], style=dict(width="25%", background="#F9F9F9", margin="10px", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Crime Type"),
                filters.dropdown_filter("crime_type")
            ], style=dict(width="25%", background="#F9F9F9", margin="10px", padding="15px")),
            html.Div(className="Element", id="filter_district", children=[
                html.Label("Select Districts"),
                filters.dropdown_filter("districts")
            ], style=dict(width="25%", background="#F9F9F9", margin="10px", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Month"),
                filters.dropdown_filter("months")
            ], style=dict(width="25%", background="#F9F9F9", margin="10px", padding="15px"))
        ], style=dict(display='flex')
    ),

    html.Div(className="Maps", children=[
        html.Div(className="MainMap", id="main_map", children=[
            dcc.Markdown(id="count_display", children=[]),
            html.Div(children=[geo_plot.get_geoplot()], style=dict(
                width="55.5%", height="360px", position="absolute"), id="pydeck_map")
        ], style=dict(width="60%", height="400px", background="#F9F9F9", margin="10px", padding="15px")),
        html.Div(className="Element", children=[
            dcc.Graph(id='sunburst_plot', figure=figures.create_sunburst())
        ], style=dict(width="40%", height="400px", background="#F9F9F9", margin="10px", padding="15px"))
    ], style=dict(display='flex')),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(className="charts_table", children=[
        html.Div(className="MinMap", id="min_map", children=[
            html.Div(className="MinMap", id="min_map1", children=[
                html.Label("Map2")
            ], style=dict(width="20%", height="380px", background="#F9F9F9", margin="10px", padding="15px")),
            html.Div(className="MinMap", id="min_map2", children=[
                html.Label("Map3")
            ], style=dict(width="20%", height="380px", background="#F9F9F9", margin="10px", padding="15px")),
            html.Div(className="MinMap", id="min_map3", children=[
                html.Label("Map4")
            ], style=dict(width="20%", height="380px", background="#F9F9F9", margin="10px", padding="15px"))
        ], style=dict(display='flex')),
        html.Div(className="Element", children=[
            # html.Div(className="ranking_table", children=[
            #     dash_table.DataTable(id='table1', columns=[
            #         {'name': 'District', 'id': 'District_Name'},
            #         {'name': 'Primary Type', 'id': 'Primary Type'},
            #         {'name': 'Number of Cases', 'id': 'total_case'},
            #     ],
            #         data=table_records_intitial.to_dict('records'),
            #         style_data_conditional=table_style_initial,
            #         style_as_list_view=True,
            #     )
            # ])
        ], style=dict(width="60%", height="500px", background="#F9F9F9", margin="10px", padding="15px", overflowY="auto")),
    ], style=dict(display='flex')),

], style={'background': '#F9F9F9'})


@app.callback(
    [Output("count_display", "children"),
     Output("pydeck_map", "children"),
     Output("sunburst_plot", "figure"),
     #  Output("table1", "data"),
     #  Output("table1", "style_data_conditional")],
     ],
    [Input("id_slider_years", "value"),
     Input("id_dropdown_crime_type", "value"),
     Input("id_dropdown_districts", "value"),
     Input("id_dropdown_months", "value")]
)
def load_pydeck_map_data(years, types, districts, months):
    if years is None:
        years = []
    if types is None:
        types = []
    if districts is None:
        districts = []
    if months is None:
        months = []
    new_data_frame = df_slice_obj.create_selection(
        years, types, districts, months)
    new_geo_obj = GeoPlot(new_data_frame)
    changed_count = "**Total Cases: {}**".format(
        str(new_data_frame["ID"].count()))
    fig_obj = FiguresCreation(new_data_frame)
    # table_data, table_style = fig_obj.create_ranking()
    return (changed_count, new_geo_obj.get_geoplot(), fig_obj.create_sunburst())


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=5000, debug=True)
