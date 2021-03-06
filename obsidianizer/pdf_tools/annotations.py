import datetime as dt
from enum import Enum
from typing import Any, List, Tuple

import fitz
import numpy as np
import pandas as pd
from obsidianizer.latex_tools.utils import DATETIME_FORMAT_MINUTE
from obsidianizer.pdf_tools import ANNOTATION, WORD_IN_PAGE

from .utils import _check_contain

ANNOTATION_DATETIME_FORMAT = (
    "%Y%m%d%H%M%S"  # D:  20201031004215   Z00'00 or D:  20190722235118+
)
ANNOTATION_DATETIME_LENGTH = (
    4 + 2 + 2 + 2 + 2 + 2
)  # Length to get just the time without timezone, there is too much diversity


class AnnotationExtractionMode(Enum):
    # It extracts only the highlighted text
    ONLY_HIGHLIGHTED_TEXT = 0

    # It extracts the entire block the highlighted text is in.
    ENTIRE_BLOCK = 1

    # It extracts all the lines the quote belongs to.
    ENTIRE_LINES = 2

    # It extracts the entire sentence the highlighted text is in.
    # (It searches for . or end of block.)
    SENTENCE = 3

    @classmethod
    def list(cls):
        return list(map(lambda c: (c.name, c.value), cls))


def str_annotation_datetime_to_dt(datetime_str: str) -> dt.datetime:
    datetime = dt.datetime.strptime(
        datetime_str[2 : 2 + ANNOTATION_DATETIME_LENGTH], ANNOTATION_DATETIME_FORMAT
    )
    return datetime


def extract_annotation(
    annot: fitz.fitz.Annot,
    page: fitz.fitz.Page,
    mode: AnnotationExtractionMode = AnnotationExtractionMode.ONLY_HIGHLIGHTED_TEXT,
) -> ANNOTATION:
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
    highlighted_text = _extract_annot(annot, words_on_page, mode)

    # Subcomments have no vertices, they are just in the main comment.
    is_subcomment = annot.vertices is None

    if is_subcomment:
        datetime = str_annotation_datetime_to_dt(annot.info["modDate"])
    else:
        datetime = str_annotation_datetime_to_dt(annot.info["creationDate"])

    annotated_text = (
        "["
        + datetime.strftime(DATETIME_FORMAT_MINUTE)
        + "] "
        + author
        + "\n"
        + annotated_text
    )

    return ANNOTATION(
        highlighted_text, annotated_text, *annot.rect, is_subcomment, datetime, author
    )  # noqa  # noqa


def _get_ith_word_box_coordinates(
    vertices: List[float], i: int
) -> Tuple[float, float, float, float]:  # noqa
    box_coordinates = vertices[i * 4 : i * 4 + 4]  # noqa
    return box_coordinates  # noqa


