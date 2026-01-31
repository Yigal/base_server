# Template Index and Navigation Guide

Complete guide to all files in the server template.

## Documentation Files

### README.md
**Size**: ~6KB | **Read first**
- Overview of the template
- Quick start guide
- Features and capabilities
- Project structure explanation
- Common tasks
- Troubleshooting guide

**Read this if**: You're new to the template

### TEMPLATE_SETUP.md
**Size**: ~8KB | **Read for customization**
- Step-by-step customization guide
- Configuration options
- Adding new endpoints
- External service integration
- Dashboard customization
- Testing instructions
- Common patterns

**Read this if**: You're setting up your own server

### QUICK_REFERENCE.md
**Size**: ~4KB | **Keep handy**
- Common commands
- Testing examples
- File organization quick lookup
- Function templates
- Response formats
- Error handling patterns

**Use this for**: Quick lookups while developing

## Configuration Files

### config.json
**Purpose**: Server configuration
**Must edit for**: Port settings, API routes, external dependencies
**Example**:
```json
{
    "run_details": {
        "root_port": 8000,
        "docker_image": "my-server:latest"
    },
    "api_details": {
        "routes": { /* Your routes here */ }
    }
}
```

### requirements.txt
**Purpose**: Python package dependencies
**Must edit for**: Adding new packages
**Example**:
```
Flask==3.0.0
python-dotenv==1.0.0
requests==2.31.0
```

### .env
**Purpose**: Environment variables and secrets
**Keep private**: Never commit to git
**Example**:
```
MY_API_KEY=secret_key_value
EXTERNAL_SERVICE_TOKEN=token_value
```

### .dockerignore
**Purpose**: Files to exclude from Docker build
**Read only**: Not needed for customization

### Dockerfile
**Purpose**: Docker container configuration
**Edit only if**: Changing base image or entry point

## Script Files

### start.sh
**Purpose**: Start the server with Docker
**When to run**: `./start.sh`
**What it does**:
1. Checks config.json exists
2. Builds Docker image
3. Starts container with port mapping
4. Mounts storage folder
5. Runs BIST tests
6. Displays URLs for dashboard and API

### stop.sh
**Purpose**: Stop the running server
**When to run**: `./stop.sh`
**What it does**:
1. Stops Docker container
2. Removes container
3. Deletes PID file

## Core Application Files

### app.py
**Purpose**: Main Flask application
**Key functions**:
- `create_app()` - Creates Flask instance
- `register_routes()` - Dynamically registers API routes from config.json
- Route wrappers for automatic event logging

**Don't modify**: Core Flask logic
**Can extend**: Add custom error handlers

## Utilities Directory (/utils)

### config_loader.py
**Purpose**: Load and parse config.json
**Key functions**:
- `load_config(path)` - Load configuration file
- `get_route_config(config, name)` - Get specific route config

**Don't modify**: Configuration loading logic

### event_logger.py
**Purpose**: Automatic request/response logging
**Key functions**:
- `log_event()` - Log a single event
- `get_recent_events(limit)` - Retrieve recent events

**Don't modify**: Logging mechanism

## UI Directory (/ui)

### dashboard.py
**Purpose**: Flask blueprint for dashboard routes
**Key functions**:
- `create_ui_blueprint(config)` - Create UI routes
- Routes: `/ui/`, `/ui/events`, `/ui/api-docs`

**Can modify**: Add custom dashboard routes
**Can extend**: Add new dashboard pages

## API Functions Directory (/functions)

### health.py
**Purpose**: Example health check endpoint
**Route**: GET /api/health
**Use as reference**: For writing your own functions

**Edit to replace**: With your custom functions
**Add more files**: Create new files for additional endpoints

### Structure Expected
Each function file should:
- Import `jsonify` from Flask
- Define one or more public functions
- Return `tuple: (response_dict, status_code)`
- Include full documentation

## Templates Directory (/templates)

### base.html
**Purpose**: Base HTML template with sidebar navigation
**Contains**: Layout, sidebar, navigation structure
**Extend in**: Other templates using `{% extends "base.html" %}`

**Can modify**: Navigation items, overall layout

### main.html
**Purpose**: Main dashboard page
**Route**: /ui/
**Displays**: Server statistics and status

**Should modify**: Add your custom metrics and status displays

### events.html
**Purpose**: Server events page
**Route**: /ui/events
**Displays**: Last 100 API requests/responses

**Can customize**: Event display format, filtering

### api_docs.html
**Purpose**: Interactive API documentation
**Route**: /ui/api-docs
**Features**:
- Lists all endpoints from config.json
- Interactive request builder
- Live response display

**Don't modify**: Core functionality
**Can customize**: Styling, layout

## Static Assets Directory (/static)

### css/style.css
**Purpose**: Dashboard styling
**Key sections**:
- Sidebar styling
- Dashboard grid layout
- Card styles
- Responsive design

**Should modify**: Colors, fonts, layout to match branding
**Follow pattern**: Use existing class names for consistency

### js/main.js
**Purpose**: Main JavaScript utilities
**Functions**:
- `fetchJSON()` - Fetch and parse JSON
- `formatJSON()` - Format JSON for display

**Can extend**: Add custom JavaScript logic
**Use for**: Dashboard interactivity

### js/api_docs.js
**Purpose**: API documentation interactive features
**Functions**:
- `selectEndpoint()` - Switch between endpoints
- `testEndpoint()` - Test endpoint and show results

