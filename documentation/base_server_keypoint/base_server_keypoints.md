# Base Server Project Keypoints

Complete guide for the base_server project.

## 1. Configuration Management
Section overview.

### 1.1 config.json as Central Hub
All server configuration should be defined in a single config.json file rather than hardcoding values throughout the application.

The `config.json` file is the single source of truth for all server configuration. Every route, external dependency, and port setting is defined here, eliminating hardcoded values. This approach ensures that the server can be deployed across different environments by simply changing the configuration file.

### 1.2 Configuration Structure
The config.json file must include run_details, external_dependencies, and api_details sections with specific nested properties.

The `config.json` must follow this structure:
```json
{
  "run_details": {
    "root_port": 8000,
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
Services are accessed through a root_port plus configurable offsets (e.g., root_port 8000 for dashboard, 8001 for API).

Ports are managed through the `root_port` and `port_offsets` mechanism. The root_port (e.g., 8000) serves the dashboard, and offset ports serve other services. Adding 1 to root_port gives the API port (8001). This allows multiple services to coexist without port conflicts.

### 1.4 Route Definition in Configuration
Every API route must be explicitly registered in config.json with its HTTP method, function name, file path, inputs, and expected outputs.

Each route must be explicitly defined in `config.json` under `api_details.routes`. This includes the HTTP method, function name, file path, input parameters, and expected output structure. The Flask application automatically imports and registers these routes at startup.

### 1.5 Environment Variables and .env
Sensitive credentials like API keys must be stored in a .env file that is added to .gitignore to prevent accidental exposure.

Sensitive information like API keys and passwords must be stored in a `.env` file that is never committed to version control. The application loads these at runtime. Add `.env` to `.gitignore` to prevent accidental credential exposure.

## 2. BIST (Built-In Self Test) System
Section overview.

### 2.1 What is BIST?
BIST is an automated testing framework that validates all endpoints, external dependencies, and dashboard pages are functional on server startup.

BIST is an automated testing framework that runs on server startup. It validates that all configured endpoints are functional, external dependencies are accessible, and the dashboard is operational. Results are saved to `results/bist_results.json` for inspection.

### 2.2 BIST Execution Flow
BIST runs automatically after the server starts, testing each endpoint defined in config.json and verifying external API connectivity.

When the server starts via `start.sh`, after the Docker container is running, BIST tests execute automatically. The tests probe each endpoint defined in `config.json`, verify external API connectivity, and check that all dashboard pages render correctly.

### 2.3 BIST Test Results
Test results are saved to results/bist_results.json containing endpoint status, response codes, success/failure flags, and dependency connectivity.

Test results are stored in `results/bist_results.json` with the following information:
- Endpoint name and route
- HTTP method used
- Response status code
- Response body
- Test pass/fail status
- Timestamp
- External dependency connectivity status

### 2.4 Testing External Dependencies
Each external API defined in config.json is tested to verify it's reachable and properly authenticated during BIST execution.

Each external API dependency defined in `config.json` under `external_dependencies` is tested during BIST. The system verifies that API endpoints are reachable and that any required authentication works before marking the dependency as healthy.

### 2.5 Dashboard Page Validation
BIST validates that all required dashboard pages exist and render without errors before marking the server as healthy.

The BIST framework validates that all dashboard pages (main.html, events.html, api_docs.html, etc.) exist and render without errors. If a required page is missing or has syntax errors, the test will flag it as failed.

## 3. Lifecycle Management (start.sh and stop.sh)
Section overview.

### 3.1 start.sh: Server Startup Process
The start.sh script reads configuration, checks ports, builds the Docker image, runs the container, saves the PID, and executes BIST tests.

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
The script dynamically extracts root_port and port_offsets from config.json to map container ports to the configured host ports.

The script extracts `root_port`, `port_offsets`, and `docker_image` from `config.json`. It maps the container's internal port 8000 to the configured root_port, and port 8001 (dashboard + 1) to root_port + 1. This allows changing server ports without modifying the script.

### 3.3 Docker Integration
The start.sh script builds a Docker image and runs it as a container with proper port mapping and volume mounting for persistent storage.

The `start.sh` script builds a Docker image using the `Dockerfile`, then runs it as a container. Volumes are mounted to persist storage data. The script ensures proper networking by mapping the internal container ports to the configured host ports.

### 3.4 Health Checking
After startup, the script waits for the container to initialize, retrieves its PID, and saves it for monitoring and shutdown purposes.

Before marking the server as started, `start.sh` waits 3 seconds for the container to initialize, then retrieves its PID and saves it to the file specified in `config.json`. This PID is used for monitoring and stopping the server.

### 3.5 stop.sh: Server Shutdown Process
The stop.sh script reads the PID file, stops and removes the Docker container, and cleans up related files.

The `stop.sh` script:
1. Reads the PID file from `config.json` path
2. Reads the container name from the Docker image name
3. Stops the Docker container
4. Removes the container
5. Cleans up the PID file
6. Verifies the port is freed before returning

### 3.6 Graceful Shutdown
The shutdown process cleanly stops the container before removal, allowing for any necessary cleanup operations.

The shutdown process is designed to be graceful. The container is stopped cleanly (allowing for any necessary cleanup), then removed. If shutdown fails, the script reports an error and the PID file remains so the user is aware a process might still be running.

## 4. Pages and Dashboard Structure
Section overview.

### 4.1 Three-Page Dashboard System
The server includes main.html for status, events.html for request logs, and api_docs.html for interactive API documentation.

The server includes three built-in dashboard pages accessible at `/ui/`:
1. **main.html** - Server status, port information, configuration display
2. **events.html** - Last 100 request/response logs with full details
3. **api_docs.html** - Interactive API documentation with request builder

### 4.2 Dashboard Route Registration
Dashboard routes are registered in ui/dashboard.py and map to template files in the templates/ directory.

The dashboard routes are registered in the Flask application via `ui/dashboard.py`. Each route maps to a template file. The templates are rendered from the `templates/` directory using Flask's template engine.

### 4.3 Main Dashboard Page
The main dashboard displays server name, port configuration, Docker image name, and links to other pages.

`main.html` displays:
- Server name and version
- Current port configuration (root_port and offsets)
- Docker image name
- Links to other dashboard pages
- Configuration summary
- Server uptime and status

### 4.4 Events Page
The events page shows the last 100 API requests and responses with timestamps, methods, payloads, status codes, and success indicators.

`events.html` displays a log of the last 100 API requests and responses:
- Timestamp of each request
- Route and HTTP method
- Full request payload
- Full response body
- HTTP status code
- Success/failure indicator
- Event logs can be exported or filtered by status

### 4.5 API Documentation Page
The API docs page lists all endpoints with their methods, parameters, expected outputs, and provides an interactive request builder.

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
Custom dashboard pages can be added by creating new HTML files in templates/ and registering routes in ui/dashboard.py.

Custom dashboard pages can be added by:
1. Creating a new HTML file in `templates/`
2. Registering a route in `ui/dashboard.py`
3. Adding the template name to the dashboard navigation
Templates inherit from `base.html` for consistent styling and navigation.

### 4.7 Static Files Organization
CSS and JavaScript files are organized in static/ with separate folders for css/ and js/ serving as static assets.

CSS and JavaScript files are organized in `static/`:
- `static/css/style.css` - Global styling
- `static/js/` - JavaScript functionality
These files are served directly and referenced in templates.

## 5. Function Organization and Conventions
Section overview.

### 5.1 Three Function Types
Functions are categorized as public (no prefix), private (_prefix), or dependency (dep_prefix) with specific rules for each type.

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
Every public function must include a docstring with description, return type, route_test block, and internal_dependencies block.

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
All endpoints must return success responses with {"success": true, "data": ...} and error responses with {"success": false, "error": "message"}.

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
Every function must wrap logic in try-except blocks returning appropriate error responses with 500 status for unexpected errors.

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
The route_test block in docstrings specifies sample input data and expected output structure for BIST validation.

The `route_test` block in function docstrings specifies:
- Sample input data
- Expected output structure
- This is parsed by BIST to validate the endpoint works correctly

### 5.6 Dependency Declaration
The internal_dependencies block lists all functions called by the current function for call chain tracing and circular dependency detection.

The `internal_dependencies` block lists all functions called by this function:
- Helps trace call chains
- Used by BIST to understand dependencies
- Enables circular dependency detection

## 6. Event Logging System
Section overview.

### 6.1 Automatic Event Logging
Every API request is automatically logged with timestamp, route, method, request/response data, status code, and execution time.

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
Events are stored as individual JSON files in storage/events/ with filenames formatted as TIMESTAMP_METHOD_ROUTE_STATUS.json.

Events are stored as individual JSON files in `storage/events/` with filenames like:
```
2024-01-31T14:30:45_POST_api_health_200.json
```

The format is: `TIMESTAMP_METHOD_ROUTE_STATUS.json`

### 6.3 Retrieving Event Logs
Event logs are displayed in the Events dashboard page showing the last 100 requests in reverse chronological order.

Event logs are displayed in the Events dashboard page (`/ui/events`). The dashboard fetches the last 100 events and displays them in reverse chronological order (newest first).

### 6.4 Event Data Structure
Each event JSON contains timestamp, route, method, request headers/body, response status/headers/body, and execution time.

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
The Events page provides filtering by HTTP method, status code, route path, and success/failure status with CSV/JSON export options.

The Events page provides tools to:
- Filter by HTTP method (GET, POST, etc.)
- Filter by status code (200, 400, 500, etc.)
- Search by route path
- Filter by success/failure
- Export events to CSV or JSON

## 7. Docker Containerization
Section overview.

### 7.1 Dockerfile Structure
The Dockerfile defines the base image, working directory, dependencies, exposed ports, and startup command.

The Dockerfile defines:
- Base image (Python)
- Working directory (/app)
- Dependency installation
- Port exposure (8000 and 8001)
- Startup command (python app.py)

### 7.2 Image Naming Convention
The Docker image is named in config.json using the format project-name:latest with the container name derived by appending _container.

The Docker image is named in `config.json` using the format:
```
project-name:latest
```
The container name is derived from the image name with `_container` suffix.

### 7.3 Volume Mounting
The start.sh script mounts the local storage/ folder to /app/storage allowing persistent event logs and easy host access.

The `start.sh` script mounts the local `storage/` folder to `/app/storage` in the container. This allows:
- Persistent event logs
- Access to server configuration from host
- Easy debugging and log inspection

### 7.4 Port Mapping
Docker maps container port 8000 to the configured root_port for the dashboard and port 8001 to root_port + 1 for the API.

Docker maps:
- Container port 8000 → Host root_port (dashboard)
- Container port 8001 → Host root_port + 1 (API)

This is configured in `start.sh` using values from `config.json`.

### 7.5 Environment Variables in Container
The Dockerfile can set default environment variables, and runtime variables from .env are made available to the Flask application.

The Dockerfile can include ENV instructions to set default values. Runtime environment variables from `.env` are made available to the Flask application through Python's `os.environ`.

## 8. Project Structure and File Organization
Section overview.

### 8.1 Modifiable vs Restricted Files
Users modify config.json, functions/, requirements.txt, templates/, and .env but should not modify app.py, utils/, tests/, Dockerfile, or scripts.

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
The project is organized with config at the root, user code in functions/ and templates/, internal code in utils/ and tests/, and runtime data in storage/.

```
base_server/
├── config.json                  ← All configuration here
├── requirements.txt             ← Python dependencies
├── .env                        ← API keys (gitignored)
├── .gitignore
├── Dockerfile
├── start.sh / stop.sh          ← Lifecycle scripts
│
├── app.py                      ← Main Flask application
├── README.md / START_HERE.md
│
├── functions/                  ← Your endpoint code HERE
│   └── health.py
│
├── ui/                         ← Dashboard routes
│   └── dashboard.py
│
├── templates/                  ← Dashboard HTML
│   ├── base.html
│   ├── main.html
│   ├── events.html
│   ├── api_docs.html
│   └── bist.html
│
├── static/                     ← CSS and JavaScript
│   ├── css/style.css
│   └── js/
│
├── utils/                      ← Internal utilities
│   ├── config_loader.py
│   └── event_logger.py
│
├── tests/                      ← BIST framework
│   └── bist_runner.py
│
└── storage/                    ← Auto-created at runtime
    ├── events/
    └── server.pid
