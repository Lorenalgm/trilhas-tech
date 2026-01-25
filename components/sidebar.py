"""Sidebar component"""
import streamlit as st
from typing import Dict, Any
from utils.data_loader import load_data


def render_sidebar():
    """Render sidebar with navigation and context/track selection"""
    DATA = load_data("data/sample.yml")
    
    with st.sidebar:
        st.title("🧭 Navegação")
        
        st.divider()
        
        # Page navigation
        page = st.radio(
            "Página",
            ["Início", "Trilha", "Detalhes", "Comparação"],
            index=["Início", "Trilha", "Detalhes", "Comparação"].index(
                st.session_state.current_page
            ) if st.session_state.current_page in ["Início", "Trilha", "Detalhes", "Comparação"] else 0,
        )
        if page != st.session_state.current_page:
            st.session_state.current_page = page
            st.rerun()
        
        st.divider()
        
        # Context and track selection
        st.markdown("### Configuração")
        
        context_keys = list(DATA["contexts"].keys())
        context = st.selectbox(
            "Contexto",
            context_keys,
            index=context_keys.index(st.session_state.selected_context) 
            if st.session_state.selected_context in context_keys else 0,
            format_func=lambda k: DATA["contexts"][k]["name"],
        )
        if context != st.session_state.selected_context:
            st.session_state.selected_context = context
            st.rerun()
        
        track_keys = list(DATA["tracks"].keys())
        track = st.selectbox(
            "Trilha",
            track_keys,
            index=track_keys.index(st.session_state.selected_track) 
            if st.session_state.selected_track in track_keys else 0,
            format_func=lambda k: DATA["tracks"][k]["name"],
        )
        if track != st.session_state.selected_track:
            st.session_state.selected_track = track
            st.rerun()
        
        # Show info if context/track not selected
        if not st.session_state.selected_context or not st.session_state.selected_track:
            st.info("💡 Selecione contexto e trilha para explorar as trilhas de carreira.")
    
    return DATA, context, track
