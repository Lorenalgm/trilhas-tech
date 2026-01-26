import streamlit as st
from utils.data_loader import load_data
from utils.helpers import sort_levels, by_name, diff_skills
from components.render import render_header, render_skill_compact
from components.charts import create_radar_chart


def render():
    DATA = load_data("data/sample.yml")
    
    context = st.session_state.selected_context or list(DATA["contexts"].keys())[0]
    track = st.session_state.selected_track or list(DATA["tracks"].keys())[0]
    levels = sort_levels(DATA["contexts"][context]["levels"][track])
    
    render_header(
        "Comparar Cargos",
        "Compare duas posições para entender novas competências, aprofundamentos e diferenças.",
    )
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        current_idx = levels.index(st.session_state.current_level) if st.session_state.current_level and st.session_state.current_level in levels else 0
        a = st.selectbox(
            "Cargo Atual",
            levels,
            index=current_idx,
        )
    with col2:
        target_idx = levels.index(st.session_state.target_level) if st.session_state.target_level and st.session_state.target_level in levels else min(1, len(levels) - 1)
        b = st.selectbox(
            "Cargo Desejado",
            levels,
            index=target_idx,
        )
    
    if a == b:
        st.warning("Escolha cargos diferentes para comparar.")
        return
    
    try:
        a_data = DATA["contexts"][context]["data"][track].get(a, {})
        b_data = DATA["contexts"][context]["data"][track].get(b, {})
        if not a_data or not b_data:
            st.error(f"Erro ao carregar dados para os níveis selecionados.")
            st.stop()
    except KeyError as e:
        st.error(f"Erro ao acessar dados: {str(e)}")
        st.stop()
    
    a_tech = a_data.get("tech", [])
    b_tech = b_data.get("tech", [])
    a_soft = a_data.get("soft", [])
    b_soft = b_data.get("soft", [])
    
    # Metrics
    new_tech, common_tech, deepen_tech = diff_skills(a_tech, b_tech)
    new_soft, common_soft, deepen_soft = diff_skills(a_soft, b_soft)
    
    st.markdown("### Visão Geral")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Novas Técnicas", len(new_tech))
    c2.metric("Aprofundar Técnicas", len(deepen_tech))
    c3.metric("Novas Não Técnicas", len(new_soft))
    c4.metric("Aprofundar Não Técnicas", len(deepen_soft))
    
    # Radar chart
    st.markdown("### Comparação Visual (Gráfico de Radar)")
    try:
        fig = create_radar_chart(a, b, a_tech, b_tech, a_soft, b_soft)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.info("Gráfico de radar não disponível. Instale plotly: `pip install plotly`")
    
    # Legend
    st.markdown(
        "<span class='chip tag-new'>Novas</span>"
        "<span class='chip tag-deepen'>Aprofundar</span>"
        "<span class='chip tag-common'>Em comum</span>",
        unsafe_allow_html=True,
    )
    
    st.markdown("---")
    
    # Technical skills comparison - SIDE BY SIDE
    st.markdown("### Competências Técnicas")
    
    a_map = by_name(a_tech)
    b_map = by_name(b_tech)
    
    # Get all skills for comparison
    all_tech_skills = sorted(set(a_map.keys()) | set(b_map.keys()))
    
    # Divide into columns
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        st.markdown(f"#### {a}")
        
        # Skills only in A
        only_a = sorted(set(a_map.keys()) - set(b_map.keys()))
        if only_a:
            st.markdown("**Apenas neste cargo:**")
            for skill_name in only_a:
                skill_a = a_map.get(skill_name)
                if skill_a:
                    render_skill_compact(skill_a)
        
        # Common skills (show A version)
        common_only = sorted(common_tech - deepen_tech)
        if common_only:
            st.markdown("**Em comum:**")
            for skill_name in common_only[:5]:
                skill_a = a_map.get(skill_name)
                if skill_a:
                    render_skill_compact(skill_a, "common")
            if len(common_only) > 5:
                st.caption(f"... e mais {len(common_only) - 5} competências")
        
        # Skills to deepen (show A version)
        if deepen_tech:
            st.markdown("**Para aprofundar:**")
            for skill_name in sorted(deepen_tech):
                skill_a = a_map.get(skill_name)
                if skill_a:
                    render_skill_compact(skill_a, "deepen")
    
    with col_right:
        st.markdown(f"#### {b}")
        
        # New skills
        if new_tech:
            st.markdown("**Novas competências:**")
            for skill_name in sorted(new_tech):
                skill_b = b_map.get(skill_name)
                if skill_b:
                    render_skill_compact(skill_b, "new")
        
        # Common skills (show B version)
        common_only = sorted(common_tech - deepen_tech)
        if common_only:
            st.markdown("**Em comum:**")
            for skill_name in common_only[:5]:
                skill_b = b_map.get(skill_name)
                if skill_b:
                    render_skill_compact(skill_b, "common")
            if len(common_only) > 5:
                st.caption(f"... e mais {len(common_only) - 5} competências")
        
        # Skills to deepen (show B version - with new depth)
        if deepen_tech:
            st.markdown("**Para aprofundar:**")
            for skill_name in sorted(deepen_tech):
                skill_b = b_map.get(skill_name)
                if skill_b:
                    render_skill_compact(skill_b, "deepen")
    
    st.markdown("---")
    
    # Soft skills comparison - SIDE BY SIDE
    st.markdown("### Competências Não Técnicas")
    
    a_map_soft = by_name(a_soft)
    b_map_soft = by_name(b_soft)
    
    all_soft_skills = sorted(set(a_map_soft.keys()) | set(b_map_soft.keys()))
    
    col_left_soft, col_right_soft = st.columns(2, gap="large")
    
    with col_left_soft:
        st.markdown(f"#### {a}")
        
        only_a_soft = sorted(set(a_map_soft.keys()) - set(b_map_soft.keys()))
        if only_a_soft:
            st.markdown("**Apenas neste cargo:**")
            for skill_name in only_a_soft:
                skill_a = a_map_soft.get(skill_name)
                if skill_a:
                    render_skill_compact(skill_a)
        
        common_only_soft = sorted(common_soft - deepen_soft)
        if common_only_soft:
            st.markdown("**Em comum:**")
            for skill_name in common_only_soft[:5]:
                skill_a = a_map_soft.get(skill_name)
                if skill_a:
                    render_skill_compact(skill_a, "common")
            if len(common_only_soft) > 5:
                st.caption(f"... e mais {len(common_only_soft) - 5} competências")
        
        if deepen_soft:
            st.markdown("**Para aprofundar:**")
            for skill_name in sorted(deepen_soft):
                skill_a = a_map_soft.get(skill_name)
                if skill_a:
                    render_skill_compact(skill_a, "deepen")
    
    with col_right_soft:
        st.markdown(f"#### {b}")
        
        if new_soft:
            st.markdown("**Novas competências:**")
            for skill_name in sorted(new_soft):
                skill_b = b_map_soft.get(skill_name)
                if skill_b:
                    render_skill_compact(skill_b, "new")
        
        common_only_soft = sorted(common_soft - deepen_soft)
        if common_only_soft:
            st.markdown("**Em comum:**")
            for skill_name in common_only_soft[:5]:
                skill_b = b_map_soft.get(skill_name)
                if skill_b:
                    render_skill_compact(skill_b, "common")
            if len(common_only_soft) > 5:
                st.caption(f"... e mais {len(common_only_soft) - 5} competências")
        
        if deepen_soft:
            st.markdown("**Para aprofundar:**")
            for skill_name in sorted(deepen_soft):
                skill_b = b_map_soft.get(skill_name)
                if skill_b:
                    render_skill_compact(skill_b, "deepen")
    
    st.markdown("---")
    if st.button("← Voltar para Detalhes", use_container_width=True):
        st.session_state.current_page = "Detalhes"
        st.rerun()
