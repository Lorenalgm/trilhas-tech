import streamlit as st
from styles import get_css
from components.sidebar import render_sidebar
from utils.data_loader import load_data
from utils.helpers import sort_levels, get_role_data
from components.render import render_header, render_skill_compact

st.set_page_config(
    page_title="Detalhes - Trilha de carreira",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_css(), unsafe_allow_html=True)

DATA, context, track = render_sidebar()

selected = st.session_state.selected_level or sort_levels(DATA["contexts"][context]["levels"][track])[0]

levels = sort_levels(DATA["contexts"][context]["levels"][track])
current_idx = levels.index(selected) if selected in levels else 0

render_header(
    f"{selected} — {DATA['tracks'][track]['name']}",
    f"Contexto: {DATA['contexts'][context]['name']}",
)

col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
with col_nav1:
    if current_idx > 0:
        prev_level = levels[current_idx - 1]
        if st.button("⬅", key="nav_prev", use_container_width=True, type="secondary"):
            st.session_state.selected_level = prev_level
            st.rerun()
with col_nav2:
    if st.button("Trilha", key="nav_home", use_container_width=True, type="secondary"):
        st.switch_page("pages/2_Trilha.py")
with col_nav3:
    if current_idx < len(levels) - 1:
        next_level = levels[current_idx + 1]
        if st.button("➡", key="nav_next", use_container_width=True, type="secondary"):
            st.session_state.selected_level = next_level
            st.rerun()

role_data = get_role_data(DATA, selected, context, track)
if not role_data:
    st.error(f"Dados não encontrados para o nível: {selected}")
    st.stop()

scope = role_data.get("scope", [])
tech = role_data.get("tech", [])
soft = role_data.get("soft", [])

if scope:
    st.markdown("### Responsabilidades")
    for s in scope:
        st.markdown(f"• {s}")

tabs = st.tabs(["Competências técnicas", "Competências não técnicas"])

with tabs[0]:
    st.caption("Clique em cada competência para ver detalhes, evidências e materiais recomendados.")
    if tech:
        for sk in tech:
            render_skill_compact(sk)
    else:
        st.info("Nenhuma competência técnica definida para este nível.")

with tabs[1]:
    st.caption("Clique em cada competência para ver detalhes, evidências e materiais recomendados.")
    if soft:
        for sk in soft:
            render_skill_compact(sk)
    else:
        st.info("Nenhuma competência não técnica definida para este nível.")

st.markdown("---")
if current_idx < len(levels) - 1:
    next_level = levels[current_idx + 1]
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        if st.button(f"Comparar com {next_level}", use_container_width=True, type="primary"):
            st.session_state.current_level = selected
            st.session_state.target_level = next_level
            st.switch_page("pages/4_Comparação.py")
