import streamlit as st
import pandas as pd
from Utils.Searchbox import *
from Utils.title import *
from streamlit_dynamic_filters import DynamicFilters
# Hero Text
render_custom_header("Shelters & Rents")
section_divider()


new_tagline_center("Find your perfect place to stay")

st.write("")

# Search Bar

search_query = styled_search_bar(

    placeholder="Enter Your Location",

    key="shelter_search",

    width_ratio=[2,5,2]

)

# Search results show up
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1] ,gap="large")

with col1:
    st.container(border=True)

with col2:
    st.container(border=True)

with col3:
    st.container(border=True)

