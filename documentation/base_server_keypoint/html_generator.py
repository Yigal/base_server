"""
HTML Generator for Base Server Documentation

Transforms JSON documentation into interactive HTML pages suitable
for display in the base_server dashboard.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


def generate_html(
    json_file: str,
    output_file: Optional[str] = None,
    template: str = "collapsible",
    include_search: bool = True,
    include_export: bool = True,
    include_theme_toggle: bool = True,
    theme: str = "light"
) -> str:
    """
    Generate HTML from JSON documentation file.

    Args:
        json_file: Path to JSON documentation file
        output_file: Optional path to write HTML file
        template: Template type (collapsible, flat, tree)
        include_search: Include search functionality
        include_export: Include export options
        include_theme_toggle: Include theme toggle button
        theme: Default theme (light, dark)

    Returns:
        HTML string

    Raises:
        FileNotFoundError: If JSON file not found
        json.JSONDecodeError: If JSON is invalid
    """
    # Read JSON file
    json_path = Path(json_file)
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_file}")

    with open(json_path, 'r', encoding='utf-8') as f:
        doc_data = json.load(f)

    # Generate HTML based on template
    if template == "collapsible":
        html = _generate_collapsible_html(
            doc_data,
            include_search=include_search,
            include_export=include_export,
            include_theme_toggle=include_theme_toggle,
            theme=theme
        )
    elif template == "flat":
        html = _generate_flat_html(doc_data, theme=theme)
    elif template == "tree":
        html = _generate_tree_html(doc_data, theme=theme)
    else:
        raise ValueError(f"Unknown template: {template}")

    # Write to file if specified
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

    return html


def _generate_collapsible_html(
    doc_data: Dict[str, Any],
    include_search: bool = True,
    include_export: bool = True,
    include_theme_toggle: bool = True,
    theme: str = "light"
) -> str:
    """Generate collapsible HTML template."""

    project = doc_data.get('project', 'Documentation')
    description = doc_data.get('description', '')
    version = doc_data.get('version', '1.0.0')
    sections = doc_data.get('sections', [])

    # Build sections HTML
    sections_html = _build_sections_html(sections, collapsible=True)

    # Build search bar
    search_html = _build_search_html() if include_search else ""

    # Build export buttons
    export_html = _build_export_html() if include_export else ""

    # Build theme toggle
    theme_html = _build_theme_toggle_html() if include_theme_toggle else ""

    # Build JavaScript
    js_code = _build_javascript(include_search=include_search)

    # Build CSS
    css_code = _build_css(theme=theme)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project}</title>
    <style>
{css_code}
    </style>
</head>
<body class="theme-{theme}">
    <header>
        <div class="header-content">
            <div class="header-left">
                <h1>{project}</h1>
                <p class="subtitle">{description}</p>
                <small>Version {version}</small>
            </div>
            <div class="header-right">
                {theme_html}
            </div>
        </div>
        {search_html}
        {export_html}
    </header>

    <main class="documentation">
        {sections_html}
    </main>

    <footer>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Project: {project} v{version}</p>
    </footer>

    <script>
{js_code}
    </script>
</body>
</html>"""

    return html


def _generate_flat_html(doc_data: Dict[str, Any], theme: str = "light") -> str:
    """Generate flat HTML template (all visible)."""
    project = doc_data.get('project', 'Documentation')
    description = doc_data.get('description', '')
    version = doc_data.get('version', '1.0.0')
    sections = doc_data.get('sections', [])

    sections_html = _build_sections_html(sections, collapsible=False)
    css_code = _build_css(theme=theme)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project}</title>
    <style>
{css_code}
    </style>
</head>
<body class="theme-{theme}">
    <header>
        <h1>{project}</h1>
        <p class="subtitle">{description}</p>
        <small>Version {version}</small>
    </header>

    <main class="documentation">
        {sections_html}
    </main>

    <footer>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </footer>
