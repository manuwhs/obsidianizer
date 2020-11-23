import calendar
from typing import Dict, List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from obsidianizer.journal.summary_statistics import get_exponential_estimation_dataset

# from obsidianizer.latex_tools.utils import get_filled_empty_days
from obsidianizer.nlp.text_cleanup import n_grams_function
from obsidianizer.plots.barcharts import (
    plot_exponential_barchart,
    plot_n_words_barchart_barchart,
)

"""High level plots for the summaries"""


def get_size_of_writings_per_entry_figs(df: pd.DataFrame) -> Dict[str, go.FigureWidget]:
    """Returns a set of charts with statistics regarding the frequency of writing"""

    journal_df = df.copy()

    journal_df["week_days"] = journal_df["datetime"].map(lambda x: x.weekday())
    journal_df["hour"] = journal_df["datetime"].map(lambda x: x.hour)
    journal_df["month"] = journal_df["datetime"].map(lambda x: x.month)
    journal_df["month_day"] = journal_df["datetime"].map(lambda x: x.day)

    # Get the by day of the week chart
    df_exponential = get_exponential_estimation_dataset(
        journal_df, groupby="week_days", column="n_words"
    )
    df_exponential.index = [calendar.day_name[i] for i in df_exponential.index]
    fig_weekdays = plot_exponential_barchart(df_exponential)
    fig_weekdays.update_layout(
        title="Average number of words written per entry by weekday",
        yaxis_title="Average number of words",
    )

    # Get the by hour of the day chart
    df_exponential = get_exponential_estimation_dataset(
        journal_df, groupby="hour", column="n_words"
    )
    fig_hours = plot_exponential_barchart(df_exponential)
    fig_hours.update_layout(
        title="Average number of words written per entry by hour",
        yaxis_title="Average number of words",
    )

    # Get the by month chart
    df_exponential = get_exponential_estimation_dataset(
        journal_df, groupby="month", column="n_words"
    )
    df_exponential.index = [calendar.month_name[i] for i in df_exponential.index]
    fig_month = plot_exponential_barchart(df_exponential)
    fig_month.update_layout(
        title="Average number of words written per entry by month",
        yaxis_title="Average number of words",
    )

    # Get the by month day chart
    df_exponential = get_exponential_estimation_dataset(
        journal_df, groupby="month_day", column="n_words"
    )
    fig_monthdays = plot_exponential_barchart(df_exponential)
    fig_monthdays.update_layout(
        title="Average number of words written per entry by day of the month",
        yaxis_title="Average number of words",
    )

    return {
        "weekdays": fig_weekdays,
        "hours": fig_hours,
        "month": fig_month,
        "monthdays": fig_monthdays,
    }


def get_amount_writing_figs(df: pd.DataFrame) -> Dict[str, go.FigureWidget]:
    """Returns a set of charts with statistics regarding the frequency of writing"""

    journal_df = df.copy()

    journal_df["week_days"] = journal_df["datetime"].map(lambda x: x.weekday())
    journal_df["hour"] = journal_df["datetime"].map(lambda x: x.hour)
    journal_df["month"] = journal_df["datetime"].map(lambda x: x.month)
    journal_df["month_day"] = journal_df["datetime"].map(lambda x: x.day)

    # Get the by day of the week chart
    df = journal_df.groupby("week_days").agg({"n_words": np.sum})
    df.index = [calendar.day_name[i] for i in df.index]
    fig_weekdays = plot_n_words_barchart_barchart(df)
    fig_weekdays.update_layout(
        title="Total number of words by weekday", yaxis_title="Number of words"
    )

    # Get the by hour of the day chart
    df = journal_df.groupby("hour").agg({"n_words": np.sum})
    fig_hours = plot_n_words_barchart_barchart(df)
    fig_hours.update_layout(
        title="Total number of words by hour", yaxis_title="Number of words"
    )

    # Get the by month chart
    df = journal_df.groupby("month").agg({"n_words": np.sum})
    df.index = [calendar.month_name[i] for i in df.index]
    fig_month = plot_n_words_barchart_barchart(df)
    fig_month.update_layout(
        title="Total number of words by month", yaxis_title="Number of words"
    )

    # Get the by month chart
    df = journal_df.groupby("month_day").agg({"n_words": np.sum})
    fig_monthdays = plot_n_words_barchart_barchart(df)
    fig_monthdays.update_layout(
        title="Total number of words by day of the month", yaxis_title="Number of words"
    )

    return {
        "weekdays": fig_weekdays,
        "hours": fig_hours,
        "month": fig_month,
        "monthdays": fig_monthdays,
    }


def get_ngrams_figs(
    journal_df: pd.DataFrame, n_list: List[int] = [2, 3], n_elements_show: int = 25
) -> Dict[str, go.FigureWidget]:
    """Returns Figures with the ngrams"""

    figs_dict = {}
    for n_ngrams in n_list:
        counted_ngrams = n_grams_function(
            journal_df.iloc[:1000], column="sentences", n=n_ngrams
        )
        counted_ngrams = counted_ngrams.iloc[:n_elements_show].sort_values("index")
        fig = go.FigureWidget(
            go.Bar(
                x=counted_ngrams["index"],
                y=counted_ngrams.index + "  ",
                orientation="h",
            )
        )
        fig.update_layout(height=n_elements_show * 30)
        figs_dict[str(n_ngrams)] = fig

    return figs_dict
