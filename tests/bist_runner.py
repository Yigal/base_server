"""BIST (Built-In Self Test) runner for server testing."""

import json
from pathlib import Path
from typing import Dict, Any, List
import requests


def run_bist() -> Dict[str, Any]:
    """
    Run Built-In Self Test for all configured routes.

    Tests:
    - API endpoints defined in config.json
    - External dependencies (if any)
    - Response structure validation

    Returns:
        Dict[str, Any]: Test results

    Examples:
        >>> results = run_bist()
        >>> 'endpoints' in results
        True
    """
    config_path = Path('config.json')
    if not config_path.exists():
        return {'success': False, 'error': 'config.json not found'}

    with open(config_path) as f:
        config = json.load(f)

    results = {
        'success': True,
        'endpoints': [],
        'dashboard_pages': [],
        'external_dependencies': [],
        'timestamp': str(Path.cwd())
    }

    # Test endpoints
    test_endpoints(config, results)

    # Test dashboard pages
    test_dashboard_pages(config, results)

    # Test external dependencies
    test_external_dependencies(config, results)

    # Save results
    results_dir = Path('results')
    results_dir.mkdir(exist_ok=True)
    with open(results_dir / 'bist_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    return results


def test_endpoints(config: Dict[str, Any], results: Dict[str, Any]) -> None:
    """Test all API endpoints (configured and built-in)."""
    routes = config.get('api_details', {}).get('routes', {})
    root_port = config.get('run_details', {}).get('root_port', 8000)
    api_offset = config.get('run_details', {}).get('port_offsets', {}).get('api', 1)
    api_port = root_port + api_offset

    # Built-in routes
    built_in_routes = {
        'health': {'route': '/health', 'method': 'GET'},
        'events': {'route': '/events', 'method': 'GET'},
        'get_last_100_api_calls': {'route': '/api/get_last_100_api_calls', 'method': 'GET'},
        'documentation': {'route': '/api/documentation', 'method': 'GET'},
        'get_all_routes': {'route': '/get_all_routes', 'method': 'GET'},
    }

    # Test configured routes
    for route_name, route_config in routes.items():
        route = route_config.get('route')
        method = route_config.get('method', 'GET').upper()
        _test_single_endpoint(api_port, route, method, results)

    # Test built-in routes
    for route_name, route_config in built_in_routes.items():
        route = route_config.get('route')
        method = route_config.get('method', 'GET').upper()
        _test_single_endpoint(api_port, route, method, results)


def _test_single_endpoint(api_port: int, route: str, method: str, results: Dict[str, Any]) -> None:
    """Test a single endpoint."""
    try:
        url = f'http://localhost:{api_port}{route}'
        response = requests.request(method, url, timeout=5)
        test_result = {
            'route': route,
            'method': method,
            'status': response.status_code,
            'success': 200 <= response.status_code < 300
        }
    except Exception as e:
        test_result = {
            'route': route,
            'method': method,
            'status': 0,
            'success': False,
            'error': str(e)
        }

    results['endpoints'].append(test_result)


def test_dashboard_pages(config: Dict[str, Any], results: Dict[str, Any]) -> None:
    """Test all dashboard pages for proper HTML structure."""
    root_port = config.get('run_details', {}).get('root_port', 8000)

    # Define dashboard pages to test
    pages = [
        {
            'name': 'Main Dashboard',
            'url': f'http://localhost:{root_port}/ui/',
            'required_elements': ['<html', '<head', '<title', '<body', 'Dashboard', 'stat-card']
        },
        {
            'name': 'Events',
            'url': f'http://localhost:{root_port}/ui/events',
            'required_elements': ['<html', '<head', '<title', '<body', 'Recent Server Events', 'events-container']
        },
        {
            'name': 'API Documentation',
            'url': f'http://localhost:{root_port}/ui/api-docs',
            'required_elements': ['<html', '<head', '<title', '<body', 'API Documentation', 'docsContainer', 'sourceContainer']
        },
        {
            'name': 'BIST Tests',
            'url': f'http://localhost:{root_port}/ui/bist',
            'required_elements': ['<html', '<head', '<title', '<body', 'BIST Tests', 'runAllBtn', 'bist-tabs']
        }
    ]

    for page in pages:
        try:
            response = requests.get(page['url'], timeout=5)

            # Check if status is 200 OK
            status_ok = 200 <= response.status_code < 300

            # Check if response contains valid HTML
            has_html = response.text and '<html' in response.text.lower()

            # Check for required elements
            missing_elements = []
            for element in page['required_elements']:
                if element.lower() not in response.text.lower():
                    missing_elements.append(element)

            test_result = {
                'page': page['name'],
                'url': page['url'],
                'status': response.status_code,
                'success': status_ok and has_html and len(missing_elements) == 0,
                'html_valid': has_html,
                'missing_elements': missing_elements if missing_elements else []
            }
        except Exception as e:
            test_result = {
                'page': page['name'],
                'url': page['url'],
                'status': 0,
                'success': False,
                'error': str(e)
            }

        results['dashboard_pages'].append(test_result)


def test_external_dependencies(config: Dict[str, Any], results: Dict[str, Any]) -> None:
    """Test external dependencies."""
    deps = config.get('external_dependencies', {})

    for dep_name, dep_config in deps.items():
        if not dep_config.get('enabled', False):
            continue

        try:
            url = dep_config.get('url')
            response = requests.head(url, timeout=5)
            test_result = {
                'dependency': dep_name,
                'status': response.status_code,
                'success': 200 <= response.status_code < 300
            }
        except Exception as e:
            test_result = {
                'dependency': dep_name,
                'status': 0,
                'success': False,
                'error': str(e)
            }

        results['external_dependencies'].append(test_result)
