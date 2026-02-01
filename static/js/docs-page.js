/**
 * Documentation Manager Page Functions
 */

let allFolders = [];
let currentFolder = null;
let currentContent = null;

/**
 * Initialize documentation on page load
 */
function initializeDocs() {
    loadFoldersList();
}

/**
 * Load list of available documentation folders
 */
async function loadFoldersList() {
    try {
        const response = await fetch('/ui/api/documentation-folders');
        const data = await response.json();

        if (data.success && data.folders) {
            allFolders = data.folders;
            populateFoldersDropdown(allFolders);
            updateStats();
        } else {
            showDocsError('Failed to load documentation folders');
        }
    } catch (error) {
        showDocsError('Error loading folders: ' + error.message);
        console.error('Error:', error);
    }
}

/**
 * Populate folders dropdown with available folders
 */
function populateFoldersDropdown(folders) {
    const dropdown = document.getElementById('docs-folder-dropdown');
    dropdown.innerHTML = '';

    if (!folders || folders.length === 0) {
        dropdown.innerHTML = '<option value="">No documentation folders found</option>';
        return;
    }

    folders.forEach(folder => {
        const option = document.createElement('option');
        option.value = folder.name;
        option.textContent = `${folder.display_name} (${folder.file_count} files)`;
        dropdown.appendChild(option);
    });

    // Auto-select first folder
    if (folders.length > 0) {
        dropdown.value = folders[0].name;
        loadDocumentation();
    }
}

/**
 * Load documentation for selected folder
 */
async function loadDocumentation() {
    const dropdown = document.getElementById('docs-folder-dropdown');
    const folder = dropdown.value;

    if (!folder) {
        showDocsEmpty('Please select a documentation folder');
        return;
    }

    showDocsLoading();
    currentFolder = folder;

    try {
        // Try summary markdown first
        let response = await fetch(
            `/ui/api/document?folder=${encodeURIComponent(folder)}&document=${encodeURIComponent(folder)}&format=summary_markdown`
        );
        let data = await response.json();

        // Fall back to full markdown if summary doesn't exist
        if (!data.success) {
            response = await fetch(
                `/ui/api/document?folder=${encodeURIComponent(folder)}&document=${encodeURIComponent(folder)}&format=full_markdown`
            );
            data = await response.json();
        }

        if (data.success && data.content) {
            currentContent = data.content;
            displayContent(data.content, folder, data.filename, data.size);
            updateMetaInfo(folder, data.filename, data.size);
        } else {
            showDocsError(`No documentation found for "${folder}"`);
        }
    } catch (error) {
        showDocsError('Error loading documentation: ' + error.message);
    }
}

/**
 * Display documentation content with markdown parsing
 */
function displayContent(content, folder, filename, size) {
    const display = document.getElementById('docs-display');

    // Parse markdown to HTML
    let html = content;

    // Preserve code blocks
    const codeBlocks = [];
    html = html.replace(/```([\s\S]*?)```/g, (match, code) => {
        const index = codeBlocks.length;
        codeBlocks.push(escapeHtml(code.trim()));
        return `__CODE_BLOCK_${index}__`;
    });

    // Escape HTML
    html = escapeHtml(html);

    // Restore code blocks
    codeBlocks.forEach((code, index) => {
        html = html.replace(`__CODE_BLOCK_${index}__`, `<pre><code>${code}</code></pre>`);
    });

    // Parse markdown
    html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.*?)$/gm, '<h1>$1</h1>');

    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/_(.*?)_/g, '<em>$1</em>');

    html = html.replace(/`(.*?)`/g, '<code>$1</code>');
    html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');

    html = html.replace(/^\* (.*?)$/gm, '<li>$1</li>');
    html = html.replace(/^\- (.*?)$/gm, '<li>$1</li>');
    html = html.replace(/^(\d+)\. (.*?)$/gm, '<li>$2</li>');
    html = html.replace(/(<li>.*?<\/li>)/s, (match) => '<ul>' + match + '</ul>');

    html = html.replace(/^&gt; (.*?)$/gm, '<blockquote>$1</blockquote>');

    html = html.replace(/\n\n+/g, '</p><p>');
    html = '<p>' + html + '</p>';
    html = html.replace(/<p>\s*<\/p>/g, '');

    display.innerHTML = html;
}

/**
 * Update documentation statistics
 */
function updateStats() {
    const totalFolders = allFolders.length;
    const totalFiles = allFolders.reduce((sum, f) => sum + f.file_count, 0);

    document.getElementById('total-folders').textContent = totalFolders;
    document.getElementById('total-files').textContent = totalFiles;
}

/**
 * Update metadata display
 */
function updateMetaInfo(folder, filename, size) {
    document.getElementById('meta-folder').textContent = escapeHtml(folder);
    document.getElementById('meta-file').textContent = escapeHtml(filename);
    document.getElementById('meta-size').textContent = (size / 1024).toFixed(1) + ' KB';
    document.getElementById('docs-meta').style.display = 'flex';

    // Update current size stat
    document.getElementById('current-size').textContent = (size / 1024).toFixed(1) + ' KB';
}

/**
 * Refresh documentation folders list
 */
async function refreshDocumentation() {
    const btn = event.target;
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = '⏳ Refreshing...';

    try {
        await loadFoldersList();
        btn.textContent = '✓ Refreshed!';
        setTimeout(() => {
            btn.textContent = originalText;
            btn.disabled = false;
        }, 2000);
    } catch (error) {
        btn.textContent = '❌ Error';
        setTimeout(() => {
            btn.textContent = originalText;
            btn.disabled = false;
        }, 2000);
    }
}

/**
 * Download current documentation as markdown file
 */
function downloadCurrentDoc() {
    if (!currentContent || !currentFolder) {
        alert('No documentation to download');
        return;
    }

    const filename = `${currentFolder}_documentation.md`;
    const blob = new Blob([currentContent], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

/**
 * Expand all documentation content
 */
function expandAll() {
    document.getElementById('docs-display').style.maxHeight = 'none';
}

/**
 * Collapse documentation content
 */
function collapseAll() {
    document.getElementById('docs-display').style.maxHeight = '70vh';
}

/**
 * Show loading state
 */
function showDocsLoading() {
    document.getElementById('docs-display').innerHTML =
        '<div class="docs-loading"><div class="docs-loading-spinner"></div><p>Loading documentation...</p></div>';
}

/**
 * Show error message
 */
function showDocsError(message) {
    document.getElementById('docs-display').innerHTML =
        `<div class="docs-error"><strong>⚠️ Error:</strong> ${escapeHtml(message)}</div>`;
}

/**
 * Show empty state
 */
function showDocsEmpty(message) {
    document.getElementById('docs-display').innerHTML =
        `<div class="docs-empty"><p>${escapeHtml(message)}</p></div>`;
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeDocs);
} else {
    initializeDocs();
}
