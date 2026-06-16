import streamlit as st
import pandas as pd
from Utils.Searchbox import *
from Utils.title import *
from streamlit_dynamic_filters import DynamicFilters

# Hero Text
render_custom_header("Food Accommodations")
section_divider()

# ── Check if user arrived here via the smart search box ──────────────────────
incoming_intent = st.session_state.get("extracted_intent")
came_from_search = incoming_intent and incoming_intent.get("category") == "food"

if came_from_search:
    location_text = incoming_intent.get("location") or "your area"
    budget_text = f" under ₹{incoming_intent['budget']}" if incoming_intent.get("budget") else ""
    new_tagline_center(f"Showing food in {location_text}{budget_text}")
else:
    new_tagline_center("Find Your Nearest Food Outing")

st.write("")

# Pre-fill search bar with extracted location, if any — keeps continuity with what user typed
prefill_location = incoming_intent.get("location") if came_from_search else ""

# Search Bar (still works for manual browsing / refining)
search_query = styled_search_bar(
    placeholder="Enter Your Location",
    key="food_search",
    width_ratio=[2, 5, 2],
    value=prefill_location
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
if came_from_search:
    st.session_state["extracted_intent"] = None