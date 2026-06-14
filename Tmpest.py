import streamlit as st
from Utils.button import *
from Utils.title import *
from Utils.section import *
st.set_page_config(
    page_title="Tmpest",
    layout="wide"
)

st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])
with col1:
    st.image('images/logo.jpg', use_container_width=True, width=100)
with col2:
    render_main_title()
    render_tagline()
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
new_tagline("Discover nearby shelters & washrooms through intelligent location-aware recommendations")
styled_button("Get Started")
###############################################
st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
section_divider()
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
##################################################

A,B = st.columns([1, 5])
with A:
    render_custom_header("Shelters")
    section_divider()
col1, col2 = st.columns([4, 4])
with col1:

    #st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
    new_tagline("Find or rent affortable temporary accommodation options even in remote areas based on: ")
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ Location proximity")
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ Budget flexibility")
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ Availability of rooms")
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ User Reviews")
    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)

    journey = styled_button("Explore", key= "shelter", icon=":material/open_in_new:")

if journey:
    st.switch_page("pages/1_Shelters.py")

st.markdown("""
        <style>
            .st-emotion-cache-yinll1 { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
with col2:
    st.image('images/shelter.jpg', use_container_width=True, width=40)


st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)



###############   Washroom  #########################
cola,colb = st.columns([5, 1])
with colb:
    render_custom_header("Washrooms")
    section_divider()
colX, colY = st.columns([4, 4])
with colY:
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    new_tagline_right("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since 1966,")
    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
    y , z = st.columns([4, 2])
    with z:
        move = styled_button("Explore", icon=":material/open_in_new:", key="toilet_button")

        if move:
            st.switch_page("pages/2_Washrooms.py")

st.markdown("""
        <style>
            .st-emotion-cache-yinll1 { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
with colX:
    st.image('images/toilet.jpg', use_container_width=True, width=30)
st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
#######################Foodings ###################

A,B = st.columns([1, 5])
with A:
    render_custom_header("Foods")
    section_divider()
col1, col2 = st.columns([4, 4])
with col1:

    #st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
    new_tagline("Find or rent affortable temporary accommodation options even in remote areas based on: ")
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ Location proximity")
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ Budget flexibility")
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ Availability of rooms")
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ User Reviews")
    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)

    journey = styled_button("Explore", key= "food", icon=":material/open_in_new:")

if journey:
    st.switch_page("pages/3_Food.py")

st.markdown("""
        <style>
            .st-emotion-cache-yinll1 { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
with col2:
    st.image('images/food.jpg', use_container_width=True, width=40)


#################End of section################




st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
section_divider()
C,D,E = st.columns([1, 3, 1])
with C:
    st.image('images/img_1.jpg', width=200)
with D:
    render_custom_header("So What Are You Getting?")