import streamlit as st
import os
import pandas as pd
import seaborn as sns

st.title("Compare animal activity of two different years")


@st.cache_data
def upload_csv(filename, date_list=None):
    FILE_PATH = os.path.join(".","data", filename)
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
yr_1 = st.sidebar.selectbox("Pick one year", unique_image_yr)
yr_2 = st.sidebar.selectbox("Pick a comparison year", unique_image_yr)
selected_yr = [yr_1, yr_2]

sns.set_style("whitegrid")
g = sns.catplot(
    data=newdata_tidy.query(
        "anim_type in @selected_anim_types and image_yr in @selected_yr"
    ),
    kind="count",
    y="anim_spotted",
    col="anim_type",
    col_wrap=2,
    sharey=False,
    sharex=False,
    hue="image_yr",
    palette=["#8BADE1", "#740000"],
)
(
    g.set_axis_labels("Count of species spotted", "Species spotted").set_titles(
        "Animal type: {col_name}", weight="bold"
    )
)
sns.move_legend(g, "upper center", bbox_to_anchor=(0.5, 1.04), ncol=2, title=None)
st.pyplot(g)

st.sidebar.write("##")
st.sidebar.warning("This demo uses synthetic data")
