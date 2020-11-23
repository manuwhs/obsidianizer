from typing import Any, Callable, List, Sequence

import fitz
import pandas as pd
from obsidianizer.pdf_tools.pages import extract_page_annotations, get_filtered_blocks


def iterate_function_over_file(filepath: str, function: Callable) -> Sequence[Any]:
    doc: fitz.fitz.Document = fitz.open(filepath)
    page: fitz.fitz.Page

    n_pages = len(doc)

    for i in range(255, n_pages):
        page = doc[i]
        # annot = page.firstAnnot
        # words = page.getText("words")

        print(f"**** PAGE {i} ****")
        words_in_page = page.getText("words")
        print(words_in_page)
        break

    return ["f"]


def get_book_filtered_blocks(
    book: List[fitz.Page], block_filter: Callable
) -> pd.DataFrame:
    """Returns the blocks across the pages which fullfill the given property"""
    all_subsections = [
        get_filtered_blocks(book[i], block_filter) for i in range(len(book))
    ]
    return pd.concat(all_subsections).reset_index(drop=True)


def extract_book_annotations(book: List[fitz.Page]) -> pd.DataFrame:
    """Returns the blocks across the pages which fullfill the given property"""
    all_annotatoins = [extract_page_annotations(book[i]) for i in range(len(book))]
    return pd.concat(all_annotatoins).reset_index(drop=True)
