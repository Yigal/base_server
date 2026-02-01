"""Dashboard UI routes and logic."""

from flask import Blueprint, render_template, jsonify
from pathlib import Path
from typing import Dict, Any
from utils.event_logger import get_recent_events
import json


def create_ui_blueprint(config: Dict[str, Any]) -> Blueprint:
    """
    Create the UI blueprint for dashboard pages.

    Args:
        config (Dict[str, Any]): Server configuration

    Returns:
        Blueprint: Flask blueprint for UI routes

    Examples:
        >>> bp = create_ui_blueprint(config)
        >>> len(bp.deferred_functions) > 0
        True
    """
    ui = Blueprint('ui', __name__, template_folder='../templates', static_folder='../static')

    @ui.route('/')
    def main():
        """Main dashboard page."""
        return render_template('main.html', config=config)

    @ui.route('/events')
    def events():
        """Server events page showing recent requests/responses."""
        return render_template('events.html', config=config)

    @ui.route('/api-docs')
    def api_docs():
        """Interactive API documentation page."""
        routes = config.get('api_details', {}).get('routes', {})
        return render_template('api_docs.html', routes=routes, config=config)

    @ui.route('/api/events')
    def get_events():
        """API endpoint to get recent events as JSON."""
        events = get_recent_events(limit=100)
        return jsonify({'success': True, 'events': events}), 200

    @ui.route('/api/config')
    def get_config():
        """API endpoint to get server configuration."""
        return jsonify({'success': True, 'config': config}), 200

    @ui.route('/api/fastapi-source')
    def get_fastapi_source():
        """API endpoint to get FastAPI server source code."""
        from pathlib import Path
        try:
            app_py = Path('../app.py').resolve()
            if not app_py.exists():
                # Try relative path from current module
                import inspect
                module_file = inspect.getfile(inspect.currentframe())
                module_dir = Path(module_file).parent.parent
                app_py = module_dir / 'app.py'

            with open(app_py, 'r') as f:
                source = f.read()

            return jsonify({
                'success': True,
                'source': source,
                'file': str(app_py)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @ui.route('/bist')
    def bist_dashboard():
        """BIST dashboard page."""
        return render_template('bist.html', config=config)

    @ui.route('/api/bist-results')
    def get_bist_results():
        """API endpoint to get BIST test results."""
        try:
            results_file = Path('results/bist_results.json').resolve()
            if results_file.exists():
                with open(results_file, 'r') as f:
                    results = json.load(f)
                return jsonify({'success': True, 'results': results}), 200
            else:
                return jsonify({'success': False, 'error': 'No BIST results found'}), 404
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @ui.route('/api/bist-run', methods=['POST'])
    def run_bist_tests():
        """API endpoint to run BIST tests."""
        try:
            from tests.bist_runner import run_bist
            results = run_bist()
            return jsonify({'success': True, 'results': results}), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @ui.route('/docs')
    def docs():
        """Documentation manager page with folder dropdown and refresh."""
        return render_template('docs.html', config=config)

    return ui
