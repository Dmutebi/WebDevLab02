# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")
csv_file = "data.csv"
# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Category", "Value"])
    df.to_csv(csv_file, index=False)
    
with st.form("study_form"):
    st.subheader("📚 Study Tracker")
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("Study:")
    value_input = st.number_input("How many hours did you study today?",
                                min_val=0.0,
                                max_val=24.0,
                                step=0.5,
                                help="Enter your total study time in hours"
                            )

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Study Hours")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.
        try:
                # Create new row of data
            new_row = pd.DataFrame([[category_input, value_input]], columns=["Category", "Value"])

                # Append new data to CSV
            new_row.to_csv(csv_file, mode='a', header=False, index=False)
        
            st.success("Your data has been submitted!")
            st.write(f"You entered: **Category:** {category_input}, **Value:** {value_input}")
        except Exception as e:
            st.error(f"❌ Error writing to CSV: {e}")

# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    try:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
    except Exception as e:
        st.error(f"Error reading 'data.csv': {e}")
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
