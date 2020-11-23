from typing import Any, List

import pandas as pd

# from obsidianizer.pdf_tools.pages import extract_page_annotations, get_blocks_summary, get_words_data_frame


def is_int(value: Any) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def are_words_numeric(words: List[str]) -> bool:
    is_content_numeric = is_int("".join(words))
    return is_content_numeric


def is_ecce_hommo_subsection(block: pd.Series) -> bool:
    # It is usually just a number, but it might be understood as several individual ones.
    is_word_no_small_enough = len(block["words"]) < 5
    is_content_numeric = block["width"] < 20  # are_words_numeric(block["words"])
    # is_space_between_upper_and_lower_bound_small_enough =

    if is_word_no_small_enough and is_content_numeric:
        return True
    return False


def is_ecce_hommo_chapter(block: pd.Series) -> bool:
    # It is usually just a number, but it might be understood as several individual ones.

    is_at_top_page = block["y0"] < 200 and block.name < 2
    # is_space_between_upper_and_lower_bound_small_enough =

    is_bigger_font = block["height"] / block["n_lines"] > 16
    if is_at_top_page and is_bigger_font:
        return True
    return False
