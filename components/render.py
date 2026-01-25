"""Render functions for UI components"""
import streamlit as st
from typing import Dict, List, Any


def render_header(title: str, subtitle: str):
    """Render page header"""
    st.markdown(
        f"""
    <div class="hero fade-in">
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_pills(items: List[str]):
    """Render pill badges"""
    if not items:
        return
    pills_html = "".join([f"<span class='pill'>{x}</span>" for x in items])
    st.markdown(pills_html, unsafe_allow_html=True)


def render_skill_compact(skill: Dict[str, Any], tag_type: str = None):
    """
    Render a compact skill card - only name and depth, details in expander
    skill = {
      name, expectation, evidence[], resources[{title,url,type}], depth(optional)
    }
    """
    title = skill["name"]
    expectation = skill.get("expectation", "")
    evidence = skill.get("evidence", [])
    resources = skill.get("resources", [])
    depth = skill.get("depth", None)

    tag_class = ""
    if tag_type == "new":
        tag_class = "tag-new"
    elif tag_type == "deepen":
        tag_class = "tag-deepen"
    elif tag_type == "common":
        tag_class = "tag-common"

    # Show title and chip before expander
    if depth:
        depth_chip = f"<span class='chip {tag_class}'>{depth}</span>"
        st.markdown(
            f"""
            <div style="margin-bottom: 0.5rem;">
                <strong>{title}</strong> {depth_chip}
            </div>
            """,
            unsafe_allow_html=True,
        )
        expander_label = title
    else:
        expander_label = title
    
    # Compact view - details in expander
    with st.expander(f"Ver detalhes: {expander_label}", expanded=False):
        st.markdown(f"**Expectativa:** {expectation}")
        
        if evidence:
            st.markdown("**Evidências esperadas:**")
            for e in evidence:
                st.write(f"• {e}")
        
        if resources:
            st.markdown("**Materiais recomendados:**")
            for r in resources:
                label = r.get("title", "Material")
                url = r.get("url", "")
                rtype = r.get("type", "link")
                if url:
                    st.markdown(f"[{label}]({url}) - {rtype}")
                else:
                    st.markdown(f"{label} - {rtype}")


def render_skill(skill: Dict[str, Any], tag_type: str = None):
    """
    Render a skill card with evidence and resources in expanders
    skill = {
      name, expectation, evidence[], resources[{title,url,type}], depth(optional)
    }
    """
    title = skill["name"]
    expectation = skill.get("expectation", "")
    evidence = skill.get("evidence", [])
    resources = skill.get("resources", [])
    depth = skill.get("depth", None)

    tag_class = ""
    if tag_type == "new":
        tag_class = "tag-new"
    elif tag_type == "deepen":
        tag_class = "tag-deepen"
    elif tag_type == "common":
        tag_class = "tag-common"

    depth_chip = f"<span class='chip {tag_class}'>{depth}</span>" if depth else ""
    st.markdown(
        f"""
    <div class="skill fade-in">
      <div class="skill-title">{title} {depth_chip}</div>
      <div class="muted">{expectation}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Evidence + resources as Streamlit-native for better accessibility
    if evidence:
        with st.expander("Evidências esperadas", expanded=False):
            for e in evidence:
                st.write(f"• {e}")

    if resources:
        with st.expander("Materiais recomendados", expanded=False):
            for r in resources:
                label = r.get("title", "Material")
                url = r.get("url", "")
                rtype = r.get("type", "link")
                if url:
                    st.markdown(f"[{label}]({url}) - {rtype}")
                else:
                    st.markdown(f"{label} - {rtype}")
