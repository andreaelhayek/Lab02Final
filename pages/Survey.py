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

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("Enter a day of the week (e.g., Monday):")
    value_input = st.text_input("How many hours of sleep did you get that night? (e.g., 7.5):")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        day = category_input.strip().title()
        if day not in DAYS:
            st.error("Please enter a valid day of the week (Monday - Sunday).")
        else:
            try:
                hours = float(value_input.strip())
                valid_number = 0 <= hours <= 24
            except ValueError:
                valid_number = False
 
            if not valid_number:
                st.error("Please enter the hours of sleep as a number between 0 and 24.")
            else:
                new_row = pd.DataFrame({"Category": [day], "Value": [hours]})
 
                if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
                    old_data = pd.read_csv("data.csv")
                    all_data = pd.concat([old_data, new_row], ignore_index=True)
                else:
                    all_data = new_row
 
                all_data.to_csv("data.csv", index=False)
 
                st.success("Your data has been submitted!")
                st.write(f"You entered: **Category:** {day}, **Value:** {hours}")
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