</body>
</html>"""

    return html


def _generate_tree_html(doc_data: Dict[str, Any], theme: str = "light") -> str:
    """Generate tree HTML template."""
    project = doc_data.get('project', 'Documentation')
    description = doc_data.get('description', '')
    version = doc_data.get('version', '1.0.0')
    sections = doc_data.get('sections', [])

    # Build TOC
    toc_html = _build_toc_html(sections)

    # Build content
    sections_html = _build_sections_html(sections, collapsible=True)

    css_code = _build_css(theme=theme)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project}</title>
    <style>
{css_code}
    </style>
</head>
<body class="theme-{theme}">
    <header>
        <h1>{project}</h1>
        <p class="subtitle">{description}</p>
    </header>

    <div class="container">
        <aside class="toc">
            {toc_html}
        </aside>
        <main class="documentation">
            {sections_html}
        </main>
    </div>

    <footer>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </footer>
</body>
</html>"""

    return html


def _build_sections_html(sections: list, collapsible: bool = True) -> str:
    """Build HTML for all sections."""
    html = ""
    for section in sections:
        section_id = f"section-{section['id']}"
        section_name = section['name']
        keypoints = section.get('keypoints', [])

        if collapsible:
            html += f'    <section class="doc-section" id="{section_id}">\n'
            html += f'        <h2 class="section-header" onclick="toggleSection(\'{section_id}\')">\n'
            html += f'            <span class="section-toggle">▼</span>\n'
            html += f'            <span class="section-title">{section["id"]}. {section_name}</span>\n'
            html += '        </h2>\n'
            html += '        <div class="section-content" style="display: none;">\n'
        else:
            html += f'    <section class="doc-section" id="{section_id}">\n'
            html += f'        <h2 class="section-header">\n'
            html += f'            <span class="section-title">{section["id"]}. {section_name}</span>\n'
            html += '        </h2>\n'
            html += '        <div class="section-content">\n'

        # Build keypoints
        for kp in keypoints:
            kp_id = kp['id']
            kp_name = kp['name']
            summary = kp['summary']
            description = kp.get('description', '')

            html += f'            <article class="keypoint" id="keypoint-{kp_id}">\n'
            html += f'                <h3 class="keypoint-header">\n'
            html += f'                    <span class="keypoint-id">{kp_id}</span>\n'
            html += f'                    <span class="keypoint-name">{kp_name}</span>\n'
            html += '                </h3>\n'
            html += f'                <p class="summary">{summary}</p>\n'

            if description:
                html += f'                <details class="keypoint-details">\n'
                html += '                    <summary>View Full Description</summary>\n'
                html += f'                    <div class="description">{_escape_html(description)}</div>\n'
                html += '                </details>\n'

            html += f'                <button class="copy-btn" onclick="copyToClipboard(\'{kp_id}\')">Copy Summary</button>\n'
            html += '            </article>\n'

        html += '        </div>\n'
        html += '    </section>\n'

    return html


def _build_search_html() -> str:
    """Build search functionality HTML."""
    return """        <div class="search-container">
            <input
                type="text"
                id="search-input"
                class="search-input"
                placeholder="Search documentation..."
                onkeyup="searchDocumentation()"
            >
            <span id="search-count" class="search-count"></span>
        </div>"""


def _build_export_html() -> str:
    """Build export buttons HTML."""
    return """        <div class="export-container">
            <button onclick="exportAsJSON()" class="export-btn">Export JSON</button>
            <button onclick="window.print()" class="export-btn">Print/PDF</button>
        </div>"""


def _build_theme_toggle_html() -> str:
    """Build theme toggle button HTML."""
    return """            <button id="theme-toggle" onclick="toggleTheme()" class="theme-toggle">
                🌙 Theme
            </button>"""


def _build_toc_html(sections: list) -> str:
    """Build table of contents HTML."""
    html = '<nav class="toc-nav">\n'
    html += '    <h3>Contents</h3>\n'
    html += '    <ul>\n'

    for section in sections:
        html += f'        <li>\n'
        html += f'            <a href="#section-{section["id"]}">{section["id"]}. {section["name"]}</a>\n'
        html += '            <ul>\n'

        for kp in section.get('keypoints', []):
            html += f'                <li>\n'
            html += f'                    <a href="#keypoint-{kp["id"]}">{kp["id"]}. {kp["name"]}</a>\n'
            html += '                </li>\n'

        html += '            </ul>\n'
        html += '        </li>\n'

    html += '    </ul>\n'
    html += '</nav>\n'

    return html


