"""Job details page"""
import streamlit as st
from utils.data_loader import load_data
from utils.helpers import sort_levels
from components.render import render_header, render_skill_compact


def render():
    """Render job details page with compact skill list"""
    DATA = load_data("data/sample.yml")
    
    context = st.session_state.selected_context or list(DATA["contexts"].keys())[0]
    track = st.session_state.selected_track or list(DATA["tracks"].keys())[0]
    selected = st.session_state.selected_level or sort_levels(DATA["contexts"][context]["levels"][track])[0]
    
    levels = sort_levels(DATA["contexts"][context]["levels"][track])
    current_idx = levels.index(selected) if selected in levels else 0
    
    render_header(
        f"{selected} — {DATA['tracks'][track]['name']}",
        f"Contexto: {DATA['contexts'][context]['name']}",
    )
    
    # Navigation buttons - more discrete
    col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
    with col_nav1:
        if current_idx > 0:
            prev_level = levels[current_idx - 1]
            if st.button("← Anterior", key="nav_prev", use_container_width=True, type="secondary"):
                st.session_state.selected_level = prev_level
                st.rerun()
    with col_nav2:
        if st.button("Voltar para Trilha", key="nav_home", use_container_width=True, type="secondary"):
            st.session_state.current_page = "Trilha"
            st.rerun()
    with col_nav3:
        if current_idx < len(levels) - 1:
            next_level = levels[current_idx + 1]
            if st.button("Próximo →", key="nav_next", use_container_width=True, type="secondary"):
                st.session_state.selected_level = next_level
                st.rerun()
    
    try:
        role_data = DATA["contexts"][context]["data"][track].get(selected, {})
        if not role_data:
            st.error(f"Dados não encontrados para o nível: {selected}")
            st.stop()
    except KeyError:
        st.error(f"Erro ao acessar dados para o nível: {selected}")
        st.stop()
    
    scope = role_data.get("scope", [])
    tech = role_data.get("tech", [])
    soft = role_data.get("soft", [])
    
    if scope:
        st.markdown("### Responsabilidades")
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.6); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(0, 0, 0, 0.1); margin: 1rem 0;">
        """, unsafe_allow_html=True)
        for s in scope:
            st.markdown(f"• {s}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    tabs = st.tabs(["Competências Técnicas", "Competências Não Técnicas"])
    
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
    
    # Compare with next level button
    st.markdown("---")
    if current_idx < len(levels) - 1:
        next_level = levels[current_idx + 1]
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button(f"Comparar com {next_level}", use_container_width=True, type="primary"):
                st.session_state.current_level = selected
                st.session_state.target_level = next_level
                st.session_state.current_page = "Comparação"
                st.rerun()
