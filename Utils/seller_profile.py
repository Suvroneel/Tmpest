from Utils.button import styled_button
from Utils.supabase_client import get_supabase
from Utils.storage import upload_listing_image
from Utils.title import render_custom_header, new_tagline
import streamlit as st

supabase = get_supabase()

TABLE_MAP = {
    "shelter": "shelters",
    "food": "foodings",
    "washroom": "washrooms",
}


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


def _insert_listing(category: str, seller_id, payload: dict, image_file) -> tuple[bool, str]:
    """Uploads image (if any) and inserts the listing row. Returns (success, message)."""
    try:
        image_url = upload_listing_image(category, seller_id, image_file) if image_file else None
        payload["image"] = image_url
        payload["seller_id"] = seller_id

        table = TABLE_MAP[category]
        supabase.table(table).insert(payload).execute()
        return True, f"{category.capitalize()} listing posted successfully!"
    except Exception as e:
        return False, f"Could not post listing: {e}"


def create_listing():
    seller = st.session_state.get("seller", {})
    seller_id = seller.get("id")
    owner_name = seller.get("name", "")
    contact = seller.get("contact", "")

    tab1, tab2, tab3 = st.tabs(["Shelter", "Food", "Washroom"])

    for tab, category in zip([tab1, tab2, tab3], ["shelter", "food", "washroom"]):
        with tab:
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            place_name = st.text_input("Name of the place", key=f"{category}_place")
            price = st.text_input("Price (₹)", key=f"{category}_price")
            location = st.text_input("Location", key=f"{category}_location")
            city = st.text_input("City", key=f"{category}_city")
            description = st.text_area("Description", key=f"{category}_description")

            opening_time = None
            cleanliness = None
            if category == "washroom":
                opening_time = st.text_input("Opening Hours (e.g. 6 AM - 10 PM)", key=f"{category}_opening_time")
                cleanliness = st.selectbox(
                    "Cleanliness",
                    ["Excellent", "Good", "Average", "Needs Improvement"],
                    key=f"{category}_cleanliness"
                )

            image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"], key=f"{category}_image")

            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            posted = styled_button("Post Listing", key=f"{category}_post", icon=":material/upload:")

            if posted:
                if not place_name or not location:
                    st.warning("Please fill in at least the name and location.")
                else:
                    payload = {
                        "name": place_name,
                        "price": int(price) if price.strip().isdigit() else None,
                        "location": location,
                        "city": city or None,
                        "description": description or None,
                        "contact": contact,
                        "owner_name": owner_name,
                    }
                    if category == "washroom":
                        payload["opening_time"] = opening_time or None
                        payload["cleanliness"] = cleanliness

                    success, message = _insert_listing(category, seller_id, payload, image)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)