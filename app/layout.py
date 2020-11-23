import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from layout_forms import (
    get_data_finding_tab,
    get_data_selection_tab,
    get_pdf_processing_tab,
)
from layout_visualization import (
    get_visualization_journal_statistics,
    get_visualization_pdf,
    get_visualization_tab_1,
)


def get_layout(journal_df: pd.DataFrame):
    """Returns the main layout, it uses the loaded journal_df to initialize the values."""

    layout = html.Div(
        [  # Session data object
            dcc.Store(id="session-storage", storage_type="session"),
            dcc.Store(id="pdf-session-storage", storage_type="session"),
            dbc.Row(
                [
                    dbc.Col(html.Div([get_panel_tabs(journal_df)]), width=3),
                    dbc.Col(data_visualization_tabs(), width=9),
                ]
            ),
        ]
    )

    return layout


def get_panel_tabs(journal_df):

    panel_tabs = html.Div(
        [
            dcc.Tabs(
                id="form-tabs",
                value="data-selection-tab",
                children=[
                    get_data_selection_tab(journal_df),
                    get_data_finding_tab(),
                    get_pdf_processing_tab(),
                ],
            ),
        ]
    )
    return panel_tabs


def data_visualization_tabs():

    visualization_tabs = html.Div(
        [
            dcc.Tabs(
                id="data-visualization-tabs",
                value="visualization-1-tab",
                children=[
                    get_visualization_tab_1(),
                    get_visualization_journal_statistics(),
                    get_visualization_pdf(),
                ],
            ),
        ]
    )
    return visualization_tabs
