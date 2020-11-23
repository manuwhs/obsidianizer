import os
from typing import Any, Dict, List

import dash
import dash_bootstrap_components as dbc

# import dash_html_components as html
import flask
from dash.dependencies import Input, Output, State

from callback_funcs import (
    get_entries_table,
    get_images_from_pdf,
    get_page_blocks,
    get_pages_pdf_figure,
    get_pdf_images_div,
    get_uploaded_pdf_outcome,
    handle_input_range_dates,
    save_files,
)
from data_loading import (
    get_journal_df,
    initial_dashboard_charts,
    store_data_to_download,
)
from layout import get_layout
from layout_visualization import (
    create_n_grams_visualization,
    create_statistics_visualization,
)
from utils import UPLOAD_DIRECTORY, create_settings_dict, filter_journal

# from flask.helpers import send_file


# Load the data initially
journal_df = get_journal_df("../../knowledge/caca.txt")

pdf_dict: Dict[str, Any] = {"filepath": None, "fitz_doc": None, "images": None}
# Layout config
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Set up the server
server = flask.Flask("app")

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)
app.layout = get_layout(journal_df)


@app.callback(
    [
        Output("journal-entries-table", "data"),
        Output("journal-entries-table", "columns"),
        Output("journal-entries-table", "tooltip_data"),
        Output("daily-entries-n_words-chart", "figure"),
    ],
    [Input("load-data-button", "n_clicks")],
    [State("session-storage", "data")],
)
def render_basic_information(n_clicks: int, settings_dict: dict):

    if n_clicks is None or n_clicks == 0:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    data, columns, tooltip_data = get_entries_table(journal_df, settings_dict)
    fig = initial_dashboard_charts(journal_df, settings_dict)
    return (data, columns, tooltip_data, fig)


@app.callback(
    [
        Output("session-storage", "data"),
    ],
    [
        Input("journal-date-picker-range", "start_date"),
        Input("journal-date-picker-range", "end_date"),
        Input("languages-dropdown", "value"),
    ],
)
def update_settings_data(start_date: str, end_date: str, languages: List[str]):
    """It updates the settings so that they are shared everywhere"""
    start_date_object, end_date_object = handle_input_range_dates(
        journal_df, start_date, end_date
    )
    settings_dict = create_settings_dict(start_date_object, end_date_object, languages)
    return [settings_dict]


@app.callback(
    [Output("download-form", "action")],
    [Input("store-data-button", "n_clicks")],
    [State("session-storage", "data")],
)
def download_data(n_clicks: int, settings_dict: dict):

    if n_clicks is None or n_clicks == 0:
        return ["downloadable/caca.txt"]

    store_data_to_download(journal_df, settings_dict)
    return ["downloadable/caca.txt"]


@app.callback(
    [
        Output("pdf-session-storage", "data"),
        Output("pdf-range-slider", "max"),
        Output("pdf-range-slider", "value"),
        Output("pdf-range-slider", "marks"),
    ],
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def upload_file(uploaded_filepaths: List[str], uploaded_file_contents: List[str]):
    """Save uploaded files and regenerate the file list."""
    if uploaded_filepaths is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    save_files(uploaded_filepaths, uploaded_file_contents)

    pdf_settings = {"pdf_filepath": UPLOAD_DIRECTORY + uploaded_filepaths[0]}

    pdf_dict["fitz_doc"] = get_uploaded_pdf_outcome(pdf_settings["pdf_filepath"])
    pdf_dict["images"] = get_images_from_pdf(uploaded_file_contents[0])

    n_pages = len(pdf_dict["fitz_doc"])

    # Get the marks:
    def get_marks_dict(n_pages: int, n_max_markers: int = 20):
        import numpy as np

        marks_dict = {}
        if n_pages <= n_max_markers:
            for i in range(n_pages):
                marks_dict[i] = str(i + 1)
        else:
            marks = list(np.linspace(0, n_pages, n_max_markers, dtype=int))
            for i in marks:
                marks_dict[int(i)] = str(i + 1)
        return marks_dict

    marks_dict = get_marks_dict(n_pages)
    return (pdf_settings, n_pages - 1, [0, 0], marks_dict)


@app.callback(
    [
        Output("pdf-properties-div", "children"),
        Output("pdf-plotly-chart", "figure"),
        Output("pdf-images", "children"),
        Output("blocks-table", "data"),
        Output("blocks-table", "columns"),
    ],
    [Input("pdf-range-slider", "value")],
    [State("session-storage", "data")],
)
def render_pdf_pages(indexes: List[str], session_data):
    if indexes is None:
        return (
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
        )

    images_div = get_pdf_images_div(pdf_dict["images"], [indexes[-1]])

    pdf_fig = get_pages_pdf_figure(pdf_dict["fitz_doc"], [indexes[-1]])

    data_blocks, columns_blocks = get_page_blocks(pdf_dict["fitz_doc"][indexes[-1]])

    page_selected = 'You have selected page"{}"'.format(int(indexes[-1]) + 1)
    return page_selected, pdf_fig, images_div, data_blocks, columns_blocks


@app.callback(
    [
        Output("journal-statistics-n_words-tab", "children"),
        Output("journal-statistics-n_gramms-tab", "children"),
    ],
    [Input("journal-statistics-button", "n_clicks")],
    [State("session-storage", "data")],
)
def plot_statistics_journal(n_clicks: int, settings_dict: Dict):
    if n_clicks is None or n_clicks == 0:
        return dash.no_update, dash.no_update

    df = filter_journal(journal_df, settings_dict)

    children_tab_statistics = create_statistics_visualization(df)
    children_n_grams = create_n_grams_visualization(df)

    return [children_tab_statistics, children_n_grams]


# @app.callback(
#     Output('click-data', 'children'),
#     [Input("pdf-plotly-chart", 'clickData')])
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)

# def add_clicked_block():
#     pass:


@app.server.route("/downloadable/<path:path>")
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, "downloadable"), path)


if __name__ == "__main__":
    app.run_server(debug=True)
