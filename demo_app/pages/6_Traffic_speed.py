import streamlit as st
import os
import pandas as pd
import seaborn as sns
from datetime import datetime
from datetime import timedelta


st.title("Traffic in Kazuma Pan National Park")


@st.cache_data
def upload_csv(filename, date_list=None):
    FILE_PATH = os.path.join(".", "data", filename)
    df = pd.read_csv(FILE_PATH, parse_dates=date_list)
    return df


cols_date = ["date"]
traffic = upload_csv("synthetic_traffic.csv", cols_date)

st.sidebar.info("Enter your preferences below")


def convert_to_datetime(val):
    dt = datetime.fromtimestamp(datetime.timestamp(val))
    return dt


min_date = convert_to_datetime(traffic["date"].min())
max_date = convert_to_datetime(traffic["date"].max())

speed_limit = st.sidebar.slider("Pick a speed limit (km/hr)", max_value=140, value=80)

date_range = st.sidebar.slider(
    "Select a range of dates",
    min_value=min_date,
    max_value=max_date,
    value=(min_date + timedelta(1), max_date),
)
st.write(
    "### Between",
    datetime.strftime(date_range[0], "%B %d, %Y"),
    "and",
    datetime.strftime(date_range[1], "%B %d, %Y"),
)

st.write("**Speed limit:** ", speed_limit, " km/hr")

df = (
    traffic.query("@date_range[0] <= date <= @date_range[1]")
    .groupby(["company", "country"])
    .agg({"speed": ["mean", "max"]})
)

df.columns = ["_".join(col) for col in df.columns.values]


def style_speeding(value, props="", limit=speed_limit):
    return props if value > limit else None


if st.checkbox("Show companies' average and maximum speed"):
    df_styled = df.style.map(style_speeding, props="color:red;").format(precision=2)
    st.dataframe(df_styled)
    st.write("Note: overspeeding are shown in red.")


if st.checkbox("Plot percentage of companies that oversped"):
    df_flat = df.reset_index()

    def is_overspeed(val, limit=speed_limit):
        if val >= limit:
            return "Yes"
        return "No"

    df_flat["overspeed"] = df_flat["speed_max"].apply(lambda x: is_overspeed(x))

    g = sns.catplot(
        data=df_flat,
        kind="count",
        x="overspeed",
        stat="percent",
        hue="overspeed",
        order=["Yes", "No"],
        hue_order=["Yes", "No"],
        palette=["#FF4B4B", "#8BADE1"],
    )

    g.set_axis_labels("Company oversped", "Percent")
    st.pyplot(g)


if st.checkbox("Plot distribution of speed"):
    sns.set_style("ticks")
    h = sns.displot(data=traffic, x="speed", binwidth=5, color="#8BADE1")
    h.set_axis_labels("Speed (km/hr)", "Count")
    h.refline(x=speed_limit, linestyle=":", color="#FF4B4B")
    st.pyplot(h)

st.sidebar.write("##")
st.sidebar.warning("This demo uses synthetic data")
