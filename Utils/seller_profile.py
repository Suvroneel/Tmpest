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
