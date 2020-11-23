from typing import Callable, List

import fitz
import pandas as pd
from obsidianizer.pdf_tools import WORD_IN_PAGE
from obsidianizer.pdf_tools.annotations import ANNOTATION, extract_annotation


def get_words_data_frame(page: fitz.fitz.Page) -> pd.DataFrame:
    """Returns the word rectangles in dataframe format."""
    words = page.getText("words")
    return pd.DataFrame(words, columns=WORD_IN_PAGE._fields)


def get_blocks_summary(page: fitz.fitz.Page) -> pd.DataFrame:
    """Computes a sumary of the properties of the blocks
    df is the dataframe of individual words"""

    df = get_words_data_frame(page)
    agg_dict = {
        "word": list,
        "x0": "min",
        "y0": "min",
        "x1": "max",
        "y1": "max",
        "line_no": "max",
    }
    blocks_data = df.groupby("block_no").agg(agg_dict)
    blocks_data["n_words"] = blocks_data["word"].map(len)
    blocks_data["height"] = blocks_data["y1"] - blocks_data["y0"]
    blocks_data["width"] = blocks_data["x1"] - blocks_data["x0"]
    blocks_data["line_no"] = blocks_data["line_no"] + 1

    blocks_data = blocks_data.reset_index()
    # Add page number and block id
    blocks_data["page"] = page.number
    blocks_data["block_id"] = compute_block_id(blocks_data)
    blocks_data["block_absolute_y0"] = compute_block_absolute_y0(blocks_data)
    blocks_data = blocks_data.rename(columns={"word": "words", "line_no": "n_lines"})
    return blocks_data


def compute_block_id(df: pd.DataFrame):
    """Page number + block number with 4 positional 0s"""

    block_id = pd.Series(df["page"] * 1000 + df["block_no"], name="block_id")
    return block_id


def compute_block_absolute_y0(df: pd.DataFrame):
    """Page number + block number with 4 positional 0s"""

    block_absolute_y0 = pd.Series(
        df["page"] * 1000 + df["y0"], name="block_absolute_y0"
    )
    return block_absolute_y0


def extract_page_annotations(page: fitz.fitz.Page) -> pd.DataFrame:
    """Returns a pandas dataframe with the anotations and their rectanble"""
    annotation_list: List[ANNOTATION] = []
    annot = page.firstAnnot
    while annot is not None:
        annotation = extract_annotation(annot, page)
        annot = annot.next

        # If the annotation is a subcomment, just add them together
        if annotation.is_subcomment:
            annotation_list[-1] = append_subcomment_to_annotation(
                annotation_list[-1], annotation.annotation_text
            )
        else:
            annotation_list.append(annotation)

    annotations_df = pd.DataFrame(annotation_list, columns=ANNOTATION._fields)
    annotations_df["page"] = page.number
    annotations_df["block_absolute_y0"] = compute_block_absolute_y0(annotations_df)
    return annotations_df


def append_subcomment_to_annotation(annotation, annotation_text):
    # Make it mutable
    annotation = list(annotation)
    annotation[1] += f"\n{annotation_text}"
    new_annotation = ANNOTATION(*annotation)
    return new_annotation


def get_filtered_blocks(page: fitz.Page, block_filter: Callable) -> pd.DataFrame:
    """Iterates through the blocks of the given page and returns the ones for which
    block_filter returns true.
    """
    block_sumary = get_blocks_summary(page)

    subsection_blocks = []
    for i in range(block_sumary.shape[0]):
        block = block_sumary.iloc[i]

        if block_filter(block):
            subsection_blocks.append(i)

    if len(subsection_blocks):

        return block_sumary.iloc[subsection_blocks].reset_index()
    return pd.DataFrame()
