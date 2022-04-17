# importing the requied modules
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import dash_bootstrap_components as dbc

# importing the components for the web application
from app_our import app, port, orig_data_frame
from datafilters.DataFilter import DataFilter
from figures.Figures import CreateFigures
from screens.navbar import Navbar

data_frame = orig_data_frame

filters = DataFilter(data_frame)

figures = CreateFigures(data_frame)

nav = Navbar()

# initilize ranking table
temp_data_frame = filters.create_ranking_filter(data_frame)
table_records_intitial, table_style_initial = figures.create_ranking_fig(
    temp_data_frame)


# dashboard layout code
body = html.Div([
    html.Div(
        className="row", children=[
            html.Div(className="Element", children=[
                html.Label("Select Years"),
                figures.range_selector_fig("years")
            ], style=dict(width="30%", background="#F9F9F9", marginLeft="40px", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Crime Type"),
                figures.dropdown_filter_fig("crime_type", filters)
            ], style=dict(width="20%", background="#F9F9F9", padding="15px")),
            html.Div(className="Element", id="filter_district", children=[
                html.Label("Select Districts"),
                figures.dropdown_filter_fig("districts", filters)
            ], style=dict(width="20%", background="#F9F9F9", padding="15px")),
            html.Div(className="Element", children=[
                html.Label("Select Month"),
                figures.dropdown_filter_fig("months", filters)
            ], style=dict(width="20%", background="#F9F9F9", padding="15px"))
        ], style=dict(display='flex',)
    ),

    html.Div(className="Maps", children=[
        html.Div(className="MainMap", id="main_map", children=[
            dcc.Markdown(id="count_display",
                         children=f"initial::{data_frame.count()}"),
            html.Div(children=[figures.pydeck_elevation_fig(filters.geo_plot_filter())], style=dict(
                width="46.5%", height="360px", position="absolute"), id="pydeck_map")
        ], style=dict(width="50%", height="400px", background="#F9F9F9", margin="10px", padding="15px")),
        html.Div(className="MainMap1", id="main_map_1", children=[
            html.Br(),
            html.Div(children=[figures.pydeck_scatter_fig(filters.geo_plot_filter())], style=dict(
                width="46.5%", height="360px", position="absolute"), id="pydeck_map_1")
        ], style=dict(width="50%", height="400px", background="#F9F9F9", margin="10px", padding="15px", paddingTop="30px")),
    ], style=dict(display='flex')),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(className="charts_table", children=[
        html.Div(className="Element", children=[
            dcc.Graph(id='sunburst_plot', figure=figures.sunburst_fig(
                filters.sunburst_filter(data_frame)))
        ], style=dict(width="40%", height="400px", background="#F9F9F9", margin="10px", padding="15px")),
        # html.Div(className="Element", children = [
        #     html.Div(className="ranking_table", children=[
        #             dash_table.DataTable(id='table1', columns=[
        #                     {'name': 'District', 'id': 'District_Name'},
        #                     {'name': 'Primary Type', 'id': 'Primary Type'},
        #                     {'name': 'Number of Cases', 'id': 'total_case'},
        #                 ],
        #                 data=table_records_intitial.to_dict('records'),
        #                 style_data_conditional=table_style_initial,
        #                 style_as_list_view=True,
        #             )
        #         ])
        # ], style=dict(width="60%", height="500px",background="#F9F9F9",margin="10px",padding="15px",overflowY="auto")),
    ], style=dict(display='flex')),

], style={'background': '#F9F9F9'})


#     # return (changed_count, figures.pydeck_elevation_fig(pydeck_data_frame), figures.pydeck_scatter_fig(pydeck_data_frame),
#     #         figures.sunburst_fig(sunburst_data_frame), table_data.to_dict("records"), table_style)


# callback for count display change when
# dropdown filter is changed
@app.callback(
    [Output("count_display", "children"),
     Output("pydeck_map", "children"),
     Output("pydeck_map_1", "children"),
     Output("sunburst_plot", "figure")],
    [Input("id_dropdown_crime_type", "value"),
        Input("id_slider_years", "value"),
        Input("filter_district", "value"),
        Input("id_dropdown_months", "value")]
)
def filter_count_display(types, years, districts, months):
    print(' i am in filter_count_display')
    if years is None:
        years = []
    if types is None:
        types = []
    if districts is None:
        districts = []
    if months is None:
        months = []

    # print old data frame count
    print("old data frame count: ", filters.data_frame.count())
    # filter data
    print('input selected years', years)
    print('input selected types', types)
    print('input selected districts', districts)
    print('input selected months', months)

    new_data_frame = filters.create_selection(years, types, districts, months)

    print('new_data_frame count', new_data_frame.count())

    # count display
    changed_count = "**Total Cases: {}**".format(str(new_data_frame.count()))

    # pydeck maps data and figures
    pydeck_data_frame = filters.geo_plot_filter(new_data_frame)
    pydeck_fig = figures.pydeck_elevation_fig(pydeck_data_frame)
    pydeck_fig_1 = figures.pydeck_scatter_fig(pydeck_data_frame)

    # sunburst data and figures
    sunburst_data_frame = filters.sunburst_filter(new_data_frame)
    sunburst_fig = figures.sunburst_fig(sunburst_data_frame)

    # ranking table data and figures
    ranking_data_frame = filters.create_ranking_filter(new_data_frame)
    ranking_table_records, ranking_table_style = figures.create_ranking_fig(
        ranking_data_frame)

    return [changed_count, pydeck_fig, pydeck_fig_1, sunburst_fig]
    return [changed_count]


def Dashboard():
    layout = html.Div([
        nav,
        body
    ])
    return layout


app.layout = Dashboard()

if __name__ == '__main__':
    app.run_server("0.0.0.0", port=port, debug=False)
