"""
This module handles the interaction with the Google Gemini LLM.
"""

import os
import json
from config import GEMINI_MODEL
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
try:
    api_key = os.environ.get("GEMINI_API_KEY")   

    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        raise ValueError("GEMINI_API_KEY not found or not set in .env file.")
    genai.configure(api_key=api_key)
except (AttributeError, ValueError) as e:
    # This will catch cases where the API key is missing or invalid
    raise SystemExit(f"Error configuring Gemini API: {e}") from e


def get_structured_query(query: str, df_columns: list) -> dict:
    """
    Uses Gemini to convert a natural language query into a structured
    JSON format for filtering a Pandas DataFrame.

    Args:
        query (str): The natural language query from the user.
        df_columns (list): The list of columns in the DataFrame.

    Returns:
        dict: A dictionary with filter conditions, or an empty dictionary if an error occurs.
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)

        # Create a detailed prompt for the model to generate a structured JSON response
        prompt = f"""
        You are a data analysis assistant. Your task is to convert a natural language query
        into a structured JSON object that can be used to filter a pandas DataFrame.

        The DataFrame has the following columns: {df_columns}

        The user's query is: "{query}"

        Based on the query, create a JSON object with keys corresponding to the
        DataFrame columns and values to filter by.

        - For the 'status' column, the possible values are 'late', 'due', and 'on-time'.
        - For columns like 'city', 'category', or 'promise_description', the value should be a string to search for.
        - If the query mentions a specific date or a date range for 'due_date', format it as a dictionary with operators like "$gt" (greater than), "$lt" (less than), or "$eq" (equal to).

        Example 1:
        Query: "show me all late promises in City A"
        JSON: {{"status": "late", "city": "City A"}}

        Example 2:
        Query: "what are the promises due after 2023"
        JSON: {{"due_date": {{"$gt": "2023-12-31"}}}}

        Example 3:
        Query: "search for infrastructure projects"
        JSON: {{"category": "Infrastructure"}}

        Now, generate the JSON for the user's query. Return only the JSON object.
        """

        # Generate content and handle potential API errors
        response = model.generate_content(prompt)
        
        # Clean the response to extract only the JSON part
        # The model might return the JSON wrapped in markdown
        json_response = response.text.strip().replace("```json", "").replace("```", "")
        
        # Parse the JSON string into a Python dictionary
        return json.loads(json_response)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from LLM response: {e}")
        print(f"LLM Response was: {response.text}")
        return {}
    except Exception as e:
        # This will catch other exceptions, such as connection errors or API issues
        print(f"An unexpected error occurred while processing the LLM response: {e}")
        return {}
