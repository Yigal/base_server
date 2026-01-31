# Template Customization Guide

Complete step-by-step guide to customize this server template for your specific needs.

## Step 1: Rename Your Server

Replace `my-server` and `my_server` throughout the project:

### Files to Update

**config.json**
```json
{
    "run_details": {
        "docker_image": "your-server-name:latest"
    }
}
```

**start.sh / stop.sh**
- Container name is derived from `docker_image`
- No changes needed if you update config.json

**Dockerfile (optional)**
- Update the CMD line if different entry point needed

## Step 2: Update Configuration (config.json)

### Port Configuration

```json
{
    "run_details": {
        "root_port": 9000,  // Change base port
        "docker_image": "my-server:latest"
    }
}
```

### Add Your First API Route

```json
{
    "api_details": {
        "routes": {
            "my_route": {
                "route": "/api/my_endpoint",
                "method": "POST",
                "function": "my_function",
                "function_file_relative_path": "functions/my_module.py",
                "input": [
                    {
                        "param_name": {
                            "type": "str",
                            "required": true,
                            "default": "value"
                        }
                    }
                ],
                "expected_output": [
                    {
                        "result": {
                            "type": "dict",
                            "required": true
                        }
                    }
                ]
            }
        }
    }
}
```

## Step 3: Create Your API Functions

### Basic Function Template

Create `functions/my_module.py`:

```python
"""My module description."""

from flask import request, jsonify


def my_function() -> tuple:
    """
    Brief description of what this function does.

    More detailed description if needed.

    Args:
        None (can add parameters as needed)

    Returns:
        tuple: (response_dict, status_code)

        Response format:
        {
            'success': bool,
            'data': any,
            'error': str (optional)
        }

    Examples:
        >>> response, status = my_function()
        >>> status
        200

    route_test:
    {
        "route_test": {
            "input": {},
            "expected_output": {
                "success": true,
                "data": {...}
            }
        }
    }

    internal_dependencies:
    {
        "internal_dependencies": []
    }
    """
    try:
        # Get request data
        data = request.get_json() if request.is_json else {}

        # Your business logic here
        result = process_data(data)

        return jsonify({
            'success': True,
            'data': result
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def _process_data(data: dict) -> dict:
    """
    Private helper function.

    Private functions start with underscore and can only call
    other private functions in the same file.
    """
    return data
```

## Step 4: Update Dependencies

Edit `requirements.txt` to add your packages:

```
Flask==3.0.0
python-dotenv==1.0.0
requests==2.31.0
# Add your dependencies:
numpy==1.24.0
pandas==2.0.0
```

Then rebuild with `./start.sh`.

## Step 5: Configure External Services

To integrate an external API or service:

### 1. Add to config.json

```json
{
    "external_dependencies": {
        "my_service": {
            "enabled": true,
            "url": "https://api.myservice.com",
            "api_key_string": "MY_SERVICE_API_KEY"
        }
    }
}
```

### 2. Add to .env

```
MY_SERVICE_API_KEY=your_actual_key_here
```

### 3. Create dependency function

Create in `functions/dependencies.py`:

```python
"""External service integrations."""

import os
import requests
from flask import jsonify


def dep_call_external_service() -> tuple:
    """
    Call an external service with proper error handling.

    Dependency functions (prefix dep_) can call external services
    and public functions from other modules.
    """
    try:
        api_key = os.getenv('MY_SERVICE_API_KEY')
        if not api_key:
            raise ValueError('API key not configured')

        response = requests.get(
            'https://api.myservice.com/endpoint',
            headers={'Authorization': f'Bearer {api_key}'},
            timeout=5
        )
        response.raise_for_status()

        return jsonify({
            'success': True,
            'data': response.json()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

### 4. BIST Will Auto-Test

The BIST test suite will automatically:
- Check if the external service is reachable
- Verify the API key is configured
- Report results in the events page

## Step 6: Customize Dashboard

### Main Dashboard Page

Edit `templates/main.html` to display your metrics:

```html
<div class="stat-card">
    <h3>Your Custom Metric</h3>
    <p class="stat-value">{{ your_data.value }}</p>
    <p class="stat-label">{{ your_data.label }}</p>
