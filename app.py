"""Main application file"""
import streamlit as st
from styles import get_css
from components.sidebar import render_sidebar
from pages import home
from pages import career_path
from pages import job_details
from pages import comparison

st.set_page_config(
    page_title="Trilha de Carreira — Software Engineer",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Início"
if "selected_context" not in st.session_state:
    st.session_state.selected_context = None
if "selected_track" not in st.session_state:
    st.session_state.selected_track = None
if "selected_level" not in st.session_state:
    st.session_state.selected_level = None
if "current_level" not in st.session_state:
    st.session_state.current_level = None
if "target_level" not in st.session_state:
    st.session_state.target_level = None

def main():
    st.markdown(get_css(), unsafe_allow_html=True)
    
    DATA, context, track = render_sidebar()
    
    if st.session_state.current_page == "Início":
        home.render()
    elif st.session_state.current_page == "Trilha":
        career_path.render()
    elif st.session_state.current_page == "Detalhes":
        job_details.render()
    elif st.session_state.current_page == "Comparação":
        comparison.render()
    
if __name__ == "__main__":
    main()