def _extract_annot(
    annot: fitz.fitz.Annot,
    words_on_page: List[Any],
    mode: AnnotationExtractionMode = AnnotationExtractionMode.ONLY_HIGHLIGHTED_TEXT,
) -> str:
    """Extracts words in a given highlight.
    Modes are:
        - "highlighted_text": It returns only the highlighted text.
        - "block": It returns the entire block the quote is in.

    The veannot.verticesrtices contain the different rectangles that the quote can be divided into
    and the words_on_page also contain the boxes of each word, combining both we just do
    overlapping of rectangles to know which words belong to the quote"""

    quad_points = annot.vertices
    if quad_points is None:
        return ""

    # Number of rectangles that make the quote
    quad_count = int(len(quad_points) / 4)

    if mode.value == AnnotationExtractionMode.ONLY_HIGHLIGHTED_TEXT.value:
        # For each rectangle that makes up the quote, find the overlapping words.
        sentences = ["" for i in range(quad_count)]
        for i in range(quad_count):
            box_coordinates = _get_ith_word_box_coordinates(quad_points, i)
            words = [
                w
                for w in words_on_page
                if _check_contain(fitz.Rect(w[:4]), box_coordinates)
            ]
            sentences[i] = " ".join(w[4] for w in words)
        sentence = " ".join(sentences)

    elif mode.value == AnnotationExtractionMode.ENTIRE_BLOCK.value:
        # For each rectangle that makes up the quote, find the overlapping blocks.
        blocks = []
        for i in range(quad_count):
            box_coordinates = _get_ith_word_box_coordinates(quad_points, i)
            words = [
                w
                for w in words_on_page
                if _check_contain(fitz.Rect(w[:4]), box_coordinates)
            ]
            blocks.extend([w[5] for w in words])

        # Compute the blocks here. We do not use the utils in pages due to circular dependencies
        # TODO: Maybe move up one function to avoid computing the groups per each qoute,
        # The benefit of having it here is so that the logic bifurcation on the mode only happens here.

        # Get the unique blocks the line belongs to
        words_df = pd.DataFrame(words_on_page, columns=WORD_IN_PAGE._fields)
        blocks_data = words_df.groupby("block_no").agg(
            {"word": lambda x: " ".join(list(x))}
        )
        unique_blocks = list(set(blocks))

        # Join the block the quote belongs to
        blocks_data_quote = blocks_data.loc[unique_blocks]["word"]
        sentence = "\n\n".join(blocks_data_quote)

    elif mode.value == AnnotationExtractionMode.ENTIRE_LINES.value:
        unique_block_line_df = _get_unique_line_block_in_annotation(
            quad_points, words_on_page
        )
        block_and_lines_data = _get_block_and_line_words_df(words_on_page)

        # Get the lines (from any block touched by the annotation)
        blocks_data_annotations = block_and_lines_data.loc[unique_block_line_df]["word"]
        sentence = " ".join(blocks_data_annotations)

    elif mode.value == AnnotationExtractionMode.SENTENCE.value:
        unique_block_line_df = _get_unique_line_block_in_annotation(
            quad_points, words_on_page
        )
        block_and_lines_data = _get_block_and_line_words_df(words_on_page)

        # Get the lines (from any block touched by the annotation)
        blocks_data_annotations = block_and_lines_data.loc[unique_block_line_df]["word"]
        sentence = " ".join(blocks_data_annotations)

        # Empty annotation
        if len(unique_block_line_df) == 0:
            return sentence

        first_setence_beginning_text = _get_beginning_of_sentence_text(
            unique_block_line_df, block_and_lines_data
        )
        last_setence_ending_text = _get_ending_of_sentence_text(
            unique_block_line_df, block_and_lines_data
        )
        # Now we look for the beginning of the first sentence and the end of the last.
        # These we find by finding a "." or the end of a block.
        sentence = (
            first_setence_beginning_text
            + " "
            + sentence
            + " "
            + last_setence_ending_text
        )
    return sentence.strip()


def _get_unique_line_block_in_annotation(
    quad_points: List[float], words_on_page: List[List[float]]
) -> pd.DataFrame:
    """Returs the (block,line) tuples that the quote belongs to."""
    # Number of rectangles that make the quote
    quad_count = int(len(quad_points) / 4)
    block_line_tuples = []
    # For each rectangle that makes up the quote, find the overlapping lines.
    for i in range(quad_count):
        box_coordinates = _get_ith_word_box_coordinates(quad_points, i)
        words = [
            w
            for w in words_on_page
            if _check_contain(fitz.Rect(w[:4]), box_coordinates)
        ]
        block_line_tuples.extend([(w[5], w[6]) for w in words])
    unique_block_line_df = pd.DataFrame(
        block_line_tuples, columns=["block_no", "line_no"]
    )
    unique_block_line_df["block_and_line"] = (
        unique_block_line_df["block_no"].map(str)
        + "__"
        + unique_block_line_df["line_no"].map(str)
    )
    unique_block_line_df = (
        unique_block_line_df.groupby(["block_and_line"]).first().index
    )
    return unique_block_line_df


