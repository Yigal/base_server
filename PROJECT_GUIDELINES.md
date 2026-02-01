# Base Server Project Guidelines

Complete guidelines for building and maintaining projects based on the base_server template pattern.

## 1. Configuration Management

### 1.1 config.json as Central Hub
The `config.json` file is the single source of truth for all server configuration. Every route, external dependency, and port setting is defined here, eliminating hardcoded values. This approach ensures that the server can be deployed across different environments by simply changing the configuration file.

### 1.2 Configuration Structure
The `config.json` must follow this structure:
```json
{
  "run_details": {
    "root_port": 9000,
    "local_storage_folder": "./storage",
    "pid_file": "./storage/server.pid",
    "docker_image": "my-server:latest",
    "port_offsets": {
      "dashboard": 0,
      "api": 1
    }
  },
  "external_dependencies": {},
  "api_details": {
    "routes": {}
  }
}
```

### 1.3 Port Offset System
Ports are managed through the `root_port` and `port_offsets` mechanism. The root_port (e.g., 9000) serves the dashboard, and offset ports serve other services. Adding 1 to root_port gives the API port (9001). This allows multiple services to coexist without port conflicts.

### 1.4 Route Definition in Configuration
Each route must be explicitly defined in `config.json` under `api_details.routes`. This includes the HTTP method, function name, file path, input parameters, and expected output structure. The Flask application automatically imports and registers these routes at startup.

### 1.5 Environment Variables and .env
Sensitive information like API keys and passwords must be stored in a `.env` file that is never committed to version control. The application loads these at runtime. Add `.env` to `.gitignore` to prevent accidental credential exposure.

## 2. BIST (Built-In Self Test) System

### 2.1 What is BIST?
BIST is an automated testing framework that runs on server startup. It validates that all configured endpoints are functional, external dependencies are accessible, and the dashboard is operational. Results are saved to `results/bist_results.json` for inspection.

### 2.2 BIST Execution Flow
When the server starts via `start.sh`, after the Docker container is running, BIST tests execute automatically. The tests probe each endpoint defined in `config.json`, verify external API connectivity, and check that all dashboard pages render correctly.

### 2.3 BIST Test Results
Test results are stored in `results/bist_results.json` with the following information:
- Endpoint name and route
- HTTP method used
- Response status code
- Response body
- Test pass/fail status
- Timestamp
- External dependency connectivity status

### 2.4 Testing External Dependencies
Each external API dependency defined in `config.json` under `external_dependencies` is tested during BIST. The system verifies that API endpoints are reachable and that any required authentication works before marking the dependency as healthy.

### 2.5 Dashboard Page Validation
The BIST framework validates that all dashboard pages (main.html, events.html, api_docs.html, etc.) exist and render without errors. If a required page is missing or has syntax errors, the test will flag it as failed.

## 3. Lifecycle Management (start.sh and stop.sh)

### 3.1 start.sh: Server Startup Process
The `start.sh` script automates the entire startup process:
1. Reads configuration from `config.json`
2. Checks if the server is already running and stops it if necessary
3. Verifies that required ports are available
4. Builds the Docker image
5. Runs the Docker container with proper port mapping and volume mounting
6. Saves the container PID
7. Runs BIST tests
8. Displays the dashboard and API URLs

### 3.2 Port Configuration in start.sh
The script extracts `root_port`, `port_offsets`, and `docker_image` from `config.json`. It maps the container's internal port 8000 to the configured root_port, and port 8001 (dashboard + 1) to root_port + 1. This allows changing server ports without modifying the script.

### 3.3 Docker Integration
The `start.sh` script builds a Docker image using the `Dockerfile`, then runs it as a container. Volumes are mounted to persist storage data. The script ensures proper networking by mapping the internal container ports to the configured host ports.

### 3.4 Health Checking
Before marking the server as started, `start.sh` waits 3 seconds for the container to initialize, then retrieves its PID and saves it to the file specified in `config.json`. This PID is used for monitoring and stopping the server.

### 3.5 stop.sh: Server Shutdown Process
The `stop.sh` script:
1. Reads the PID file from `config.json` path
2. Reads the container name from the Docker image name
3. Stops the Docker container
4. Removes the container
5. Cleans up the PID file
6. Verifies the port is freed before returning

### 3.6 Graceful Shutdown
The shutdown process is designed to be graceful. The container is stopped cleanly (allowing for any necessary cleanup), then removed. If shutdown fails, the script reports an error and the PID file remains so the user is aware a process might still be running.

## 4. Pages and Dashboard Structure

### 4.1 Three-Page Dashboard System
The server includes three built-in dashboard pages accessible at `/ui/`:
1. **main.html** - Server status, port information, configuration display, embedded documentation viewer
2. **events.html** - Last 100 request/response logs with full details
3. **api_docs.html** - Interactive API documentation with request builder

