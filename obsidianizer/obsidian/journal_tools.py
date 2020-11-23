import datetime as dt
from typing import Tuple

import pandas as pd
from obsidianizer.latex_tools.utils import DATETIME_FORMAT_MINUTE, str_to_date


def get_vault_df_from_journal(journal_df: pd.DataFrame, vault_path: str = "./Journal_vault/"):
    """Returns a dataframe containing a vault of the diaries.
    The filepath architecture is: YYYY/MM/DD/HH/
    TODO: Rethink the name and hierarchy of folders.
    """

    filepaths = []
    relative_keyword_paths = []
    keywords = []
    markdowns = []

    for i, row in journal_df.iterrows():
        entry_path, entry_filepath = get_journal_entry_filepath(row["datetime"])
        text = get_journal_entry_markdown(row)

        filepaths.append(vault_path + entry_path + entry_filepath)
        relative_keyword_paths.append(entry_path)
        keywords.append(entry_filepath.replace(".md", ""))
        markdowns.append(text)

    vault_dict = {
        "filepath": filepaths,
        "keyword": keywords,
        "relative_keyword_path": relative_keyword_paths,
        "markdown": markdowns,
    }

    vault_df = pd.DataFrame(vault_dict)

    return vault_df


def get_journal_entries_from_vault(vault_df: pd.DataFrame) -> pd.DataFrame:
    """It returns the data entries associated to the journal vault previously created"""

    entry_text_list = []
    datetime_list = []

    for i, row in vault_df.iterrows():
        datetimes_and_entries_text = row["markdown"].split("\n\n")
        for entry_text in datetimes_and_entries_text:
            sentences = entry_text.split("\n")

            datetime_list.append(sentences[0])
            entry_text_list.append("\n\n".join([sentences[i] for i in range(1, len(sentences))]))

    dictionary = {"datetime_str": datetime_list, "entry_text": entry_text_list}

    contents_df = pd.DataFrame(dictionary)
    contents_df["datetime"] = contents_df["datetime_str"].map(str_to_date)
    contents_df["date"] = contents_df["datetime"].map(lambda x: x.date())
    return contents_df


def get_journal_entry_filepath(datetime: dt.datetime) -> Tuple[str, str]:
    return f"{datetime.year}/{datetime.month}/{datetime.day}/", f"{datetime.hour}.md"


def get_journal_entry_markdown(entry: pd.Series) -> str:
    text = entry["datetime"].strftime(DATETIME_FORMAT_MINUTE) + "\n" + "\n".join(entry["sentences"])
    return text
