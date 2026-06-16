from Utils.title import render_custom_header, section_divider
import streamlit as st
from streamlit_folium import st_folium
import folium
from Utils.Searchbox import *

render_custom_header("Find Washrooms")
section_divider()

# ── Check if user arrived here via the smart search box ──────────────────────
incoming_intent = st.session_state.get("extracted_intent")

if incoming_intent and incoming_intent.get("category") == "washroom":
    location_text = incoming_intent.get("location") or "your area"
    st.success(f"Showing washrooms near **{location_text}** based on your search.")
    st.session_state["extracted_intent"] = None

# --- map ---
m = folium.Map(location=[22.5726, 88.3639], zoom_start=10)

folium.Marker(location=[22.5726, 88.3639]).add_to(m)
st_folium(m, width=700)