def _get_block_and_line_words_df(words_on_page: List[Tuple[float]]) -> pd.DataFrame:
    """Return the unique blocks the line belongs to"""
    words_df = pd.DataFrame(words_on_page, columns=WORD_IN_PAGE._fields)
    words_df["block_and_line"] = (
        words_df["block_no"].map(str) + "__" + words_df["line_no"].map(str)
    )
    block_and_lines_data = words_df.groupby(["block_and_line"]).agg(
        {"word": lambda x: " ".join(list(x)), "line_no": "first", "block_no": "first"}
    )
    return block_and_lines_data


def _get_beginning_of_sentence_text(
    unique_block_line_df: pd.DataFrame, block_and_lines_data: pd.DataFrame
) -> str:
    """Returns all the text belonging to the first sentence which could be in the previous lines"""
    first_sentece_block, first_sentence_line = [
        int(x) for x in unique_block_line_df[0].split("__")
    ]
    first_setence_beginning_text = ""
    while True:
        if first_sentence_line > 0:  # Not at the top of the block
            first_sentence_line = first_sentence_line - 1
            index_value = f"{first_sentece_block}__{first_sentence_line}"

            # If it is a blank line, we also stop
            if index_value not in block_and_lines_data.index:
                break
            text_in_line = block_and_lines_data.loc[index_value]["word"]
            start_of_sentence_position_in_line = text_in_line.find(".")
            if start_of_sentence_position_in_line != -1:
                if start_of_sentence_position_in_line != len(text_in_line) - 1:
                    first_setence_beginning_text = (
                        text_in_line[start_of_sentence_position_in_line + 1 :]
                        + " "
                        + first_setence_beginning_text
                    )
                break
            else:
                first_setence_beginning_text = (
                    text_in_line + " " + first_setence_beginning_text
                )

        else:
            # Go up to the previous block just in case basically.
            if first_sentece_block > 0:
                first_sentece_block -= 1
                first_sentence_line = block_and_lines_data[
                    block_and_lines_data["block_no"] == first_sentece_block
                ]["line_no"].max()
                continue
            else:
                break

    return first_setence_beginning_text


def _get_ending_of_sentence_text(
    unique_block_line_df: pd.DataFrame, block_and_lines_data: pd.DataFrame
) -> str:
    """Returns all the text belonging to the last sentence which could be in the previous lines"""
    last_sentence_block, last_sentence_line = [
        int(x) for x in unique_block_line_df[0].split("__")
    ]
    last_setence_ending_text = ""

    while True:
        last_sentence_line = last_sentence_line + 1
        index_value = f"{last_sentence_block}__{last_sentence_line}"

        # If it is a blank line, we also stop (possibly end of block as well)
        # TODO: It seems that the blocks are not so reliable, and we should look only at the logic of line.
        # In the future we should simply compute 1000*block + line and do simple logic with it.
        if index_value not in block_and_lines_data.index:
            break
        text_in_line = block_and_lines_data.loc[index_value]["word"]
        end_of_sentence_position_in_line = text_in_line.find(".")
        if end_of_sentence_position_in_line != -1:
            last_setence_ending_text = (
                last_setence_ending_text
                + " "
                + text_in_line[: end_of_sentence_position_in_line + 1]
            )
            break
        else:
            last_setence_ending_text = last_setence_ending_text + " " + text_in_line

    return last_setence_ending_text


def find_position_candidates_in_list(
    candidate_df: pd.DataFrame, list_df: pd.DataFrame, column: str = "block_absolute_y0"
) -> pd.DataFrame:
    """Returns a vector indicating for each element in candidate_df[column], where do they fit
    in the ordered list list_df[column]"""

    # Replicate the original list to compare by the number of elements we are gonna compare it with
    repeated_list_df = np.repeat(
        list_df[[column]].values, candidate_df.shape[0], axis=1
    )

    # Compare the values in candidate_df[column] with all the ones in list_df[column]
    # Finding where it falsl
    position_candidates_in_list = (
        np.sum(np.array(candidate_df[column]) > repeated_list_df, axis=0) - 1
    )

    return position_candidates_in_list
