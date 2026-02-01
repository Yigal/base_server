# Base Server Project Keypoints - Quick Reference

Quick reference guide for the base_server project.

## 1. Configuration Management

### 1.1 config.json as Central Hub
All server configuration should be defined in a single config.json file rather than hardcoding values throughout the application.

### 1.2 Configuration Structure
The config.json file must include run_details, external_dependencies, and api_details sections with specific nested properties.

### 1.3 Port Offset System
Services are accessed through a root_port plus configurable offsets (e.g., root_port 8000 for dashboard, 8001 for API).

### 1.4 Route Definition in Configuration
Every API route must be explicitly registered in config.json with its HTTP method, function name, file path, inputs, and expected outputs.

### 1.5 Environment Variables and .env
Sensitive credentials like API keys must be stored in a .env file that is added to .gitignore to prevent accidental exposure.

## 2. BIST (Built-In Self Test) System

### 2.1 What is BIST?
BIST is an automated testing framework that validates all endpoints, external dependencies, and dashboard pages are functional on server startup.

### 2.2 BIST Execution Flow
BIST runs automatically after the server starts, testing each endpoint defined in config.json and verifying external API connectivity.

### 2.3 BIST Test Results
Test results are saved to results/bist_results.json containing endpoint status, response codes, success/failure flags, and dependency connectivity.

### 2.4 Testing External Dependencies
Each external API defined in config.json is tested to verify it's reachable and properly authenticated during BIST execution.

### 2.5 Dashboard Page Validation
BIST validates that all required dashboard pages exist and render without errors before marking the server as healthy.

## 3. Lifecycle Management (start.sh and stop.sh)

### 3.1 start.sh: Server Startup Process
The start.sh script reads configuration, checks ports, builds the Docker image, runs the container, saves the PID, and executes BIST tests.

### 3.2 Port Configuration in start.sh
The script dynamically extracts root_port and port_offsets from config.json to map container ports to the configured host ports.

### 3.3 Docker Integration
The start.sh script builds a Docker image and runs it as a container with proper port mapping and volume mounting for persistent storage.

### 3.4 Health Checking
After startup, the script waits for the container to initialize, retrieves its PID, and saves it for monitoring and shutdown purposes.

### 3.5 stop.sh: Server Shutdown Process
The stop.sh script reads the PID file, stops and removes the Docker container, and cleans up related files.

### 3.6 Graceful Shutdown
The shutdown process cleanly stops the container before removal, allowing for any necessary cleanup operations.

## 4. Pages and Dashboard Structure

### 4.1 Three-Page Dashboard System
The server includes main.html for status, events.html for request logs, and api_docs.html for interactive API documentation.

### 4.2 Dashboard Route Registration
Dashboard routes are registered in ui/dashboard.py and map to template files in the templates/ directory.

### 4.3 Main Dashboard Page
The main dashboard displays server name, port configuration, Docker image name, and links to other pages.

### 4.4 Events Page
The events page shows the last 100 API requests and responses with timestamps, methods, payloads, status codes, and success indicators.

### 4.5 API Documentation Page
The API docs page lists all endpoints with their methods, parameters, expected outputs, and provides an interactive request builder.

### 4.6 Template Extension
Custom dashboard pages can be added by creating new HTML files in templates/ and registering routes in ui/dashboard.py.

### 4.7 Static Files Organization
CSS and JavaScript files are organized in static/ with separate folders for css/ and js/ serving as static assets.

## 5. Function Organization and Conventions

### 5.1 Three Function Types
Functions are categorized as public (no prefix), private (_prefix), or dependency (dep_prefix) with specific rules for each type.

### 5.2 Function Documentation Format
Every public function must include a docstring with description, return type, route_test block, and internal_dependencies block.

### 5.3 Response Format Standard
All endpoints must return success responses with {"success": true, "data": ...} and error responses with {"success": false, "error": "message"}.

### 5.4 Error Handling Pattern
Every function must wrap logic in try-except blocks returning appropriate error responses with 500 status for unexpected errors.

### 5.5 Testing in Docstring
The route_test block in docstrings specifies sample input data and expected output structure for BIST validation.

### 5.6 Dependency Declaration
The internal_dependencies block lists all functions called by the current function for call chain tracing and circular dependency detection.

## 6. Event Logging System

### 6.1 Automatic Event Logging
Every API request is automatically logged with timestamp, route, method, request/response data, status code, and execution time.

### 6.2 Event File Storage
Events are stored as individual JSON files in storage/events/ with filenames formatted as TIMESTAMP_METHOD_ROUTE_STATUS.json.

### 6.3 Retrieving Event Logs
Event logs are displayed in the Events dashboard page showing the last 100 requests in reverse chronological order.

