from typing import Callable, List

import pandas as pd
from deep_translator import GoogleTranslator
from langdetect import detect


def get_translator(language: str) -> Callable:
    """Returns a general translator into English"""
    translator = GoogleTranslator(source=language, target="en")

    def translate_to_eng(sentence: str) -> str:
        n_max_attempts = 20
        translation = ""

        for _ in range(n_max_attempts):
            try:
                translation = translator.translate(sentence)
                break
            except:  # noqa
                continue

        return translation

    return translate_to_eng


def get_journal_translator(language: str = "es") -> Callable:
    """Returns the journal translator for the journal example.
    The function returned by the closure is meant to be applied over
    the journal dataframe.
    """
    translator = get_translator(language)

    def translate_sentences(entry: pd.Series) -> List[str]:
        sentences, languages = entry["sentences"], entry["languages"]

        translations = []
        for i in range(len(languages)):
            if languages[i] == language:
                translation = translator([sentences[i]])
                translations.append(translation)
            else:
                translations.append(sentences[i])

        return translations

    return translate_sentences


def detect_language(sentences: List[str]) -> List[str]:
    """Returns a list with the detected language of each of the input sentences"""
    languages = []
    for sent in sentences:
        try:
            # TODO: strip non numeric
            language = detect(sent.lower())

            if language not in ["en", "es"]:
                # print(language, sent)
                language = "en"

        except:  # noqa
            language = "error"
            # print("This row throws and error:", sent)
        languages.append(language)
    return languages
