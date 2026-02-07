import streamlit as st
from typing import Dict, Any
from utils.data_loader import load_data


def render_sidebar():
    DATA = load_data("data/sample.yml")
    
    with st.sidebar:
        st.markdown("### Escolha:")
        
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
        
        if not st.session_state.selected_context or not st.session_state.selected_track:
            st.info("💡 Selecione contexto e trilha para explorar as trilhas de carreira.")
        
    return DATA, context, track
