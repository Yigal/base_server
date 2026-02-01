"""Configuration loader utility."""

import json
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: Path) -> Dict[str, Any]:
    """
    Load configuration from config.json file.

    Args:
        config_path (Path): Path to config.json file

    Returns:
        Dict[str, Any]: Configuration dictionary

    Examples:
        >>> config = load_config(Path('config.json'))
        >>> config['run_details']['root_port']
        8000
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r') as f:
        config = json.load(f)

    return config
