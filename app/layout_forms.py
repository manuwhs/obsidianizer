import datetime as dt
import itertools

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from data_loading import get_initial_date_range
from layout_visualization import get_base_table
from utils import DATES_FORMAT_DATEPICKER, optionizer_dropdown


def get_data_selection_tab(journal_df: pd.DataFrame) -> dcc.Tab:
    start_date, end_date = get_initial_date_range(journal_df)

    language_options = list(
        pd.Series(itertools.chain.from_iterable(journal_df["languages"])).unique()
    )
    language_options_dropdown = optionizer_dropdown(language_options)

    return dcc.Tab(
        label="Data selection",
        value="data-selection-tab",
        children=[
            dcc.Markdown("**Select Data Range**"),
            get_entries_selection_form(start_date, end_date),
            dcc.Markdown("**Select Languages**"),
            dcc.Dropdown(
                id="languages-dropdown",
                options=language_options_dropdown,
                value=["en"],
                multi=True,
            ),
            dcc.Markdown("** Click to load data **"),
            html.Button("Load data", id="load-data-button", n_clicks=0),
            html.Hr(),
            html.Button("Store data", id="store-data-button", n_clicks=0),
            html.Form(
                id="download-form",
                action="downloadable/caca.tex",
                method="get",
                children=[
                    html.Button(
                        className="button", type="submit", children=["download"]
                    )
                ],
            ),
        ],
    )


def get_data_finding_tab():
    return dcc.Tab(
        label="Data Findings",
        value="data-findings-tab",
        children=[
            html.Button(
                "Compute statistics", id="journal-statistics-button", n_clicks=0
            ),
        ],
    )


def get_pdf_processing_tab():

    return dcc.Tab(
        label="Pdf processing",
        value="pdf-processing-tab",
        children=[
            html.H2("Upload"),
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    ["Drag and drop or click to select a file to upload."]
                ),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                },
                multiple=True,
            ),
            html.Div(id="pdf-properties-div"),
            dcc.Markdown("**Select pages**"),
            html.Div(
                [
                    dcc.RangeSlider(
                        id="pdf-range-slider", min=0, max=0, step=1, value=[0, 0]
                    )
                ]
            ),
            dcc.Markdown("**Subsection blocks**"),
            get_base_table("chapters-table"),
        ],
    )


def get_entries_selection_form(start_date: dt.date, end_date: dt.date):
    selection_form = html.Div(
        [
            dcc.DatePickerRange(
                id="journal-date-picker-range",
                start_date=start_date,
                end_date=end_date,
                display_format=DATES_FORMAT_DATEPICKER,
            ),
        ]
    )
    return selection_form
