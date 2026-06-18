from Utils.supabase_client import get_supabase
from Utils.storage import upload_identity_doc

supabase = get_supabase()


def signup_seller(email, password, name, phone, identity_file):
    """Returns (seller_dict, session, error_message)."""
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        user = res.user
        session = res.session  # None if email confirmation is required

        if not user:
            return None, None, "Signup failed — no user returned."

        # Orphan recovery: a sellers row may already exist from a previous partial failure
        existing = supabase.table("sellers").select("*").eq("email", email).execute()
        if existing.data:
            return existing.data[0], session, None

        identity_path = upload_identity_doc(identity_file)

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
    """Returns (seller_dict, session, error_message)."""
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = res.user
        session = res.session

        if not user:
            return None, None, "Login failed — invalid credentials."

        seller = supabase.table("sellers").select("*").eq("email", email).execute()
        if not seller.data:
            return None, session, "No seller profile found for this account."

        return seller.data[0], session, None

    except Exception as e:
        return None, None, str(e)


def get_seller(email):
    res = supabase.table("sellers").select("*").eq("email", email).execute()
    return res.data[0] if res.data else None