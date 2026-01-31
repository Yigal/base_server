# Server Template - Start Here

Welcome! This is a production-ready Flask server template that follows all SERVER_GUIDELINES.md requirements.

## What You Get

A complete, tested server template with:
- ✓ Flask REST API framework
- ✓ Configuration-driven routes (no hardcoding)
- ✓ Docker containerization
- ✓ Automatic BIST testing
- ✓ Event logging system
- ✓ Web dashboard (3 pages)
- ✓ Interactive API documentation
- ✓ External service integration support

## Your First 5 Minutes

### 1. See It Working (1 minute)

```bash
cd /Users/yigalweinberger/Documents/Code/server_template
./start.sh
```

### 2. Open Dashboard (1 minute)

Open your browser to:
- **Main Dashboard**: http://localhost:8000/ui/
- **API**: http://localhost:8001/api/

### 3. Test Health Endpoint (1 minute)

```bash
curl http://localhost:8001/api/health
```

You should see:
```json
{
    "success": true,
    "status": "healthy",
    "message": "Server is running"
}
```

### 4. View Recent Events (1 minute)

Visit: http://localhost:8000/ui/events

### 5. Stop Server (1 minute)

```bash
./stop.sh
```

## Documentation Map

Read in this order:

1. **This file (START_HERE.md)** - You're reading it!
   - Overview and quick start

2. **README.md** (7 min)
   - Features overview
   - Project structure
   - Common tasks

3. **TEMPLATE_SETUP.md** (15 min) - When ready to customize
   - Step-by-step customization
   - Adding endpoints
   - Configuration options

4. **QUICK_REFERENCE.md** - Keep open while coding
   - Common commands
   - Code snippets
   - Troubleshooting

5. **TEMPLATE_INDEX.md** (5 min) - For navigation
   - File-by-file reference
   - What each file does
   - Modification guide

## 30-Minute Customization

Want to make it yours? Follow these steps:

### Step 1: Configure (5 min)

Edit `config.json`:
```json
{
    "run_details": {
        "root_port": 8000,
        "docker_image": "my-server:latest"
    }
}
```

### Step 2: Create First Endpoint (10 min)

Create `functions/process.py`:
```python
from flask import request, jsonify

def process_data() -> tuple:
    """Process input data."""
    try:
        data = request.get_json()
        result = {"processed": True, "input": data}
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
```

### Step 3: Register Route (5 min)

Add to `config.json`:
```json
{
    "api_details": {
        "routes": {
            "process": {
                "route": "/api/process",
                "method": "POST",
                "function": "process_data",
                "function_file_relative_path": "functions/process.py",
                "input": [{"data": {"type": "dict", "required": true}}],
                "expected_output": [{"result": {"type": "dict", "required": true}}]
            }
        }
    }
}
```

### Step 4: Test (10 min)

```bash
./start.sh

# Test your endpoint
curl -X POST http://localhost:8001/api/process \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

./stop.sh
```

Done! You now have a custom API endpoint.

## File Organization

**You will modify:**
- `config.json` - Define your routes here
- `functions/` - Write your API logic here
- `requirements.txt` - Add Python packages
- `templates/` - Customize dashboard HTML
- `.env` - Add API keys (never commit!)

**You won't touch:**
- `app.py` - Core Flask app
- `utils/` - Logging and config
- `tests/` - BIST framework
- `Dockerfile` - Container setup

## Key Features Explained

### Configuration-Driven Routes

No hardcoding endpoints. Define everything in `config.json`:

```json
{
    "routes": {
        "my_route": {
            "route": "/api/endpoint",
            "method": "POST",
            "function": "my_function",
            "function_file_relative_path": "functions/module.py"
        }
    }
}
```

Flask automatically:
1. Imports your function
2. Registers the route
3. Logs all requests/responses
4. Tests the endpoint on startup

### Automatic Event Logging

Every API call is logged automatically:
- Timestamp
- Route and method
- Full input data
- Full output data
- HTTP status
- Success/failure flag

View in dashboard or `storage/events/` folder.

### BIST Testing

On startup, the server automatically:
1. Tests all API endpoints
2. Tests external dependencies
3. Saves results to `results/bist_results.json`
4. Displays results in events page

### Web Dashboard

Three built-in pages:

**Main Dashboard** (/ui/)
- Server status
- Port information
- Configuration display

**Events Page** (/ui/events)
- Last 100 requests
- Full request/response details
- Timestamps and status codes

**API Documentation** (/ui/api-docs)
- List of all endpoints
- Interactive request builder
- Live response display
- cURL examples

## Function Guidelines

### Correct Function Format

