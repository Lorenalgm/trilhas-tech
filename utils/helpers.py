import re
import streamlit as st
from typing import Dict, List, Any, Tuple, Set

LEVEL_ORDER = ["Estágio", "Júnior", "Pleno", "Sênior", "Staff", "Líder", "Principal"]


def init_session_state():
    """Inicializa os valores do session_state se não existirem."""
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


def by_name(skills: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {s["name"].strip(): s for s in skills}


def _parse_level(level: str) -> tuple:
    base_order = {name: i for i, name in enumerate(LEVEL_ORDER)}
    match = re.match(r'^(\w+)\s+(\d+)$', level)
    if match:
        base_name = match.group(1)
        number = int(match.group(2))
        base_idx = base_order.get(base_name, 999)
        return (base_idx, number, level)
    
    base_idx = base_order.get(level, 999)
    return (base_idx, 0, level)


def sort_levels(levels: List[str]) -> List[str]:
    return sorted(levels, key=_parse_level)


def diff_skills(a: List[Dict[str, Any]], b: List[Dict[str, Any]]) -> Tuple[Set[str], Set[str], Set[str]]:
    a_map = by_name(a)
    b_map = by_name(b)

    a_set = set(a_map.keys())
    b_set = set(b_map.keys())
    new = b_set - a_set
    common = a_set & b_set

    depth_ladder = ["Conhece", "Aplica", "Decide", "Orienta"]
    dpos = {d: i for i, d in enumerate(depth_ladder)}

    deepen = set()
    for name in common:
        da = a_map[name].get("depth", "")
        db = b_map[name].get("depth", "")
        if da and db and dpos.get(db, 0) > dpos.get(da, 0):
            deepen.add(name)

    return new, common, deepen


def get_role_data(data: Dict[str, Any], level: str, context: str, track: str) -> Dict[str, Any]:
    levels_data = data.get("levels", {})
    
    base_level_match = re.match(r'^(\w+)(?:\s+\d+)?$', level)
    if base_level_match:
        base_level = base_level_match.group(1)
    else:
        base_level = level
    
    if base_level not in levels_data:
        return {}
    
    level_data = levels_data[base_level]
    
    if context not in level_data:
        return {}
    
    context_data = level_data[context]
    
    if track in context_data:
        return context_data[track]
    
    if context == "established" and level != base_level:
        if level in context_data:
            track_data = context_data[level].get(track, {})
            return track_data
    
    return {}
