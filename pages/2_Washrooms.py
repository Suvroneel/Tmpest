from Utils.title import render_custom_header,section_divider
import streamlit as st
from streamlit_folium import st_folium
import folium
from Utils.Searchbox import *
# Download latest version

render_custom_header("Find Washrooms")
section_divider()





#--map
m = folium.Map(location=[22.5726,88.3639], zoom_start=10)

folium.Marker(location=[22.5726,88.3639],

              ).add_to(m)
st_folium(m, width=700)