</div>
```

### Styling

Edit `static/css/style.css` for custom styling:

```css
/* Your custom styles */
:root {
    --primary-color: #3498db;
    --secondary-color: #2c3e50;
}
```

### JavaScript

Add custom JavaScript in `static/js/main.js`:

```javascript
// Your custom code
async function loadCustomData() {
    const response = await fetch('/ui/api/custom-data');
    const data = await response.json();
    // Update UI with data
}
```

## Step 7: Test Your Implementation

### Local Testing (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask directly
python app.py

# Access at http://localhost:8000
```

### Docker Testing

```bash
# Start with Docker
./start.sh

# Test an endpoint
curl -X POST http://localhost:8001/api/my_endpoint \
  -H "Content-Type: application/json" \
  -d '{"param": "value"}'

# View dashboard
open http://localhost:8000/ui/

# Stop
./stop.sh
```

## Step 8: Monitoring and Logging

### View Recent Events

Visit http://localhost:8000/ui/events to see:
- All API requests and responses
- Timestamps and status codes
- Full input/output details

### View Logs

```bash
# Docker logs
docker logs -f my-server_container

# Check BIST results
cat results/bist_results.json
```

## Common Patterns

### Pattern 1: Processing Data

```python
def process_file() -> tuple:
    """Process uploaded file."""
    try:
        data = request.get_json()
        processed = _validate_and_process(data)
        return jsonify({'success': True, 'data': processed}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


def _validate_and_process(data: dict) -> dict:
    """Private validation and processing."""
    if 'content' not in data:
        raise ValueError('Missing content')
    return {'processed': True, 'content': data['content']}
```

### Pattern 2: Calling External API

```python
import os
import requests
from flask import jsonify


def dep_fetch_external_data() -> tuple:
    """Fetch data from external API."""
    try:
        api_key = os.getenv('EXTERNAL_API_KEY')
        response = requests.get(
            'https://api.example.com/data',
            headers={'Authorization': f'Bearer {api_key}'},
            timeout=10
        )
        response.raise_for_status()
        return jsonify({'success': True, 'data': response.json()}), 200
    except requests.RequestException as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

### Pattern 3: Multiple Parameters

```python
def calculate() -> tuple:
    """Calculate based on multiple inputs."""
    try:
        data = request.get_json()
        result = _calculate(
            data.get('value1'),
            data.get('value2'),
            data.get('operation')
        )
        return jsonify({'success': True, 'result': result}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


def _calculate(val1, val2, op):
    """Private calculation logic."""
    operations = {
        'add': lambda a, b: a + b,
        'multiply': lambda a, b: a * b,
    }
    return operations[op](val1, val2)
```

## Checklist

- [ ] Updated server name in config.json
- [ ] Configured root_port
- [ ] Created API functions in functions/
- [ ] Registered routes in config.json
- [ ] Updated requirements.txt with dependencies
- [ ] Set up external services (if needed)
- [ ] Added .env variables (if needed)
- [ ] Tested locally with `python app.py`
- [ ] Built and tested with Docker `./start.sh`
- [ ] Verified BIST tests pass
- [ ] Customized dashboard (optional)
- [ ] Reviewed event logging

## What's Next?

1. **Testing**: Write proper tests in `tests/`
2. **Monitoring**: Set up log aggregation
3. **Deployment**: Push Docker image to registry
4. **Documentation**: Document your specific endpoints
5. **Scaling**: Add load balancing if needed

## Getting Help

- Check the main README.md for overview
- Review SERVER_GUIDELINES.md for architecture requirements
- Look at example functions in functions/ directory
- Check results/bist_results.json for test failures