### 4.2 Dashboard Route Registration
The dashboard routes are registered in the Flask application via `ui/dashboard.py`. Each route maps to a template file. The templates are rendered from the `templates/` directory using Flask's template engine.

### 4.3 Main Dashboard Page
`main.html` displays:
- Server name and version
- Current port configuration (root_port and offsets)
- Docker image name
- Links to other dashboard pages
- Configuration summary
- Server uptime and status
- **Embedded documentation viewer with format selector**

### 4.4 Events Page
`events.html` displays a log of the last 100 API requests and responses:
- Timestamp of each request
- Route and HTTP method
- Full request payload
- Full response body
- HTTP status code
- Success/failure indicator
- Event logs can be exported or filtered by status

### 4.5 API Documentation Page
`api_docs.html` provides:
- List of all configured endpoints
- Method (GET, POST, PUT, DELETE, etc.)
- Request input parameters with types
- Expected output structure
- Interactive request builder
- Live response display
- Automatic cURL command generation
- Example requests

### 4.6 Template Extension
Custom dashboard pages can be added by:
1. Creating a new HTML file in `templates/`
2. Registering a route in `ui/dashboard.py`
3. Adding the template name to the dashboard navigation
Templates inherit from `base.html` for consistent styling and navigation.

### 4.7 Static Files Organization
CSS and JavaScript files are organized in `static/`:
- `static/css/style.css` - Global styling
- `static/js/` - JavaScript functionality
These files are served directly and referenced in templates.

## 5. Function Organization and Conventions

### 5.1 Three Function Types
The project uses three distinct function types, each with specific rules:

**Public Functions** (no prefix):
- Called directly by Flask routes
- Must have complete docstrings
- Can only call private functions
- Must return tuple: (dict/jsonify, status_code)

**Private Functions** (`_` prefix):
- Helper functions for public functions
- Cannot be called by Flask
- Used for internal logic and data processing
- Return any type

**Dependency Functions** (`dep_` prefix):
- Call external APIs or services
- Can access private functions
- Can call other public functions
- Handle authentication and error recovery

### 5.2 Function Documentation Format
Every public function must include:
- Description of what it does
- Return type documentation
- route_test block with test input/output
- internal_dependencies block listing functions it calls

```python
def my_function() -> tuple:
    """
    Description of what this does.

    Returns:
        tuple: (response_dict, status_code)

    route_test: {
        "route_test": {
            "input": {"key": "value"},
            "expected_output": {"success": true}
        }
    }

    internal_dependencies: {
        "internal_dependencies": ["_helper_function"]
    }
    """
```

### 5.3 Response Format Standard
All endpoints must return responses in this format:

Success response:
```python
return jsonify({"success": True, "data": {...}}), 200
```

Error response:
```python
return jsonify({"success": False, "error": "message"}), 400
```

### 5.4 Error Handling Pattern
Every public function must wrap its logic in try-except:
```python
try:
    data = request.get_json() if request.is_json else {}
    # Process logic here
    return jsonify({"success": True, "data": result}), 200
except Exception as e:
    return jsonify({"success": False, "error": str(e)}), 500
```

### 5.5 Testing in Docstring
The `route_test` block in function docstrings specifies:
- Sample input data
- Expected output structure
- This is parsed by BIST to validate the endpoint works correctly

### 5.6 Dependency Declaration
The `internal_dependencies` block lists all functions called by this function:
- Helps trace call chains
- Used by BIST to understand dependencies
- Enables circular dependency detection

## 6. Event Logging System

### 6.1 Automatic Event Logging
Every API request is automatically logged to `storage/events/` with the following information:
- Timestamp (ISO 8601 format)
- Route path
- HTTP method
- Request headers
- Request body
- Response headers
- Response body
- HTTP status code
- Execution time (in milliseconds)
- Success/failure flag

### 6.2 Event File Storage
Events are stored as individual JSON files in `storage/events/` with filenames like:
```
2024-01-31T14:30:45_POST_api_health_200.json
```

The format is: `TIMESTAMP_METHOD_ROUTE_STATUS.json`

### 6.3 Retrieving Event Logs
Event logs are displayed in the Events dashboard page (`/ui/events`). The dashboard fetches the last 100 events and displays them in reverse chronological order (newest first).

### 6.4 Event Data Structure
Each event JSON file contains:
```json
{
  "timestamp": "2024-01-31T14:30:45.123Z",
  "route": "/api/health",
  "method": "GET",
  "request": {
    "headers": {},
    "body": null,
    "query_params": {}
  },
  "response": {
    "status_code": 200,
    "headers": {"Content-Type": "application/json"},
    "body": {"success": true, "status": "healthy"}
  },
  "execution_time_ms": 12,
  "success": true
}
```

