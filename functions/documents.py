"""Documentation management functions."""

import json
from pathlib import Path
from flask import request, jsonify


def get_documentation_folders() -> tuple:
    """
    Get list of all available documentation folders.

    Returns:
        tuple: (response_dict, status_code)

    route_test: {
        "route_test": {
            "input": {},
            "expected_output": {"success": true, "folders": []}
        }
    }

    internal_dependencies: {
        "internal_dependencies": []
    }
    """
    try:
        docs_dir = Path('documentation')

        if not docs_dir.exists():
            return jsonify({
                "success": False,
                "error": "Documentation directory not found"
            }), 404

        folders = []

        # Scan for all subdirectories in documentation
        for item in sorted(docs_dir.iterdir()):
            if item.is_dir():
                folder_name = item.name
                # Get markdown and json files in this folder
                files = {
                    'markdown': list(item.glob('*.md')),
                    'json': list(item.glob('*.json'))
                }

                # Count files
                file_count = len(files['markdown']) + len(files['json'])

                folders.append({
                    "name": folder_name,
                    "display_name": folder_name.replace('_', ' ').title(),
                    "file_count": file_count,
                    "has_markdown": len(files['markdown']) > 0,
                    "has_json": len(files['json']) > 0
                })

        return jsonify({
            "success": True,
            "folders": folders,
            "total": len(folders)
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def get_documents() -> tuple:
    """
    Get list of available documentation with all format types.

    Returns:
        tuple: (response_dict, status_code)

    route_test: {
        "route_test": {
            "input": {},
            "expected_output": {"success": true, "documents": []}
        }
    }

    internal_dependencies: {
        "internal_dependencies": []
    }
    """
    try:
        docs_dir = Path('documentation/base_server_keypoint')

        if not docs_dir.exists():
            return jsonify({
                "success": False,
                "error": "Documentation directory not found"
            }), 404

        documents = []

        # Scan for base_server_keypoint documentation
        doc_entry = {
            "name": "Base Server Keypoints",
            "folder": "base_server_keypoint",
            "description": "Complete guide for the base_server project",
            "formats": {
                "full_markdown": None,
                "summary_markdown": None,
                "full_json": None,
                "summary_json": None
            }
        }

        # Check for markdown files
        full_md = docs_dir / "base_server_keypoints.md"
        if full_md.exists():
            doc_entry["formats"]["full_markdown"] = {
                "file": "base_server_keypoints.md",
                "path": str(full_md),
                "size": full_md.stat().st_size,
                "type": "markdown"
            }

        summary_md = docs_dir / "base_server_keypoints_summary.md"
        if summary_md.exists():
            doc_entry["formats"]["summary_markdown"] = {
                "file": "base_server_keypoints_summary.md",
                "path": str(summary_md),
                "size": summary_md.stat().st_size,
                "type": "markdown"
            }

        # Check for JSON files
        full_json = docs_dir / "base_server_keypoints_full.json"
        if full_json.exists():
            doc_entry["formats"]["full_json"] = {
                "file": "base_server_keypoints_full.json",
                "path": str(full_json),
                "size": full_json.stat().st_size,
                "type": "json"
            }

        summary_json = docs_dir / "base_server_keypoints_summary.json"
        if summary_json.exists():
            doc_entry["formats"]["summary_json"] = {
                "file": "base_server_keypoints_summary.json",
                "path": str(summary_json),
                "size": summary_json.stat().st_size,
                "type": "json"
            }

        documents.append(doc_entry)

        return jsonify({
            "success": True,
            "documents": documents,
            "total": len(documents)
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def get_document_content() -> tuple:
    """
    Get specific document content by folder, document name, and format.

    Query Parameters:
        folder (str): Document folder name (e.g., 'base_server_keypoint')
        document (str): Document name (e.g., 'base_server_keypoints')
        format (str): Format type (full_markdown, summary_markdown, full_json, summary_json)

    Returns:
        tuple: (response_dict, status_code)

    route_test: {
        "route_test": {
            "input": {
                "folder": "base_server_keypoint",
                "document": "base_server_keypoints",
                "format": "summary_markdown"
            },
            "expected_output": {"success": true, "content": "string"}
        }
    }

    internal_dependencies: {
        "internal_dependencies": []
    }
    """
    try:
        # Get query parameters
        folder = request.args.get('folder', 'base_server_keypoint')
        document = request.args.get('document', 'base_server_keypoints')
        format_type = request.args.get('format', 'summary_markdown')

        # Validate inputs
        if not folder or not document:
            return jsonify({
                "success": False,
                "error": "Missing required parameters: folder, document"
            }), 400

        # Map format to file extension
        format_map = {
            'full_markdown': ('base_server_keypoints.md', 'markdown'),
            'summary_markdown': ('base_server_keypoints_summary.md', 'markdown'),
            'full_json': ('base_server_keypoints_full.json', 'json'),
            'summary_json': ('base_server_keypoints_summary.json', 'json')
        }

        if format_type not in format_map:
            return jsonify({
                "success": False,
                "error": f"Invalid format. Choose from: {list(format_map.keys())}"
            }), 400

        filename, file_type = format_map[format_type]

        # Build file path
        file_path = Path(f'documentation/{folder}/{filename}')

        # Check if file exists
        if not file_path.exists():
            return jsonify({
                "success": False,
                "error": f"Document not found: {filename} in {folder}"
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
                    "success": False,
                    "error": f"Invalid JSON in file: {str(e)}"
                }), 500

        return jsonify({
            "success": True,
            "folder": folder,
            "document": document,
            "format": format_type,
            "file_type": file_type,
            "filename": filename,
            "size": file_path.stat().st_size,
            "content": content
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
