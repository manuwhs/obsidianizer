import itertools
from typing import List, Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def get_rectangles_from_data_frame(
    df: pd.DataFrame,
    name: Optional[str],
    color: Optional[str] = "blue",
    opacity: Optional[float] = 0.5,
) -> go.Scatter:
    """Plots all the rectangles in the given dataframe with x0, x1, y0, y1 columns.

    Args:
        df (pd.DataFrame): [description]
        name (Optional[str]): [description]
        color (Optional[str], optional): [description]. Defaults to "blue".
        opacity (Optional[float], optional): [description]. Defaults to 0.5.

    Returns:
        go.Scatter: [description]
    """
    if df.empty:
        return go.Scatter()

    def get_x_values(row: pd.Series) -> List[float]:
        return [row["x0"], row["x1"], row["x1"], row["x0"], row["x0"], np.nan]

    def get_y_values(row) -> List[float]:
        return [row["y0"], row["y0"], row["y1"], row["y1"], row["y0"], np.nan]

    x_axis_values = df.apply(get_x_values, axis=1)
    y_axis_values = df.apply(get_y_values, axis=1)

    x_axis_values = list(itertools.chain(*x_axis_values))
    y_axis_values = list(itertools.chain(*y_axis_values))
    y_axis_values = np.array(y_axis_values) * -1

    scatter = go.Scatter(
        x=x_axis_values, y=y_axis_values, fill="toself", name=name, opacity=opacity
    )

    return scatter


def adjust_range_from_data_frame(fig: go.Figure, df: pd.DataFrame) -> None:
    """Set axes properties"""
    offset = 40
    fig.update_xaxes(range=[df["x0"].min() - offset, df["x1"].max() + offset])
    fig.update_yaxes(range=[df["y0"].min() - offset, df["y1"].max() + offset])
