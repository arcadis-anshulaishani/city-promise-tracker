"""
This module contains the layout definition for the City Promise Tracker app.
"""

from dash import dcc, html
import dash_bootstrap_components as dbc


def create_layout(total_promises, late_promises, due_promises, on_time_promises):
    """
    Creates the layout for the Dash application.

    Args:
        total_promises (int): The total number of promises.
        late_promises (int): The number of late promises.
        due_promises (int): The number of due promises.
        on_time_promises (int): The number of on-time promises.

    Returns:
        dbc.Container: The layout of the application.
    """
    try:
        return dbc.Container(
            fluid=True,
            children=[
                dcc.Store(id="chat-history-store", data=[]),
                dcc.Download(id="download-report"),
                html.Div(
                    id="alert-placeholder",
                    style={
                        "position": "fixed",
                        "top": "10px",
                        "right": "10px",
                        "zIndex": "1050",
                    },
                ),
                # Title
                html.H1(
                    "CITY PROMISE TRACKER",
                    className="text-center text-uppercase p-3",
                    style={"color": "darkblue"},
                ),
                # KPI Cards
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.B(
                                            [
                                                html.I(
                                                    className="fas fa-list-check me-2",
                                                    style={"color": "#17a2b8"},
                                                ),
                                                "Total Promises",
                                            ]
                                        ),
                                        className="text-center",
                                    ),
                                    dbc.CardBody(
                                        f"{total_promises}", className="text-center h3"
                                    ),
                                ]
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.B(
                                            [
                                                html.I(
                                                    className="fas fa-exclamation-triangle me-2",
                                                    style={"color": "red"},
                                                ),
                                                "Late Promises",
                                            ]
                                        ),
                                        className="text-center",
                                    ),
                                    dbc.CardBody(
                                        f"{late_promises}",
                                        className="text-center h3 text-danger",
                                    ),
                                ]
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.B(
                                            [
                                                html.I(
                                                    className="fas fa-hourglass-half me-2",
                                                    style={"color": "orange"},
                                                ),
                                                "Promises Due",
                                            ]
                                        ),
                                        className="text-center",
                                    ),
                                    dbc.CardBody(
                                        f"{due_promises}",
                                        className="text-center h3 text-warning",
                                    ),
                                ]
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.B(
                                            [
                                                html.I(
                                                    className="fas fa-check-circle me-2",
                                                    style={"color": "green"},
                                                ),
                                                "On-Time Promises",
                                            ]
                                        ),
                                        className="text-center",
                                    ),
                                    dbc.CardBody(
                                        f"{on_time_promises}",
                                        className="text-center h3 text-success",
                                    ),
                                ]
                            )
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        # Left Panel
                        dbc.Col(
                            [
                                dcc.Textarea(
                                    id="query-input",
                                    placeholder="Ask about promises, e.g., 'late promises in City A' or 'infrastructure projects due next year'",
                                    style={"width": "100%", "height": 100},
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Button(
                                                ["🔍 Show Results"],
                                                id="show-results-button",
                                                n_clicks=0,
                                                style={
                                                    "background-color": "blue",
                                                    "color": "white",
                                                    "border": "none",
                                                    "padding": "10px 20px",
                                                    "border-radius": "5px",
                                                    "width": "100%",
                                                },
                                            ),
                                            width=6,
                                        ),
                                        dbc.Col(
                                            html.Button(
                                                [
                                                    html.I(
                                                        className="fas fa-download me-2"
                                                    ),
                                                    "Download",
                                                ],
                                                id="download-button",
                                                n_clicks=0,
                                                disabled=True,
                                                style={
                                                    "background-color": "#6c757d",
                                                    "color": "white",
                                                    "border": "none",
                                                    "padding": "10px 20px",
                                                    "border-radius": "5px",
                                                    "width": "100%",
                                                },
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    className="mt-2",
                                ),
                                html.Div(id="record-count-display", className="mt-2 mb-2 text-center"),
                                html.Hr(className="my-3"),
                                html.H4("Chat History"),
                                html.Div(
                                    id="chat-history-output",
                                    style={
                                        "height": "calc(100vh - 500px)",
                                        "overflow-y": "auto",
                                        "border": "1px solid #ddd",
                                        "padding": "10px",
                                        "border-radius": "5px",
                                    },
                                ),
                            ],
                            width=3,
                            style={
                                "border": "1px solid #ddd",
                                "padding": "20px",
                                "border-radius": "5px",
                            },
                        ),
                        # Middle Panel
                        dbc.Col(
                            [
                                html.H4("Locations"),
                                dbc.Spinner(
                                    html.Iframe(
                                        id="map",
                                        srcDoc=None,
                                        style={
                                            "width": "100%",
                                            "height": "calc(100vh - 250px)",
                                        },
                                    )
                                ),
                            ],
                            width=5,
                            style={
                                "border": "1px solid #ddd",
                                "padding": "20px",
                                "border-radius": "5px",
                            },
                        ),
                        # Right Panel
                        dbc.Col(
                            [
                                html.H4("Query Results"),
                                dbc.Tabs(
                                    [
                                        dbc.Tab(label="Results", tab_id="results-tab"),
                                        dbc.Tab(
                                            label="Tabular View", tab_id="tabular-tab"
                                        ),
                                    ],
                                    id="results-tabs",
                                    active_tab="results-tab",
                                ),
                                dbc.Spinner(
                                    html.Div(
                                        id="results-content",
                                        style={
                                            "height": "calc(100vh - 300px)",
                                            "overflow-y": "auto",
                                            "padding-top": "10px",
                                        },
                                    )
                                ),
                            ],
                            width=4,
                            style={
                                "border": "1px solid #ddd",
                                "padding": "20px",
                                "border-radius": "5px",
                            },
                        ),
                    ]
                ),
            ],
        )
    except Exception as e:
        print(f"Error creating layout: {e}")
        return html.Div("Error creating layout. Please check the logs.")
