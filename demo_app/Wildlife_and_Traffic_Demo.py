import streamlit as st

st.set_page_config(page_title="Home")

st.write("# Wildlife and Traffic Demo")

st.sidebar.info("Select a demo above")

st.write("")
st.markdown(
    """
   The wildlife and traffic activity dashboard is part of a [Statistic Without Borders](https://www.statisticswithoutborders.org/) (SWB) project with [Painted Dog Research Trust](https://www.painteddogresearch.org/) (PDRT).
   
   When deployed using actual datasets, the dashboard helps PDRT view animal activity in Zimbabwe at different times and in different environmental conditions. It also enables PDRT to keep track of traffic speed, especially overspeeding, in national parks and forests in Zimbabwe.  

   ##

    **:point_left: Select a demo from the sidebar** for an interactive view of wildlife or traffic activity! 
"""
)

st.write("")
col1, col2, col3 = st.columns([2, 3, 2])
col2.warning("**This demo uses synthetic data**")
