/**
 * Shared Utility Functions
 */

/**
 * Escape HTML special characters to prevent XSS attacks
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

/**
 * Show loading state
 */
function showLoading(containerId, message = 'Loading...') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="loading"><p>${message}</p></div>`;
    }
}

/**
 * Show error message
 */
function showError(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="error-message"><strong>Error:</strong> ${escapeHtml(message)}</div>`;
    }
}

/**
 * Show empty state message
 */
function showEmpty(containerId, message = 'No data available') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="empty-state"><p>${escapeHtml(message)}</p></div>`;
    }
}

/**
 * Fetch JSON with error handling
 */
async function fetchJSON(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        throw new Error(`Failed to fetch: ${error.message}`);
    }
}

/**
 * Format timestamp to readable date string
 */
function formatTimestamp(timestamp) {
    return new Date(timestamp * 1000).toLocaleString();
}
