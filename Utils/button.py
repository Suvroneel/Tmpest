import streamlit as st
def styled_button(label, icon=None, key=None):

    st.markdown("""
    <style>

    .stButton > button {
        background: linear-gradient(
            135deg,
            #b8f24a,
            #9ed93a
        );

        color: #2c2c2c !important;

        width: 260px;
        height: 64px;

        border: none;
        border-radius: 14px;

        font-size: 20px;
        font-weight: 700;
        letter-spacing: 0.3px;

        cursor: pointer;
        transition: all 0.3s ease;

        box-shadow:
            0 4px 14px rgba(158, 217, 58, 0.35);
    }

    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #c4f95a,
            #a8e63f
        );

        transform: translateY(-2px);

        box-shadow:
            0 8px 20px rgba(168, 230, 63, 0.45);

        color: #222 !important;
    }

    </style>
    """, unsafe_allow_html=True)

    return st.button(
        label,
        icon=icon,
        key=key,
        use_container_width=False
    )


