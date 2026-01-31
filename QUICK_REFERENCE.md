# Quick Reference

Common commands and patterns for the server template.

## Startup and Shutdown

```bash
# Start server with Docker
./start.sh

# Stop server
./stop.sh

# Run locally (without Docker)
python app.py

# Restart
./stop.sh && ./start.sh
```

## Testing

```bash
# Test health endpoint
curl -X GET http://localhost:8001/api/health

# Test with JSON data
curl -X POST http://localhost:8001/api/my_endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# Test with form data
curl -X POST http://localhost:8001/api/my_endpoint \
  -d "key=value"

# View BIST results
cat results/bist_results.json

# Check Docker logs
docker logs -f my-server_container
```

## Configuration

```bash
# View current config
cat config.json

# Edit ports
# Edit root_port in config.json, then restart

# Add new endpoint
# 1. Create function in functions/
# 2. Add route to config.json
# 3. Restart with ./start.sh
```

## Dashboard

```
# Main page
http://localhost:8000/ui/

# Events page (last 100 requests)
http://localhost:8000/ui/events

# API documentation (interactive tester)
http://localhost:8000/ui/api-docs
```

## File Organization

```
config.json              ← Modify routes here
requirements.txt         ← Add Python packages
functions/              ← Add new API functions
templates/              ← Modify dashboard HTML
static/                 ← Add CSS/JavaScript
.env                    ← API keys (don't commit)
storage/                ← Runtime data (auto-created)
```

## Common Tasks

### Add a New Endpoint

1. Create function in `functions/new_feature.py`
2. Add to `config.json`:
```json
"new_route": {
    "route": "/api/new",
    "method": "POST",
    "function": "new_function",
    "function_file_relative_path": "functions/new_feature.py",
    "input": [],
    "expected_output": []
}
```
3. Restart: `./start.sh`

### Add External API

1. Add to `config.json`:
```json
"external_dependencies": {
    "my_api": {
        "enabled": true,
        "url": "https://api.example.com",
        "api_key_string": "MY_API_KEY"
    }
}
```
2. Add to `.env`: `MY_API_KEY=your_key`
3. Create function with `dep_` prefix
4. Restart: `./start.sh`

### View Server Events

```bash
# Via dashboard
open http://localhost:8000/ui/events

# Via API
curl http://localhost:8000/ui/api/events | jq

# View raw event files
ls storage/events/
```

### Debug Port Issues

```bash
# Check what's using port 8000
lsof -i :8000

# Kill process using port
kill -9 <PID>

# Or change port in config.json
# Edit root_port, then restart
```

### Docker Troubleshooting

```bash
# View running containers
docker ps

# View logs
docker logs my-server_container

# Enter container
docker exec -it my-server_container bash

# Remove container
docker rm my-server_container

# Remove image
docker rmi my-server:latest

# Clean up all unused Docker resources
docker system prune -a
```

## Environment Variables

Add to `.env`:

```
# External services
MY_API_KEY=your_key
ANOTHER_SERVICE_TOKEN=token_value

# Flask settings
FLASK_ENV=production
FLASK_DEBUG=0

# Custom settings
MY_SETTING=value
```

Access in code:
```python
import os
api_key = os.getenv('MY_API_KEY')
```

## File Structure Quick Reference

```
/config.json                 Main configuration
/requirements.txt           Python dependencies
/Dockerfile                Docker image definition
/start.sh                  Start server
/stop.sh                   Stop server
/.env                      Environment variables

/app.py                    Flask application
/functions/                ← Add your API functions here
  /health.py              Example endpoint
  /my_feature.py          Your new functions

/utils/                    Core utilities (don't modify)
  /config_loader.py
  /event_logger.py

/ui/                       Dashboard routes
  /dashboard.py

/templates/                ← Customize HTML
  /base.html
  /main.html
  /events.html
  /api_docs.html

/static/                   ← Add CSS/JavaScript
  /css/style.css
  /js/main.js

/tests/                    Test suite
  /bist_runner.py

/storage/                  ← Auto-created runtime data
  /events/
  /server.pid
```

## Function Template

```python
"""Module docstring."""

from flask import request, jsonify


def my_function() -> tuple:
    """
    Brief description.

    Returns:
        tuple: (response, status_code)

    route_test: {
        "route_test": {
            "input": {},
            "expected_output": {}
        }
    }

    internal_dependencies: {
        "internal_dependencies": []
    }
    """
    try:
        data = request.get_json() if request.is_json else {}
        # Your code here
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

## Response Format

All endpoints should return:

```python
# Success
return jsonify({
    'success': True,
    'data': {...}
}), 200

# Error
return jsonify({
    'success': False,
    'error': 'Error message'
}), 400
```

## Common HTTP Methods

```python
# Get request data
data = request.get_json()

# Get query parameters
param = request.args.get('param')

# Get form data
form_data = request.form

# Get request method
method = request.method

# Get request headers
headers = request.headers
```

## Error Handling

```python
def my_function() -> tuple:
    try:
        # Your code
        if not valid:
            return jsonify({'success': False, 'error': 'Invalid input'}), 400
        return jsonify({'success': True}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Server error'}), 500
```

## Status Codes

```
200 OK                   - Success
201 Created              - Resource created
400 Bad Request          - Invalid input
401 Unauthorized         - Authentication required
403 Forbidden            - Permission denied
404 Not Found            - Resource not found
500 Internal Server Error - Server error
503 Service Unavailable  - Service down
```

## Testing Checklist

- [ ] Endpoint returns correct status code
- [ ] Response matches expected_output in config.json
- [ ] Error handling works
- [ ] External dependencies tested
- [ ] BIST tests passing
- [ ] Events logged correctly
- [ ] Dashboard shows recent events
