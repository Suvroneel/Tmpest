import streamlit as st
from datetime import datetime


def render_main_title():
    st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
        """, unsafe_allow_html=True)

    st.markdown("""
        <h1 style='font-family:"Poppins";font-weight: 400; font-size: 90px;'>Tmpest
        </h1>
    """, unsafe_allow_html=True)


# B22222
def render_tagline():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    st.markdown("""
        <h3 style='font-family:"Poppins"; font-size: 28px;color:#84B63A; font-weight: 400; margin-top:-15px;'>
            Find peace when you require it most
        </h3>
    """, unsafe_allow_html=True)


def new_tagline(tagline_text):
    st.markdown(f"""
        <div style='font-size:30px;font-weight: 400; text-align:left; margin-top: -10px;'>
          {tagline_text}
        </div>
        """, unsafe_allow_html=True)

def new_tagline_right(tagline_text):
    st.markdown(f"""
        <div style='font-size:30px;font-weight: 400; text-align:right; margin-top: -10px;'>
          {tagline_text}
        </div>
        """, unsafe_allow_html=True)

def new_tagline_center(tagline_text):
    st.markdown(f"""
        <div style='font-size:30px;font-weight: 400; text-align:center; margin-top: -10px;'>
          {tagline_text}
        </div>
        """, unsafe_allow_html=True)




def render_welcome_message(username="User"):
    st.markdown(
        f"""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap" rel="stylesheet">
        <style>
        .custom-welcome {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            font-size: 25px;
            font-weight: 400;
            color: ;
            margin-bottom: 1rem;
            text-align: center; /* Added to center the text */
        }}
        </style>
        <div class="custom-welcome">Welcome, {username}</div>

        """,
        unsafe_allow_html=True
    )


def render_dynamic_greeting():
    current_time = datetime.now()
    hour = current_time.hour
    username = st.session_state.get("username", "friend")  # Default to "friend" if no username

    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:  # 02:01 PM IST falls here
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    st.markdown(
        f'<p style="text-align: center; font-family: Inter, sans-serif; font-size: 25px; font-weight: 400;">{greeting}, {username}</p>',
        unsafe_allow_html=True)


def render_custom_header(header_text):
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap" rel="stylesheet">
        <style>
            .streamlit-like-header {
                font-family: 'Inter', sans-serif;
                font-size: 50px;  /* Larger for stronger presence */
                font-weight: 500;
                color: var(--text-color);
                margin-bottom: -8px;  /* Pull divider closer */
                margin-top: 32px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="streamlit-like-header">{header_text}</div>', unsafe_allow_html=True)


def section_divider(
    color="#b8f24a",
    height=12,
    margin_top=60,
    margin_bottom=60
):
    st.markdown(
        f"""
        <div style="
            height:{height}px;
            background:{color};
            border-radius:999px;
            margin:{margin_top}px 0 {margin_bottom}px 0;
        "></div>
        """,
        unsafe_allow_html=True
    )


