# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")


# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.
csv_data = None
if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    try:
        csv_data = pd.read_csv("data.csv")
        st.success("✅ CSV data loaded successfully.")
        st.dataframe(csv_data)  #NEW: Show loaded CSV data
    except Exception as e:
        st.error(f"Failed to read CSV file: {e}")
else:
    st.warning("CSV file not found or empty.")
    
json_data = None
if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
    try:
        with open("data.json", "r") as f:
            json_data = json.load(f)
        st.success("✅ JSON data loaded successfully.")
        st.json(json_data)  #NEW: Display raw JSON data for review
    except Exception as e:
        st.error(f"Failed to read JSON file: {e}")
else:
    st.warning("JSON file not found or empty.")

st.info("TODO: Add your data loading logic here.")


# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Static- Frequency of Categories")# CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.
if csv_data is not None:
    try:
        # Count occurrences of each category
        category_counts = csv_data["Category"].value_counts()

        # Bar chart
        st.bar_chart(category_counts)

        # Description
        st.caption("This static bar chart shows how frequently each category appears in the submitted survey data.")
    except Exception as e:
        st.error(f"Error creating static graph: {e}")
else:
    st.warning("Placeholder for your first graph.")


# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Dynamic") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.

if csv_data is not None:
    # Create session state for selected category
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = csv_data["Category"].iloc[0]

    # Dropdown to select category
    category_options = csv_data["Category"].unique()
    selected = st.selectbox("Choose a category to visualize its values", category_options)
    st.session_state.selected_category = selected  #NEW: Save selection in session state

    # Filter and convert value column to numeric
    filtered = csv_data[csv_data["Category"] == selected].copy()
    filtered["Value"] = pd.to_numeric(filtered["Value"], errors="coerce").dropna()

    # Line chart
    st.line_chart(filtered["Value"].reset_index(drop=True))

    st.caption(f"This dynamic line chart shows all numeric values submitted for category **{selected}**.")
else:
    st.warning("CSV data is required for this graph.")


# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Dynamic - Study Hours Filter (JSON)") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.
if json_data is not None and "study_log" in json_data:
    try:
        study_df = pd.DataFrame(json_data["study_log"])

    # Convert mood column to numeric just in case
        study_df["hours"] = pd.to_numeric(study_df["hours"], errors="coerce").fillna(0)

    # Create session state for threshold
        if "study_threshold" not in st.session_state:
            st.session_state.mood_threshold = 2

    # Slider to choose threshold
        min_hours = st.slider("Minimum study hours to display", 0, 10, st.session_state.study_threshold)  #NEW
        st.session_state.study_threshold = min_hours

    # Filter data
        filtered_study = study_df[study_df["hours"] >= min_hours]

    # Line chart
        st.line_chart(filtered_study.set_index("day"))

        st.caption(f"This dynamic chart shows days where you studied **{min_hours} hours or more** based on JSON study data.")
    except Exception as e:
        st.error(f"Error processing JSON study data: {e}")
else:
    st.warning("❌ JSON data not available or 'study_log' key is missing.")
