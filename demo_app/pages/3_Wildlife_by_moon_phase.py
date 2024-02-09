import streamlit as st
import os
import pandas as pd
import seaborn as sns

st.title("Animal activity by moon phase")


@st.cache_data
def upload_csv(filename, date_list=None):
    FILE_PATH = os.path.join(".","data", filename)
    df = pd.read_csv(FILE_PATH, parse_dates=date_list)
    return df


cols_date = ["image_date", "date_time"]
newdata_tidy = upload_csv("synthetic_wildlife.csv", cols_date)

st.sidebar.info("Enter your preferences below")
unique_anim_type = sorted(newdata_tidy["anim_type"].unique())
selected_anim_type = st.sidebar.radio("Pick an animal type", unique_anim_type)

unique_image_yr = sorted(newdata_tidy["image_yr"].unique())
selected_image_yr = st.sidebar.multiselect(
    "Select one or multiple years", unique_image_yr, unique_image_yr
)

df = (
    newdata_tidy.query(
        "anim_type in @selected_anim_type and image_yr in @selected_image_yr"
    )
    .groupby("moon_phase")["anim_spotted"]
    .value_counts()
    .to_frame()
    .reset_index()
)


if st.checkbox("Show dataframe"):
    df_styled = df.rename(
        columns={
            "moon_phase": "Moon phase",
            "anim_spotted": "Animal spotted",
            "count": "Count",
        }
    )
    st.dataframe(df_styled)

if st.checkbox("Show heatmap"):
    df_crosstab = (
        pd.crosstab(
            df["anim_spotted"], df["moon_phase"], values=df["count"], aggfunc="sum"
        )
        .fillna(0)
        .astype(int)
    )
    hm = sns.heatmap(df_crosstab, annot=True, fmt="d", cmap="YlGnBu", linewidths=0.15)
    hm.set(xlabel="", ylabel="")
    hm.xaxis.tick_top()
    hm.set_xticklabels(
        hm.get_xticklabels(), rotation=45, ha="left", fontweight="semibold"
    )
    st.pyplot(hm.get_figure())

if st.checkbox("Show scatterplot"):
    sns.set_style("ticks")
    g = sns.catplot(
        data=df,
        x="count",
        y="moon_phase",
        hue="anim_spotted",
        palette=sns.color_palette("colorblind"),
    )
    (g.set_axis_labels("Count of species spotted", ""))
    sns.move_legend(
        g,
        "center right",
        bbox_to_anchor=(1.35, 0.65),
        ncol=2,
        frameon=True,
        title="Animal spotted",
    )
    st.pyplot(g)

st.sidebar.write("##")
st.sidebar.warning("This demo uses synthetic data")
