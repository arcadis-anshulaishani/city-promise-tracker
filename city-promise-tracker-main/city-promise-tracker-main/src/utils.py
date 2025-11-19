"""
This module contains utility functions for the City Promise Tracker app.
"""

import folium
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
import llm

def create_map(data_df):
    """
    Creates a Folium map with markers for the given dataframe.

    Args:
        data_df (pd.DataFrame): A DataFrame with 'latitude' and 'longitude' columns.

    Returns:
        str: The HTML representation of the Folium map.
    """
    try:
        if data_df.empty:
            # Return a default map if the dataframe is empty
            return folium.Map(location=[39.8283, -98.5795], zoom_start=4).get_root().render()

        # Create a Folium map centered on the average location
        map_center = [data_df["latitude"].mean(), data_df["longitude"].mean()]
        m = folium.Map(location=map_center, zoom_start=6)

        for _, row in data_df.iterrows():
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=f"<b>{row['city']}</b><br>{row['promise_description']}",
                tooltip=row["city"],
            ).add_to(m)

        return m.get_root().render()
    except Exception as e:
        print(f"Error creating map: {e}")
        # Return a default map in case of an error
        return folium.Map(location=[39.8283, -98.5795], zoom_start=4).get_root().render()


def get_status_badge(status):
    """
    Returns a color-coded badge with an icon for a given status.

    Args:
        status (str): The status of the promise ('late', 'due', 'on-time').

    Returns:
        dbc.Badge: A Dash Bootstrap Components Badge.
    """
    try:
        status_map = {
            "late": {"color": "danger", "icon": "fas fa-exclamation-triangle", "text": "Late"},
            "due": {"color": "warning", "icon": "fas fa-hourglass-half", "text": "Due"},
            "on-time": {"color": "success", "icon": "fas fa-check-circle", "text": "On-Time"},
        }
        status_info = status_map.get(status, {"color": "secondary", "icon": "", "text": status})
        return dbc.Badge(
            [html.I(className=f"{status_info['icon']} me-1"), status_info["text"]],
            color=status_info["color"],
            className="ms-1",
        )
    except Exception as e:
        print(f"Error creating status badge: {e}")
        return dbc.Badge("Error", color="danger")


def filter_dataframe_from_query(data_df, query):
    """
    Filters the DataFrame based on a natural language query using the LLM.

    Args:
        data_df (pd.DataFrame): The DataFrame to filter.
        query (str): The natural language query.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    try:
        if not query:
            return data_df.copy()

        # Get structured query from LLM
        structured_query = llm.get_structured_query(query, data_df.columns.tolist())

        if not structured_query:
            return pd.DataFrame()  # Return empty df if LLM fails

        filtered_df = data_df.copy()

        for key, value in structured_query.items():
            if key in filtered_df.columns:
                if isinstance(value, dict):
                    # Handle date ranges or other complex queries
                    for op, val in value.items():
                        if op == "$gt":
                            filtered_df = filtered_df[filtered_df[key] > pd.to_datetime(val)]
                        elif op == "$lt":
                            filtered_df = filtered_df[filtered_df[key] < pd.to_datetime(val)]
                        elif op == "$eq":
                            filtered_df = filtered_df[filtered_df[key] == pd.to_datetime(val)]
                else:
                    # Handle simple string matching (case-insensitive)
                    filtered_df = filtered_df[
                        filtered_df[key].str.contains(value, case=False, na=False)
                    ]
        
        return filtered_df
    except Exception as e:
        print(f"Error filtering dataframe: {e}")
        return pd.DataFrame()
