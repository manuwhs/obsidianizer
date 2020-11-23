import datetime as dt
from typing import Any, List

import fitz
import numpy as np
import pandas as pd
from obsidianizer.latex_tools.utils import DATETIME_FORMAT_MINUTE
from obsidianizer.pdf_tools import ANNOTATION

from .utils import _check_contain

ANNOTATION_DATETIME_FORMAT = "%Y%m%d%H%M%S"  # D:  20201031004215   Z00'00


def extract_annotation(annot: fitz.fitz.Annot, page: fitz.fitz.Page) -> ANNOTATION:
    """Extracts the highlighted text and annotation from the
    annotation object given as input.

    Args:
        annot ([type]): [description]

    Returns:
        ANNOTATION: Annotation of the text
    """
    annotated_text = annot.info["content"]
    author = annot.info["title"]

    words_on_page = page.getText("words")
    highlighted_text = _extract_annot(annot, words_on_page)

    is_subcomment = annot.vertices is None

    if is_subcomment:
        datetime = dt.datetime.strptime(annot.info["modDate"][2:-6], ANNOTATION_DATETIME_FORMAT)
    else:
        datetime = dt.datetime.strptime(annot.info["creationDate"][2:-6], ANNOTATION_DATETIME_FORMAT)
    annotated_text = "[" + datetime.strftime(DATETIME_FORMAT_MINUTE) + "] " + author + "\n" + annotated_text

    return ANNOTATION(highlighted_text, annotated_text, *annot.rect, is_subcomment, datetime, author)  # noqa


def _extract_annot(annot: fitz.fitz.Annot, words_on_page: List[Any]) -> str:
    """Extract words in a given highlight."""
    quad_points = annot.vertices

    if quad_points is None:
        return ""

    quad_count = int(len(quad_points) / 4)
    sentences = ["" for i in range(quad_count)]
    for i in range(quad_count):
        points = quad_points[i * 4 : i * 4 + 4]
        words = [w for w in words_on_page if _check_contain(fitz.Rect(w[:4]), points)]
        sentences[i] = " ".join(w[4] for w in words)
    sentence = " ".join(sentences)

    return sentence


def find_position_candidates_in_list(
    candidate_df: pd.DataFrame, list_df: pd.DataFrame, column: str = "block_absolute_y0"
) -> pd.DataFrame:
    """Returns a vector indicating for each element in candidate_df[column], where do they fit
    in the ordered list list_df[column]"""

    # Replicate the original list to compare by the number of elements we are gonna compare it with
    repeated_list_df = np.repeat(list_df[[column]].values, candidate_df.shape[0], axis=1)

    # Compare the values in candidate_df[column] with all the ones in list_df[column]
    # Finding where it falsl
    position_candidates_in_list = np.sum(np.array(candidate_df[column]) > repeated_list_df, axis=0) - 1

    return position_candidates_in_list
