import datetime as dt
from typing import Tuple

import pandas as pd
import plotly.graph_objects as go
from obsidianizer.latex_tools.journal_processing import get_sentences
from obsidianizer.latex_tools.plots import get_statistics_email_draft
from obsidianizer.latex_tools.utils import (
    load_drafts_entries,
    save_cleaned_sentences_to_latex,
)

from utils import filter_journal


def get_journal_df(filepath: str) -> pd.DataFrame:

    journal_df = load_drafts_entries(filepath)
    journal_df = get_sentences(journal_df)

    return journal_df


def get_initial_date_range(
    journal_df: pd.DataFrame, last_n_days: int = 30
) -> Tuple[dt.date, dt.date]:
    """It returns the last n days dates."""
    end_date = journal_df["date"].iloc[-1]
    start_date = end_date + dt.timedelta(days=-last_n_days)
    return start_date, end_date


def initial_dashboard_charts(
    journal_df: pd.DataFrame, options_dict: dict
) -> go.FigureWidget:
    journal_df = filter_journal(journal_df, options_dict)
    fig = get_statistics_email_draft(journal_df)
    return fig


def store_data_to_download(journal_df: pd.DataFrame, options_dict: dict) -> None:
    journal_df = filter_journal(journal_df, options_dict)
    output_cleaned_journal = "./downloadable/caca.txt"
    _ = save_cleaned_sentences_to_latex(journal_df, output_cleaned_journal)
