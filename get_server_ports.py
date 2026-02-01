#!/usr/bin/env python3
"""
Utility to get server ports from config.json.

This script reads the configuration and displays the actual port
numbers being used for the dashboard and API.

Usage:
    python get_server_ports.py
    python get_server_ports.py --dashboard
    python get_server_ports.py --api
    python get_server_ports.py --json
"""

import json
import sys
from pathlib import Path


def get_ports():
    """Get server ports from config.json."""
    config_path = Path('config.json')

    if not config_path.exists():
        print("Error: config.json not found", file=sys.stderr)
        sys.exit(1)

    try:
        with open(config_path) as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config.json: {e}", file=sys.stderr)
        sys.exit(1)

    run_details = config.get('run_details', {})
    root_port = run_details.get('root_port', 8000)
    port_offsets = run_details.get('port_offsets', {})

    dashboard_offset = port_offsets.get('dashboard', 0)
    api_offset = port_offsets.get('api', 1)

    dashboard_port = root_port + dashboard_offset
    api_port = root_port + api_offset

    return {
        'root_port': root_port,
        'dashboard_port': dashboard_port,
        'api_port': api_port,
        'dashboard_offset': dashboard_offset,
        'api_offset': api_offset,
    }


def main():
    """Main entry point."""
    ports = get_ports()

    # Parse command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == '--dashboard':
            print(ports['dashboard_port'])
        elif arg == '--api':
            print(ports['api_port'])
        elif arg == '--json':
            print(json.dumps(ports, indent=2))
        elif arg in ['-h', '--help']:
            print(__doc__)
        else:
            print(f"Unknown argument: {arg}", file=sys.stderr)
            print(__doc__, file=sys.stderr)
            sys.exit(1)
    else:
        # Default: print all ports
        print("╔════════════════════════════════════════════════════════╗")
        print("║              Server Ports (from config.json)           ║")
        print("╚════════════════════════════════════════════════════════╝")
        print()
        print(f"Root Port:        {ports['root_port']}")
        print(f"Dashboard Offset: {ports['dashboard_offset']}")
        print(f"API Offset:       {ports['api_offset']}")
        print()
        print(f"Dashboard Port:   {ports['dashboard_port']}")
        print(f"API Port:         {ports['api_port']}")
        print()
        print("╔════════════════════════════════════════════════════════╗")
        print(f"Dashboard:  http://localhost:{ports['dashboard_port']}/ui/")
        print(f"API:        http://localhost:{ports['api_port']}/api/")
        print("╚════════════════════════════════════════════════════════╝")


if __name__ == '__main__':
    main()
