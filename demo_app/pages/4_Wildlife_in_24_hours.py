import streamlit as st
import os
import pandas as pd
import seaborn as sns

st.title("Animal activity in 24 hours")


@st.cache_data
def upload_csv(filename, date_list=None):
    FILE_PATH = os.path.join(".", "data", filename)
    df = pd.read_csv(FILE_PATH, parse_dates=date_list)
    return df


cols_date = ["image_date", "date_time"]
newdata_tidy = upload_csv("synthetic_wildlife.csv", cols_date)

st.sidebar.info("Enter your preferences below")
unique_anim_type = sorted(newdata_tidy["anim_type"].unique())
selected_anim_types = st.sidebar.multiselect(
    "Select one or multiple animal types", unique_anim_type, unique_anim_type
)

unique_image_yr = sorted(newdata_tidy["image_yr"].unique())
selected_image_yr = st.sidebar.multiselect(
    "Select one or multiple years", unique_image_yr, unique_image_yr
)

df = (
    newdata_tidy.query(
        "anim_type in @selected_anim_types and image_yr in @selected_image_yr"
    )
    .groupby(["image_hr"])["anim_type"]
    .value_counts()
    .to_frame()
    .reset_index()
)

sns.set_style("ticks")
g = sns.relplot(
    data=df, x="image_hr", y="count", kind="line", hue="anim_type", style="anim_type"
)
(
    g.set_axis_labels("Hours", "Count of species spotted").ax.set_xticks(
        [0, 4, 8, 12, 16, 20, 24]
    )
)
sns.move_legend(g, "center right", bbox_to_anchor=(1.1, 0.55), title="Animal type")
st.pyplot(g)

st.sidebar.write("##")
st.sidebar.warning("This demo uses synthetic data")