def _build_css(theme: str = "light") -> str:
    """Build CSS stylesheet."""
    return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --color-primary: #007bff;
            --color-secondary: #6c757d;
            --color-success: #28a745;
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --border-color: #dee2e6;
        }

        html.theme-dark {
            --bg-primary: #1e1e1e;
            --bg-secondary: #2d2d2d;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --border-color: #404040;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background-color: var(--bg-primary);
        }

        header {
            position: sticky;
            top: 0;
            background-color: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            padding: 1.5rem;
            z-index: 100;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }

        h1 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }

        .documentation {
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }

        .doc-section {
            border: 1px solid var(--border-color);
            border-radius: 4px;
            margin-bottom: 1.5rem;
            overflow: hidden;
        }

        .section-header {
            padding: 1rem;
            background-color: var(--bg-secondary);
            cursor: pointer;
            user-select: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: background-color 0.2s;
        }

        .section-header:hover {
            background-color: #e9ecef;
        }

        .section-toggle {
            display: inline-block;
            transition: transform 0.3s;
            width: 1.2rem;
            text-align: center;
        }

        .section-toggle.collapsed {
            transform: rotate(-90deg);
        }

        .section-content {
            padding: 0;
        }

        .keypoint {
            padding: 1.5rem;
            border-bottom: 1px solid var(--border-color);
        }

        .keypoint:last-child {
            border-bottom: none;
        }

        .keypoint-header {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }

        .keypoint-id {
            font-weight: bold;
            color: var(--color-primary);
            min-width: 3rem;
        }

        .summary {
            margin-bottom: 0.75rem;
            font-style: italic;
            color: var(--text-secondary);
        }

        .keypoint-details {
            margin: 0.75rem 0;
            padding: 0.75rem;
            background-color: var(--bg-secondary);
            border-left: 3px solid var(--color-primary);
            border-radius: 2px;
            cursor: pointer;
        }

        .keypoint-details > summary {
            font-weight: 500;
            padding: 0.25rem 0;
            user-select: none;
        }

        .description {
            margin-top: 0.75rem;
            padding-top: 0.75rem;
            border-top: 1px solid var(--border-color);
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        button {
            padding: 0.5rem 1rem;
            background-color: var(--color-primary);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 0.5rem;
            transition: background-color 0.2s;
        }

        button:hover {
            background-color: #0056b3;
        }

        .copy-btn {
            font-size: 0.9rem;
            padding: 0.35rem 0.75rem;
        }

        .search-container {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        .search-input {
            flex: 1;
            padding: 0.75rem;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            font-size: 1rem;
            color: var(--text-primary);
            background-color: var(--bg-primary);
        }

        .search-count {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .export-container {
            display: flex;
            gap: 0.5rem;
            margin-top: 0.75rem;
        }

        .export-btn {
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }

        .theme-toggle {
            padding: 0.5rem 1rem;
        }

        footer {
            text-align: center;
            padding: 2rem;
            color: var(--text-secondary);
            border-top: 1px solid var(--border-color);
            margin-top: 2rem;
            font-size: 0.9rem;
        }

        /* Responsive */
        @media (max-width: 768px) {
            body {
                font-size: 0.95rem;
            }

            header {
                padding: 1rem;
            }

            .header-content {
                flex-direction: column;
                gap: 1rem;
            }

            h1 {
                font-size: 1.5rem;
            }

            .documentation {
                padding: 1rem 0.5rem;
            }

            .doc-section {
                margin-bottom: 1rem;
            }

            .keypoint {
                padding: 1rem;
            }

            .search-input {
                padding: 0.5rem;
            }
        }

        /* Print styles */
        @media print {
            header, footer {
                display: none;
            }

            .doc-section {
                break-inside: avoid;
                page-break-inside: avoid;
            }

            .section-content {
                display: block !important;
            }

            button {
                display: none;
            }

            .section-header {
                background-color: transparent;
                border-bottom: 2px solid var(--text-primary);
                padding-bottom: 0.5rem;
            }
        }
"""


def _build_javascript(include_search: bool = True) -> str:
    """Build JavaScript code."""
    js = """
        // Collapse/Expand functionality
        function toggleSection(sectionId) {
            const section = document.getElementById(sectionId);
            const header = section.querySelector('.section-header');
            const content = section.querySelector('.section-content');
            const toggle = header.querySelector('.section-toggle');

            const isHidden = content.style.display === 'none';
            content.style.display = isHidden ? 'block' : 'none';
            toggle.classList.toggle('collapsed', !isHidden);

            // Save state
            localStorage.setItem(sectionId, isHidden ? 'open' : 'closed');
        }

        // Load saved state on page load
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.doc-section').forEach(section => {
                const sectionId = section.id;
                const state = localStorage.getItem(sectionId);
                const content = section.querySelector('.section-content');
                const toggle = section.querySelector('.section-toggle');

                if (state === 'closed') {
                    content.style.display = 'none';
                    toggle.classList.add('collapsed');
                }
            });
        });

        // Copy to clipboard
        function copyToClipboard(keypointId) {
            const article = document.getElementById('keypoint-' + keypointId);
            const summary = article.querySelector('.summary').textContent;

            navigator.clipboard.writeText(summary).then(() => {
                const btn = article.querySelector('.copy-btn');
                const original = btn.textContent;
                btn.textContent = '✓ Copied!';
                setTimeout(() => {
                    btn.textContent = original;
                }, 2000);
            });
        }

        // Theme toggle
        function toggleTheme() {
            const html = document.documentElement;
            const isDark = html.classList.contains('theme-dark');
            const newTheme = isDark ? 'light' : 'dark';

            html.className = 'theme-' + newTheme;
            localStorage.setItem('theme', newTheme);

            const btn = document.getElementById('theme-toggle');
            btn.textContent = newTheme === 'dark' ? '☀️ Theme' : '🌙 Theme';
        }

        // Load theme preference
        document.addEventListener('DOMContentLoaded', function() {
            const savedTheme = localStorage.getItem('theme') || 'light';
            const html = document.documentElement;
            html.className = 'theme-' + savedTheme;
            const btn = document.getElementById('theme-toggle');
            if (btn) {
                btn.textContent = savedTheme === 'dark' ? '☀️ Theme' : '🌙 Theme';
            }
        });

        // Export as JSON
        function exportAsJSON() {
            const data = {};
            document.querySelectorAll('.doc-section').forEach(section => {
                const sectionId = section.id.replace('section-', '');
                const keypoints = [];

                section.querySelectorAll('.keypoint').forEach(kp => {
                    keypoints.push({
                        id: kp.id.replace('keypoint-', ''),
                        name: kp.querySelector('.keypoint-name').textContent,
                        summary: kp.querySelector('.summary').textContent
                    });
                });

                data[sectionId] = keypoints;
            });

            const json = JSON.stringify(data, null, 2);
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'documentation-' + new Date().toISOString().split('T')[0] + '.json';
            a.click();
        }
