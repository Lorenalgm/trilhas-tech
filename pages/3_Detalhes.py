import streamlit as st
import pandas as pd
from styles import get_css
from components.sidebar import render_sidebar
from utils.data_loader import load_data
from utils.helpers import sort_levels, get_role_data
from components.render import render_header

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
    f"{selected}: {DATA['tracks'][track]['name']}",
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
    with st.container():
        for i, s in enumerate(scope, 1):
            st.markdown(f"**{i}.** {s}")

def create_skills_dataframe(skills):
    if not skills:
        return None
    
    data = []
    for skill in skills:
        depth = skill.get("depth", "N/A")
        depth_map = {
            "Conhece": "📚 Conhece",
            "Aplica": "⚙️ Aplica",
            "Decide": "🎯 Decide",
            "Orienta": "👥 Orienta"
        }
        depth_display = depth_map.get(depth, depth) if depth != "N/A" else "—"
        
        expectation = skill.get("expectation", "")
        expectation_short = expectation[:120] + "..." if len(expectation) > 120 else expectation
        
        data.append({
            "Competência": skill.get("name", ""),
            "Profundidade": depth_display,
            "Expectativa": expectation_short,
            "Evidências": len(skill.get("evidence", [])),
            "Materiais": len(skill.get("resources", [])),
            "_skill_data": skill
        })
    
    return pd.DataFrame(data)

def render_skill_details(skill, skill_name):
    with st.expander(f"{skill_name}", expanded=False):
        st.markdown(f"**Expectativa:** {skill.get('expectation', 'N/A')}")
        
        evidence = skill.get("evidence", [])
        if evidence:
            st.markdown("**Evidências esperadas:**")
            for e in evidence:
                st.markdown(f"• {e}")
        
        resources = skill.get("resources", [])
        if resources:
            st.markdown("**Materiais recomendados:**")
            for r in resources:
                label = r.get("title", "Material")
                url = r.get("url", "")
                rtype = r.get("type", "link")
                if url:
                    st.markdown(f"[{label}]({url}) - *{rtype}*")
                else:
                    st.markdown(f"{label} - *{rtype}*")

tabs = st.tabs(["Competências técnicas", "Competências não técnicas"])

with tabs[0]:
    if tech:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("#### Tabela de competências técnicas")
        with col2:
            st.metric("Total", len(tech))
        
        st.caption("Visualize todas as competências na tabela interativa abaixo. Role para ver mais detalhes de cada uma.")
        
        df_tech = create_skills_dataframe(tech)
        if df_tech is not None:
            df_display = df_tech.drop(columns=["_skill_data"])
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Competência": st.column_config.TextColumn(
                        "Competência",
                        width="medium",
                        help="Nome da competência técnica"
                    ),
                    "Profundidade": st.column_config.TextColumn(
                        "Profundidade",
                        width="small",
                        help="Nível de profundidade esperado"
                    ),
                    "Expectativa": st.column_config.TextColumn(
                        "Expectativa",
                        width="large",
                        help="Resumo da expectativa para esta competência"
                    ),
                    "Evidências": st.column_config.NumberColumn(
                        "Evidências",
                        width="small",
                        format="%d",
                        help="Quantidade de evidências esperadas"
                    ),
                    "Materiais": st.column_config.NumberColumn(
                        "Materiais",
                        width="small",
                        format="%d",
                        help="Quantidade de materiais recomendados"
                    ),
                }
            )
            
            st.markdown("---")
            st.markdown("#### Detalhes das competências")
            st.caption("Expanda cada seção para ver expectativas completas, evidências e materiais recomendados.")
            for skill in tech:
                render_skill_details(skill, skill.get("name", ""))
    else:
        st.info("Nenhuma competência técnica definida para este nível.")

with tabs[1]:
    if soft:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("#### Tabela de competências não técnicas")
        with col2:
            st.metric("Total", len(soft))
        
        st.caption("Visualize todas as competências na tabela interativa abaixo. Role para ver mais detalhes de cada uma.")
        
        df_soft = create_skills_dataframe(soft)
        if df_soft is not None:
            df_display = df_soft.drop(columns=["_skill_data"])
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Competência": st.column_config.TextColumn(
                        "Competência",
                        width="medium",
                        help="Nome da competência não técnica"
                    ),
                    "Profundidade": st.column_config.TextColumn(
                        "Profundidade",
                        width="small",
                        help="Nível de profundidade esperado"
                    ),
                    "Expectativa": st.column_config.TextColumn(
                        "Expectativa",
                        width="large",
                        help="Resumo da expectativa para esta competência"
                    ),
                    "Evidências": st.column_config.NumberColumn(
                        "Evidências",
                        width="small",
                        format="%d",
                        help="Quantidade de evidências esperadas"
                    ),
                    "Materiais": st.column_config.NumberColumn(
                        "Materiais",
                        width="small",
                        format="%d",
                        help="Quantidade de materiais recomendados"
                    ),
                }
            )
            
            st.markdown("---")
            st.markdown("#### Detalhes completos das competências")
            st.caption("Expanda cada seção para ver expectativas completas, evidências e materiais recomendados.")
            for skill in soft:
                render_skill_details(skill, skill.get("name", ""))
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
