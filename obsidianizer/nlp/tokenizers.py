from typing import List

import nltk

# import numpy as np
from nltk.tokenize import word_tokenize

nltk.download("punkt")


def nltk_tokenizer(sentences: List[str]) -> List[List[str]]:

    tokenized_sent = []
    for s in sentences:
        tokenized_sent.append(word_tokenize(s.lower()))

    return tokenized_sent
