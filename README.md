# Server Template

A production-ready Flask server template with Docker containerization, automatic testing, event logging, and a web dashboard.

## Features

- ✓ **Configuration-Driven**: Define all API routes in `config.json`
- ✓ **Docker Ready**: One-command startup with `./start.sh`
- ✓ **Event Logging**: Automatic request/response logging
- ✓ **BIST Testing**: Built-In Self Test on startup
- ✓ **Web Dashboard**: Three-page UI for monitoring
- ✓ **API Documentation**: Interactive endpoint tester
- ✓ **Guidelines Compliant**: 100% follows SERVER_GUIDELINES.md

## Quick Start

### Start the Server

```bash
./start.sh
```

This will:
1. Look for `config.json` in the current directory
2. Build the Docker image
3. Start the container with proper port mapping
4. Mount the storage folder
5. Run BIST tests

### View the Dashboard

- **Dashboard**: http://localhost:8000/ui/
- **API Port**: http://localhost:8001/

### Test an Endpoint

```bash
curl -X GET http://localhost:8001/api/health
```

### Stop the Server

```bash
./stop.sh
```

## Project Structure

```
.
├── config.json              # Server configuration (CUSTOMIZE THIS)
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container definition
├── start.sh / stop.sh      # Docker lifecycle scripts
├── .env                    # Environment variables
├── app.py                  # Main Flask application
│
├── functions/              # Your API implementations
│   ├── health.py          # Example health check
│   └── __init__.py
│
├── utils/                  # Core utilities (don't modify)
│   ├── config_loader.py
│   ├── event_logger.py
│   └── __init__.py
│
├── ui/                     # Dashboard routes
│   ├── dashboard.py
│   └── __init__.py
│
├── templates/              # HTML pages
│   ├── base.html
│   ├── main.html
│   ├── events.html
│   └── api_docs.html
│
├── static/                 # CSS and JavaScript
│   ├── css/style.css
│   └── js/
│       ├── main.js
│       └── api_docs.js
│
├── tests/                  # Test suite
│   ├── bist_runner.py
│   └── __init__.py
│
└── storage/                # Runtime data (gitignored)
    ├── events/
    └── server.pid
```

## Configuration

### config.json Structure

```json
{
    "run_details": {
        "root_port": 8000,                    // Base port
        "local_storage_folder": "./storage",  // Event storage
        "pid_file": "./storage/server.pid",   // PID file location
        "docker_image": "my-server:latest",   // Docker image name
        "port_offsets": {
            "dashboard": 0,                   // Dashboard port = root_port + 0
            "api": 1                          // API port = root_port + 1
        }
    },
    "external_dependencies": {},              // External services (optional)
    "api_details": {
        "routes": {
            "health_check": {
                "route": "/api/health",
                "method": "GET",
                "function": "health_check",
                "function_file_relative_path": "functions/health.py",
                "input": [],
                "expected_output": [
                    {
                        "status": {
                            "type": "str",
                            "required": true
                        }
                    }
                ]
            }
        }
    }
}
```

## Adding a New API Endpoint

### 1. Create Function

Create a new file in `functions/`:

```python
# functions/my_feature.py
from flask import jsonify

def my_function() -> tuple:
    """
    Your function description.

    Returns:
        tuple: (response_dict, status_code)

    route_test:
    {
        "route_test": {
            "input": {},
            "expected_output": {"success": true}
        }
    }

    internal_dependencies:
    {
        "internal_dependencies": []
    }
    """
    return jsonify({'success': True, 'data': 'result'}), 200
```

### 2. Register in config.json

```json
"my_route": {
    "route": "/api/my_endpoint",
    "method": "POST",
    "function": "my_function",
    "function_file_relative_path": "functions/my_feature.py",
    "input": [{
        "param": {
            "type": "str",
            "required": true
        }
    }],
    "expected_output": [{
        "success": {
            "type": "bool",
            "required": true
        }
    }]
}
```

### 3. Test

```bash
./start.sh
curl -X POST http://localhost:8001/api/my_endpoint \
  -H "Content-Type: application/json" \
  -d '{"param": "value"}'
./stop.sh
```

## Function Guidelines

### Public Functions

- Must have complete docstring with input/output documentation
- Must return a tuple: `(response_dict, status_code)`
- Can only call private functions in the same file
- Should be defined in their own functions file

### Private Functions

- Start with `_` prefix
- Cannot call external functions
- Used internally by public functions

### External Dependency Functions

- Prefix with `dep_` (e.g., `dep_process_data`)
- Can call public functions and external services
- Can access private functions

## External Dependencies

To add an external service (like an API):

### 1. Add to config.json

```json
"external_dependencies": {
    "my_service": {
        "enabled": false,
        "url": "https://api.service.com",
        "api_key_string": "MY_SERVICE_API_KEY"
    }
}
```

### 2. Add to .env

```
MY_SERVICE_API_KEY=your_key_here
```

### 3. BIST automatically tests the connection

## Dashboard Pages

### Main Page (/ui/)
- Server status and statistics
- Port information
- Configuration display

### Events Page (/ui/events)
- Last 100 server events
- Request and response details
- Timestamp and status information

### API Documentation (/ui/api-docs)
- Interactive endpoint tester
- JSON request builder
- Live response display
- cURL examples

## Troubleshooting

### Port Already in Use
```bash
# Change root_port in config.json
# Or kill the process:
lsof -i :8000
kill -9 <PID>
```

### Docker Build Fails
```bash
docker system prune -a
./start.sh
```

### Flask Errors
```bash
# Check Docker logs
docker logs -f my_server_container

# Or run without Docker
python app.py
```

### BIST Tests Failing
- Check `results/bist_results.json` for details
- Verify routes in `config.json` are correct
- Ensure functions exist and are callable

## Development

### Local Development (without Docker)

```bash
pip install -r requirements.txt
python app.py
```

Then visit: http://localhost:8000/

### Adding Tests

Create tests in `tests/test_api_routes.py`:

```python
def test_my_endpoint():
    client = app.test_client()
    response = client.post('/api/my_endpoint', json={'param': 'value'})
    assert response.status_code == 200
```

## Deployment

For production deployment:

1. Set environment variables in `.env`
2. Configure external services in `config.json`
3. Update `config.json` with production ports
4. Run `./start.sh`
5. Set up monitoring and backups for `storage/` folder

## Documentation Files

- **README.md** - This file
- **TEMPLATE_SETUP.md** - Detailed customization guide
- **SERVER_GUIDELINES.md** - Server architecture requirements

## License

This is a template project. Customize as needed for your use case.
