# City Promise Tracker

A Dash web application for tracking promises and commitments made by various entities across different cities. This interactive dashboard allows users to visualize the locations of these promises on a map, filter them based on status or city, and generate reports.

## Features

-   **Interactive Map:** Visualizes the geographical location of each promise.
-   **KPI Dashboard:** At-a-glance metrics for total, late, due, and on-time promises.
-   **Dynamic Filtering:** Query promises based on their status (e.g., "late", "due") or by city name.
-   **Detailed Results:** View detailed information for each promise that matches the query.
-   **Report Generation:** Download a professional HTML report of the filtered results.

## Project Structure

```
city-promise-tracker/
├── app.py              # Main Dash application file
├── promises.csv        # Data file containing the promises
├── requirements.txt    # Python dependencies
├── reports/            # Directory where generated reports are saved
└── README.md           # This file
```

## Setup and Usage

### Prerequisites

-   Python 3.6+
-   pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd city-promise-tracker
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Run the Dash app:**
    ```bash
    python app.py
    ```

2.  **Open your web browser** and navigate to `http://12.0.0.1:8050/`.

## Data Format

The `promises.csv` file contains the data for the application. It has the following columns:

-   `city`: The name of the city.
-   `promise_id`: A unique identifier for the promise.
-   `promise_description`: A description of the promise.
-   `due_date`: The date the promise is due.
-   `status`: The current status of the promise (`late`, `due`, `on-time`).
-   `latitude`: The latitude for the promise's location.
-   `longitude`: The longitude for the promise's location.
-   `category`: The category of the promise (e.g., `Roads`, `Water`).