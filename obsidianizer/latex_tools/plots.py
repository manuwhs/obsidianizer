import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .utils import get_filled_empty_days


def get_statistics_email_draft(df: pd.DataFrame) -> go.Figure:
    """Returns chart with basic statistics about the given text"""

    grouped_by_date = df.groupby("date").agg(
        {"datetime": "count", "entry_text": lambda x: len("".join(x)), "n_words": "sum"}
    )
    filled_dates = get_filled_empty_days(grouped_by_date)

    if filled_dates.empty:
        return go.Figure()

    column = "n_words"
    filled_dates["SMA_7_days"] = filled_dates[column].rolling(window=7).mean()

    # Create the charts
    fig = px.bar(filled_dates, x=filled_dates.index, y=[column])

    if filled_dates["SMA_7_days"].dropna().empty is not True:
        fig.add_trace(
            go.Scatter(
                x=filled_dates.index, y=filled_dates["SMA_7_days"], name="SMA_7_days"
            )
        )

    return fig
