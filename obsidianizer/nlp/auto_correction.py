import re
from typing import List

from spellchecker import SpellChecker

# from textblob import TextBlob


def get_misspelled_words(sentence: str) -> List[str]:
    """Returns the miss spelled words in the given text"""
    s = re.sub(r"[^\w\s]", "", sentence)
    wordlist = s.split()

    spell = SpellChecker()
    misspelled = list(spell.unknown(wordlist))

    return misspelled


def correct_sentence(sentence: str) -> str:
    """Returns sentence with automatically corrected words"""
    spell = SpellChecker()
    misspelled = get_misspelled_words(sentence)
    for misspelled_word in misspelled:
        sentence = sentence.replace(misspelled_word, spell.correction(misspelled_word))
    return sentence


def correct_sentences(sentences: List[str]) -> List[str]:
    """Returns sentences with automatically corrected words"""
    corrected_sentences = [correct_sentence(sent) for sent in sentences]
    return corrected_sentences


def get_candidates(misspelled: List[str]) -> List[str]:
    """Returns the possibly misspelled words"""
    spell = SpellChecker()
    candidates = [spell.correction(word) for word in misspelled]
    return candidates
