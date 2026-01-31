/**
 * Main JavaScript for server dashboard
 */

// Initialize page on load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard loaded');
});

// Utility function to fetch JSON
async function fetchJSON(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        return null;
    }
}

// Format JSON for display
function formatJSON(obj) {
    return JSON.stringify(obj, null, 2);
}
