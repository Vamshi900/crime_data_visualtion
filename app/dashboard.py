# importing the requied modules
from dash import html, dcc, Input, Output, dash_table
import pandas as pd

# importing the components for the web application
from app import app, port
from filters import FilterCreation
from geoplot import GeoPlot
from filter_values import LoadFilterValues
from figures import FiguresCreation
from navbar import Navbar


# loading the data frame
data_frame = pd.read_csv("processed_crimes_sample_5000.csv")

# initializing the filter object for passed data frame
filters = FilterCreation(data_frame)
# initializing the geoplot object for passed data frame
geo_plot = GeoPlot(data_frame)
# initializing the filter value object for passed data frame
df_slice_obj = LoadFilterValues(data_frame)
# initializing the figures object for passed data frame
figures = FiguresCreation(data_frame)

#initilize ranking table
table_records_intitial, table_style_initial = figures.create_ranking()


# setting up the navigation bar
nav = Navbar()

# dashboard layout code
body = html.Div([
    html.Div(
        className = "row", children = [
            html.Div(className="Element", children = [
                html.Label("Select Years"),
                filters.range_selector("years")
            ], style=dict(width="30%",background="#F9F9F9",marginLeft="40px",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Crime Type"),
                filters.dropdown_filter("crime_type")
            ], style=dict(width="20%",background="#F9F9F9",padding="15px")),
            html.Div(className="Element", id="filter_district", children = [
                html.Label("Select Districts"),
                filters.dropdown_filter("districts")
            ], style=dict(width="20%",background="#F9F9F9",padding="15px")),
            html.Div(className="Element", children = [
                html.Label("Select Month"),
                filters.dropdown_filter("months")
            ], style=dict(width="20%",background="#F9F9F9",padding="15px"))
        ], style=dict(display='flex',)
    ),

    html.Div(className="Maps", children = [
        html.Div(className="MainMap", id="main_map", children = [
            dcc.Markdown(id="count_display", children=[]),
            html.Div(children= [geo_plot.get_geoplot()], style=dict(width="46.5%", height="360px", position="absolute"), id="pydeck_map")
        ], style=dict(width="50%", height="400px",background="#F9F9F9",margin="10px",padding="15px")),
        html.Div(className="MainMap1", id="main_map_1", children = [
            html.Br(),
            html.Div(children= [geo_plot.get_geoScatterPlot()], style=dict(width="46.5%", height="360px", position="absolute"), id="pydeck_map_1")
        ], style=dict(width="50%", height="400px",background="#F9F9F9",margin="10px",padding="15px", paddingTop="30px")),
    ],style=dict(display='flex')),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(className = "charts_table", children=[
        html.Div(className="Element", children = [
            dcc.Graph(id='sunburst_plot', figure=figures.create_sunburst())
        ], style=dict(width="40%", height="400px",background="#F9F9F9",margin="10px",padding="15px")),
        html.Div(className="Element", children = [
            html.Div(className="ranking_table", children=[
                    dash_table.DataTable(id='table1', columns=[
                            {'name': 'District', 'id': 'District_Name'},
                            {'name': 'Primary Type', 'id': 'Primary Type'},
                            {'name': 'Number of Cases', 'id': 'total_case'},
                        ],
                        data=table_records_intitial.to_dict('records'),
                        style_data_conditional=table_style_initial,
                        style_as_list_view=True,
                    )
                ])
        ], style=dict(width="60%", height="500px",background="#F9F9F9",margin="10px",padding="15px",overflowY="auto")),
    ], style=dict(display='flex')),

], style = {'background': '#F9F9F9'})


def Dashboard():
    layout = html.Div([
        nav,
        body
    ])
    return layout


@app.callback(
    [Output("count_display", "children"),
     Output("pydeck_map", "children"),
     Output("pydeck_map_1", "children"),
     Output("sunburst_plot", "figure"),
     Output("table1", "data"),
     Output("table1", "style_data_conditional")],
    [Input("id_slider_years", "value"),
     Input("id_dropdown_crime_type", "value"),
     Input("id_dropdown_districts", "value"),
     Input("id_dropdown_months", "value")]
)
def filter_plots(years, types, districts, months):
    if years is None:
        years = []
    if types is None:
        types = []
    if districts is None:
        districts = []
    if months is None:
        months = []
    new_data_frame = df_slice_obj.create_selection(years, types, districts, months)
    new_geo_obj = GeoPlot(new_data_frame)
    changed_count = "**Total Cases: {}**".format(str(new_data_frame["ID"].count()))
    fig_obj = FiguresCreation(new_data_frame)
    table_data, table_style = fig_obj.create_ranking()
    return (changed_count, new_geo_obj.get_geoplot(), new_geo_obj.get_geoScatterPlot(), fig_obj.create_sunburst(), table_data.to_dict("records"), table_style)


app.layout = Dashboard()

if __name__ == '__main__':
    app.run_server("0.0.0.0",port=port,debug=False)