### 6.4 Event Data Structure
Each event JSON contains timestamp, route, method, request headers/body, response status/headers/body, and execution time.

### 6.5 Event Filtering and Search
The Events page provides filtering by HTTP method, status code, route path, and success/failure status with CSV/JSON export options.

## 7. Docker Containerization

### 7.1 Dockerfile Structure
The Dockerfile defines the base image, working directory, dependencies, exposed ports, and startup command.

### 7.2 Image Naming Convention
The Docker image is named in config.json using the format project-name:latest with the container name derived by appending _container.

### 7.3 Volume Mounting
The start.sh script mounts the local storage/ folder to /app/storage allowing persistent event logs and easy host access.

### 7.4 Port Mapping
Docker maps container port 8000 to the configured root_port for the dashboard and port 8001 to root_port + 1 for the API.

### 7.5 Environment Variables in Container
The Dockerfile can set default environment variables, and runtime variables from .env are made available to the Flask application.

## 8. Project Structure and File Organization

### 8.1 Modifiable vs Restricted Files
Users modify config.json, functions/, requirements.txt, templates/, and .env but should not modify app.py, utils/, tests/, Dockerfile, or scripts.

### 8.2 Directory Tree
The project is organized with config at the root, user code in functions/ and templates/, internal code in utils/ and tests/, and runtime data in storage/.

## 9. Adding New Endpoints

### 9.1 Complete Endpoint Addition Workflow
Adding endpoints involves creating a function file, implementing the function, registering it in config.json, updating requirements.txt, and restarting.

### 9.2 Function File Creation
New endpoint files should be created in functions/ with the required function format, documentation, error handling, and return tuple.

### 9.3 Configuration Registration
Each route must be registered in config.json under api_details.routes with method, function name, file path, input parameters, and outputs.

### 9.4 Testing New Endpoints
After restarting, new endpoints appear in the API docs page and can be tested via the interactive builder or by checking event logs.

## 10. External API Integration

### 10.1 Integrating External Services
External APIs are defined in config.json under external_dependencies with base URL, required headers, and timeout settings.

### 10.2 Dependency Functions
Create functions with dep_ prefix to call external APIs, and they should handle authentication, retries, and error recovery.

### 10.3 Error Recovery in Dependencies
Dependency functions should implement retry logic, timeout handling, auth error recovery, rate limiting awareness, and fallbacks.

### 10.4 Testing External Dependencies
BIST automatically tests external dependencies by making test requests and verifying connectivity, authentication, and response status.

## 11. Development and Deployment Workflow

### 11.1 Development Environment
For local development without Docker, create a virtual environment, install requirements, and run python app.py directly.

### 11.2 Local Testing Workflow
Development involves modifying code, updating config, restarting, testing via API docs, and reviewing event logs and BIST results.

### 11.3 Production Checklist
Before production deployment, verify all routes are configured, functions created, dependencies added, credentials set, and tests pass.

### 11.4 Deployment Steps
Production deployment involves building the Docker image, tagging for the registry, pushing to registry, updating config, and running start.sh.

## 12. Troubleshooting and Debugging

### 12.1 Common Issues and Solutions
Common issues include port conflicts, missing config.json, function not found errors, and BIST failures, each with specific solutions.

### 12.2 Debugging Techniques
Debugging involves viewing container logs, accessing container shell, checking event logs, monitoring BIST results, or running locally.

### 12.3 Log Locations
Flask logs appear in Docker container output, event logs in storage/events/, BIST results in results/bist_results.json, and PID in storage/server.pid.

## 13. Configuration Reference

### 13.1 Configuration Parameters
Key configuration parameters include root_port, port_offsets, local_storage_folder, docker_image, and individual route properties.

### 13.2 Environment Variables
Sensitive information like API_KEY, EXTERNAL_API_URL, and DATABASE_URL should be stored in .env files never committed to version control.

## 14. Performance Optimization

### 14.1 Response Optimization
Optimize responses by returning only necessary data, implementing pagination, caching frequently accessed data, and minimizing JSON payloads.

### 14.2 Scaling Considerations
For scaling, use connection pooling, implement rate limiting, consider load balancing, and monitor response times via event logs.

## 15. Security Best Practices

### 15.1 Credential Management
Never hardcode credentials, use .env files, add .env to .gitignore, rotate credentials regularly, and maintain environment-specific configs.

### 15.2 Input Validation
Validate all request parameters, use type hints, check request.is_json, and return 400 Bad Request for invalid inputs.

### 15.3 Output Sanitization
Avoid exposing internal error details, log full errors internally while returning generic messages, and remove sensitive data from logs.

