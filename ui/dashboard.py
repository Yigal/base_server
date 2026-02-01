"""Dashboard UI routes and logic."""

from flask import Blueprint, render_template, jsonify, send_from_directory, request
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

    @ui.route('/api/documentation-folders')
    def get_documentation_folders():
        """API endpoint to get list of all documentation folders."""
        try:
            docs_dir = Path('documentation')

            if not docs_dir.exists():
                return jsonify({
                    'success': False,
                    'error': 'Documentation directory not found'
                }), 404

            folders = []

            # Scan for all subdirectories in documentation
            for item in sorted(docs_dir.iterdir()):
                if item.is_dir():
                    folder_name = item.name
                    # Skip 'agents' folder as it contains subdirectories of agents
                    if folder_name == 'agents':
                        continue

                    # Get markdown and json files in this folder
                    markdown_files = list(item.glob('*.md'))
                    json_files = list(item.glob('*.json'))

                    file_count = len(markdown_files) + len(json_files)

                    folders.append({
                        'name': folder_name,
                        'display_name': folder_name.replace('_', ' ').title(),
                        'file_count': file_count,
                        'has_markdown': len(markdown_files) > 0,
                        'has_json': len(json_files) > 0,
                        'files': {
                            'markdown': [f.name for f in markdown_files],
                            'json': [f.name for f in json_files]
                        }
                    })

            return jsonify({
                'success': True,
                'folders': folders,
                'total': len(folders)
            }), 200

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @ui.route('/api/document')
    def get_document():
        """API endpoint to get specific document content by folder and format."""
        try:
            # Get query parameters
            folder = request.args.get('folder', 'base_server_keypoint')
            document = request.args.get('document', 'base_server_keypoints')
            format_type = request.args.get('format', 'summary_markdown')

            # Validate inputs
            if not folder or not document:
                return jsonify({
                    'success': False,
                    'error': 'Missing required parameters: folder, document'
                }), 400

            # Map format to file extension
            format_map = {
                'full_markdown': ('base_server_keypoints.md', 'markdown'),
                'summary_markdown': ('base_server_keypoints_summary.md', 'markdown'),
                'full_json': ('base_server_keypoints_full.json', 'json'),
                'summary_json': ('base_server_keypoints_summary.json', 'json')
            }

            # For other folders, dynamically determine file names
            if folder != 'base_server_keypoint':
                # Get the list of files in the folder to determine naming pattern
                folder_path = Path(f'documentation/{folder}')
                if folder_path.exists():
                    # Find the appropriate file based on format
                    markdown_files = list(folder_path.glob('*.md'))
                    json_files = list(folder_path.glob('*.json'))

                    # Map formats to available files
                    if format_type.endswith('_markdown') and markdown_files:
                        # Use the first markdown file found
                        filename = markdown_files[0].name
                        file_type = 'markdown'
                    elif format_type.endswith('_json') and json_files:
                        # Use the first json file found
                        filename = json_files[0].name
                        file_type = 'json'
                    else:
                        return jsonify({
                            'success': False,
                            'error': f'No {format_type} files found in {folder}'
                        }), 404
                else:
                    return jsonify({
                        'success': False,
                        'error': f'Folder not found: {folder}'
                    }), 404
            else:
                # Use hardcoded format_map for base_server_keypoint
                if format_type not in format_map:
                    return jsonify({
                        'success': False,
                        'error': f'Invalid format. Choose from: {list(format_map.keys())}'
                    }), 400

                filename, file_type = format_map[format_type]

            # Build file path
            file_path = Path(f'documentation/{folder}/{filename}')

            # Check if file exists
            if not file_path.exists():
                return jsonify({
                    'success': False,
                    'error': f'Document not found: {filename} in {folder}'
                }), 404

            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse if JSON
            if file_type == 'json':
                try:
                    content = json.loads(content)
                except json.JSONDecodeError as e:
                    return jsonify({
                        'success': False,
                        'error': f'Invalid JSON in file: {str(e)}'
                    }), 500

            return jsonify({
                'success': True,
                'folder': folder,
                'document': document,
                'format': format_type,
                'file_type': file_type,
                'filename': filename,
                'size': file_path.stat().st_size,
                'content': content
            }), 200

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    return ui
