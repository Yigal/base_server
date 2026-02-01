"""Agent and Skills management functions."""

import json
from pathlib import Path
from flask import request, jsonify


def get_agents_file_names() -> tuple:
    """
    Get list of all agent files with metadata.

    Returns:
        tuple: (response_dict, status_code)
    """
    try:
        agents_dir = Path('documentation/agents')

        if not agents_dir.exists():
            return jsonify({
                "success": False,
                "error": "Agents directory not found"
            }), 404

        agents = []

        # Scan for all agent folders
        for agent_folder in sorted(agents_dir.iterdir()):
            if not agent_folder.is_dir():
                continue

            agent_name = agent_folder.name
            files = {
                'agent_md': None,
                'skills_md': None,
                'folder': agent_name
            }

            # Check for agent.md
            agent_md = agent_folder / 'agent.md'
            if agent_md.exists():
                files['agent_md'] = {
                    'name': 'agent.md',
                    'path': str(agent_md),
                    'size': agent_md.stat().st_size
                }

            # Check for skills.md
            skills_md = agent_folder / 'skills.md'
            if skills_md.exists():
                files['skills_md'] = {
                    'name': 'skills.md',
                    'path': str(skills_md),
                    'size': skills_md.stat().st_size
                }

            # Only add if it has at least one file
            if files['agent_md'] or files['skills_md']:
                # Format agent name for display
                display_name = agent_name.replace('_agent', '').replace('_', ' ').title()
                agents.append({
                    'id': agent_name,
                    'name': display_name,
                    'folder': agent_name,
                    'files': files
                })

        return jsonify({
            "success": True,
            "agents": agents,
            "total": len(agents)
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def get_agent_file() -> tuple:
    """
    Get specific agent file content (agent.md or skills.md).

    Query Parameters:
        agent (str): Agent folder name (e.g., 'code_quality_agent')
        file_type (str): 'agent' or 'skills'

    Returns:
        tuple: (response_dict, status_code)
    """
    try:
        agent = request.args.get('agent', '')
        file_type = request.args.get('file_type', 'agent')

        if not agent:
            return jsonify({
                "success": False,
                "error": "Missing required parameter: agent"
            }), 400

        if file_type not in ['agent', 'skills']:
            return jsonify({
                "success": False,
                "error": "Invalid file_type. Must be 'agent' or 'skills'"
            }), 400

        # Map file_type to filename
        filename_map = {
            'agent': 'agent.md',
            'skills': 'skills.md'
        }
        filename = filename_map[file_type]

        # Build file path
        file_path = Path(f'documentation/agents/{agent}/{filename}')

        if not file_path.exists():
            return jsonify({
                "success": False,
                "error": f"File not found: {filename} in {agent}"
            }), 404

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return jsonify({
            "success": True,
            "agent": agent,
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


def get_all_agents_and_skills() -> tuple:
    """
    Get all agent and skills files organized by agent.

    Returns:
        tuple: (response_dict, status_code)
    """
    try:
        agents_dir = Path('documentation/agents')

        if not agents_dir.exists():
            return jsonify({
                "success": False,
                "error": "Agents directory not found"
            }), 404

        all_agents = []

        # Scan for all agent folders
        for agent_folder in sorted(agents_dir.iterdir()):
            if not agent_folder.is_dir():
                continue

            agent_name = agent_folder.name
            agent_data = {
                'id': agent_name,
                'name': agent_name.replace('_agent', '').replace('_', ' ').title(),
                'folder': agent_name,
                'files': {}
            }

            # Read agent.md
            agent_md = agent_folder / 'agent.md'
            if agent_md.exists():
                with open(agent_md, 'r', encoding='utf-8') as f:
                    agent_data['files']['agent'] = {
                        'name': 'agent.md',
                        'content': f.read(),
                        'size': agent_md.stat().st_size
                    }

            # Read skills.md
            skills_md = agent_folder / 'skills.md'
            if skills_md.exists():
                with open(skills_md, 'r', encoding='utf-8') as f:
                    agent_data['files']['skills'] = {
                        'name': 'skills.md',
                        'content': f.read(),
                        'size': skills_md.stat().st_size
                    }

            # Only add if it has at least one file
            if agent_data['files']:
                all_agents.append(agent_data)

        return jsonify({
            "success": True,
            "agents": all_agents,
            "total": len(all_agents)
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
