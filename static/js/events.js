/**
 * Event Management Functions
 */

/**
 * Load events from API
 */
async function loadEvents() {
    try {
        const response = await fetch('/ui/api/events');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error loading events:', error);
        throw error;
    }
}

/**
 * Refresh events display
 */
async function refreshEvents() {
    const btn = event?.target;
    const originalText = btn?.textContent;

    if (btn) {
        btn.disabled = true;
        btn.textContent = '⏳ Refreshing...';
    }

    try {
        await loadEvents().then(data => {
            if (data.success && data.events) {
                displayEvents(data.events);
            }
        });

        if (btn) {
            btn.textContent = '✓ Refreshed!';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.disabled = false;
            }, 2000);
        }
    } catch (error) {
        if (btn) {
            btn.textContent = '❌ Error';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.disabled = false;
            }, 2000);
        }
        console.error('Error refreshing events:', error);
    }
}

/**
 * Display events in the page
 */
function displayEvents(events) {
    const container = document.getElementById('events-container');
    if (!container) return;

    if (!events || events.length === 0) {
        showEmpty('events-container', 'No events recorded yet');
        return;
    }

    const html = events.map(event => {
        const timestamp = new Date(event.timestamp * 1000);
        const statusClass = event.status === 'success' ? 'success' : event.status === 'error' ? 'error' : 'pending';

        return `
            <div class="event-item">
                <div class="event-header">
                    <span class="event-method ${event.method.toLowerCase()}">${event.method}</span>
                    <span class="event-route">${escapeHtml(event.route)}</span>
                    <span class="event-status ${statusClass}">${event.status}</span>
                    <span class="event-time">${timestamp.toLocaleString()}</span>
                </div>
                <div class="event-details">
                    <div><strong>Status:</strong> ${event.status_code}</div>
                    ${event.response_size ? `<div><strong>Size:</strong> ${event.response_size} bytes</div>` : ''}
                </div>
            </div>
        `;
    }).join('');

    container.innerHTML = html;
}
