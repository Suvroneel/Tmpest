import uuid
#from Utils.auth import supabase
from Utils.supabase_client import get_supabase
supabase = get_supabase()



LISTING_BUCKET = "listing-images"
DOCS_BUCKET = "seller-docs"


def upload_listing_image(category: str, file) -> str | None:
    """category should be 'food' / 'shelter' / 'washroom'. Returns a public URL."""
    if file is None:
        return None

    file_ext = file.name.split(".")[-1]
    bucket_path = f"{category}/{uuid.uuid4()}.{file_ext}"

    supabase.storage.from_(LISTING_BUCKET).upload(
        bucket_path, file.getvalue(), {"content-type": file.type}
    )
    return supabase.storage.from_(LISTING_BUCKET).get_public_url(bucket_path)


def upload_identity_doc(file) -> str | None:
    """Uploads to the private bucket. Returns a storage PATH, not a public URL."""
    if file is None:
        return None

    file_ext = file.name.split(".")[-1]
    bucket_path = f"sellers/{uuid.uuid4()}.{file_ext}"

    supabase.storage.from_(DOCS_BUCKET).upload(
        bucket_path, file.getvalue(), {"content-type": file.type}
    )
    return bucket_path


def get_signed_identity_url(path: str, expires_in: int = 3600) -> str | None:
    """Generates a short-lived viewable URL for a private identity doc."""
    if not path:
        return None
    res = supabase.storage.from_(DOCS_BUCKET).create_signed_url(path, expires_in)
    return res.get("signedURL") or res.get("signed_url")