import copy
import datetime as dt
import glob
from typing import List

import pandas as pd
from obsidianizer.latex_tools.utils import (
    load_drafts_entries,
    save_cleaned_sentences_to_latex,
)


def write_to_disk_split_journals(
    journal_df: pd.DataFrame, path: str = "../../../knowledge/"
) -> None:
    """Splits the journal into its languages and writes different journal files for each language"""

    journal_language_groupby = split_journal_by_languages(journal_df)

    for language in journal_language_groupby.groups.keys():
        output_cleaned_journal = f"{path}/journal_split_language_{language}.txt"
        df_language = journal_language_groupby.get_group(language)
        _ = save_cleaned_sentences_to_latex(df_language, output_cleaned_journal)


def load_journals_splitted_languages(path: str = "../../../knowledge/") -> pd.DataFrame:
    """Loads and joins all the files related to language journal in the path"""
    journal_languages_list = []
    language_splits_filepaths = get_language_journal_splits_in_filedir(path)
    for filepath in language_splits_filepaths:
        journal_languages_list.append(load_drafts_entries(filepath))

    if len(journal_languages_list) == 0:
        return pd.DataFrame()
    else:
        return (
            pd.concat(journal_languages_list)
            .sort_values(by="datetime")
            .reset_index(drop=True)
        )


def get_language_journal_splits_in_filedir(path: str) -> List[str]:
    """Returns the list of the splited language files in the given filedir"""
    filepaths = [f for f in glob.glob(path + "**/*.txt", recursive=True)]
    language_splits_filepaths = [
        filepath for filepath in filepaths if "journal_split_language_" in filepath
    ]
    return language_splits_filepaths


def get_language_split_journal_file_path(path: str, language: str) -> str:
    """Bakes path for the journal split by language"""
    return f"{path}/journal_split_language_{language}.txt"


def split_journal_by_languages(
    journal_df: pd.DataFrame,
) -> pd.core.groupby.DataFrameGroupBy:  # Dict[str, pd.Index]:
    """It splits each entry in the journal into their languages groups and return
    a new journal with the expanded entries. The entries are expanded by adding minutes
    to the original variable. (Given that the original registration of time only has hours)
    """
    rows = [
        split_entry_by_language(journal_df.iloc[i]) for i in range(journal_df.shape[0])
    ]
    journal_df_split_languages = pd.concat(rows, axis=1).T.reset_index(drop=True)
    journal_language_groupby = journal_df_split_languages.groupby("language")

    return journal_language_groupby


def create_new_subset_sentences_row(
    row: pd.Series, start_index: int, end_index: int
) -> pd.Series:
    """Create new row with the subset of sentences.
    WARNING: It is going to add a number of minutes equal to the index of the sentence in order
    keep the order of the sentences across the new splits"""
    new_row = copy.deepcopy(row)
    new_row["datetime"] += dt.timedelta(minutes=start_index)
    new_row["sentences"] = [
        new_row["sentences"][j] for j in range(start_index, end_index)
    ]
    new_row["languages"] = [
        new_row["languages"][j] for j in range(start_index, end_index)
    ]
    new_row["entry_text"] = "\n\n".join(new_row["sentences"])
    new_row["language"] = new_row["languages"][0]

    return new_row


def split_entry_by_language(row: pd.Series) -> pd.DataFrame:
    """Splits the given diary entry into its languages"""

    new_rows_list = []

    n_sentences = len(row["languages"])
    aux_i = 0

    for i in range(1, n_sentences):
        if row["languages"][i] != row["languages"][aux_i]:
            new_row = create_new_subset_sentences_row(row, aux_i, i)
            new_rows_list.append(new_row)
            aux_i = i

    new_row = create_new_subset_sentences_row(row, aux_i, n_sentences)
    new_rows_list.append(new_row)

    if len(new_rows_list) > 0:
        return pd.concat(new_rows_list, axis=1)
    else:
        return pd.DataFrame(row)