```

## 9. Adding New Endpoints
Section overview.

### 9.1 Complete Endpoint Addition Workflow
Adding endpoints involves creating a function file, implementing the function, registering it in config.json, updating requirements.txt, and restarting.

Adding a new endpoint follows these steps:
1. Create a function file in `functions/` (e.g., `functions/process.py`)
2. Implement the function with correct format and documentation
3. Register the route in `config.json` under `api_details.routes`
4. Add any Python dependencies to `requirements.txt`
5. Restart the server with `./start.sh`
6. Verify BIST tests pass
7. Test the endpoint via API docs page or curl

### 9.2 Function File Creation
New endpoint files should be created in functions/ with the required function format, documentation, error handling, and return tuple.

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
Each route must be registered in config.json under api_details.routes with method, function name, file path, input parameters, and outputs.

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
After restarting, new endpoints appear in the API docs page and can be tested via the interactive builder or by checking event logs.

After restarting the server:
1. Visit `/ui/api-docs` to see the new endpoint
2. Use the interactive request builder to test
3. Check `/ui/events` for request/response logs
4. Verify BIST results in `results/bist_results.json`

## 10. External API Integration
Section overview.

### 10.1 Integrating External Services
External APIs are defined in config.json under external_dependencies with base URL, required headers, and timeout settings.

External APIs are defined in `config.json` under `external_dependencies`:
```json
{
  "external_dependencies": {
    "openai": {
      "base_url": "https://api.openai.com/v1",
      "required_headers": ["Authorization"],
      "timeout": 30
    }
  }
}
```

### 10.2 Dependency Functions
Create functions with dep_ prefix to call external APIs, and they should handle authentication, retries, and error recovery.

Create dependency functions with `dep_` prefix:
```python
def dep_call_external_api(endpoint: str, method: str = "GET") -> dict:
    """Call external API, handles auth and retries."""
    auth_header = {"Authorization": f"Bearer {os.environ.get('API_KEY')}"}
    # Implementation here
    return response.json()
