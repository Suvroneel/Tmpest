from Utils.button import styled_button
from Utils.supabase_client import get_supabase
from Utils.title import render_custom_header, new_tagline
import streamlit as st

supabase = get_supabase()


def fetch_contact(email: str) -> str:
    try:
        res = supabase.table("sellers").select("contact").eq("email", email).execute()
        if res.data:
            return res.data[0]["contact"] or "Not provided"
        return "Not provided"
    except Exception as e:
        return "Not provided"


def profile(seller: dict):
    name = seller.get("name", "Seller")
    email = seller.get("email", "")
    contact = fetch_contact(email)

    render_custom_header(f"{name}")

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline(email)

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    new_tagline(contact)

def create_listing():
    tab1, tab2, tab3 = st.tabs(["Shelter", "Food", "Washroom"])

    for tab, category in zip([tab1, tab2, tab3], ["shelter", "food", "washroom"]):
        with tab:
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            place_name = st.text_input("Name of the place", key=f"{category}_place")
            price = st.text_input("Price (₹)", key=f"{category}_price")
            location = st.text_input("Location", key=f"{category}_location")
            city = st.text_input("City", key=f"{category}_city")
            image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"], key=f"{category}_image")

            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            styled_button("Post Listing", key=f"{category}_post", icon=":material/upload:")