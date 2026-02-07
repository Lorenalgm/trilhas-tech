import streamlit as st
from styles import get_css
from components.sidebar import render_sidebar
from components.render import render_header

st.set_page_config(
    page_title="Início - Trilha de carreira",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

st.markdown(get_css(), unsafe_allow_html=True)

DATA, context, track = render_sidebar()

render_header(
    "Carreira em tech",
    "Explore diferentes caminhos de crescimento profissional em desenvolvimento de software.",
)

st.markdown("""
### Sobre o Projeto

Esta aplicação foi criada para ajudar desenvolvedores a entenderem e planejarem sua jornada de carreira 
em software engineering. Aqui você pode explorar diferentes contextos de trabalho e comparar as competências 
necessárias em cada nível de carreira.

### Como usar

1. **Configure sua trilha**: No menu lateral, selecione o contexto (Startup Early Stage ou Empresa Estruturada) 
   e a trilha (Backend ou Frontend)
2. **Explore os níveis**: Navegue pela página "Trilha" para ver todos os níveis disponíveis
3. **Veja detalhes**: Clique em um cargo para entender as competências técnicas e não técnicas esperadas, além de materiais recomendados. 
4. **Compare cargos**: Use a página "Comparação" para entender o que você precisa desenvolver para evoluir

### Dicas

- Cada competência tem um nível de profundidade: **Conhece**, **Aplica**, **Decide**, ou **Orienta**
- Use a comparação para criar um plano de desenvolvimento personalizado
- Skills podem se repetir entre níveis, o que muda é a profundidade esperada

---

**Feito para o Meetup do Pupunha Code** — fork e customize as trilhas via YAML.
""")