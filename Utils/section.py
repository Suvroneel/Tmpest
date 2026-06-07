import streamlit as st

def section_start():
    st.markdown("""
    <div style="
        background-color:#EAF4E1;
        border-radius:24px;
        padding:60px;
        margin:40px 0;
    ">
    """, unsafe_allow_html=True)

def section_end():
    st.markdown("</div>", unsafe_allow_html=True)