import pandas as pd
import plotly.graph_objects as go


def plot_exponential_barchart(
    df_exponential: pd.DataFrame, *args, **kwargs
) -> go.FigureWidget:
    fig = go.FigureWidget()

    fig.add_trace(
        go.Bar(
            # name="Control",
            x=df_exponential.index,
            y=df_exponential["loc_scale"].map(lambda x: x[0] + x[1]),
            error_y=dict(
                type="data",
                symmetric=False,
                array=df_exponential["loc_scale"].map(lambda x: x[1]),
                arrayminus=df_exponential["interval"].map(lambda x: x[0]),
            ),
        )
    )
    fig.update_layout(*args, **kwargs)
    # fig.update_layout(
    #     title="Plot Title",
    #     xaxis_title="X Axis Title",
    #     yaxis_title="X Axis Title",
    #     legend_title="Legend Title",
    #     font=dict(
    #         family="Courier New, monospace",
    #         size=18,
    #         color="RebeccaPurple"
    #     )
    return fig


def plot_n_words_barchart_barchart(
    df: pd.DataFrame, column: str = "n_words", *args, **kwargs
) -> go.FigureWidget:
    fig = go.FigureWidget()

    fig.add_trace(
        go.Bar(
            # name="Control",
            x=df.index,
            y=df[column],
        )
    )
    fig.update_layout(*args, **kwargs)
    # fig.update_layout(
    #     title="Plot Title",
    #     xaxis_title="X Axis Title",
    #     yaxis_title="X Axis Title",
    #     legend_title="Legend Title",
    #     font=dict(
    #         family="Courier New, monospace",
    #         size=18,
    #         color="RebeccaPurple"
    #     )
    return fig
