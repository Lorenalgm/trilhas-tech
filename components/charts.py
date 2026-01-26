import plotly.graph_objects as go
from typing import Dict, List, Any


def create_radar_chart(
    level_a: str,
    level_b: str,
    a_tech: List[Dict[str, Any]],
    b_tech: List[Dict[str, Any]],
    a_soft: List[Dict[str, Any]],
    b_soft: List[Dict[str, Any]],
):
    categories = {
        "Fundamentos": ["Linguagem", "Sintaxe", "Estruturas"],
        "APIs & Backend": ["API", "REST", "Endpoint", "Autenticação"],
        "Banco de Dados": ["SQL", "Database", "Banco"],
        "Arquitetura": ["Arquitetura", "Sistema", "Distribuído"],
        "Qualidade": ["Testes", "Observabilidade", "Segurança"],
        "Liderança": ["Liderança", "Mentoria", "Estratégia"],
        "Comunicação": ["Comunicação", "Documentação"],
    }
    
    # Calculate scores for each category
    def get_category_score(skills: List[Dict[str, Any]], category_keywords: List[str]):
        depth_values = {"Conhece": 1, "Aplica": 2, "Decide": 3, "Orienta": 4}
        score = 0
        count = 0
        for skill in skills:
            name_lower = skill["name"].lower()
            if any(keyword.lower() in name_lower for keyword in category_keywords):
                depth = skill.get("depth", "")
                score += depth_values.get(depth, 0)
                count += 1
        return score / max(count, 1) if count > 0 else 0
    
    cat_names = list(categories.keys())
    a_scores = [get_category_score(a_tech + a_soft, categories[cat]) for cat in cat_names]
    b_scores = [get_category_score(b_tech + b_soft, categories[cat]) for cat in cat_names]
    
    # Normalize scores to 0-5 scale
    max_score = max(max(a_scores + b_scores, default=1), 1)
    a_scores = [s * 5 / max_score for s in a_scores]
    b_scores = [s * 5 / max_score for s in b_scores]
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=a_scores + [a_scores[0]],  # Close the polygon
        theta=cat_names + [cat_names[0]],
        fill='toself',
        name=level_a,
        line=dict(color='#10B981', width=2),
        fillcolor='rgba(16, 185, 129, 0.2)',
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=b_scores + [b_scores[0]],  # Close the polygon
        theta=cat_names + [cat_names[0]],
        fill='toself',
        name=level_b,
        line=dict(color='#3B82F6', width=2),
        fillcolor='rgba(59, 130, 246, 0.2)',
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
            ),
        ),
        showlegend=True,
        legend=dict(
            x=0.5,
            y=1.15,
            xanchor='center',
        ),
        height=500,
        margin=dict(t=80, b=50, l=50, r=50),
    )
    
    return fig
