"""Data loading utilities"""
import yaml
from typing import Dict, Any


def load_data(path: str) -> Dict[str, Any]:
    """Load YAML data file"""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
