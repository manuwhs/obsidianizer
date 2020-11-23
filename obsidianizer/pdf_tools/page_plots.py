from typing import List, Optional

import fitz
import plotly.graph_objects as go
from ipywidgets import widgets
from obsidianizer.pdf_tools.pages import (
    extract_page_annotations,
    get_blocks_summary,
    get_words_data_frame,
)
from obsidianizer.pdf_tools.plots import get_rectangles_from_data_frame


def get_page_figure_widget(
    page: fitz.fitz.Page,
    include_rectangles=["words", "blocks", "annotations"],
    width: Optional[int] = None,
) -> go.FigureWidget:
    """Returns Figure Widget with the plotting as rectangles of:
    - Words
    - Blocks
    - Annotations
    """
    fig = go.FigureWidget()

    if "words" in include_rectangles:
        df_words = get_words_data_frame(page)
        words_rectangles = get_rectangles_from_data_frame(
            df_words, color="yellow", name="words", opacity=0.5
        )
        fig.add_trace(words_rectangles)

    if "blocks" in include_rectangles:
        block_sumary = get_blocks_summary(page)
        blocks_rectangles = get_rectangles_from_data_frame(
            block_sumary, color="blue", name="blocks", opacity=0.5
        )
        fig.add_trace(blocks_rectangles)

    if "annotations" in include_rectangles:
        annotations_df = extract_page_annotations(page)

        if not annotations_df.empty:
            anotations_rectangles = get_rectangles_from_data_frame(
                annotations_df, color="red", name="annotations", opacity=0.5
            )
            fig.add_trace(anotations_rectangles)

    if width is not None:
        fig.update_layout(width=width, height=width * 1.4142)

    return fig


def get_book_figure_widget(doc: List[fitz.fitz.Page], width=1000) -> widgets.Tab:
    """Returns tabs with the plotted pages of a document"""

    tab = widgets.Tab()

    pages_plots = []

    for page in doc:
        page_plot = get_page_figure_widget(page, width=width)
        pages_plots.append(page_plot)

    tab.children = pages_plots
    tab.titles = [str(i) for i in range(len(pages_plots))]
    return tab
