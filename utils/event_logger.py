"""Event logging utility for server requests and responses."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


def log_event(
    route: str,
    method: str,
    input_data: Dict[str, Any],
    output_data: Dict[str, Any],
    status: int,
    success: bool
) -> None:
    """
    Log an API event (request/response).

    Args:
        route (str): API route path
        method (str): HTTP method (GET, POST, etc.)
        input_data (Dict): Request input data
        output_data (Dict): Response output data
        status (int): HTTP status code
        success (bool): Whether the request was successful

    Examples:
        >>> log_event(
        ...     route='/api/health',
        ...     method='GET',
        ...     input_data={},
        ...     output_data={'status': 'ok'},
        ...     status=200,
        ...     success=True
        ... )
    """
    event = {
        'timestamp': datetime.utcnow().isoformat(),
        'route': route,
        'method': method,
        'input': input_data,
        'output': output_data,
        'status': status,
        'success': success
    }

    # Create events directory if it doesn't exist
    events_dir = Path('storage/events')
    events_dir.mkdir(parents=True, exist_ok=True)

    # Save event to file
    event_file = events_dir / f"{datetime.utcnow().timestamp()}.json"
    with open(event_file, 'w') as f:
        json.dump(event, f)


def get_recent_events(limit: int = 100) -> list:
    """
    Get recent logged events.

    Args:
        limit (int): Maximum number of events to return

    Returns:
        list: List of event dictionaries

    Examples:
        >>> events = get_recent_events(limit=10)
        >>> len(events)
        10
    """
    events_dir = Path('storage/events')
    if not events_dir.exists():
        return []

    events = []
    event_files = sorted(events_dir.glob('*.json'), reverse=True)[:limit]

    for event_file in event_files:
        try:
            with open(event_file, 'r') as f:
                event = json.load(f)
                events.append(event)
        except (json.JSONDecodeError, IOError):
            continue

    return events
