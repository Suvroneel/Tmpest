"""
tmpest_results.py — Mixed multi-category listing renderer.
Called after user confirms intent in chat flow.
"""

import streamlit as st
from Utils.listings import fetch_listings, render_listing_card

CATEGORY_LABELS = {
    "shelter": "Shelters",
    "food": "Food",
    "washroom": "Washrooms",
}


def render_mixed_results(intent: dict):
    primary = intent.get("category")
    location = intent.get("location")
    budget = intent.get("budget")

    if not primary or not location:
        st.warning("Couldn't determine location or category. Please start a new search.")
        return

    # ── Summary banner ─────────────────────────────────────────────────────────
    budget_text = f" · under ₹{budget}" if budget else ""
    st.markdown(f"""
    <div style="
        background:#f0fad9;
        border:1.5px solid #b8f24a;
        border-radius:12px;
        padding:14px 20px;
        font-family:'Inter',sans-serif;
        font-size:15px;
        color:#2c2c2c;
        margin-bottom:28px;
    ">
        Showing <strong>{CATEGORY_LABELS.get(primary, primary)}</strong>
        near <strong>{location}</strong>{budget_text}
    </div>
    """, unsafe_allow_html=True)

    # Primary category first, then others at same location
    order = [primary] + [c for c in ["shelter", "food", "washroom"] if c != primary]
    found_any = False

    for cat in order:
        listings = fetch_listings(category=cat, location=location)

        # Budget filter on primary only
        if budget and cat == primary:
            listings = [r for r in listings if r.get("price") is None or (r.get("price") or 9999) <= budget]

        if not listings:
            continue

        found_any = True
        listings = listings[:3]  # cap at 3 per category

        # Section header
        label = CATEGORY_LABELS.get(cat, cat.capitalize())
        is_primary = cat == primary

        st.markdown(f"""
        <div style="
            font-family:'Poppins',sans-serif;
            font-size:{'24px' if is_primary else '20px'};
            font-weight:{'600' if is_primary else '400'};
            color:#2c2c2c;
            margin:{'8px' if is_primary else '32px'} 0 12px 0;
            {'border-left:4px solid #b8f24a; padding-left:12px;' if is_primary else 'color:#555;'}
        ">{label}</div>
        """, unsafe_allow_html=True)

        cols = st.columns(len(listings), gap="large")
        for col, row in zip(cols, listings):
            with col:
                st.markdown(render_listing_card(row), unsafe_allow_html=True)

    if not found_any:
        st.info(f"No listings found near {location} right now. Sellers are adding more every day.")
        st.markdown(f"""
        <div style="
            font-family:'Inter',sans-serif;
            font-size:14px;
            color:#6b7280;
            margin-top:8px;
        ">
            You can also <a href='/4_Seller_Section' style='color:#84B63A;'>share your space</a> to help others.
        </div>
        """, unsafe_allow_html=True)
