/**
 * API Documentation Page Functions
 */

// API_PORT and API_BASE_URL will be set in the template
let API_PORT;
let API_BASE_URL;

/**
 * Initialize API base URL
 */
function initializeApiConfig(port) {
    API_PORT = port;
    API_BASE_URL = `http://localhost:${API_PORT}`;
}

/**
 * Fetch API documentation from FastAPI server
 */
async function fetchDocumentation() {
    const container = document.getElementById('docsContainer');
    const statusEl = document.getElementById('docsStatus');
    const btn = document.getElementById('fetchDocsBtn');

    btn.disabled = true;
    statusEl.textContent = 'Fetching documentation...';
    container.innerHTML = '<p class="loading">Loading...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/documentation`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        if (!data.success || !data.routes) {
            throw new Error('Invalid documentation format');
        }

        container.innerHTML = '';
        let count = 0;

        Object.entries(data.routes).forEach(([routeName, route]) => {
            count++;
            const routeCard = document.createElement('div');
            routeCard.className = 'route-card';

            routeCard.innerHTML = `
                <div class="route-header">
                    <span class="route-method ${route.method.toLowerCase()}">${route.method}</span>
                    <span class="route-path">${route.route}</span>
                </div>
                <div class="route-info">
                    <div><strong>Function:</strong> ${route.function}</div>
                    <div><strong>Description:</strong> ${route.description}</div>
                    ${route.file ? `<div><strong>File:</strong> ${route.file}</div>` : ''}
                    <div><strong>Example:</strong> <code>${route.example_curl}</code></div>
                </div>
            `;

            container.appendChild(routeCard);
        });

        statusEl.textContent = `✓ Loaded ${count} routes`;

    } catch (error) {
        console.error('Error:', error);
        container.innerHTML = `
            <div class="error-message">
                <strong>Error loading documentation:</strong><br>
                ${error.message}<br><br>
                <small>Make sure the FastAPI server is running on port ${API_PORT}</small>
            </div>
        `;
        statusEl.textContent = '✗ Failed to load';
    } finally {
        btn.disabled = false;
    }
}

/**
 * Fetch and display FastAPI source code
 */
async function refreshSourceCode() {
    const container = document.getElementById('sourceContainer');
    const btn = document.getElementById('refreshSourceBtn');

    btn.disabled = true;
    container.innerHTML = '<p class="loading">Loading source code...</p>';

    try {
        const response = await fetch('/ui/api/fastapi-source');

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            container.innerHTML = `<pre><code class="language-python">${escapeHtml(data.source)}</code></pre>`;
            hljs.highlightAll();
        } else {
            throw new Error(data.error || 'Unknown error');
        }

    } catch (error) {
        container.innerHTML = `
            <div class="error-message">
                <strong>Error loading source:</strong><br>
                ${error.message}
            </div>
        `;
    } finally {
        btn.disabled = false;
    }
}

// Load source code on page load
document.addEventListener('DOMContentLoaded', refreshSourceCode);