"""

    if include_search:
        js += """
        // Search functionality
        function searchDocumentation() {
            const query = document.getElementById('search-input').value.toLowerCase();
            let matchCount = 0;

            document.querySelectorAll('.doc-section').forEach(section => {
                let sectionHasMatch = false;
                let anyKeypointVisible = false;

                section.querySelectorAll('.keypoint').forEach(keypoint => {
                    const name = keypoint.querySelector('.keypoint-name').textContent.toLowerCase();
                    const summary = keypoint.querySelector('.summary').textContent.toLowerCase();

                    const isMatch = query === '' || name.includes(query) || summary.includes(query);
                    keypoint.style.display = isMatch ? 'block' : 'none';

                    if (isMatch) {
                        sectionHasMatch = true;
                        anyKeypointVisible = true;
                        matchCount++;
                    }
                });

                section.style.display = anyKeypointVisible ? 'block' : 'none';

                // Auto-expand section if it has matches
                if (sectionHasMatch && query !== '') {
                    const content = section.querySelector('.section-content');
                    if (content.style.display === 'none') {
                        content.style.display = 'block';
                        const toggle = section.querySelector('.section-toggle');
                        toggle.classList.remove('collapsed');
                    }
                }
            });

            // Update match count
            const countEl = document.getElementById('search-count');
            if (countEl) {
                countEl.textContent = query ? `${matchCount} results` : '';
            }
        }
"""

    return js


def _escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


if __name__ == '__main__':
    # Example usage
    import sys

    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        template = sys.argv[3] if len(sys.argv) > 3 else 'collapsible'

        html = generate_html(
            json_file=json_file,
            output_file=output_file,
            template=template
        )

        print(f"Generated {len(html)} bytes of HTML")
        if output_file:
            print(f"Written to: {output_file}")
    else:
        print("Usage: python html_generator.py <json_file> [output_file] [template]")
        print("Templates: collapsible, flat, tree")