```python
def my_function() -> tuple:
    """
    Description of what this does.

    Returns:
        tuple: (response_dict, status_code)

    route_test: {
        "route_test": {
            "input": {},
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

### Three Types of Functions

**Public Functions** (no prefix)
- Called by Flask
- Can only call private functions
- Must have full documentation

**Private Functions** (`_` prefix)
- Helper functions
- Used by public functions
- Cannot call external functions

**Dependency Functions** (`dep_` prefix)
- Call external APIs
- Can access private functions
- Can call public functions

## Response Format

All endpoints should return:

```python
# Success
return jsonify({
    "success": True,
    "data": {...your data...}
}), 200

# Error
return jsonify({
    "success": False,
    "error": "Error message"
}), 400
```

## Common Tasks

### Add a New Endpoint
1. Create function in `functions/`
2. Register in `config.json`
3. Restart: `./start.sh`

### Integrate External API
1. Add to `config.json` external_dependencies
2. Add API key to `.env`
3. Create `dep_` function
4. Restart: `./start.sh`

### Change Port
1. Edit `root_port` in `config.json`
2. Restart: `./start.sh`

### View Events
1. Visit: http://localhost:8000/ui/events
2. Or read: `storage/events/*.json`

### Debug Issues
1. Check: `results/bist_results.json`
2. View logs: `docker logs my-server_container`
3. Test locally: `python app.py`

## Directory Structure at a Glance

```
server_template/
├── START_HERE.md                    ← You are here
├── README.md                        ← Overview
├── TEMPLATE_SETUP.md               ← Customization guide
├── QUICK_REFERENCE.md              ← Commands & snippets
├── TEMPLATE_INDEX.md               ← File reference
│
├── config.json                      ← Define your routes HERE
├── requirements.txt                 ← Add packages HERE
├── .env                            ← API keys HERE
│
├── app.py                          ← Main Flask app
├── Dockerfile                      ← Container config
├── start.sh / stop.sh             ← Start/stop scripts
│
├── functions/                      ← Your API code HERE
│   └── health.py                  ← Example
│
├── templates/                      ← Dashboard HTML
│   ├── main.html
│   ├── events.html
│   └── api_docs.html
│
├── static/                         ← CSS and JavaScript
│   ├── css/style.css
│   └── js/
│
├── utils/                          ← Don't modify
│   ├── config_loader.py
│   └── event_logger.py
│
├── ui/                            ← Dashboard routes
│   └── dashboard.py
│
├── tests/                         ← Don't modify
│   └── bist_runner.py
│
└── storage/                       ← Auto-created
    ├── events/                   ← Event logs
    └── server.pid               ← Process ID
```

## Getting Help

**Quick questions?** → QUICK_REFERENCE.md
**How to customize?** → TEMPLATE_SETUP.md
**What does this file do?** → TEMPLATE_INDEX.md
**Stuck?** → Check README.md troubleshooting section
**Command format?** → See examples in QUICK_REFERENCE.md

## Production Checklist

Before deploying:
- [ ] Updated `config.json` with your routes
- [ ] Created functions in `functions/`
- [ ] Updated `requirements.txt`
- [ ] Set environment variables in `.env`
- [ ] Tested with `./start.sh`
- [ ] Verified BIST tests pass
- [ ] Checked event logging works
- [ ] Customized dashboard (if needed)
- [ ] Set up monitoring
- [ ] Configured external services
- [ ] Tested error handling
- [ ] Reviewed logs

## Next Steps

### Right Now (5 min)
1. Run `./start.sh`
2. Visit http://localhost:8000/ui/
3. Test API at http://localhost:8001/api/health
4. Run `./stop.sh`

### Soon (30 min)
1. Read README.md
2. Create your first endpoint
3. Update config.json
4. Test with `./start.sh`

### When Ready (1-2 hours)
1. Follow TEMPLATE_SETUP.md
2. Add all your endpoints
3. Customize dashboard
4. Set up external services
5. Deploy!

---

## Quick Start Commands

```bash
# Start server
./start.sh

# Stop server
./stop.sh

# Test endpoint
curl http://localhost:8001/api/health

# View dashboard
open http://localhost:8000/ui/

# Check logs
docker logs my-server_container

# Run locally (no Docker)
python app.py

# View events (last 100 requests)
cat storage/events/* | jq .
```

---

**Ready to dive in?**

1. **See it work**: `./start.sh` then visit http://localhost:8000/ui/
2. **Learn setup**: Read TEMPLATE_SETUP.md
3. **Start coding**: Create endpoint in functions/, register in config.json
4. **Deploy**: Follow production checklist above

Good luck! 🚀

For detailed information, see the documentation files listed above.
