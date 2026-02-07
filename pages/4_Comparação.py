import streamlit as st
import pandas as pd
from styles import get_css
from components.sidebar import render_sidebar
from utils.data_loader import load_data
from utils.helpers import sort_levels, by_name, diff_skills, get_role_data
from components.render import render_header
from components.charts import create_radar_chart


def _render_comparison_table(
    a_name: str,
    b_name: str,
    a_map: dict,
    b_map: dict,
    new_skills: set,
    common_skills: set,
    deepen_skills: set,
    all_skills: list
):
    rows = []
    
    for skill_name in all_skills:
        skill_a = a_map.get(skill_name)
        skill_b = b_map.get(skill_name)
        
        a_status = ""
        b_status = ""
        a_depth = skill_a.get("depth", "") if skill_a else ""
        b_depth = skill_b.get("depth", "") if skill_b else ""
        
        if skill_name in new_skills:
            b_status = "🟢 Nova"
        elif skill_name in deepen_skills:
            a_status = "🟡 Aprofundar"
            b_status = "🟡 Aprofundar"
        elif skill_name in common_skills:
            a_status = "⚪ Em comum"
            b_status = "⚪ Em comum"
        else:
            a_status = "⚪ Apenas aqui"
        
        depth_a = f" ({a_depth})" if a_depth else ""
        depth_b = f" ({b_depth})" if b_depth else ""
        
        rows.append({
            "Competência": skill_name,
            a_name: f"{a_status}{depth_a}",
            b_name: f"{b_status}{depth_b}",
        })
    
    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Competência": st.column_config.TextColumn("Competência", width="medium"),
            a_name: st.column_config.TextColumn(a_name, width="large"),
            b_name: st.column_config.TextColumn(b_name, width="large"),
        }
    )


st.set_page_config(
    page_title="Comparação - Trilha de carreira",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_css(), unsafe_allow_html=True)

DATA, context, track = render_sidebar()

levels = sort_levels(DATA["contexts"][context]["levels"][track])

render_header(
    "Comparar cargos",
    "Compare duas posições para entender novas competências, aprofundamentos e diferenças.",
)

col1, col2 = st.columns(2, gap="large")
with col1:
    current_level = st.session_state.get("current_level")
    current_idx = levels.index(current_level) if current_level in levels else 0
    a = st.selectbox("Cargo atual", levels, index=current_idx)
with col2:
    target_level = st.session_state.get("target_level")
    target_idx = levels.index(target_level) if target_level in levels else min(1, len(levels) - 1)
    b = st.selectbox("Cargo desejado", levels, index=target_idx)

if a == b:
    st.warning("Escolha cargos diferentes para comparar.")
    st.stop()

a_data = get_role_data(DATA, a, context, track)
b_data = get_role_data(DATA, b, context, track)
if not a_data or not b_data:
    st.error("Erro ao carregar dados para os níveis selecionados.")
    st.stop()

a_tech = a_data.get("tech", [])
b_tech = b_data.get("tech", [])
a_soft = a_data.get("soft", [])
b_soft = b_data.get("soft", [])

new_tech, common_tech, deepen_tech = diff_skills(a_tech, b_tech)
new_soft, common_soft, deepen_soft = diff_skills(a_soft, b_soft)

st.markdown("### Visão Geral")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Novas técnicas", len(new_tech))
c2.metric("Aprofundar técnicas", len(deepen_tech))
c3.metric("Novas não técnicas", len(new_soft))
c4.metric("Aprofundar não técnicas", len(deepen_soft))

try:
    fig = create_radar_chart(a, b, a_tech, b_tech, a_soft, b_soft)
    st.plotly_chart(fig, use_container_width=True)
except Exception:
    st.info("Gráfico de radar não disponível.")

st.markdown("### Competências técnicas")
a_map_tech = by_name(a_tech)
b_map_tech = by_name(b_tech)
all_tech_skills = sorted(set(a_map_tech.keys()) | set(b_map_tech.keys()))

_render_comparison_table(
    a, b, a_map_tech, b_map_tech, new_tech, common_tech, deepen_tech, all_tech_skills
)

st.markdown("### Competências não técnicas")
a_map_soft = by_name(a_soft)
b_map_soft = by_name(b_soft)
all_soft_skills = sorted(set(a_map_soft.keys()) | set(b_map_soft.keys()))

_render_comparison_table(
    a, b, a_map_soft, b_map_soft, new_soft, common_soft, deepen_soft, all_soft_skills
)

if st.button("← Voltar para Detalhes", use_container_width=True):
    st.switch_page("pages/3_Detalhes.py")