### 6.5 Event Filtering and Search
The Events page provides tools to:
- Filter by HTTP method (GET, POST, etc.)
- Filter by status code (200, 400, 500, etc.)
- Search by route path
- Filter by success/failure
- Export events to CSV or JSON

## 7. Docker Containerization

### 7.1 Dockerfile Structure
The Dockerfile defines:
- Base image (Python)
- Working directory (/app)
- Dependency installation
- Port exposure (8000 and 8001)
- Startup command (python app.py)

### 7.2 Image Naming Convention
The Docker image is named in `config.json` using the format:
```
project-name:latest
```
The container name is derived from the image name with `_container` suffix.

### 7.3 Volume Mounting
The `start.sh` script mounts the local `storage/` folder to `/app/storage` in the container. This allows:
- Persistent event logs
- Access to server configuration from host
- Easy debugging and log inspection

### 7.4 Port Mapping
Docker maps:
- Container port 8000 → Host root_port (dashboard)
- Container port 8001 → Host root_port + 1 (API)

This is configured in `start.sh` using values from `config.json`.

### 7.5 Environment Variables in Container
The Dockerfile can include ENV instructions to set default values. Runtime environment variables from `.env` are made available to the Flask application through Python's `os.environ`.

## 8. Project Structure and File Organization

### 8.1 Modifiable vs Restricted Files
**You will modify:**
- `config.json` - Define routes and external dependencies
- `functions/` - Write all API endpoint logic
- `requirements.txt` - Add Python package dependencies
- `templates/` - Customize dashboard HTML
- `.env` - Store API keys and secrets

**Do not modify:**
- `app.py` - Core Flask application
- `utils/` - Logging and configuration utilities
- `tests/` - BIST testing framework
- `Dockerfile` - Container configuration
- `start.sh` / `stop.sh` - Lifecycle scripts

### 8.2 Directory Tree
```
base_server/
├── PROJECT_GUIDELINES.md            ← Main project guidelines
├── DOCUMENTATION_GUIDELINES.md      ← Documentation guidelines
├── config.json                      ← Configuration
├── requirements.txt                 ← Dependencies
├── .env                            ← API keys
├── .gitignore
├── Dockerfile
├── start.sh / stop.sh              ← Lifecycle scripts
│
├── app.py                          ← Main Flask app
├── functions/                      ← Endpoint code
├── ui/                             ← Dashboard routes
├── templates/                      ← HTML templates
├── static/                         ← CSS and JavaScript
├── utils/                          ← Utilities
├── tests/                          ← BIST framework
│
├── documentation/                  ← Documentation system
│   ├── base_server_keypoint/
│   │   ├── base_server_keypoints_full.json
│   │   ├── base_server_keypoints_summary.json
│   │   ├── agent.md
│   │   ├── skills.md
│   │   └── schemas/
│   └── INDEX.md
│
└── storage/                        ← Runtime data
    ├── events/
    └── server.pid
```

## 9. Adding New Endpoints

### 9.1 Complete Endpoint Addition Workflow
Adding a new endpoint follows these steps:
1. Create a function file in `functions/` (e.g., `functions/process.py`)
2. Implement the function with correct format and documentation
3. Register the route in `config.json` under `api_details.routes`
4. Add any Python dependencies to `requirements.txt`
5. Restart the server with `./start.sh`
6. Verify BIST tests pass
7. Test the endpoint via API docs page or curl

### 9.2 Function File Creation
Create a new file `functions/my_endpoint.py`:
```python
from flask import request, jsonify

def my_endpoint() -> tuple:
    """
    Process user input and return result.

    Returns:
        tuple: (response_dict, status_code)

    route_test: {
        "route_test": {
            "input": {"data": "test"},
            "expected_output": {"success": true}
        }
    }

    internal_dependencies: {
        "internal_dependencies": []
    }
    """
    try:
        data = request.get_json() if request.is_json else {}
        # Your logic here
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
```

### 9.3 Configuration Registration
Add to `config.json`:
```json
{
  "api_details": {
    "routes": {
      "my_route": {
        "route": "/api/my-endpoint",
        "method": "POST",
        "function": "my_endpoint",
        "function_file_relative_path": "functions/my_endpoint.py",
        "input": [
          {"data": {"type": "dict", "required": true}}
        ],
        "expected_output": [
          {"result": {"type": "dict", "required": true}}
        ]
      }
    }
  }
}
```

### 9.4 Testing New Endpoints
After restarting the server:
1. Visit `/ui/api-docs` to see the new endpoint
2. Use the interactive request builder to test
3. Check `/ui/events` for request/response logs
4. Verify BIST results in `results/bist_results.json`

## 10. API Routes and Documentation Endpoints

