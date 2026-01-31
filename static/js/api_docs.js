/**
 * API Documentation interactive tester
 */

function selectEndpoint(event, endpointName) {
    event.preventDefault();

    // Hide all sections
    document.querySelectorAll('.endpoint-section').forEach(el => {
        el.style.display = 'none';
    });

    // Show selected section
    document.getElementById(endpointName).style.display = 'block';

    // Update active link
    document.querySelectorAll('.endpoint-link').forEach(el => {
        el.style.background = '';
    });
    event.target.closest('.endpoint-link').style.background = '#f0f0f0';
}

async function testEndpoint(routeName, route, method) {
    const responseStatus = document.getElementById(`response-status-${routeName}`);
    const responseBody = document.getElementById(`response-body-${routeName}`);

    responseStatus.textContent = 'Testing...';
    responseBody.textContent = 'Loading...';

    try {
        // Get API port from current URL or default
        const port = 8001;
        const url = `http://localhost:${port}${route}`;

        // Collect form data
        const formData = {};
        document.querySelectorAll(`#${routeName} .param-field`).forEach(field => {
            const param = field.dataset.param;
            const value = field.value;
            formData[param] = value || null;
        });

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: method !== 'GET' ? JSON.stringify(formData) : undefined
        });

        const status = response.status;
        const data = await response.json();

        responseStatus.textContent = `Status: ${status} ${response.statusText}`;
        responseStatus.style.backgroundColor = status >= 200 && status < 300 ? '#d4edda' : '#f8d7da';
        responseStatus.style.color = status >= 200 && status < 300 ? '#155724' : '#721c24';
        responseBody.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        responseStatus.textContent = `Error: ${error.message}`;
        responseStatus.style.backgroundColor = '#f8d7da';
        responseStatus.style.color = '#721c24';
        responseBody.textContent = error.toString();
    }
}
