import base64
import datetime as dt
import io
from typing import Any, Dict, List, Tuple

import dash_html_components as html
import fitz
import pandas as pd
import plotly.graph_objects as go
from obsidianizer.pdf_tools.page_plots import get_page_figure_widget
from pdf2image import convert_from_bytes

from utils import DATES_FORMAT, UPLOAD_DIRECTORY, filter_journal


def handle_input_range_dates(
    journal_df: pd.DataFrame, start_date: str, end_date: str
) -> Tuple[dt.date, dt.date]:
    if start_date is not None:
        start_date_object = dt.datetime.strptime(start_date, DATES_FORMAT).date()
    else:
        start_date_object = journal_df["date"].iloc[0]

    if end_date is not None:
        end_date_object = dt.datetime.strptime(end_date, DATES_FORMAT).date()
    else:
        end_date_object = journal_df["date"].iloc[-1]

    return start_date_object, end_date_object


def get_dash_table_data_and_columns(
    df: pd.DataFrame,
) -> Tuple[Any, List[Dict[str, Any]]]:
    """Helper function to convert dataframe to dash data and columns"""

    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("records")
    return data, columns


def get_entries_table(journal_df: pd.DataFrame, settings_dict: Dict[str, Any]):
    """Returns the data for the journal entries table"""
    df = filter_journal(journal_df, settings_dict)[
        ["datetime", "sentences", "n_sentences", "n_words"]
    ]

    data, columns = get_dash_table_data_and_columns(df)
    tooltip_data = [
        {
            column: {"value": str(value), "type": "markdown"}
            for column, value in row.items()
        }
        for row in df.to_dict("rows")
    ]

    return data, columns, tooltip_data


def save_file(filepath: str, content: str) -> None:
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(filepath, "wb") as fp:
        fp.write(base64.decodebytes(data))


def save_files(
    filenames: List[str], contents: List[str], filedir: str = UPLOAD_DIRECTORY
):
    """Saves files to the uploads folder directory"""
    if filenames is not None and contents is not None:
        for name, data in zip(filenames, contents):
            save_file(filedir + name, data)


def get_uploaded_pdf_outcome(filepath: str) -> int:
    """Reads the uploaded pdf"""
    doc = fitz.open(filepath)
    return doc


def pil_to_b64_dash(im):
    """Converts image to bytes format to render in page"""
    buffered = io.BytesIO()
    im.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return bytes("data:image/jpeg;base64,", encoding="utf-8") + img_str


def get_images_from_pdf(contents: str) -> List[str]:
    """Converts the pdf given as input to images"""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    images = convert_from_bytes(decoded)
    return images


def get_pdf_images_div(images, indexes=[1, 5]):
    """Returns image embedded in div to be rendered"""

    encoded = pil_to_b64_dash(images[indexes[0]])

    images_div = html.Div(
        [
            html.Img(
                src=encoded.decode("utf-8"), style={"height": "90%", "width": "90%"}
            ),
        ]
    )
    return images_div


def get_pages_pdf_figure(doc: List, indexes=[1, 5]):
    fig = get_page_figure_widget(
        doc[indexes[0]], include_rectangles=["blocks", "annotations"]
    )
    margin = go.layout.Margin(
        l=0,  # left margin
        r=0,  # right margin
        b=0,  # bottom margin
        t=0,  # top margin
    )
    fig.update_layout(margin=margin)
    return fig


def get_page_blocks(page: fitz.Page):
    """Returns table to plot with the blocks"""
    from obsidianizer.pdf_tools.pages import get_blocks_summary

    df = get_blocks_summary(page)[["block_id", "words"]]
    df["words"] = df["words"].map(lambda x: " ".join(x))
    return get_dash_table_data_and_columns(df)
