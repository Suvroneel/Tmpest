from Utils.title import render_custom_header, section_divider, new_tagline_center
import streamlit as st
from Utils.Searchbox import styled_search_bar

render_custom_header("Washrooms")
section_divider()

# ── Check if user arrived here via the smart search box ──────────────────────
incoming_intent = st.session_state.get("extracted_intent")
came_from_search = incoming_intent and incoming_intent.get("category") == "washroom"

if came_from_search:
    location_text = incoming_intent.get("location") or "your area"
    new_tagline_center(f"Showing washrooms near {location_text}")
else:
    new_tagline_center("Find washrooms near your location")

st.write("")

# Pre-fill search bar with extracted location, if any
prefill_location = incoming_intent.get("location") if came_from_search else ""

# Search Bar
search_query = styled_search_bar(
    placeholder="Enter Your Location",
    key="washroom_search",
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
