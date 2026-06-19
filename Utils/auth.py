from supabase import create_client
import streamlit as st
import uuid
from Utils.storage import upload_identity_doc

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def signup_seller(email, password, name, phone, identity_file):
    """
    Returns (seller_dict, session, error_message).
    Session will be None if email confirmation is required —
    in that case the user needs to verify their email before logging in.
    """
    try:
        # Step 1: Create Supabase Auth user
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "display_name": name
                }
            }
        })

        user = res.user
        session = res.session

        if not user:
            return None, None, "Signup failed — no user returned from Supabase."

        # Step 2: Set session if available (only happens if email confirm is OFF)
        # If email confirm is ON, session is None here — that's expected and fine
        if session:
            supabase.auth.set_session(session.access_token, session.refresh_token)

        # Step 3: Orphan recovery — if sellers row already exists for this email, return it
        existing = supabase.table("sellers").select("*").eq("email", email).execute()
        if existing.data:
            return existing.data[0], session, None

        # Step 4: Upload identity document if provided
        # This may fail silently and return None if no file — that's fine, column is nullable
        identity_path = upload_identity_doc(identity_file)

        # Step 5: Insert into sellers table, linked by email and name only
        seller = supabase.table("sellers").insert({
            "name": name,
            "email": email,
            "contact": phone,
            "identity_document_url": identity_path
        }).execute()

        return seller.data[0], session, None

    except Exception as e:
        return None, None, str(e)


def login_seller(email, password):
    """
    Returns (seller_dict, session, error_message).
    """
    try:
        # Step 1: Sign in via Supabase Auth
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = res.user
        session = res.session

        if not user:
            return None, None, "Login failed — invalid credentials."

        # Step 2: Set session so all subsequent DB/storage calls are authenticated
        if session:
            supabase.auth.set_session(session.access_token, session.refresh_token)

        # Step 3: Fetch seller profile from sellers table by email
        seller = supabase.table("sellers").select("*").eq("email", email).execute()

        if not seller.data:
            return None, session, "No seller profile found for this account."

        return seller.data[0], session, None

    except Exception as e:
        return None, None, str(e)


def get_seller(email):
    """Fetch a seller row by email. Returns dict or None."""
    try:
        res = supabase.table("sellers").select("*").eq("email", email).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        return None