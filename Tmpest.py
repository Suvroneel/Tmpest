import streamlit as st
from Utils.button import styled_button
from Utils.title import *

from Utils.section import section_start, section_end
from Utils.ai import extract_intent  # 🆕 AI utility

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

# ── Header (smaller than before) ──────────────────────────────────────────────
col1, col2 = st.columns([1, 5])
with col1:
    st.image('images/logo.jpg', use_container_width=True, width=70)   # slightly smaller
with col2:
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
        <h1 style='font-family:"Poppins"; font-weight:400; font-size:60px; margin-bottom:0;'>Tmpest</h1>
        <h3 style='font-family:"Poppins"; font-size:20px; color:#84B63A; font-weight:400; margin-top:-10px;'>
            Find peace when you require it most
        </h3>
    """, unsafe_allow_html=True)
st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)

new_tagline_center("Find nearby shelter, foodings, and washrooms when you need them most.")
st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)

# ── Smart Search Box ───────────────────────────────────────────────────────────
st.markdown("""
    <style>
        div[data-baseweb="input"] {
            background: #ffffff;
            border: 2px solid #b8f24a;
            border-radius: 999px;
            padding-left: 20px;
            padding-right: 20px;
            min-height: 62px;
            box-shadow: 0 2px 16px rgba(184,242,74,0.15);
            transition: all 0.25s ease;
        }
        div[data-baseweb="input"]:focus-within {
            box-shadow: 0 0 0 5px rgba(184,242,74,0.2), 0 8px 24px rgba(184,242,74,0.2);
        }
        div[data-baseweb="input"] input {
            font-size: 18px;
            font-weight: 400;
            color: #2c2c2c;
            background: transparent;
        }
        div[data-baseweb="input"] input::placeholder {
            color: #9ca3af;
        }
    </style>
""", unsafe_allow_html=True)

left, mid, right = st.columns([1, 6, 1])
with mid:
    query = st.text_input(
        "",
        placeholder="Tell us what you need",
        label_visibility="collapsed",
        key="main_search"
    )

# ── Handle Search ──────────────────────────────────────────────────────────────
if query:
    with st.spinner("Finding the best option for you..."):
        intent = extract_intent(query)
        st.session_state["search_query"] = query
        st.session_state["extracted_intent"] = intent

    category = intent.get("category", "").lower()

    if category == "shelter":
        st.switch_page("pages/1_Shelters.py")
    elif category == "washroom":
        st.switch_page("pages/2_Washrooms.py")
    elif category == "food":
        st.switch_page("pages/3_Food.py")
    else:
        st.warning("Couldn't figure out what you need. Try being more specific!")

st.markdown("<div style='margin-top: 80px;'></div>", unsafe_allow_html=True)
section_divider()
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

# ── Shelters Section (same as before) ─────────────────────────────────────────
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
    journey = styled_button("Explore", key="shelter", icon=":material/open_in_new:")

if journey:
    st.switch_page("pages/1_Shelters.py")

with col2:
    st.image('images/shelter.jpg', use_container_width=True, width=40)

st.markdown("""
    <style>.st-emotion-cache-yinll1 { display: none !important; }</style>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)

# ── Washrooms Section ──────────────────────────────────────────────────────────
cola, colb = st.columns([5, 1])
with colb:
    render_custom_header("Washrooms")
    section_divider()

colX, colY = st.columns([4, 4])
with colY:
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    new_tagline("Locate clean, safe, and accessible washrooms near you — instantly, without the stress of searching.")
    st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)
    y, z = st.columns([4, 2])
    with z:
        move = styled_button("Explore", icon=":material/open_in_new:", key="toilet_button")
        if move:
            st.switch_page("pages/2_Washrooms.py")

with colX:
    st.image('images/toilet.jpg', use_container_width=True, width=30)

st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)

# ── Food Section ───────────────────────────────────────────────────────────────
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
    food_btn = styled_button("Explore", key="food", icon=":material/open_in_new:")

if food_btn:
    st.switch_page("pages/3_Food.py")

with col2:
    st.image('images/food.jpg', use_container_width=True, width=40)

st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
section_divider()

################# END ################

C,D,E = st.columns([1, 3, 1])
with C:
    st.image('images/img_1.jpg', width=200)
with D:
    render_custom_header("So what do you get ?")
    new_tagline("You show up. Tmpest quietly finds what you need nearby.")