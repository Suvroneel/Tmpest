import streamlit as st
import pandas as pd
from Utils.Searchbox import styled_search_bar
from Utils.title import *
from Utils.listings import fetch_listings, render_listing_grid

render_custom_header("Shelters & Rents")
section_divider()

incoming_intent = st.session_state.get("extracted_intent")
came_from_search = incoming_intent and incoming_intent.get("category") == "shelter"

if came_from_search:
    location_text = incoming_intent.get("location") or "your area"
    budget_text = f" under ₹{incoming_intent['budget']}" if incoming_intent.get("budget") else ""
    new_tagline_center(f"Showing shelters in {location_text}{budget_text}")
    st.session_state["shelter_search"] = incoming_intent.get("location") or ""
    st.session_state["extracted_intent"] = None
else:
    new_tagline_center("Find your perfect place to stay")

st.write("")

search_query = styled_search_bar(
    placeholder="Enter Your Location",
    key="shelter_search",
    width_ratio=[2, 5, 2]
)

st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

# Fetch and render listings — location filter only applied if user typed something
listings = fetch_listings(category="shelter", location=search_query.strip() if search_query else None)
render_listing_grid(listings)