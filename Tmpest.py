import streamlit as st
from Utils import title
from Utils.title import render_main_title, render_full_header, render_tagline

st.set_page_config(
    page_title="Tmpest",

)

st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)


#col1, col2 = st.columns([1,4]) with col1:
# st.image('images/flower.png', use_container_width=True, width=50)
render_main_title()

render_tagline()

