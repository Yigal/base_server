/**
 * BIST (Built-In Self Test) Dashboard Page Functions
 */

let currentTab = 'endpoints';

/**
 * Switch between test result tabs
 */
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.bist-tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Find and activate the corresponding button
    document.querySelectorAll('.tab-btn').forEach(btn => {
        if (btn.textContent.toLowerCase().includes(tabName.replace('pages', 'dashboard pages'))) {
            btn.classList.add('active');
        }
    });

    currentTab = tabName;
}

/**
 * Load BIST test results from API
 */
async function loadBistResults() {
    try {
        const response = await fetch('/ui/api/bist-results');
        const data = await response.json();

        if (!data.success) {
            showPlaceholder('No test results available. Click "Run Tests" to start.');
            return;
        }

        const results = data.results;
        renderResults(results);

    } catch (error) {
        console.error('Error loading BIST results:', error);
        showPlaceholder('Error loading test results');
    }
}

/**
 * Render all test results sections
 */
function renderResults(results) {
    renderEndpoints(results.endpoints);
    renderPages(results.dashboard_pages);
    renderDependencies(results.external_dependencies);
    renderSummary(results);
}

/**
 * Render API endpoint test results
 */
function renderEndpoints(endpoints) {
    const container = document.getElementById('endpoints-container');

    if (!endpoints || endpoints.length === 0) {
        container.innerHTML = '<p class="placeholder">No endpoints tested</p>';
        return;
    }

    container.innerHTML = endpoints.map(test => {
        const statusClass = test.success ? 'success' : 'failed';
        const statusIcon = test.success ? '✓' : '✗';

        return `
            <div class="test-item ${statusClass}">
                <div class="test-header">
                    <span class="test-status-badge ${statusClass}">${statusIcon}</span>
                    <div class="test-title">${test.method} ${test.route}</div>
                </div>
                <div class="test-details">
                    <strong>Status Code:</strong> ${test.status}
                    ${test.error ? `<div class="test-error"><strong>Error:</strong> ${escapeHtml(test.error)}</div>` : ''}
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Render dashboard page test results
 */
function renderPages(pages) {
    const container = document.getElementById('pages-container');

    if (!pages || pages.length === 0) {
        container.innerHTML = '<p class="placeholder">No pages tested</p>';
        return;
    }

    container.innerHTML = pages.map(test => {
        const statusClass = test.success ? 'success' : (test.missing_elements.length > 0 ? 'warning' : 'failed');
        const statusIcon = test.success ? '✓' : '!';

        let details = `<strong>Status:</strong> ${test.status}<br>
                       <strong>Valid HTML:</strong> ${test.html_valid ? 'Yes' : 'No'}`;

        if (test.missing_elements && test.missing_elements.length > 0) {
            details += `<br><strong>Missing Elements:</strong><br>
                        ${test.missing_elements.map(e => `• ${escapeHtml(e)}`).join('<br>')}`;
        }

        return `
            <div class="test-item ${statusClass}">
                <div class="test-header">
                    <span class="test-status-badge ${statusClass}">${statusIcon}</span>
                    <div class="test-title">${test.page}</div>
                </div>
                <div class="test-details">
                    ${details}
                    ${test.error ? `<div class="test-error"><strong>Error:</strong> ${escapeHtml(test.error)}</div>` : ''}
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Render external dependency test results
 */
function renderDependencies(deps) {
    const container = document.getElementById('dependencies-container');

    if (!deps || deps.length === 0) {
        container.innerHTML = '<p class="placeholder">No dependencies configured</p>';
        return;
    }

    container.innerHTML = deps.map(test => {
        const statusClass = test.success ? 'success' : 'failed';
        const statusIcon = test.success ? '✓' : '✗';

        return `
            <div class="test-item ${statusClass}">
                <div class="test-header">
                    <span class="test-status-badge ${statusClass}">${statusIcon}</span>
                    <div class="test-title">${test.dependency}</div>
                </div>
                <div class="test-details">
                    <strong>Status:</strong> ${test.status}
                    ${test.error ? `<div class="test-error"><strong>Error:</strong> ${escapeHtml(test.error)}</div>` : ''}
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Render test summary statistics
 */
function renderSummary(results) {
    const container = document.getElementById('summary-container');

    const endpoints = results.endpoints || [];
    const pages = results.dashboard_pages || [];
    const deps = results.external_dependencies || [];

    const endpointsPassed = endpoints.filter(t => t.success).length;
    const pagesPassed = pages.filter(t => t.success).length;
    const depsPassed = deps.filter(t => t.success).length;

    const totalTests = endpoints.length + pages.length + deps.length;
    const totalPassed = endpointsPassed + pagesPassed + depsPassed;
    const totalFailed = totalTests - totalPassed;

    container.innerHTML = `
        <div class="stat-box total">
            <h3>Total Tests</h3>
            <div class="stat-value">${totalTests}</div>
        </div>
        <div class="stat-box success">
            <h3>Passed</h3>
            <div class="stat-value">${totalPassed}</div>
        </div>
        <div class="stat-box failed">
            <h3>Failed</h3>
            <div class="stat-value">${totalFailed}</div>
        </div>
        <div class="stat-box">
            <h3>Pass Rate</h3>
            <div class="stat-value">${totalTests > 0 ? Math.round((totalPassed / totalTests) * 100) : 0}%</div>
        </div>
        <div class="stat-box">
            <h3>API Endpoints</h3>
            <div class="stat-value">${endpointsPassed}/${endpoints.length}</div>
        </div>
        <div class="stat-box">
            <h3>Dashboard Pages</h3>
            <div class="stat-value">${pagesPassed}/${pages.length}</div>
        </div>
        <div class="stat-box">
            <h3>Dependencies</h3>
            <div class="stat-value">${depsPassed}/${deps.length}</div>
        </div>
    `;
}

/**
 * Run BIST tests
 */
async function runBistTests(testType = 'all') {
    const runAllBtn = document.getElementById('runAllBtn');
    const statusEl = document.getElementById('runStatus');

    // Disable all run buttons
    document.querySelectorAll('.btn-run, .btn-run-small').forEach(btn => {
        btn.disabled = true;
    });

    let statusText = 'Running tests...';
    if (testType !== 'all') {
        statusText = `Running ${testType} tests...`;
    }
    statusEl.textContent = statusText;

    try {
        const response = await fetch('/ui/api/bist-run', {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            statusEl.textContent = '✓ Tests completed';

            // If selective test type, switch to that tab
            if (testType !== 'all') {
                switchTab(testType);
            }

            renderResults(data.results);
        } else {
            throw new Error(data.error || 'Unknown error');
        }

    } catch (error) {
        console.error('Error running BIST tests:', error);
        statusEl.textContent = '✗ Error running tests';
    } finally {
        // Re-enable all run buttons
        document.querySelectorAll('.btn-run, .btn-run-small').forEach(btn => {
            btn.disabled = false;
        });
    }
}

/**
 * Show placeholder message in all test containers
 */
function showPlaceholder(message) {
    document.getElementById('endpoints-container').innerHTML = `<p class="placeholder">${message}</p>`;
    document.getElementById('pages-container').innerHTML = `<p class="placeholder">${message}</p>`;
    document.getElementById('dependencies-container').innerHTML = `<p class="placeholder">${message}</p>`;
    document.getElementById('summary-container').innerHTML = `<p class="placeholder">${message}</p>`;
}

// Load results on page load
document.addEventListener('DOMContentLoaded', loadBistResults);
