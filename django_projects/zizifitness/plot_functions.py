import pandas as pd
import numpy as np
import accounting.helper_functions as hf

from bokeh.plotting import figure, output_file, show 
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Legend
from bokeh.models.tools import HoverTool, WheelZoomTool, ResetTool, BoxZoomTool
from bokeh.palettes import Spectral
from bokeh.core.properties import value as bvalue


def plot_area_chart(xaxis, y, names, colors, title, xlabel='time', ylabel='', xaxis_type='datetime'):

    if len(y) != len(names):
        raise ValueError('The length of `names` has to be equal to the length of `y`!')

    tooltips = [(f'Date', '@xaxis{%F}')]
    for i in range(len(names)):
        tooltips.append((f'{names[i][0]}', f'@{names[i][0]}'))

    data = {'xaxis':xaxis}
    for i, name in enumerate(names):
        print(y[i])
        data[name[0]] = y[i]

    if xaxis_type=='datetime':
        p = figure(plot_width=600, plot_height=350, x_axis_type='datetime', title=title)
    else:
        p = figure(plot_width=600, plot_height=350, title=title)

    for i in range(len(y)):
        p.circle(x='xaxis', y=names[i][0], source=data, size = 15, color=colors[i])
        p.line(x='xaxis', y=names[i][0], source=data, line_width = 2, color=colors[i])

    p.left[0].formatter.use_scientific=False
    # p.xaxis.ticker=xaxis
    # p.xaxis.major_label_overrides={value:value.strftime('%b-%d') for value in xaxis}
    p.add_tools(HoverTool(tooltips=tooltips, formatters = {'@xaxis': 'datetime'}))

    script, div = components(p)
    return script, div
