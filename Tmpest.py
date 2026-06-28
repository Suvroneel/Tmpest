import streamlit as st
from Utils.button import styled_button
from Utils.title import *
from Utils.section import section_start, section_end
from Utils.tmpest_chat import render_chat, render_search_trigger

st.set_page_config(
    page_title="Tmpest",
    layout="wide",
    page_icon="images/icon/favicon.ico"
)

st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 4])
with col1:
    st.image('images/logo.jpg', use_container_width=True, width=70)
with col2:
    render_main_title()
    render_green_text("Minimum Friction, Maximum Action")

    st.markdown("<div style='margin-top: 55px;'></div>", unsafe_allow_html=True)

    dash = styled_button("Seller Dashboard", key="dash", icon=":material/dashboard:")
    if dash:
        st.switch_page("pages/4_Seller_Section.py")

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

# ── Chat or Search ─────────────────────────────────────────────────────────────
if st.session_state.get("chat_mode"):
    render_chat()
    st.stop()
else:
    render_search_trigger()

st.markdown("<div style='margin-top: 80px;'></div>", unsafe_allow_html=True)
section_divider()
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

# ── Shelters ───────────────────────────────────────────────────────────────────
A, B = st.columns([1, 5])
with A:
    render_custom_header("Shelters")
    section_divider()

col1, col2 = st.columns([4, 4])
with col1:
    new_tagline("Find or rent affordable temporary accommodation options even in remote areas based on: ")
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ Location proximity")
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ Budget flexibility")
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ Availability of rooms")
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ User Reviews")
    st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)

    m, n = st.columns([1, 2])
    with m:
        journey = styled_button("Explore", key="shelter", icon=":material/open_in_new:")
    with n:
        share_shelter = styled_button("Share", key="share_shelter", icon=":material/favorite:")

if journey:
    st.switch_page("pages/1_Shelters.py")
if share_shelter:
    st.switch_page("pages/4_Seller_Section.py")

with col2:
    st.image('images/shelter.jpg', use_container_width=True, width=40)

st.markdown("""
    <style>.st-emotion-cache-yinll1 { display: none !important; }</style>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)

# ── Washrooms ──────────────────────────────────────────────────────────────────
cola, colb = st.columns([5, 1])
with colb:
    render_custom_header("Washrooms")
    section_divider()

colX, colY = st.columns([4, 4])
with colY:
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    new_tagline("Locate clean, safe, and accessible washrooms near you — instantly, without the stress of searching.")
    st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)
    x, y, z = st.columns([3, 3, 2])
    with y:
        move = styled_button("Explore", icon=":material/open_in_new:", key="toilet_button")
    with z:
        share_toilet = styled_button("Share", key="share_toilet", icon=":material/favorite:")
    if move:
        st.switch_page("pages/2_Washrooms.py")
    if share_toilet:
        st.switch_page("pages/4_Seller_Section.py")

with colX:
    st.image('images/toilet.jpg', use_container_width=True, width=30)

st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)

# ── Food ───────────────────────────────────────────────────────────────────────
A, B = st.columns([1, 5])
with A:
    render_custom_header("Foods")
    section_divider()

col1, col2 = st.columns([4, 4])
with col1:
    new_tagline("Find affordable meals and immediate food access nearby based on: ")
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ Location proximity")
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ Budget flexibility")
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ Open now")
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline("•‎ ‎ ‎ ‎ ‎ ‎ ‎ User Reviews")
    st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)

    m, n = st.columns([1, 2])
    with m:
        food_btn = styled_button("Explore", key="food", icon=":material/open_in_new:")
    with n:
        share_food = styled_button("Share", key="share_food", icon=":material/favorite:")

if food_btn:
    st.switch_page("pages/3_Food.py")
if share_food:
    st.switch_page("pages/4_Seller_Section.py")

with col2:
    st.image('images/food.jpg', use_container_width=True, width=40)

st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
section_divider()

C, D, E = st.columns([1, 3, 1])
with C:
    st.image('images/img_1.jpg', width=200)
with D:
    render_custom_header("So what do you get ?")
