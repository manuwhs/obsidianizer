import datetime as dt
from typing import Dict, List

import pandas as pd
from obsidianizer.nlp.text_cleanup import (
    filter_entries_by_date,
    filter_entries_by_languages,
)

# Download and Upload folders

UPLOAD_DIRECTORY = "./uploads/"
DOWNLOAD_DIRECTORY = "./downloads/"


DATES_FORMAT = "%Y-%m-%d"
DATES_FORMAT_DATEPICKER = "DD-MM-YYYY"


def optionizer_dropdown(options: List[str]) -> List[Dict[str, str]]:
    """Returns options for the dropdowns in Dash format"""
    return [{"label": x, "value": x} for x in options]


def create_settings_dict(start_date_object, end_date_object, languages):
    settings_dict = {}
    settings_dict["start_date"] = start_date_object
    settings_dict["end_date"] = end_date_object
    settings_dict["languages"] = languages
    return settings_dict


def filter_journal(journal_df: pd.DataFrame, options_dict: dict) -> pd.DataFrame:
    """Master function to filter the dataframe according to the inputs"""

    # Filter dates
    start_date = dt.datetime.strptime(options_dict["start_date"], DATES_FORMAT).date()
    end_date = dt.datetime.strptime(options_dict["end_date"], DATES_FORMAT).date()
    filter_entries_by_date(journal_df, start_date, end_date)

    # Filter languages
    journal_df = filter_entries_by_languages(journal_df, options_dict["languages"])

    return journal_df
