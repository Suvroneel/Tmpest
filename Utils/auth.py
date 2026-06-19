import streamlit as st
from Utils.supabase_client import get_supabase
from Utils.storage import upload_identity_doc

supabase = get_supabase()  # same client instance storage.py uses


def signup_seller(email, password, name, phone, identity_file):
    """Returns (seller_dict, session, error_message)."""
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"display_name": name}}
        })

        user = res.user
        session = res.session

        if not user:
            return None, None, "Signup failed — no user returned from Supabase."

        if session:
            supabase.auth.set_session(session.access_token, session.refresh_token)

        existing = supabase.table("sellers").select("*").eq("email", email).execute()

        # 🔍 DEBUG
        import streamlit as st
        st.write("DEBUG — phone received:", repr(phone))
        st.write("DEBUG — identity_file received:", identity_file)
        st.write("DEBUG — existing row found?:", existing.data)

        if existing.data:
            st.write("DEBUG — returning early via orphan recovery, this is likely the bug")
            return existing.data[0], session, None

        identity_path = upload_identity_doc(identity_file)
        st.write("DEBUG — identity_path after upload:", identity_path)

        payload = {
            "name": name,
            "email": email,
            "contact": phone,
            "identity_document_url": identity_path
        }
        st.write("DEBUG — payload about to insert:", payload)

        seller = supabase.table("sellers").insert(payload).execute()
        st.write("DEBUG — insert response:", seller.data)

        return seller.data[0], session, None

    except Exception as e:
        import streamlit as st
        st.write("DEBUG — exception caught:", str(e))
        return None, None, str(e)


def login_seller(email, password):
    """Returns (seller_dict, session, error_message)."""
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = res.user
        session = res.session

        if not user:
            return None, None, "Login failed — invalid credentials."

        if session:
            supabase.auth.set_session(session.access_token, session.refresh_token)

        seller = supabase.table("sellers").select("*").eq("email", email).execute()
        if not seller.data:
            return None, session, "No seller profile found for this account."

        return seller.data[0], session, None

    except Exception as e:
        return None, None, str(e)


def get_seller(email):
    try:
        res = supabase.table("sellers").select("*").eq("email", email).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None