from typing import Dict

import ipywidgets as widgets
import plotly.graph_objects as go


def charts_dict_to_tab(charts_dict: Dict[str, go.FigureWidget]) -> widgets.Tab:
    names = [str(x) for x in charts_dict.keys()]
    charts = [charts_dict[name] for name in names]

    tab = widgets.Tab()
    tab.children = charts
    tab.titles = names
    return tab
