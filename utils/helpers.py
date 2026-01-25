"""Helper functions"""
import re
from typing import Dict, List, Any, Tuple, Set

LEVEL_ORDER = ["Estágio", "Júnior", "Pleno", "Sênior", "Staff", "Líder", "Principal"]


def by_name(skills: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Convert skills list to dict by name"""
    return {s["name"].strip(): s for s in skills}


def _parse_level(level: str) -> tuple:
    """
    Parse level name to get base level and number for sorting.
    Returns (base_level_index, number, original_string)
    """
    # Base level order
    base_order = {name: i for i, name in enumerate(LEVEL_ORDER)}
    
    # Try to match patterns like "Júnior 1", "Pleno 2", etc.
    match = re.match(r'^(\w+)\s+(\d+)$', level)
    if match:
        base_name = match.group(1)
        number = int(match.group(2))
        base_idx = base_order.get(base_name, 999)
        return (base_idx, number, level)
    
    # Simple level without number
    base_idx = base_order.get(level, 999)
    return (base_idx, 0, level)


def sort_levels(levels: List[str]) -> List[str]:
    """Sort levels according to LEVEL_ORDER, supporting numbered levels"""
    return sorted(levels, key=_parse_level)


def diff_skills(a: List[Dict[str, Any]], b: List[Dict[str, Any]]) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Compare A -> B:
    - new: exists in B but not in A
    - common: exists both
    - deepen: common but depth changed/increased (heuristic)
    """
    a_map = by_name(a)
    b_map = by_name(b)

    a_set = set(a_map.keys())
    b_set = set(b_map.keys())
    new = b_set - a_set
    common = a_set & b_set

    # Depth heuristic: compare index in known depth ladder
    depth_ladder = ["Conhece", "Aplica", "Decide", "Orienta"]
    dpos = {d: i for i, d in enumerate(depth_ladder)}

    deepen = set()
    for name in common:
        da = a_map[name].get("depth", "")
        db = b_map[name].get("depth", "")
        if da and db and dpos.get(db, 0) > dpos.get(da, 0):
            deepen.add(name)

    return new, common, deepen
