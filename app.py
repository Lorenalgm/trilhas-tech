"""Main application file"""
import streamlit as st
from styles import get_css
from components.sidebar import render_sidebar
from pages import home
from pages import career_path
from pages import job_details
from pages import comparison

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Trilha de Carreira — Software Engineer",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# Initialize session state
# ----------------------------
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

# ----------------------------
# Main App
# ----------------------------
def main():
    # Apply CSS
    st.markdown(get_css(), unsafe_allow_html=True)
    
    # Render sidebar
    DATA, context, track = render_sidebar()
    
    # Render current page
    if st.session_state.current_page == "Início":
        home.render()
    elif st.session_state.current_page == "Trilha":
        if not st.session_state.selected_context or not st.session_state.selected_track:
            st.warning("⚠️ Por favor, selecione o contexto e a trilha no menu lateral.")
            home.render()
        else:
            career_path.render()
    elif st.session_state.current_page == "Detalhes":
        if not st.session_state.selected_context or not st.session_state.selected_track:
            st.warning("⚠️ Por favor, selecione o contexto e a trilha no menu lateral.")
            st.session_state.current_page = "Trilha"
            st.rerun()
        else:
            job_details.render()
    elif st.session_state.current_page == "Comparação":
        if not st.session_state.selected_context or not st.session_state.selected_track:
            st.warning("⚠️ Por favor, selecione o contexto e a trilha no menu lateral.")
            st.session_state.current_page = "Trilha"
            st.rerun()
        else:
            comparison.render()
    
    # Footer
    st.markdown("---")
    st.caption("Feito para o Pupunha Code Meetup — fork e customize as trilhas via YAML.")

if __name__ == "__main__":
    main()
