from Utils.title import render_custom_header, section_divider, new_tagline_center
import streamlit as st
from Utils.Searchbox import styled_search_bar
from Utils.listings import fetch_listings, render_listing_grid

render_custom_header("Washrooms")
section_divider()

incoming_intent = st.session_state.get("extracted_intent")
came_from_search = incoming_intent and incoming_intent.get("category") == "washroom"

if came_from_search:
    location_text = incoming_intent.get("location") or "your area"
    new_tagline_center(f"Showing washrooms near {location_text}")
    st.session_state["washroom_search"] = incoming_intent.get("location") or ""
    st.session_state["extracted_intent"] = None
else:
    new_tagline_center("Find washrooms near your location")

st.write("")

search_query = styled_search_bar(
    placeholder="Enter Your Location",
    key="washroom_search",
    width_ratio=[2, 5, 2]
)

st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

# Fetch and render listings — location filter only applied if user typed something
listings = fetch_listings(category="washroom", location=search_query.strip() if search_query else None)
render_listing_grid(listings)