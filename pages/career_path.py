import streamlit as st
from utils.data_loader import load_data
from utils.helpers import sort_levels, get_role_data
from components.render import render_header, render_pills


def render():
    DATA = load_data("data/sample.yml")
    
    context = st.session_state.selected_context or list(DATA["contexts"].keys())[0]
    track = st.session_state.selected_track or list(DATA["tracks"].keys())[0]
    
    levels = sort_levels(DATA["contexts"][context]["levels"][track])
    
    render_header(
        f"Trilha de Carreira — {DATA['tracks'][track]['name']}",
        f"Contexto: {DATA['contexts'][context]['name']}",
    )
    
    st.markdown("## Níveis da Trilha")
    
    cols_per_row = min(4, len(levels))
    num_rows = (len(levels) + cols_per_row - 1) // cols_per_row
    
    for row in range(num_rows):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            level_idx = row * cols_per_row + col_idx
            if level_idx < len(levels):
                level = levels[level_idx]
                with cols[col_idx]:
                    try:
                        role_data = get_role_data(DATA, level, context, track)
                        
                        scope = role_data.get("scope", [])
                        tech = role_data.get("tech", [])
                        soft = role_data.get("soft", [])
                        
                        tech_count = len(tech) if tech else 0
                        soft_count = len(soft) if soft else 0
                        
                        scope_preview = scope[0][:60] + "..." if scope and len(scope[0]) > 60 else (scope[0] if scope else "Nível de carreira")
                        
                        st.markdown(
                            f"""
                            <div style="border: 1px solid rgba(0, 0, 0, 0.1); border-radius: 12px; padding: 1.25rem; background: rgba(255, 255, 255, 0.6); margin-bottom: 1rem;">
                                <h4 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">{level}</h4>
                                <p style="margin: 0.5rem 0; opacity: 0.8; font-size: 0.9rem;">{scope_preview}</p>
                                <p style="margin: 0.5rem 0 0 0; opacity: 0.7; font-size: 0.85rem;">{tech_count} técnicas | {soft_count} soft skills</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
                        if st.button(
                            "Ver detalhes",
                            key=f"level_{level}",
                            use_container_width=True,
                        ):
                            st.session_state.selected_level = level
                            st.session_state.current_page = "Detalhes"
                            st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao carregar dados para {level}: {str(e)}")
