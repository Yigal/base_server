"""
Main application for the server.

This application runs:
- Flask on port 8000 for the dashboard UI
- FastAPI on port 8001 for the REST API

Both servers run concurrently using threading.
"""

import json
import sys
import threading
from pathlib import Path
from typing import Callable

from flask import Flask, jsonify, redirect
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.config_loader import load_config
from utils.event_logger import log_event, get_recent_events
from ui.dashboard import create_ui_blueprint


def create_flask_app():
    """Create and configure the Flask application for the dashboard."""
    app = Flask(__name__)

    # Load environment variables
    load_dotenv(PROJECT_ROOT / '.env')

    # Load configuration
    config_path = PROJECT_ROOT / 'config.json'
    if not config_path.exists():
        raise FileNotFoundError(f"config.json not found at {config_path}")

    config = load_config(config_path)
    app.config['APP_CONFIG'] = config

    # Register UI blueprint (dashboard)
    ui_blueprint = create_ui_blueprint(config)
    app.register_blueprint(ui_blueprint, url_prefix='/ui')

    # Root route - redirect to dashboard
    @app.route('/')
    def root():
        """Redirect root to dashboard."""
        return redirect('/ui/')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 'Not found'}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

    return app, config


def create_fastapi_app(config: dict, flask_app: Flask):
    """Create and configure the FastAPI application for the API."""
    app = FastAPI(title="Server API")

    # Add CORS middleware to allow requests from dashboard
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routes from config
    register_fastapi_routes(app, config, flask_app)

    return app


