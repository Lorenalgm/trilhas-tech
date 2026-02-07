import streamlit as st
from styles import get_css
from components.sidebar import render_sidebar
from utils.data_loader import load_data
from utils.helpers import sort_levels, get_role_data
from components.render import render_header, render_pills

st.set_page_config(
    page_title="Trilha - Trilha de carreira",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_css(), unsafe_allow_html=True)

DATA, context, track = render_sidebar()

levels = sort_levels(DATA["contexts"][context]["levels"][track])

render_header(
    f"Trilha de carreira: {DATA['tracks'][track]['name']}",
    f"Contexto: {DATA['contexts'][context]['name']}",
)

st.markdown("## Níveis")

st.markdown(
    """
    <style>
        .level-card-container {
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.6);
            height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
            margin-bottom: 1rem;
        }
        .level-card-container:hover {
            background: rgba(255, 255, 255, 0.8);
            border-color: rgba(0, 0, 0, 0.2);
        }
        .level-card-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin: 0 0 0.5rem 0;
        }
        .level-card-description {
            opacity: 0.8;
            font-size: 0.9rem;
            margin: 0.5rem 0;
            flex: 1;
        }
        .level-card-skills {
            opacity: 0.7;
            font-size: 0.85rem;
            margin-top: auto;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

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
                    
                    button_key = f"level_{level}"
                    
                    st.markdown(
                        f"""
                        <div class="level-card-container">
                            <div class="level-card-title">{level}</div>
                            <div class="level-card-skills">{tech_count} técnicas | {soft_count} soft skills</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    
                    button_clicked = st.button(
                        "Ver detalhes",
                        key=button_key,
                        use_container_width=True,
                    )
                    
                    st.markdown(
                        f"""
                        <style>
                            button[key="{button_key}"] {{
                                background: transparent !important;
                                border: none !important;
                                color: #0066cc !important;
                                text-decoration: underline !important;
                                padding: 0.5rem 0 !important;
                                margin-top: 0.5rem !important;
                                font-size: 0.9rem !important;
                                box-shadow: none !important;
                            }}
                            button[key="{button_key}"]:hover {{
                                background: transparent !important;
                                color: #0052a3 !important;
                                border: none !important;
                                box-shadow: none !important;
                            }}
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )
                    
                    if button_clicked:
                        st.session_state.selected_level = level
                        st.switch_page("pages/3_Detalhes.py")
                except Exception as e:
                    st.error(f"Erro ao carregar dados para {level}: {str(e)}")
