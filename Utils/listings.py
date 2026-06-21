"""
listings.py — Fetch layer for Tmpest's user-facing listing pages
(Shelters / Food / Washrooms)

Handles fuzzy-ish location matching so "Kalighat" matches a DB row
stored as "Kali Ghat" (or vice versa) by stripping spaces before
comparing, since Postgres ILIKE alone won't bridge that gap.
"""

from Utils.supabase_client import get_supabase

supabase = get_supabase()

TABLE_MAP = {
    "shelter": "shelters",
    "food": "foodings",
    "washroom": "washrooms",
}

PLACEHOLDER_IMAGE = "https://placehold.co/400x300?text=No+Image+Yet"


def _normalize(text: str) -> str:
    """Lowercase + strip all whitespace, so 'Kali Ghat' == 'kalighat'."""
    return text.lower().replace(" ", "").strip() if text else ""


def fetch_listings(category: str, location: str | None = None, city: str | None = None, debug: bool = False) -> list[dict]:
    """
    Fetch listings for a given category ('shelter' / 'food' / 'washroom'),
    optionally filtered by location (fuzzy, space-insensitive match) or city.

    Returns a list of row dicts. Empty list if nothing found or category invalid.
    Pass debug=True to print diagnostic info via st.write (temporary, for troubleshooting).
    """
    import streamlit as st

    table = TABLE_MAP.get(category)
    if not table:
        if debug:
            st.write(f"DEBUG — invalid category '{category}', no table matched")
        return []

    query = supabase.table(table).select("*")

    # We pull broader and filter in Python for the space-insensitive match,
    # since Supabase/Postgrest ILIKE can't strip spaces on the DB side easily.
    try:
        response = query.execute()
    except Exception as e:
        if debug:
            st.write(f"DEBUG — Supabase query raised an exception: {e}")
        return []

    rows = response.data or []

    if debug:
        st.write(f"DEBUG — table queried: {table}")
        st.write(f"DEBUG — raw row count returned: {len(rows)}")
        st.write("DEBUG — raw rows:", rows)

    if not location:
        return rows

    target = _normalize(location)
    matched = [
        row for row in rows
        if target in _normalize(row.get("location", "")) or _normalize(row.get("location", "")) in target
    ]

    if debug:
        st.write(f"DEBUG — location filter applied: '{location}' -> normalized '{target}'")
        st.write(f"DEBUG — matched row count: {len(matched)}")
        for row in rows:
            st.write(f"DEBUG — row location='{row.get('location')}' normalized='{_normalize(row.get('location', ''))}'")

    return matched


def get_image_url(row: dict) -> str:
    """Returns the row's image if present, otherwise a local placeholder."""
    return row.get("image") or PLACEHOLDER_IMAGE


def render_listing_card(row: dict) -> str:
    """
    Returns an HTML string for a single listing card, styled to match
    Tmpest's existing lime-green design system (see button.py / Searchbox.py).
    Meant to be passed into st.markdown(..., unsafe_allow_html=True).
    """
    name = row.get("name") or "Unnamed listing"
    price = row.get("price")
    price_text = f"₹{price}" if price is not None else "Price on request"
    location = row.get("location") or "Location not specified"
    city = row.get("city")
    location_text = f"{location}, {city}" if city else location
    owner = row.get("owner_name") or "Unknown host"
    contact = row.get("contact") or "Not provided"
    rating = row.get("ratings") or 0
    image_url = get_image_url(row)

    return f"""
    <div style="
        background:#ffffff;
        border:1.5px solid #e5e7eb;
        border-radius:16px;
        overflow:hidden;
        box-shadow:0 2px 12px rgba(0,0,0,0.05);
        transition:all 0.25s ease;
        margin-bottom:20px;
        font-family:'Inter', sans-serif;
    ">
        <img src="{image_url}" style="
            width:100%;
            height:170px;
            object-fit:cover;
            display:block;
        ">
        <div style="padding:16px 18px 18px 18px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div style="font-size:19px; font-weight:600; color:#2c2c2c; font-family:'Poppins', sans-serif; line-height:1.3;">
                    {name}
                </div>
                <div style="font-size:14px; font-weight:600; color:#2c2c2c; white-space:nowrap; margin-left:8px;">
                    {rating}
                </div>
            </div>
            <div style="font-size:17px; font-weight:600; color:#84B63A; margin-top:4px;">
                {price_text}
            </div>
            <div style="font-size:13.5px; color:#6b7280; margin-top:10px;">
                {location_text}
            </div>
            <div style="font-size:13.5px; color:#6b7280; margin-top:4px;">
                {owner}
            </div>
            <div style="font-size:13.5px; color:#6b7280; margin-top:4px;">
                {contact}
            </div>
        </div>
    </div>
    """


def render_listing_grid(rows: list[dict], max_columns: int = 3) -> None:
    """
    Renders a row of listing cards using dynamic Streamlit columns —
    1 row, N columns based on result count (capped at max_columns).
    If there are more results than max_columns, wraps to additional rows.
    Call this directly inside a page (needs `streamlit as st` in that page).
    """
    import streamlit as st

    if not rows:
        st.info("No listings found nearby. Try a different location, or check back soon — sellers are adding more every day.")
        return

    for i in range(0, len(rows), max_columns):
        chunk = rows[i:i + max_columns]
        cols = st.columns(len(chunk), gap="large")
        for col, row in zip(cols, chunk):
            with col:
                st.markdown(render_listing_card(row), unsafe_allow_html=True)