from bokeh.models import (
    GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxZoomTool,
    ResetTool, BoxSelectTool, HoverTool, ZoomInTool
)
from bokeh.layouts import layout
from bokeh.io import show, output_file
from bokeh.palettes import Category20
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from CONFIG import plot_Api_Key



def countryCoutns(data_country):
    source_country = ColumnDataSource(data_country)
    p = figure(x_range=data_country['country_names'], title="Wines by country")
    p.vbar(x='country_names', top='country_counts', width=0.9, source=source_country, legend="country_names",
           line_color='white', fill_color=factor_cmap('country_names', palette=Category20[15],
                                                      factors=data_country['country_names']))
    hover = HoverTool(tooltips=[
        ("Country", "@country_names"),
        ("Counts", "@country_counts"),
        ("Percentage", "@percentage"),
    ])

    p.add_tools(hover)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = max(data_country['country_counts']) + 10
    p.legend.orientation = "horizontal"
    p.legend.location = "top_right"
    return p


def wineTypesCount(data):
    source_type = ColumnDataSource(data)
    f = figure(x_range=data['variety_names'], title="Types of wines")
    f.vbar(x='variety_names', top='variety_counts', width=0.9, source=source_type, legend="variety_names",
           line_color='white', fill_color=factor_cmap('variety_names', palette=Category20[11],
                                                      factors=data['variety_names']))
    hover = HoverTool(tooltips=[
        ("Variety", "@variety_names"),
        ("Counts", "@variety_counts"),
        ("Percentage", "@percentage"),
    ])

    f.add_tools(hover)
    f.xgrid.grid_line_color = None
    f.y_range.start = 0
    f.y_range.end = max(data['variety_counts']) + 10
    f.legend.orientation = "horizontal"
    f.legend.location = "top_right"
    return f


def wineVintageCount(data):
    source_vintage = ColumnDataSource(data)
    g = figure(x_range=data['vintage_years'], title="Vintages")
    g.vbar(x='vintage_years', top='vintage_count', width=0.9, source=source_vintage, legend="vintage_years",
           line_color='white', fill_color=factor_cmap('vintage_years', palette=Category20[15],
                                                      factors=data['vintage_years']))
    hover = HoverTool(tooltips=[
        ("Vintage", "@vintage_years"),
        ("Counts", "@vintage_count"),
        ("Percentage", "@percentage"),

    ])

    g.add_tools(hover)
    g.xgrid.grid_line_color = None
    g.y_range.start = 0
    g.y_range.end = max(data['vintage_count']) + 10
    g.legend.orientation = "vertical"
    g.legend.location = "top_left"
    return g


def mapPlotter(data):
    map_options = GMapOptions(lat=41, lng=12, map_type="hybrid", zoom=4)

    plot = GMapPlot(
        x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, plot_width=1000, plot_height=500,
    )
    plot.title.text = "Our wines!"

    hover = HoverTool(tooltips=[
        ("Winery", "@Winery"),
        ("Wine Name", "@wineName"),
    ])

    # For GMaps to function, Google requires you obtain and enable an API key:
    #
    #     https://developers.google.com/maps/documentation/javascript/get-api-key
    #
    # Replace the value below with your personal API key:
    plot.api_key = plot_Api_Key

    source_map = ColumnDataSource(
        data
    )

    circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.5, line_color=None)
    plot.add_glyph(source_map, circle)

    plot.add_tools(hover, PanTool(), WheelZoomTool(), BoxSelectTool(), BoxZoomTool(), ResetTool(), ZoomInTool())
    # output_file("gmap_plot.html")
    # show(plot)
    return plot


def plot_all(data_country, data_types, data_vintage, data_maps):
    output_file("colormapped_bars.html")
    l = layout([
        [countryCoutns(data_country),
         wineTypesCount(data_types)],
        mapPlotter(data_maps),
        wineVintageCount(data_vintage)
    ], sizing_mode='stretch_both')
    show(l)

# show(p)