def register_fastapi_routes(app: FastAPI, config: dict, flask_app: Flask):
    """Dynamically register API routes from config.json using FastAPI."""
    routes = config.get('api_details', {}).get('routes', {})

    for route_name, route_config in routes.items():
        route = route_config.get('route')
        method = route_config.get('method', 'POST').upper()
        function_name = route_config.get('function')
        function_file = route_config.get('function_file_relative_path')

        if not all([route, function_name, function_file]):
            print(f"Warning: Incomplete route config for {route_name}")
            continue

        try:
            # Import the function
            module_path = str(PROJECT_ROOT / function_file)
            spec = __import__('importlib.util').util.spec_from_file_location(
                f"functions.{function_name}",
                module_path
            )
            module = __import__('importlib.util').util.module_from_spec(spec)
            spec.loader.exec_module(module)

            func = getattr(module, function_name)

            # Create a wrapper that logs events
            def create_wrapper(fn, route_cfg):
                async def wrapper(http_request: Request, body: dict = None):
                    try:
                        # Build query string from FastAPI request
                        from urllib.parse import urlencode
                        query_params = dict(http_request.query_params)
                        query_string = urlencode(query_params) if query_params else ""

                        # Call function with Flask app context and query parameters
                        with flask_app.test_request_context('/?{}'.format(query_string)):
                            response, status = fn()
                            # Extract JSON from Flask response
                            response_data = response.get_json() if hasattr(response, 'get_json') else response

                        log_event(
                            route=route_cfg.get('route'),
                            method=route_cfg.get('method'),
                            input_data=body or query_params or {},
                            output_data=response_data,
                            status=status,
                            success=(status >= 200 and status < 300)
                        )
                        return JSONResponse(content=response_data, status_code=status)
                    except Exception as e:
                        error_response = {'success': False, 'error': str(e)}
                        log_event(
                            route=route_cfg.get('route'),
                            method=route_cfg.get('method'),
                            input_data=body or dict(http_request.query_params) or {},
                            output_data=error_response,
                            status=500,
                            success=False
                        )
                        return JSONResponse(content=error_response, status_code=500)
                return wrapper

            wrapper = create_wrapper(func, route_config)

            # Register the route based on HTTP method
            if method == 'GET':
                app.get(route)(wrapper)
            elif method == 'POST':
                app.post(route)(wrapper)
            elif method == 'PUT':
                app.put(route)(wrapper)
            elif method == 'DELETE':
                app.delete(route)(wrapper)
            elif method == 'PATCH':
                app.patch(route)(wrapper)

            print(f"Registered FastAPI route: {method} {route} -> {function_name}")

        except Exception as e:
            print(f"Error registering route {route_name}: {e}")

    # Add built-in routes for events and monitoring
    @app.get("/events")
    async def get_events_json():
        """Get the last 100 API events as JSON."""
        events = get_recent_events(limit=100)
        return {"success": True, "events": events, "count": len(events)}

    @app.get("/api/get_last_100_api_calls")
    async def get_last_100_api_calls():
        """Get the last 100 API calls (alternate endpoint)."""
        events = get_recent_events(limit=100)
        return {"success": True, "events": events, "count": len(events)}

    @app.get("/api/documentation")
    async def get_api_documentation():
        """Get complete API documentation for all routes."""
        return _build_documentation(config)

    @app.get("/get_all_routes")
    async def get_all_routes():
        """Get documentation of all API endpoints."""
        return _build_documentation(config)

    def _build_documentation(cfg: dict) -> dict:
        """Build complete API documentation."""
        routes = cfg.get('api_details', {}).get('routes', {})

        documentation = {
            "success": True,
            "server_info": {
                "name": "Server API",
                "version": "1.0.0",
                "description": "REST API Server with event logging and monitoring"
            },
            "routes": {}
        }

        # Add configured routes
        for route_name, route_config in routes.items():
            documentation["routes"][route_name] = {
                "route": route_config.get('route'),
                "method": route_config.get('method', 'GET'),
                "function": route_config.get('function'),
                "description": f"Route: {route_config.get('route')}",
                "file": route_config.get('function_file_relative_path'),
                "input": route_config.get('input', []),
                "output": route_config.get('expected_output', []),
                "example_curl": f"curl -X {route_config.get('method', 'GET')} http://localhost:8001{route_config.get('route')}"
            }

        # Add built-in routes
        documentation["routes"]["events"] = {
            "route": "/events",
            "method": "GET",
            "function": "get_events_json",
            "description": "Get the last 100 API events with full request/response details",
            "input": [],
            "output": [{"success": {"type": "bool"}, "events": {"type": "list"}, "count": {"type": "int"}}],
            "example_curl": "curl http://localhost:8001/events"
        }

        documentation["routes"]["get_last_100_api_calls"] = {
            "route": "/api/get_last_100_api_calls",
            "method": "GET",
            "function": "get_last_100_api_calls",
            "description": "Get the last 100 API calls (alternate endpoint)",
            "input": [],
            "output": [{"success": {"type": "bool"}, "events": {"type": "list"}, "count": {"type": "int"}}],
            "example_curl": "curl http://localhost:8001/api/get_last_100_api_calls"
        }

        documentation["routes"]["health"] = {
            "route": "/health",
            "method": "GET",
            "function": "health_check",
            "description": "Health check endpoint - verify server is running",
            "input": [],
            "output": [{"success": {"type": "bool"}, "status": {"type": "str"}, "message": {"type": "str"}}],
            "example_curl": "curl http://localhost:8001/health"
        }

        documentation["routes"]["documentation"] = {
            "route": "/api/documentation",
            "method": "GET",
            "function": "get_api_documentation",
            "description": "Get complete API documentation",
            "input": [],
            "output": [{"success": {"type": "bool"}, "routes": {"type": "dict"}}],
            "example_curl": "curl http://localhost:8001/api/documentation"
        }

        documentation["routes"]["get_all_routes"] = {
            "route": "/get_all_routes",
            "method": "GET",
            "function": "get_all_routes",
            "description": "Get documentation of all API endpoints",
            "input": [],
            "output": [{"success": {"type": "bool"}, "routes": {"type": "dict"}}],
            "example_curl": "curl http://localhost:8001/get_all_routes"
        }

        return documentation

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"success": True, "status": "healthy", "message": "FastAPI Server is running"}

    print("Registered FastAPI route: GET /events -> get_events_json")
    print("Registered FastAPI route: GET /api/get_last_100_api_calls -> get_last_100_api_calls")
    print("Registered FastAPI route: GET /api/documentation -> get_api_documentation")
    print("Registered FastAPI route: GET /get_all_routes -> get_all_routes")
    print("Registered FastAPI route: GET /health -> health_check")


def run_flask_app(app: Flask):
    """Run Flask server on port 8000."""
    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)


def run_fastapi_app(app: FastAPI):
    """Run FastAPI server on port 8001."""
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001, log_level='info')


def run_bist_tests():
    """Run BIST tests after startup."""
    try:
        from tests.bist_runner import run_bist
        print("Running BIST tests...")
        run_bist()
    except ImportError:
        print("BIST tests not available")
    except Exception as e:
        print(f"BIST tests error: {e}")


if __name__ == '__main__':
    # Create Flask app (dashboard on port 8000)
    flask_app, config = create_flask_app()

    # Create FastAPI app (API on port 8001)
    fastapi_app = create_fastapi_app(config, flask_app)

    # Run BIST tests
    run_bist_tests()

    # Start Flask in main thread
    print("Starting Flask dashboard on port 8000...")
    print("Starting FastAPI on port 8001...")

    # Run FastAPI in a background thread
    fastapi_thread = threading.Thread(target=run_fastapi_app, args=(fastapi_app,), daemon=False)
    fastapi_thread.start()

    # Run Flask in main thread
    flask_app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)
