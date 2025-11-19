"""
This module contains the callback functions for the City Promise Tracker app.
"""

from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime
import markdown2
import os
from utils import create_map, get_status_badge, filter_dataframe_from_query
from report_templates import REPORT_CSS, REPORT_SEARCH_SCRIPT

def register_callbacks(app, df):
    """
    Registers all the callbacks for the application.

    Args:
        app (dash.Dash): The Dash application instance.
        df (pd.DataFrame): The DataFrame containing the promise data.
    """

    @app.callback(
        [Output("results-content", "children"),
         Output("record-count-display", "children")],
        [Input("show-results-button", "n_clicks"), Input("results-tabs", "active_tab")],
        [State("query-input", "value")],
    )
    def update_results_content(n_clicks, active_tab, query):
        """Renders the content for the active results tab and updates record count."""
        try:
            if n_clicks == 0 or df.empty:
                return html.P("Enter a query and click 'Show Results'."), ""

            filtered_df = filter_dataframe_from_query(df, query)
            record_count = len(filtered_df)

            if filtered_df.empty:
                return html.P("No results found for your query."), "No records matched your search criteria."

            record_count_message = f"{record_count} records matched your search criteria."

            if active_tab == "results-tab":
                results_children = []
                for _, row in filtered_df.iterrows():
                    results_children.append(
                        html.Div(
                            [
                                html.H5(f"{row['city']} - {row['category']}"),
                                html.P(f"Promise: {row['promise_description']}"),
                                html.P(f"Due: {row['due_date'].strftime('%Y-%m-%d')}"),
                                html.Div(["Status: ", get_status_badge(row["status"])]),
                            ],
                            style={
                                "border": "1px solid #ddd",
                                "padding": "10px",
                                "margin-bottom": "10px",
                                "border-radius": "5px",
                            },
                        )
                    )
                return results_children, record_count_message
            
            elif active_tab == "tabular-tab":
                desired_columns = ["city", "promise_description", "category", "due_date", "status"]
                
                # Ensure all desired columns exist in the filtered_df
                # If not, handle the error or skip missing columns
                existing_desired_columns = [col for col in desired_columns if col in filtered_df.columns]

                table_header = [
                    html.Thead(html.Tr([html.Th(col.replace('_', ' ').title()) for col in existing_desired_columns]))
                ]
                table_body = [
                    html.Tbody(
                        [
                            html.Tr(
                                [html.Td(filtered_df.iloc[i][col]) for col in existing_desired_columns]
                            )
                            for i in range(len(filtered_df))
                        ]
                    )
                ]
                return dbc.Table(table_header + table_body, bordered=True, striped=True, hover=True), record_count_message

            return html.P("Select a tab."), record_count_message
        except Exception as e:
            print(f"Error updating results content: {e}")
            return html.P("An error occurred while updating results."), ""

    @app.callback(
        [
            Output("map", "srcDoc"),
            Output("download-button", "disabled"),
            Output("chat-history-store", "data"),
        ],
        [Input("show-results-button", "n_clicks")],
        [State("query-input", "value"), State("chat-history-store", "data")],
    )
    def update_map_and_history(n_clicks, query, chat_history):
        """Updates the map, download button, and chat history."""
        try:
            if n_clicks == 0 or df.empty:
                return create_map(df), True, []

            # Update chat history
            if query:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                chat_history.append({"query": query, "timestamp": timestamp})

            filtered_df = filter_dataframe_from_query(df, query)
            map_html = create_map(filtered_df)
            download_disabled = filtered_df.empty

            return map_html, download_disabled, chat_history
        except Exception as e:
            print(f"Error updating map and history: {e}")
            return create_map(df), True, chat_history

    @app.callback(
        Output("chat-history-output", "children"),
        Input("chat-history-store", "data"),
    )
    def update_chat_history_display(chat_history):
        """Updates the visible chat history log."""
        try:
            if not chat_history:
                return [html.P("No queries yet.", className="text-muted")]

            history_elements = []
            for entry in reversed(chat_history):
                history_elements.append(
                    html.Div(
                        [
                            html.P(f"• {entry['query']}", className="mb-0"),
                            html.Span(
                                entry["timestamp"],
                                className="text-muted",
                                style={"fontSize": "0.8em"},
                            ),
                        ],
                        style={"marginBottom": "10px"},
                    )
                )
            return history_elements
        except Exception as e:
            print(f"Error updating chat history display: {e}")
            return [html.P("An error occurred while updating chat history.")]

    @app.callback(
        [Output("download-report", "data"), Output("alert-placeholder", "children")],
        Input("download-button", "n_clicks"),
        State("query-input", "value"),
        prevent_initial_call=True,
    )
    def generate_report(n_clicks, query):
        """Generates and serves a professional HTML report with search functionality."""
        try:
            # Filter dataframe using the same LLM-powered function
            filtered_df = filter_dataframe_from_query(df, query)

            if filtered_df.empty:
                return None, dbc.Alert(
                    "No data to generate report for the given query.",
                    color="warning",
                    dismissable=True,
                )

            # --- Generate Markdown Content ---
            md_content = ""
            for _, row in filtered_df.iterrows():
                md_content += f"<div class='report-item'>"
                md_content += f"<h2>{row['city']} - {row['category']}</h2>"
                md_content += f"<p><strong>Promise:</strong> {row['promise_description']}</p>"
                md_content += (
                    f"<p><strong>Due Date:</strong> {row['due_date'].strftime('%Y-%m-%d')}</p>"
                )
                md_content += f"<p><strong>Status:</strong> {row['status'].title()}</p>"
                md_content += f"</div><hr>"

            # --- Convert Markdown to HTML ---
            html_content = markdown2.markdown(
                md_content, extras=["tables", "fenced-code-blocks", "break-on-newline"]
            )

            # --- Create Full HTML Document ---
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filename = f"reports/city_promises_report_{timestamp}.html"

            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>City Promises Report</title>
                {REPORT_CSS}
                {REPORT_SEARCH_SCRIPT}
            </head>
            <body>
                <div class="report-container">
                    <div class="cover-page">
                        <h1>City Promises Report</h1>
                        <p>This report details the status of various city promises based on the query: '{query}'.</p>
                        <p>Generated on: {report_date}</p>
                    </div>
                    <div class="report-content">
                        <div class="search-bar">
                            <input type="text" id="searchInput" onkeyup="searchReport()" placeholder="Search for promises, cities, or statuses...">
                        </div>
                        <div id="report-content-items">
                            {html_content}
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """

            with open(filename, "w", encoding="utf-8") as f:
                f.write(full_html)

            alert_message = dbc.Alert(
                f"Report '{os.path.basename(filename)}' generated successfully!",
                color="success",
                dismissable=True,
            )

            return dcc.send_file(filename), alert_message
        except Exception as e:
            print(f"Error generating report: {e}")
            return None, dbc.Alert("An error occurred while generating the report.", color="danger", dismissable=True)
