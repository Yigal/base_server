"""Health check endpoint."""

from flask import jsonify


def health_check() -> tuple:
    """
    Health check endpoint to verify server is running.

    This is a simple endpoint that returns server status.

    Returns:
        tuple: (response_dict, status_code)

        Response format:
        {
            'success': bool,
            'status': str,
            'message': str
        }

    Examples:
        >>> response, status = health_check()
        >>> status
        200

    route_test:
    {
        "route_test": {
            "input": {},
            "expected_output": {
                "success": true,
                "status": "healthy"
            }
        }
    }

    internal_dependencies:
    {
        "internal_dependencies": []
    }
    """
    response = {
        'success': True,
        'status': 'healthy',
        'message': 'Server is running'
    }
    return jsonify(response), 200
