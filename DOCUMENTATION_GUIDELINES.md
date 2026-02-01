# Documentation Guidelines

Complete guidelines for managing the documentation system of the base_server project.

## 1. Documentation System Overview

### 1.1 Multi-Format Documentation Approach
The documentation system maintains the same content in 4 synchronized formats to support different use cases and access patterns. All formats are generated from a single source, ensuring consistency and reducing maintenance burden. The system is designed for both human reading and programmatic access.

### 1.2 Documentation Formats
The system maintains four synchronized versions of documentation:
- **Summary Markdown** - Quick reference with one-sentence summaries
- **Full Markdown** - Comprehensive guide with detailed descriptions
- **Summary JSON** - Lightweight structured data for APIs
- **Full JSON** - Complete structured data with full descriptions

### 1.3 Documentation Structure
Each document is organized into numbered sections (##) and keypoints (###). Sections represent major topic areas (15 total), and keypoints represent specific guidelines within each section (60+ total). Each keypoint has a name, one-sentence summary, and full description.

### 1.4 Content Organization
The documentation follows a hierarchical structure:
- Level 1: Document (PROJECT_GUIDELINES.md, DOCUMENTATION_GUIDELINES.md)
- Level 2: Sections (##) - 15 sections numbered 1-15
- Level 3: Keypoints (###) - Multiple keypoints per section, numbered 1.1, 1.2, etc.
- Content: Description text under each keypoint

### 1.5 Single Source of Truth
The markdown files (PROJECT_GUIDELINES.md and DOCUMENTATION_GUIDELINES.md) serve as the authoritative source. JSON files and other formats are generated from these markdown sources. When updates are needed, always modify the markdown files first.

## 2. Accessing Documentation

### 2.1 Web Dashboard Viewer
The documentation is integrated into the main dashboard at `http://localhost:9000/ui/`. The viewer includes:
- Format selector dropdown (4 options)
- View controls (Compact/Expanded)
- Download button
- Interactive content display with JSON collapsing

### 2.2 API Access Points
Two REST endpoints provide programmatic access to documentation:

**GET /api/documents**
Returns metadata about all available documents and their formats. No query parameters required.

**GET /api/document**
Returns specific document content. Required parameters:
- `folder` - Document folder name
- `document` - Document name
- `format` - One of: summary_markdown, full_markdown, summary_json, full_json

### 2.3 Direct File Access
Documentation files are stored in `documentation/base_server_keypoint/`:
- `*.md` - Markdown files (human-readable)
- `*_full.json` - Full JSON versions
- `*_summary.json` - Summary JSON versions
- `agent.md` - Agent specification
- `skills.md` - Skills definitions

### 2.4 Offline Access
All documentation formats can be downloaded from the dashboard viewer or via API. Downloaded files work completely offline with no external dependencies.

## 3. Creating and Maintaining Documentation

### 3.1 Documentation File Format
Each markdown file must follow this structure:
```markdown
# Document Title

Document description and overview.

## 1. Section Name
Section introduction text.

### 1.1 Keypoint Name
Full description of the keypoint, including:
- Purpose and why it matters
- Implementation details
- Code examples
- Best practices
- Common pitfalls

### 1.2 Another Keypoint
Additional content...

## 2. Next Section
Continue with more sections...
```

### 3.2 Keypoint Guidelines
When writing keypoints:
1. **Name** - Clear, descriptive title (3-7 words)
2. **Summary** - One sentence capturing the essence (15-25 words)
3. **Description** - Full explanation (100-300 words)
4. **Examples** - Code blocks or procedures when applicable
5. **Structure** - Follow consistent formatting

### 3.3 Markdown Conventions
Follow these conventions for consistent formatting:
- Headers: Use `#`, `##`, `###` only (no deeper levels)
- Code blocks: Use triple backticks with language specification
- Inline code: Use backticks for file names, config keys, function names
- Lists: Use `-` for bullet points, `1.` for numbered
- Bold: Use `**text**` for emphasis
- Links: Use `[text](url)` format

### 3.4 Updating Documentation
When documentation changes are needed:
1. Edit the markdown file directly (PROJECT_GUIDELINES.md or DOCUMENTATION_GUIDELINES.md)
2. Update the section and keypoint structure if needed
3. Ensure the summary is one sentence
4. Keep descriptions clear and concise
5. Update related keypoints if impacts are wide-ranging

### 3.5 Adding New Sections
To add a new documentation section:
1. Identify the appropriate location in the document
2. Add a new `## N. Section Name` header
3. Add at least 3-5 keypoints as `### N.1 Keypoint Name`
4. Write descriptions for each keypoint
5. Update the navigation in appropriate places
6. Regenerate JSON formats if needed

### 3.6 Adding New Keypoints
To add a new keypoint to an existing section:
1. Find the appropriate section (##)
2. Add `### X.Y Keypoint Name` in the correct sequence
3. Write one-sentence summary
4. Write full description (100-300 words)
5. Include examples if applicable
6. Update numbering of subsequent keypoints if needed

## 4. JSON Documentation Format

### 4.1 Full JSON Structure
The full JSON documentation contains complete information including descriptions:
```json
{
  "project": "string",
  "version": "string",
  "sections": [
    {
      "id": 1,
      "name": "string",
      "keypoints": [
        {
          "id": "1.1",
          "name": "string",
          "summary": "string",
          "description": "string"
        }
      ]
    }
  ]
}
```

### 4.2 Summary JSON Structure
The summary JSON contains only essential information:
```json
{
  "project": "string",
  "version": "string",
  "sections": [
    {
      "id": 1,
      "name": "string",
      "keypoints": [
        {
          "id": "1.1",
          "name": "string",
          "summary": "string"
        }
      ]
    }
  ]
}
```

### 4.3 JSON Field Requirements
- `id` - Section ID (integer 1-15) or keypoint ID (string "X.Y")
- `name` - Human-readable section or keypoint name
- `summary` - One-sentence summary (no more than 200 characters)
- `description` - Full description (optional in summary version)
- `project` - Document project name
- `version` - Semantic version (X.Y.Z format)

### 4.4 JSON Validation
JSON documentation must validate against the provided schemas:
- `schemas/base_server_keypoints_full.schema.json` - Validates full JSON
- `schemas/base_server_keypoints_summary.schema.json` - Validates summary JSON

Validation includes:
- Required field presence
- Field types
- ID format (X.Y pattern)
- String length constraints
- Nested structure validity

## 5. Documentation Generation

### 5.1 Manual Generation Process
To manually generate JSON from markdown:
1. Parse markdown file
2. Extract sections (## headers)
3. Extract keypoints (### headers)
4. Extract one-sentence summaries from descriptions
5. Build JSON structure
6. Validate against schema
7. Save to appropriate file

### 5.2 Using the HTML Generator
The HTML generator converts JSON to interactive web pages:
```bash
python documentation/base_server_keypoint/html_generator.py \
  documentation/base_server_keypoint/base_server_keypoints_summary.json \
  templates/documentation_generated.html collapsible
```

Template options: `collapsible`, `flat`, `tree`

### 5.3 Regeneration Workflow
When documentation is updated:
1. Edit markdown files (source of truth)
2. Manually or automatically generate JSON versions
3. Validate JSON against schemas
4. Regenerate HTML from JSON if needed
5. Test in dashboard viewer
6. Commit changes to version control

### 5.4 Version Management
Each documentation file contains a version number:
- Format: `X.Y.Z` (semantic versioning)
- Increment on significant changes
- Track in git commits
- Include in JSON metadata

## 6. Documentation in the API

### 6.1 GET /api/documents Endpoint
Lists all available documentation with metadata:

Response includes:
- Document name and folder
- Description
- All 4 format types available
- File sizes
- File paths

### 6.2 GET /api/document Endpoint
Retrieves specific document content:

Query parameters:
- `folder` (required) - "base_server_keypoint"
- `document` (required) - "base_server_keypoints"
- `format` (required) - One of 4 formats

Response includes:
- Success flag
- File metadata
- Full content (markdown string or JSON object)

### 6.3 API Usage Patterns
Get all documents:
```bash
curl http://localhost:9001/api/documents
```

Get summary markdown:
```bash
curl "http://localhost:9001/api/document?folder=base_server_keypoint\
  &document=base_server_keypoints&format=summary_markdown"
```

Get full JSON:
```bash
curl "http://localhost:9001/api/document?folder=base_server_keypoint\
  &document=base_server_keypoints&format=full_json"
```

## 7. Dashboard Documentation Viewer

### 7.1 Viewer Features
The embedded dashboard viewer provides:
- Format selector dropdown
- View mode toggle (Compact/Expanded)
- Download button
- Real-time content loading
- JSON collapsible tree
- Markdown text display

### 7.2 Format Selection
Users can switch between formats:
- **Summary (Markdown)** - Quick reference, one-sentence summaries
- **Full (Markdown)** - Complete guide with all details
- **Summary (JSON)** - Lightweight data structure
- **Full (JSON)** - Complete data structure

### 7.3 View Modes
Two viewing modes available:
- **Compact** - Content height limited to 400px with scrolling
- **Expanded** - Full content visible without height restrictions

### 7.4 Download Functionality
Users can download documentation:
- Click "Download" button
- File downloads to local system
- Filename includes format type
- Markdown downloads as .md files
- JSON downloads as .json files

### 7.5 JSON Rendering
JSON is displayed as an interactive collapsible tree:
- Click section headers to expand/collapse
- Nested structures fully expandable
- Color-coded by type (strings, numbers, booleans, null)
- Visual formatting for readability

## 8. Documentation Best Practices

### 8.1 Writing Guidelines
When writing documentation:
1. **Be clear** - Use simple, direct language
2. **Be complete** - Cover the full topic
3. **Be consistent** - Follow existing patterns
4. **Be concise** - Avoid unnecessary words
5. **Be current** - Keep up-to-date with code changes

### 8.2 Keypoint Structure
Each keypoint should follow this pattern:
1. **Name** - Clear, descriptive (3-7 words)
2. **Summary** - One sentence (15-25 words)
3. **What** - What this keypoint addresses
4. **Why** - Why it matters
5. **How** - Implementation details
6. **Example** - Code or procedure
7. **Best practice** - Do's and don'ts

### 8.3 Code Examples
When including code:
- Use proper syntax highlighting
- Keep examples focused (10-20 lines)
- Include comments explaining non-obvious parts
- Show both correct and incorrect patterns when applicable
- Ensure code is tested and accurate

### 8.4 Cross-References
When one keypoint references another:
- Use section number (e.g., "See section 3.1")
- Keep reader in context
- Update all references when renumbering
- Don't create circular references

### 8.5 Avoiding Common Mistakes
- Don't duplicate content across keypoints
- Don't make summaries longer than one sentence
- Don't use advanced jargon without explanation
- Don't include version numbers in content (use metadata)
- Don't commit JSON files with manual edits (regenerate from markdown)

## 9. Version Control and Git

### 9.1 What to Commit
Commit to git:
- ✓ `PROJECT_GUIDELINES.md` - Source markdown
- ✓ `DOCUMENTATION_GUIDELINES.md` - Source markdown
- ✓ `*.json` - Generated JSON documentation
- ✓ `agent.md` - Agent specification
- ✓ `skills.md` - Skills definition

### 9.2 What to Ignore
Do NOT commit:
- ✗ `*.html` - Generated HTML files
- ✗ Temporary working files
- ✗ Cache directories

### 9.3 Commit Messages
When committing documentation changes:
```
docs: Update section 3.1 configuration guidelines

- Clarify port offset system
- Add example for .env variables
- Remove outdated deployment steps

Regenerated JSON from markdown source.
```

### 9.4 Branching for Documentation
For major documentation updates:
1. Create feature branch: `docs/section-name-update`
2. Update markdown files
3. Regenerate JSON files
4. Test in dashboard
5. Create pull request
6. Merge after review

## 10. Documentation Maintenance Schedule

### 10.1 Regular Maintenance
- **Weekly** - Review for accuracy as features change
- **Monthly** - Update examples and add new keypoints
- **Quarterly** - Major review and reorganization
- **On change** - Update immediately when features change

### 10.2 Update Triggers
Update documentation when:
- Code changes affect functionality
- API endpoints are added or modified
- Configuration options change
- New best practices emerge
- User feedback indicates gaps

### 10.3 Review Process
Before committing documentation:
1. Read through entire section
2. Check all examples are accurate
3. Verify all links and references work
4. Validate JSON against schema
5. Test in dashboard viewer
6. Spell-check and grammar review

## 11. Multi-Document System

### 11.1 Adding New Documentation Folders
To create documentation for another component:
1. Create `documentation/component_name/` folder
2. Create `component_name_keypoints.md` file
3. Follow same structure as main guidelines
4. Create corresponding JSON files
5. Create `agent.md` and `skills.md` if applicable
6. Create schemas in `schemas/` directory

### 11.2 Maintaining Multiple Documents
When managing multiple documentation sets:
- Keep consistent structure across all documents
- Share the same version numbering approach
- Use the same JSON schema format
- Reference each other when appropriate
- Test all formats in dashboard

### 11.3 Cross-Document References
When one document references another:
- Use full paths: "See DOCUMENTATION_GUIDELINES.md section 2.1"
- Link via API: Reference the other document's folder
- Keep dependencies clear
- Update all references when structure changes

## 12. Search and Discovery

### 12.1 Making Documentation Searchable
Documentation is searchable via:
- Dashboard search box (searches both sections and summaries)
- API queries (filter by format and content)
- Direct file access (grep/search in markdown)
- JSON query tools (jq for programmatic access)

### 12.2 SEO and Indexing
The documentation system supports:
- Section-based navigation
- Keyword-rich headings
- Clear structure for crawlers
- Semantic HTML in generated pages
- Anchor links for deep linking

### 12.3 Search Optimization
To improve discoverability:
- Use clear, searchable keypoint names
- Include common terminology in descriptions
- Cross-reference related topics
- Keep summaries scannable
- Use bullet points for lists

## 13. Security and Privacy

### 13.1 Sensitive Information Handling
When documenting:
- Never include API keys or credentials
- Never include internal IP addresses
- Never include database passwords
- Reference secrets via environment variables
- Document security practices, not vulnerabilities

### 13.2 Access Control
The documentation system:
- Is served via the internal dashboard
- Is accessible via internal APIs
- Does not require authentication (if server is secured)
- Can be protected by network access control
- Should be treated as internal documentation

### 13.3 Updates to Security Guidelines
Security guidelines are updated:
- When vulnerabilities are discovered
- When best practices change
- When new threats emerge
- Quarterly security reviews
- As part of regular maintenance

## 14. Tools and Automation

### 14.1 Generation Tools
Available tools:
- `html_generator.py` - Converts JSON to interactive HTML
- JSON schema validators - Validate document structure
- Markdown parsers - Parse and analyze content
- API endpoints - Access documentation programmatically

### 14.2 Validation Tools
Ensure documentation quality:
```bash
# Validate JSON against schema
python -m jsonschema -i file.json schema.json

# Check JSON syntax
cat file.json | jq .

# Validate markdown structure
# Use markdown linters
```

### 14.3 Regeneration Commands
Generate documentation formats:
```bash
# From markdown to JSON: Use agent or manual process
# From JSON to HTML:
python documentation/base_server_keypoint/html_generator.py \
  documentation/base_server_keypoint/base_server_keypoints_summary.json \
  templates/documentation_generated.html collapsible
```

## 15. Documentation Quality Metrics

### 15.1 Completeness
Document is complete when:
- All sections are documented
- All keypoints have descriptions
- All code examples are tested
- All references are valid
- All JSON validates against schema

### 15.2 Accuracy
Documentation accuracy includes:
- Code examples run correctly
- Procedures produce expected results
- Version numbers are current
- API endpoints match actual endpoints
- Configuration options match actual options

### 15.3 Clarity
Documentation is clear when:
- Summaries are one sentence
- Descriptions explain the "why"
- Examples are easy to follow
- Technical terms are explained
- Jargon is minimized

### 15.4 Consistency
Documentation is consistent when:
- Style is uniform across sections
- Structure follows established pattern
- Terminology is consistent
- Formatting is regular
- All formats have matching content

### 15.5 Currency
Documentation is current when:
- Matches current code version
- Reflects current best practices
- Updated within last quarter
- Examples run on current system
- Links point to current resources