### 10.1 Built-in API Routes
The server automatically registers endpoints defined in `config.json`:
- GET `/api/health` - Health check
- GET `/api/documents` - List all documents and formats
- GET `/api/document` - Retrieve specific document content

### 10.2 Dashboard API Routes
Accessible via Flask:
- GET `/ui/` - Main dashboard
- GET `/ui/events` - Events page
- GET `/ui/api-docs` - API documentation
- GET `/ui/documentation` - Documentation viewer
- GET `/ui/bist` - BIST results

### 10.3 Accessing Documentation via API
Get available documents:
```
GET /api/documents
```

Get specific document:
```
GET /api/document?folder=base_server_keypoint&document=base_server_keypoints&format=summary_json
```

Available formats:
- `summary_markdown` - Quick reference
- `full_markdown` - Complete guide
- `summary_json` - Lightweight JSON
- `full_json` - Complete JSON

## 11. Development and Deployment Workflow

### 11.1 Development Environment
For local development without Docker:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The Flask app will run on the configured ports directly.

### 11.2 Local Testing Workflow
1. Make code changes in `functions/`
2. Update `config.json` if routes changed
3. Restart with `./start.sh`
4. Test via API docs (`/ui/api-docs`)
5. Check logs at `/ui/events`
6. Review BIST results

### 11.3 Production Checklist
Before deploying to production:
- [ ] All routes defined in `config.json`
- [ ] All functions created and documented
- [ ] All dependencies added to `requirements.txt`
- [ ] All environment variables set in `.env`
- [ ] BIST tests pass successfully
- [ ] Event logging is working
- [ ] Dashboard pages render correctly
- [ ] External API integrations tested
- [ ] Error handling implemented for all endpoints
- [ ] Sensitive data removed from logs
- [ ] Docker image tested locally

### 11.4 Deployment Steps
1. Build the Docker image: `docker build -t my-server:latest .`
2. Tag for registry: `docker tag my-server:latest registry/my-server:latest`
3. Push to registry: `docker push registry/my-server:latest`
4. Update `config.json` with production image name
5. Copy `.env` with production credentials
6. Run `./start.sh` on production server

## 12. Troubleshooting and Debugging

### 12.1 Common Issues and Solutions
**Port already in use:** Change `root_port` in `config.json` or kill the process using the port
**config.json not found:** Ensure `config.json` is in the same directory as `start.sh`
**Function not found:** Verify `function_file_relative_path` and function name in `config.json`
**BIST tests failing:** Check `results/bist_results.json` for specific test failures

### 12.2 Debugging Techniques
1. View container logs: `docker logs my_server_container`
2. Access container shell: `docker exec -it my_server_container bash`
3. Check event logs: Browse `/ui/events` or read `storage/events/`
4. Monitor BIST results: `cat results/bist_results.json | jq .`
5. Run server locally: `python app.py` (no Docker)

### 12.3 Log Locations
- Flask logs: Docker container stdout (view with `docker logs`)
- Event logs: `storage/events/` (JSON files)
- BIST results: `results/bist_results.json`
- Server PID: `storage/server.pid`

## 13. Configuration Reference

### 13.1 Configuration Parameters
| Parameter | Location | Purpose | Example |
|-----------|----------|---------|---------|
| root_port | run_details | Base port for dashboard | 9000 |
| port_offsets | run_details | Service port increments | {"api": 1} |
| local_storage_folder | run_details | Event logs directory | "./storage" |
| docker_image | run_details | Image name and tag | "my-server:latest" |
| route | api_details.routes | URL path | "/api/health" |
| method | api_details.routes | HTTP method | "GET", "POST" |
| function | api_details.routes | Function name | "health_check" |

### 13.2 Environment Variables
Store in `.env` (never commit):
```
API_KEY=sk-xxxxxxxxxxxx
EXTERNAL_API_URL=https://api.example.com
DATABASE_URL=postgresql://user:pass@host/db
```

Load with: `os.environ.get('API_KEY')`

## 14. Performance and Scaling

### 14.1 Response Optimization
- Return only necessary data
- Use pagination for large datasets
- Cache frequently accessed data
- Minimize JSON payload size

### 14.2 Scaling Considerations
- Use connection pooling for databases
- Implement request rate limiting
- Consider load balancing for multiple containers
- Monitor response times via event logs

## 15. Security Best Practices

### 15.1 Credential Management
- Never hardcode API keys
- Use `.env` file for all secrets
- Add `.env` to `.gitignore`
- Rotate credentials regularly
- Use environment-specific configuration

### 15.2 Input Validation
- Validate all request parameters
- Use type hints for clarity
- Check request.is_json before accessing data
- Return 400 Bad Request for invalid input

### 15.3 Output Sanitization
- Don't expose internal error details
- Log full errors internally, return generic messages
- Avoid exposing system paths or file locations
- Remove sensitive data from event logs
