import datetime as dt
from typing import List, Tuple

import pandas as pd
from TexSoup import TexSoup

DATETIME_FORMAT_HOUR = "%a, %d %b %Y %H"
DATETIME_FORMAT_MINUTE = "%a, %d %b %Y %H:%M"

LATEX_DOCUMENT_HEADER = """\\documentclass{article}
\\usepackage{geometry}
\\geometry{
    a4paper,
    total={160mm,255mm},
    left=35mm,
    top=20mm,
}
\\begin{document}
\\begin{itemize}

"""
LATEX_DOCUMENT_ENDING = """
\\end{itemize}
\\end{document}
"""


def preprocess_email_text(text: str) -> str:
    """The text returned by email has peculiarities to avoid"""

    # gmail adds \n at the end of every sentence (wrapped by gmail)
    sentences = text.split("\n\n")
    processed_sentences = []

    for sentence in sentences:
        processed_sentence = sentence.replace("\n", "")

        # Gmail adds the escape character to the minus somehow
        processed_sentence = processed_sentence.replace("\-", "-")  # noqa

        # Latex percertage escaping (first one just in case it was already escaped)
        escape_characters = ["%", "_", "#"]
        for char in escape_characters:
            processed_sentence = processed_sentence.replace(f"\{char}", char)  # noqa
            processed_sentence = processed_sentence.replace(char, f"\{char}")  # noqa

        processed_sentence = processed_sentence.strip()
        if len(processed_sentence) > 0:
            processed_sentences.append(processed_sentence)

    cleaned_text = "\n\n".join(processed_sentences)
    return cleaned_text


def parse_dated_comment_to_latex_item(text: str, datetime: dt.datetime) -> str:
    """Bakes the given text and date into an item entry of latex"""
    text = (
        r"\item ["
        + datetime.strftime(DATETIME_FORMAT_MINUTE)
        + "] \n"
        + preprocess_email_text(text)
        + "\n\n"
    )
    return text


def str_to_date(datetime_str: str) -> dt.datetime:
    """Parse string data to datetime"""

    try:
        datetime_dt = dt.datetime.strptime(datetime_str, DATETIME_FORMAT_MINUTE)
    except:  # noqa
        pass

    try:
        datetime_dt = dt.datetime.strptime(datetime_str, DATETIME_FORMAT_HOUR)
    except:  # noqa
        pass

    return datetime_dt


def load_drafts_entries(filepath: str) -> pd.DataFrame:
    """It loads and combines different text files with the draft text"""
    with open(filepath) as f:
        content = f.read().encode("utf-8").decode("utf-8")

    dates_str = []
    items_str = []
    soup = TexSoup(content)
    list_items = list(soup.find_all("item"))

    for item in list_items:
        # First text item is the date. From
        date_str = item.text[0]
        item_text = ""

        if len(item.text) > 1:
            item_text += "".join(item.text[1:])[2:]  # We remove the initial new line

        dates_str.append(date_str)
        items_str.append(item_text)

    dictionary = {"datetime_str": dates_str, "entry_text": items_str}

    contents_df = pd.DataFrame(dictionary)
    contents_df["datetime"] = contents_df["datetime_str"].map(str_to_date)
    contents_df["date"] = contents_df["datetime"].map(lambda x: x.date())
    return contents_df.reset_index(drop=True)


def save_cleaned_sentences_to_latex(df: pd.DataFrame, filepath: str) -> str:
    """It loads and combines different text files with the draft text.
    It does it based on the "sentences" and "datetime" columns.
    """
    df = df.copy()
    text = r"" + LATEX_DOCUMENT_HEADER

    df["latex_entry"] = df["sentences"].map(lambda x: "\n\n".join(x))
    for index, row in df.iterrows():
        text += parse_dated_comment_to_latex_item(row["latex_entry"], row["datetime"])

    text += LATEX_DOCUMENT_ENDING
    with open(filepath, mode="w") as f:
        f.write(text)

    return text


def get_filled_empty_days(df: pd.DataFrame) -> pd.DataFrame:
    """Returns version of the input dataframe which contains one row
    for each possible date between the index[0] and index[-1]
    """
    days_difference = df.index[-1] - df.index[0]
    all_dates = [
        df.index[0] + dt.timedelta(days=i) for i in range(days_difference.days)
    ]

    pd_all_dates = pd.DataFrame(index=all_dates)
    pd_all_dates = pd_all_dates.join(df).fillna(0)

    return pd_all_dates


def get_different_sentences_journals(
    journal_df: pd.DataFrame, journal_df_2: pd.DataFrame
) -> Tuple[List[int], List[int]]:
    """Find the different sentences between journals to know if the processing of
    the sentences and writing to disk is idempotent
    """
    weird_indices = []
    weird_sentence_within_index = []
    journal_df = journal_df.reset_index(drop=True)
    journal_df_2 = journal_df_2.reset_index(drop=True)
    for index, row in journal_df_2.iterrows():
        for i in range(len(row["sentences"])):
            if (
                i >= len(journal_df.iloc[index]["sentences"])
                or row["sentences"][i] != journal_df.iloc[index]["sentences"][i]
            ):
                weird_indices.append(index)
                weird_sentence_within_index.append(i)
                break
    return weird_indices, weird_sentence_within_index


def print_differences_in_journals(
    journal_df: pd.DataFrame, journal_df_2: pd.DataFrame
) -> Tuple[List[int], List[int]]:
    weird_indices, weird_sentence_within_index = get_different_sentences_journals(
        journal_df, journal_df_2
    )
    for i in range(len(weird_indices)):
        print(
            journal_df.iloc[weird_indices[i]]["sentences"][
                weird_sentence_within_index[i]
            ]
        )
        print("========")
        print(
            journal_df_2.iloc[weird_indices[i]]["sentences"][
                weird_sentence_within_index[i]
            ]
        )
        print("--- \n")
    return weird_indices, weird_sentence_within_index
