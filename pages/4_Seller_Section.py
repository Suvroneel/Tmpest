import streamlit as st
from Utils.auth import signup_seller, login_seller
from Utils.button import *
from Utils.title import *


col1, col2 = st.columns([1, 10])
with col1:
    st.image('images/logo.jpg', use_container_width=True, width=70)
with col2:
    render_main_title()

section_divider()

# ── Logged-in view ─────────────────────────────────────────────────────────
if "seller" in st.session_state:
    seller = st.session_state["seller"]
    st.success(f"Welcome, {seller['name']}")
    st.write(seller)

    if styled_button("Logout", key="logout_btn"):
        del st.session_state["seller"]
        st.session_state.pop("access_token", None)
        st.session_state.pop("refresh_token", None)
        st.rerun()

    st.stop()

# ── Logged-out view ────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["Login", "Sign Up"])

with tab1:
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if styled_button("Login", key="login_btn"):
        seller, session, error = login_seller(email, password)
        if seller:
            st.session_state["seller"] = seller
            if session:
                st.session_state["access_token"] = session.access_token
                st.session_state["refresh_token"] = session.refresh_token
            st.rerun()
        else:
            st.error(error or "Login failed.")

with tab2:
    st.subheader("Sign Up")
    name = st.text_input("Full Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    phone = st.text_input("Phone Number", key="signup_phone")
    password = st.text_input("Password", type="password", key="signup_password")
    identity_file = st.file_uploader("Upload Identity Document", type=["png", "jpg", "jpeg", "pdf"])

    if styled_button("Create Account", key="signup_btn"):
        seller, session, error = signup_seller(email, password, name, phone, identity_file)
        if seller:
            st.session_state["seller"] = seller
            if session:
                st.session_state["access_token"] = session.access_token
                st.session_state["refresh_token"] = session.refresh_token
                st.success(f"Welcome, {seller['name']}!")
                st.rerun()
            else:
                st.success("Account created! Check your email to verify, then log in.")
        else:
            st.error(error or "Signup failed.")