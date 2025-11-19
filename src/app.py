"""
Main application file for the City Promise Tracker.
"""

import dash
import pandas as pd
import dash_bootstrap_components as dbc
import os
from dotenv import load_dotenv
from layout import create_layout
from callbacks import register_callbacks

# Load environment variables from .env file
load_dotenv()

# --- Data Loading ---
try:
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    # Load promise data from CSV (located in parent directory)
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "promises.csv")
    df = pd.read_csv(csv_path)
    df["due_date"] = pd.to_datetime(df["due_date"])
except FileNotFoundError:
    print(
        "Error: promises.csv not found. Make sure the file is in the correct directory."
    )
    df = pd.DataFrame()  # Create empty dataframe to avoid further errors
except Exception as e:
    print(f"An error occurred while loading data: {e}")
    df = pd.DataFrame()

# --- Initialize the Dash app ---
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
)
app.title = "City Promise Tracker"
server = app.server

# --- KPI Calculations ---
try:
    if not df.empty:
        total_promises = len(df)
        late_promises = len(df[df["status"] == "late"])
        due_promises = len(df[df["status"] == "due"])
        on_time_promises = len(df[df["status"] == "on-time"])
    else:
        total_promises = late_promises = due_promises = on_time_promises = 0
except Exception as e:
    print(f"Error calculating KPIs: {e}")
    total_promises = late_promises = due_promises = on_time_promises = "Error"

# --- App Layout and Callbacks ---
app.layout = create_layout(
    total_promises, late_promises, due_promises, on_time_promises
)
register_callbacks(app, df)

# --- Main Execution Block ---
if __name__ == "__main__":
    app.run(debug=False)
