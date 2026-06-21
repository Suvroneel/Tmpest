import streamlit as st


def styled_search_bar(
    placeholder="Search...",
    key=None,
    width_ratio=[2,5,2],
    value=""
):

    st.markdown("""
    <style>

    /* Outer container */

    div[data-baseweb="input"] {

        background: #ffffff;

        border: 1.5px solid #e5e7eb;

        border-radius: 999px;

        padding-left: 18px;

        padding-right: 18px;

        min-height: 58px;

        box-shadow:

            0 2px 12px rgba(0,0,0,0.05);

        transition: all 0.25s ease;

    }


    /* Hover */

    div[data-baseweb="input"]:hover {

        border-color: #b8f24a;

        box-shadow:

            0 0 0 4px rgba(184,242,74,0.12),

            0 6px 18px rgba(184,242,74,0.18);

    }


    /* Focus */

    div[data-baseweb="input"]:focus-within {

        border-color: #b8f24a;

        box-shadow:

            0 0 0 5px rgba(184,242,74,0.18),

            0 8px 24px rgba(184,242,74,0.22);

    }


    /* Actual input */

    div[data-baseweb="input"] input {

        font-size: 18px;

        font-weight: 400;

        color: #2c2c2c;

        padding-top: 12px;

        padding-bottom: 12px;

        background: transparent;

    }


    /* Placeholder */

    div[data-baseweb="input"] input::placeholder {

        color: #9ca3af;

        font-weight: 400;

        opacity: 1;

    }


    /* Hide label spacing */

    label {

        display: none !important;

    }

    </style>
    """, unsafe_allow_html=True)


    left, middle, right = st.columns(width_ratio)

    with middle:

        # IMPORTANT: when a `key` is supplied, we deliberately do NOT pass
        # `value=` into st.text_input. Streamlit ties widgets with a `key`
        # to st.session_state[key] — if we ALSO pass a competing `value`
        # argument on every rerun, it can silently override a value that
        # was pre-seeded into session_state (e.g. by the AI-search routing
        # flow setting st.session_state["food_search"] = "Kalighat" before
        # this widget renders). That was causing the search box to reset
        # to empty and the page to show all listings instead of filtered
        # ones. Pre-seed session_state[key] BEFORE calling this function
        # if you want a default value — that's now the only supported way.
        if key is not None:
            if value and key not in st.session_state:
                st.session_state[key] = value

            query = st.text_input(
                "",
                placeholder=placeholder,
                key=key,
                label_visibility="collapsed"
            )
        else:
            query = st.text_input(
                "",
                value=value,
                placeholder=placeholder,
                label_visibility="collapsed"
            )

    return query