```

### 10.3 Error Recovery in Dependencies
Dependency functions should implement retry logic, timeout handling, auth error recovery, rate limiting awareness, and fallbacks.

Dependency functions should include:
- Retry logic with exponential backoff
- Timeout handling
- Authentication error recovery
- Rate limiting awareness
- Fallback responses

### 10.4 Testing External Dependencies
BIST automatically tests external dependencies by making test requests and verifying connectivity, authentication, and response status.

BIST automatically tests all external dependencies by:
1. Making a test request to the base_url
2. Verifying required headers are present
3. Checking response status and timeout
4. Recording results in `bist_results.json`

## 11. Development and Deployment Workflow
Section overview.

### 11.1 Development Environment
For local development without Docker, create a virtual environment, install requirements, and run python app.py directly.

For local development without Docker:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The Flask app will run on the configured ports directly.

### 11.2 Local Testing Workflow
Development involves modifying code, updating config, restarting, testing via API docs, and reviewing event logs and BIST results.

1. Make code changes in `functions/`
2. Update `config.json` if routes changed
3. Restart with `./start.sh`
4. Test via API docs (`/ui/api-docs`)
5. Check logs at `/ui/events`
6. Review BIST results

### 11.3 Production Checklist
Before production deployment, verify all routes are configured, functions created, dependencies added, credentials set, and tests pass.

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
Production deployment involves building the Docker image, tagging for the registry, pushing to registry, updating config, and running start.sh.

1. Build the Docker image: `docker build -t my-server:latest .`
2. Tag for registry: `docker tag my-server:latest registry/my-server:latest`
3. Push to registry: `docker push registry/my-server:latest`
4. Update `config.json` with production image name
5. Copy `.env` with production credentials
6. Run `./start.sh` on production server

## 12. Troubleshooting and Debugging
Section overview.

### 12.1 Common Issues and Solutions
Common issues include port conflicts, missing config.json, function not found errors, and BIST failures, each with specific solutions.

**Port already in use:** Change `root_port` in `config.json` or kill the process using the port
**config.json not found:** Ensure `config.json` is in the same directory as `start.sh`
**Function not found:** Verify `function_file_relative_path` and function name in `config.json`
**BIST tests failing:** Check `results/bist_results.json` for specific test failures

### 12.2 Debugging Techniques
Debugging involves viewing container logs, accessing container shell, checking event logs, monitoring BIST results, or running locally.

1. View container logs: `docker logs my_server_container`
2. Access container shell: `docker exec -it my_server_container bash`
3. Check event logs: Browse `/ui/events` or read `storage/events/`
4. Monitor BIST results: `cat results/bist_results.json | jq .`
5. Run server locally: `python app.py` (no Docker)

### 12.3 Log Locations
Flask logs appear in Docker container output, event logs in storage/events/, BIST results in results/bist_results.json, and PID in storage/server.pid.

- Flask logs: Docker container stdout (view with `docker logs`)
- Event logs: `storage/events/` (JSON files)
- BIST results: `results/bist_results.json`
- Server PID: `storage/server.pid`

## 13. Configuration Reference
Section overview.

### 13.1 Configuration Parameters
Key configuration parameters include root_port, port_offsets, local_storage_folder, docker_image, and individual route properties.

| Parameter | Location | Purpose | Example |
|-----------|----------|---------|----------|
| root_port | run_details | Base port for dashboard | 8000 |
| port_offsets | run_details | Service port increments | {"api": 1} |
| local_storage_folder | run_details | Event logs directory | "./storage" |
| docker_image | run_details | Image name and tag | "my-server:latest" |
| route | api_details.routes | URL path | "/api/health" |
| method | api_details.routes | HTTP method | "GET", "POST" |
| function | api_details.routes | Function name | "health_check" |

### 13.2 Environment Variables
Sensitive information like API_KEY, EXTERNAL_API_URL, and DATABASE_URL should be stored in .env files never committed to version control.

Store in `.env` (never commit):
```
API_KEY=sk-xxxxxxxxxxxx
EXTERNAL_API_URL=https://api.example.com
DATABASE_URL=postgresql://user:pass@host/db
```

Load with: `os.environ.get('API_KEY')`

## 14. Performance Optimization
Section overview.

### 14.1 Response Optimization
Optimize responses by returning only necessary data, implementing pagination, caching frequently accessed data, and minimizing JSON payloads.

- Return only necessary data
- Use pagination for large datasets
- Cache frequently accessed data
- Minimize JSON payload size

### 14.2 Scaling Considerations
For scaling, use connection pooling, implement rate limiting, consider load balancing, and monitor response times via event logs.

- Use connection pooling for databases
- Implement request rate limiting
- Consider load balancing for multiple containers
- Monitor response times via event logs

## 15. Security Best Practices
Section overview.

### 15.1 Credential Management
Never hardcode credentials, use .env files, add .env to .gitignore, rotate credentials regularly, and maintain environment-specific configs.

- Never hardcode API keys
- Use `.env` file for all secrets
- Add `.env` to `.gitignore`
- Rotate credentials regularly
- Use environment-specific configuration

### 15.2 Input Validation
Validate all request parameters, use type hints, check request.is_json, and return 400 Bad Request for invalid inputs.

- Validate all request parameters
- Use type hints for clarity
- Check request.is_json before accessing data
- Return 400 Bad Request for invalid input

### 15.3 Output Sanitization
Avoid exposing internal error details, log full errors internally while returning generic messages, and remove sensitive data from logs.

- Don't expose internal error details
- Log full errors internally, return generic messages
- Avoid exposing system paths or file locations
- Remove sensitive data from event logs

