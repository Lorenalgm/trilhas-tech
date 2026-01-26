import streamlit as st
from components.render import render_header


def render():
    render_header(
        "Trilha de Carreira — Software Engineer",
        "Explore diferentes caminhos de crescimento profissional em desenvolvimento de software.",
    )
    
    st.markdown("""
    ### Sobre o Projeto
    
    Esta aplicação foi criada para ajudar desenvolvedores a entenderem e planejarem sua jornada de carreira 
    em software engineering. Aqui você pode explorar diferentes contextos de trabalho e comparar as competências 
    necessárias em cada nível de carreira.
    
    ### Como Usar
    
    1. **Configure sua trilha**: No menu lateral, selecione o contexto (Startup Early Stage ou Empresa Estruturada) 
       e a trilha (Backend ou Frontend)
    2. **Explore os níveis**: Navegue pela página "Trilha" para ver todos os níveis disponíveis
    3. **Veja detalhes**: Clique em um cargo para entender as competências técnicas e não técnicas esperadas
    4. **Compare cargos**: Use a página "Comparação" para entender o que você precisa desenvolver para evoluir
    
    ### Dicas
    
    - Cada competência tem um nível de profundidade: **Conhece**, **Aplica**, **Decide**, ou **Orienta**
    - Use a comparação para criar um plano de desenvolvimento personalizado
    - Os materiais recomendados incluem artigos, vídeos, cursos e documentação
    - Skills podem se repetir entre níveis, o que muda é a profundidade esperada
    
    ---
    
    **Feito para o Meetup do Pupunha Code** — fork e customize as trilhas via YAML.
    """)