**Don't modify**: Core functionality
**Can extend**: Add custom testing features

## Tests Directory (/tests)

### bist_runner.py
**Purpose**: Built-In Self Test suite
**Key functions**:
- `run_bist()` - Run all tests
- `test_endpoints()` - Test API endpoints
- `test_external_dependencies()` - Test external services

**When runs**: Automatically when server starts
**Results stored in**: results/bist_results.json

**Don't modify**: BIST framework
**Can extend**: Add custom tests

## Runtime Files (Auto-Created)

### storage/
**Purpose**: Runtime data storage
**Contains**:
- `events/` - JSON files for each API event
- `server.pid` - Process ID file

**Auto-created by**: start.sh
**Keep in gitignore**: These are runtime files

### results/
**Purpose**: Test results
**Contains**:
- `bist_results.json` - BIST test results

**Auto-created by**: BIST runner on startup

## File Dependencies

```
app.py
├── config.json (reads)
├── .env (loads)
├── utils/config_loader.py
├── utils/event_logger.py
└── ui/dashboard.py
    ├── templates/
    │   ├── base.html
    │   ├── main.html
    │   ├── events.html
    │   └── api_docs.html
    ├── static/
    │   ├── css/style.css
    │   ├── js/main.js
    │   └── js/api_docs.js
    └── utils/event_logger.py (for events)

config.json
└── functions/ (defines which functions to call)
    └── Each function file returns (response, status)
```

## Modification Guide by Purpose

### I Want to...

**Add a new API endpoint**
1. Edit: `config.json` (add route)
2. Create: `functions/my_module.py` (implement function)
3. Run: `./start.sh`

**Integrate an external service**
1. Edit: `config.json` (add to external_dependencies)
2. Edit: `.env` (add API key)
3. Create: `functions/dependencies.py` (with `dep_` prefix function)
4. Run: `./start.sh`

**Customize the dashboard**
1. Edit: `templates/main.html` (layout)
2. Edit: `static/css/style.css` (styling)
3. Edit: `static/js/main.js` (behavior)
4. Run: `./start.sh`

**Change server port**
1. Edit: `config.json` (root_port)
2. Run: `./start.sh`

**Add Python dependencies**
1. Edit: `requirements.txt`
2. Run: `./start.sh`

**View server events**
1. Visit: `http://localhost:8000/ui/events`
2. Or view: `storage/events/*.json`

**Debug server issues**
1. Check: `docker logs my-server_container`
2. Check: `results/bist_results.json`
3. Run: `python app.py` (local testing)

## File Size Summary

| File | Lines | Purpose |
|------|-------|---------|
| app.py | ~150 | Main Flask app |
| config.json | ~30 | Configuration |
| templates/main.html | ~40 | Dashboard |
| templates/api_docs.html | ~90 | API docs page |
| static/css/style.css | ~200 | Styling |
| TEMPLATE_SETUP.md | ~300 | Setup guide |
| README.md | ~250 | Overview |
| Total | ~2000+ | Entire template |

## Best Practices

### Functions
- ✓ Use docstrings with examples
- ✓ Return `(response_dict, status_code)` tuple
- ✓ Handle errors gracefully
- ✓ Log all events automatically
- ✗ Don't hardcode configuration
- ✗ Don't skip error handling

### Configuration
- ✓ Keep config.json clean
- ✓ Use external_dependencies for services
- ✓ Document all routes
- ✓ Specify expected input/output
- ✗ Don't commit .env file
- ✗ Don't hardcode API keys

### Deployment
- ✓ Test locally first
- ✓ Run BIST tests
- ✓ Check event logs
- ✓ Monitor storage folder
- ✗ Don't modify core files
- ✗ Don't bypass error handling

## Getting Started Path

1. **First**: Read README.md (5 min)
2. **Second**: Run `./start.sh` to see it work (2 min)
3. **Third**: Browse dashboard at http://localhost:8000/ui/ (2 min)
4. **Fourth**: Read TEMPLATE_SETUP.md (10 min)
5. **Fifth**: Create your first endpoint (15 min)
6. **Always**: Keep QUICK_REFERENCE.md handy

## Quick Links

- **Documentation**: See top of this file
- **Common Commands**: See QUICK_REFERENCE.md
- **Setup Instructions**: See TEMPLATE_SETUP.md
- **Configuration**: Edit config.json
- **Add Endpoints**: Create in functions/, register in config.json
- **Dashboard**: Run `./start.sh`, visit http://localhost:8000/ui/
- **API**: Visit http://localhost:8001/api/
- **Events**: Visit http://localhost:8000/ui/events

## File Checklist

Essential files to exist:
- [ ] config.json
- [ ] requirements.txt
- [ ] .env
- [ ] Dockerfile
- [ ] start.sh (executable)
- [ ] stop.sh (executable)
- [ ] app.py
- [ ] utils/config_loader.py
- [ ] utils/event_logger.py
- [ ] ui/dashboard.py
- [ ] templates/base.html
- [ ] templates/main.html
- [ ] static/css/style.css
- [ ] static/js/main.js
- [ ] tests/bist_runner.py
- [ ] functions/health.py (at minimum)

All files present: ✓

## Support

- **Quick answers**: Check QUICK_REFERENCE.md
- **How to customize**: Read TEMPLATE_SETUP.md
- **Understand structure**: Read this file (TEMPLATE_INDEX.md)
- **Full overview**: Read README.md
- **Stuck?**: Check results/bist_results.json for errors
