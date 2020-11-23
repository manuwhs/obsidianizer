from typing import Dict

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go
from obsidianizer.journal.summary_plots import (
    get_amount_writing_figs,
    get_ngrams_figs,
    get_size_of_writings_per_entry_figs,
)


def get_visualization_tab_1():
    """Tab with the basic journal visualizations"""
    visualization_tab = dcc.Tab(
        label="Data visualization 1",
        value="visualization-1-tab",
        children=[
            dcc.Graph(id="daily-entries-n_words-chart"),
            get_base_table(id="journal-entries-table"),
        ],
    )
    return visualization_tab


def get_visualization_journal_statistics():

    statistics_tabs = dcc.Tabs(
        id="visualization-journal-sub-tabs",
        value="journal-statistics-n_words-tab",
        children=[
            dcc.Tab(
                id="journal-statistics-n_words-tab",
                label="Number of words ",
                value="visualization-2-xxtab",
                children=[],
            ),
            dcc.Tab(
                id="journal-statistics-n_gramms-tab",
                label="n_gramms analysis",
                value="visualization-2--XXXXtab",
                children=[],
            ),
        ],
    )

    """Tab with the basic analysis journal"""
    visualization_tab = dcc.Tab(
        id="journal-statistics-tab",
        label="Data visualization journal statistics",
        value="visualization-2-tab",
        children=[statistics_tabs],
    )
    return visualization_tab


def create_statistics_visualization(journal_df) -> html.Div:
    charts_dict = get_amount_writing_figs(journal_df)
    return charts_dict_to_dash_tabs(charts_dict)


def create_statistics_visualization_ammount(journal_df) -> html.Div:
    charts_dict = get_size_of_writings_per_entry_figs(journal_df)
    return charts_dict_to_dash_tabs(charts_dict)


def charts_dict_to_dash_tabs(charts_dict: Dict[str, go.FigureWidget]) -> html.Div:
    """Creates a dash division with the dictionary of charts"""
    charts_dict_keys = list(charts_dict.keys())
    div_children = [
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=charts_dict[charts_dict_keys[0]]), width=6),
                dbc.Col(dcc.Graph(figure=charts_dict[charts_dict_keys[1]]), width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=charts_dict[charts_dict_keys[2]]), width=6),
                dbc.Col(dcc.Graph(figure=charts_dict[charts_dict_keys[3]]), width=6),
            ]
        ),
    ]
    return html.Div(div_children)


def create_n_grams_visualization(journal_df) -> html.Div:
    charts_dict = get_ngrams_figs(journal_df, n_list=[2, 3, 4, 5])
    return charts_dict_to_dash_tabs(charts_dict)


def get_visualization_pdf():
    """Tab with the basic pdf visualizations"""

    visualization_tab = dcc.Tab(
        label="Pdf visualization",
        value="visualization-pdf",
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            dcc.Graph(id="pdf-plotly-chart"),
                            style={"padding-top": "62.5%"},
                        ),
                        width=4,
                    ),
                    dbc.Col([get_base_table(id="blocks-table")], width=3),
                    dbc.Col(html.Div(id="pdf-images"), width=4),
                ]
            ),
            # dbc.Row(dbc.Col([get_base_table(id="blocks-table")], width=11)),
        ],
    )
    return visualization_tab


def get_base_table(id: str):

    base_table = dash_table.DataTable(
        id=id,
        page_size=100,
        style_table={"height": "500px", "overflowY": "auto"},
        # fixed_rows={"headers": True},
        style_cell={
            "whiteSpace": "normal",
            "height": "auto",
            "overflow": "hidden",
            "textOverflow": "ellipsis",
            "maxWidth": 0,
            "textAlign": "left",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
        ],
        style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
        css=[
            {
                "selector": ".dash-spreadsheet td div",
                "rule": """
            line-height: 15px;
            max-height: 30px; min-height: 30px; height: 30px;
            display: block;
            overflow-y: hidden;
        """,
            },
            {"selector": ".row", "rule": "margin: 0"},
        ],
        tooltip_duration=None,
        filter_action="native",
    )
    return base_table
