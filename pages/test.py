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

# ── Check if user arrived here via the smart search box ──────────────────────
incoming_intent = st.session_state.get("extracted_intent")

if incoming_intent and incoming_intent.get("category") == "shelter":
    location_text = incoming_intent.get("location") or "your area"
    budget_text = f" under ₹{incoming_intent['budget']}" if incoming_intent.get("budget") else ""
    st.success(f"Showing shelters near **{location_text}**{budget_text} based on your search.")
    # clear it so manual browsing later isn't stuck showing this banner
    # (only clear after rendering, not before)

# Search Bar (still works for manual browsing / refining)
search_query = styled_search_bar(
    placeholder="Enter Your Location",
    key="shelter_search",
    width_ratio=[2, 5, 2]
)

# Search results show up
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1], gap="large")

with col1:
    st.container(border=True)

with col2:
    st.container(border=True)

with col3:
    st.container(border=True)

# Clear the intent after displaying so it doesn't persist on next manual visit
if incoming_intent and incoming_intent.get("category") == "shelter":
    st.session_state["extracted_intent"] = None