"""Set of functionalities that take the journals read from XXX and perform operations
"""


import pandas as pd
from obsidianizer.nlp.auto_correction import correct_sentences
from obsidianizer.nlp.text_cleanup import (
    lematize_sentences,
    stem_sentences,
    tokenize_sentences,
    word_count,
)
from obsidianizer.nlp.translation import detect_language, get_journal_translator


def get_sentences(df: pd.DataFrame) -> pd.DataFrame:
    """It processes the strings in the "entry_text" column containing the text to
    each diary entry and:
        - Divided it into sentences.
        - Counts the number of sentences.
        - Detects the language of every sentence.
    """
    journal_df = df.copy()
    journal_df["sentences"] = journal_df["entry_text"].apply(tokenize_sentences)
    journal_df["n_sentences"] = journal_df["sentences"].apply(len)
    journal_df = journal_df[journal_df["n_sentences"] > 0]

    journal_df["languages"] = journal_df["sentences"].map(detect_language)
    journal_df["n_words"] = journal_df["sentences"].map(word_count)

    return journal_df.reset_index(drop=True)


def get_translations(df: pd.DataFrame, language: str = "es") -> pd.DataFrame:
    """Translates the Spanish sentences in the dictionary"""
    journal_df = df.copy()
    journal_translator = get_journal_translator(language)
    journal_df["sentences_translated"] = journal_df[["sentences", "languages"]].apply(
        journal_translator, axis=1
    )

    return journal_df


def get_autocorrections(df: pd.DataFrame) -> pd.DataFrame:
    """Translates the Spanish sentences in the dictionary"""
    journal_df = df.copy()
    journal_df["autocorrected_sentences"] = journal_df["sentences_translated"].apply(
        correct_sentences
    )

    return journal_df


def get_lemmatizations(
    df: pd.DataFrame, column: str = "sentences_translated"
) -> pd.DataFrame:
    """Gets the lemmas of all the sentences"""
    journal_df = df.copy()
    journal_df["lematization"] = journal_df[column].apply(lematize_sentences)

    return journal_df


def get_stems(df: pd.DataFrame, column: str = "sentences_translated") -> pd.DataFrame:
    """Gets the stems of all the sentences"""
    journal_df = df.copy()
    journal_df["stemming"] = journal_df[column].apply(stem_sentences)

    return journal_df
