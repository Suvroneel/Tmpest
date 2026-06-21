import uuid
import streamlit as st
from Utils.supabase_client import get_supabase

supabase = get_supabase()

LISTING_BUCKET = "listing-images"
DOCS_BUCKET = "seller-docs"


def upload_listing_image(category: str, seller_id, file) -> str | None:
    """category = 'food' / 'shelter' / 'washroom'. Returns public URL.
    Path includes seller_id so files are traceable to the uploading seller,
    same spirit as Ashva Diaries' username-folder pattern in journal.py."""
    if file is None:
        return None

    try:
        if "access_token" in st.session_state and "refresh_token" in st.session_state:
            supabase.auth.set_session(
                st.session_state["access_token"],
                st.session_state["refresh_token"]
            )

        file_ext = file.name.split(".")[-1]
        bucket_path = f"{category}/{seller_id}_{uuid.uuid4()}.{file_ext}"

        supabase.storage.from_(LISTING_BUCKET).upload(
            bucket_path,
            file.read(),
            {"content-type": file.type}
        )
        return supabase.storage.from_(LISTING_BUCKET).get_public_url(bucket_path)
    except Exception as e:
        st.error(f"Image upload failed: {e}")
        return None


def upload_identity_doc(file) -> str | None:
    """Uploads to private bucket. Returns storage PATH not a public URL.
    No seller_id prefix here — at signup time the sellers row (and its id)
    doesn't exist yet, since `id` is an auto-generated identity column."""
    if file is None:
        return None

    try:
        if "access_token" in st.session_state and "refresh_token" in st.session_state:
            supabase.auth.set_session(
                st.session_state["access_token"],
                st.session_state["refresh_token"]
            )

        file_ext = file.name.split(".")[-1]
        bucket_path = f"sellers/{uuid.uuid4()}.{file_ext}"

        supabase.storage.from_(DOCS_BUCKET).upload(
            bucket_path,
            file.read(),
            {"content-type": file.type}
        )
        return bucket_path
    except Exception as e:
        st.error(f"Identity document upload failed: {e}")
        return None


def get_signed_identity_url(path: str, expires_in: int = 3600) -> str | None:
    """Generates short-lived viewable URL for a private identity doc."""
    if not path:
        return None
    res = supabase.storage.from_(DOCS_BUCKET).create_signed_url(path, expires_in)
    return res.get("signedURL") or res.get("signed_url")