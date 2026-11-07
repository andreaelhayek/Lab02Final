# This creates the page for displaying data visualizations.

import json
import streamlit as st
import pandas as pd
import altair as alt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json

with open("data.json", "r") as file:
    json_data = json.load(file)

json_df = pd.DataFrame(json_data["data_points"])
json_df["week"] = range(1, len(json_df) + 1) 

st.header(json_data["chart_title"])

st.subheader("Static Chart: Study Hours for Every Week")

static_chart = alt.Chart(json_df).mark_bar().encode(
    x=alt.X("label", sort=None, title="Week"),
    y=alt.Y("value", title="Study Hours"),
).properties(title="Weekly Study Hours (All Weeks)")

st.altair_chart(static_chart, use_container_width=True)
 
st.subheader("Dynamic Chart: Choose How Many Weeks to Show")

if "prev_mean" not in st.session_state:
    st.session_state.prev_mean = None
    st.session_state.prev_median = None

weeks_shown = st.slider(
    "Number of weeks to display",
    min_value=3,
    max_value=len(json_df),
    value=len(json_df),
    key="weeks_shown",
)

subset = json_df.head(st.session_state.weeks_shown)

st.line_chart(subset, x="week", y="value")

mean_value = subset["value"].mean()
median_value = subset["value"].median()

if st.session_state.prev_mean is None:
    mean_delta = None
    median_delta = None
else:
    mean_delta = round(mean_value - st.session_state.prev_mean, 2)
    median_delta = round(median_value - st.session_state.prev_median, 2)

col1, col2 = st.columns(2)
col1.metric("Mean Study Hours", round(mean_value, 2), mean_delta)
col2.metric("Median Study Hours", round(median_value, 2), median_delta)

st.session_state.prev_mean = mean_value
st.session_state.prev_median = median_value


# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
st.divider()
st.header("Sleep Survey Results")
 
csv_df = pd.read_csv("data.csv")
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
 
if csv_df.empty:
    st.warning("No survey data yet. Go to the Survey page and add some responses!")
else:
    st.subheader("Static Chart: Average Sleep for Each Day")
 
    avg_df = csv_df.groupby("Category", as_index=False)["Value"].mean()
 
    csv_static_chart = alt.Chart(avg_df).mark_bar().encode(
        x=alt.X("Category", sort=days_order, title="Day of the Week"),
        y=alt.Y("Value", title="Average Hours of Sleep"),
    ).properties(title="Average Hours of Sleep by Day")
 
    st.altair_chart(csv_static_chart, use_container_width=True)
 
    st.subheader("Dynamic Chart: Choose Which Days to Show")
 
    if "csv_prev_mean" not in st.session_state:
        st.session_state.csv_prev_mean = None
        st.session_state.csv_prev_median = None
 
    available_days = [d for d in days_order if d in csv_df["Category"].values]
 
    st.multiselect(
        "Days to display",
        options=available_days,
        default=available_days,
        key="days_selected",
    )
 
    filtered_df = csv_df[csv_df["Category"].isin(st.session_state.days_selected)].copy()
 
    if filtered_df.empty:
        st.info("Select at least one day to see the chart.")
    else:
        filtered_df["entry"] = range(1, len(filtered_df) + 1)
        st.line_chart(filtered_df, x="entry", y="Value")
 
        csv_mean = filtered_df["Value"].mean()
        csv_median = filtered_df["Value"].median()
 
        if st.session_state.csv_prev_mean is None:
            csv_mean_delta = None
            csv_median_delta = None
        else:
            csv_mean_delta = round(csv_mean - st.session_state.csv_prev_mean, 2)
            csv_median_delta = round(csv_median - st.session_state.csv_prev_median, 2)
 
        col3, col4 = st.columns(2)
        col3.metric("Mean Hours of Sleep", round(csv_mean, 2), csv_mean_delta)
        col4.metric("Median Hours of Sleep", round(csv_median, 2), csv_median_delta)
 
        st.session_state.csv_prev_mean = csv_mean
        st.session_state.csv_prev_median = csv_median

