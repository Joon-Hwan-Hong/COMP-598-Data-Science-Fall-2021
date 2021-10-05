#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python file to run the bokeh server on AWS.
example: http://3.23.151.142:8080/dropdown_graph?username=nyc&password=iheartnyc
"""

# header metadata
__author__ = 'Joon Hwan Hong'
__version__ = '1.0'
__maintainer__ = 'Joon Hwan Hong'
__email__ = 'joon.hong@mail.mcgill.ca'


# ================== Imports ==================


import json
from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Dropdown, Legend, LegendItem
from bokeh.models.tickers import SingleIntervalTicker


# ================== Functions ==================


# Authentication with URL Query
def check_access(curdoc):
    url_args = curdoc.session_context.request.arguments
    username = url_args.get('username')[0].decode('utf-8')  # normally a b'string'
    password = url_args.get('password')[0].decode('utf-8')

    if username != 'nyc':
        raise Exception('Incorrect Username or Password, raising Exception.')
    if password != 'iheartnyc':
        raise Exception('Incorrect Username or Password, raising Exception.')


# Hosting Data & GUI
def dropdown_update1(event):
    source_n = zip_dict[event.item]
    source.data = dict(colors=[color1, color2, color3], xs=xs, ys=[source_n, source.data['ys'][1], monthly_all])
    # update y axis
    plot.y_range.start = 0
    plot.y_range.end = max(max(source_n), max(source.data['ys'][1]), max(monthly_all))


def dropdown_update2(event):
    source_n = zip_dict[event.item]
    source.data = dict(colors=[color1, color2, color3], xs=xs, ys=[source.data['ys'][0], source_n, monthly_all])
    # update y axis
    plot.y_range.start = 0
    plot.y_range.end = max(max(source.data['ys'][0]), max(source_n), max(monthly_all))


# ================== Server ==================


# authenticate URL query
doc = curdoc()
doc.title = 'Response Time to Complaints'
check_access(doc)

# load pre-determined data
with open('data_loaded.json', 'r') as f:
    data_loaded = json.load(f)
tuple_zips = data_loaded[0]
zip_dict = data_loaded[1]
monthly_all = data_loaded[2]

# constant vars
color1 = '#228B22'
color2 = '#FF8C00'
color3 = '#1500C8'
xs = [[*range(0,12)], [*range(0,12)], [*range(0,12)]]
ys = [[0]*12, [0]*12, monthly_all]

# plot
source = ColumnDataSource(dict(colors=[color1, color2, color3], xs=xs, ys=ys, labels=['Zip1', 'Zip2', 'ALL 2020']))
plot = figure(x_range=(0, 12), x_axis_label='Months', y_axis_label='Average Duration (h)', title="Incident Durations")
plot.multi_line(xs='xs', ys='ys', line_color='colors', legend_group='labels', source=source)
plot.xaxis.ticker = SingleIntervalTicker(interval=1)
plot.xaxis.minor_tick_line_color = None
plot.y_range.start = 0

# dropdown UI
dropdown1 = Dropdown(label="Zipcode 1", button_type="success", menu=tuple_zips)
dropdown2 = Dropdown(label="Zipcode 2", button_type="warning", menu=tuple_zips)
dropdown1.on_click(dropdown_update1)
dropdown2.on_click(dropdown_update2)

# result
doc.add_root(column(dropdown1, dropdown2, plot))
