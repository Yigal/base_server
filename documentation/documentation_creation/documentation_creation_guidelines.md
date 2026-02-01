# Documentation Creation Guidelines

Complete guide for creating multi-format documentation systems following the base_server architecture pattern.

## 1. Documentation System Architecture

### 1.1 Overview of Multi-Format Documentation
A multi-format documentation system maintains synchronized documentation in multiple formats from a single source. This approach ensures consistency while supporting different use cases and access patterns. The system generates four synchronized formats (full markdown, summary markdown, full JSON, summary JSON) from markdown source files.

### 1.2 Folder Structure for Documentation
Each documentation set lives in its own folder under `documentation/`. The structure follows this pattern:
```
documentation/
├── component_name/
│   ├── component_name_keypoints.md (source document)
│   ├── component_name_keypoints_full.json (generated)
│   ├── component_name_keypoints_summary.json (generated)
│   ├── agent.md (agent specification)
│   ├── skills.md (skills definition)
│   └── schemas/
│       ├── component_name_keypoints_full.schema.json
│       ├── component_name_keypoints_summary.schema.json
│       └── skills.schema.json
```

### 1.3 Core Components Required
Every documentation folder must include these files:
1. **Markdown Source** - The authoritative documentation in markdown format
2. **JSON Versions** - Generated from markdown (full and summary)
3. **Agent Specification** - Defines the documentation generation agent
4. **Skills Definition** - Describes required skills for documentation creation
5. **JSON Schemas** - Validate structure of generated JSON documents

### 1.4 Documentation Naming Convention
All files share a common base name derived from the component:
- Component name: `component_name`
- Base name: `component_name_keypoints`
- Files: `component_name_keypoints.md`, `component_name_keypoints_full.json`, etc.
- Folder: `documentation/component_name/`

## 2. Creating the Markdown Source Document

### 2.1 Markdown Document Structure
The markdown source document is the single source of truth. It must follow a strict hierarchical structure:

```markdown
# Document Title

Brief overview of the document and its purpose.

## 1. Section Name
Section introduction text explaining the topic area.

### 1.1 Keypoint Name
Full description of the keypoint, including purpose, implementation details, examples, and best practices.

### 1.2 Another Keypoint
Additional content for the second keypoint in section 1.

## 2. Next Section
Continue with additional sections...
```

### 2.2 Hierarchical Numbering System
- **Document**: Single # header with title
- **Sections**: ## headers numbered 1-15 (e.g., ## 1, ## 2, ## 3)
- **Keypoints**: ### headers numbered X.Y (e.g., ### 1.1, ### 1.2, ### 2.1)
- **Content**: Regular text under each keypoint

### 2.3 Section Guidelines
Aim for 15 major sections covering all aspects of the component. Each section:
- Has a clear, descriptive name (3-5 words)
- Includes 3-5 keypoints
- Contains an introduction paragraph
- Groups related keypoints logically
- Should be independent but can cross-reference others

### 2.4 Keypoint Guidelines
Each keypoint must include:
1. **Name** - Clear, descriptive title (3-7 words)
2. **Summary** - One sentence capturing essence (15-25 words)
3. **Description** - Full explanation (100-300 words) including:
   - Purpose and why it matters
   - Implementation details
   - Code examples or procedures
   - Best practices
   - Common pitfalls
4. **Examples** - Code blocks or concrete procedures when applicable

### 2.5 Formatting Standards
- Headers: Use only `#`, `##`, `###` (no deeper levels)
- Code blocks: Triple backticks with language specification
- Inline code: Backticks for filenames, variables, config keys
- Lists: `-` for bullets, `1.` for numbered
- Bold: `**text**` for emphasis
- Links: `[text](url)` format
- Tables: Standard markdown tables with pipes

### 2.6 Content Guidelines
When writing documentation:
- **Be clear** - Use simple, direct language
- **Be complete** - Cover the full topic comprehensively
- **Be consistent** - Follow established patterns throughout
- **Be concise** - Avoid unnecessary words
- **Be current** - Keep synchronized with actual implementation

## 3. Generating JSON from Markdown

### 3.1 Markdown to JSON Conversion Process
Transform the markdown source into two JSON versions:

**Steps:**
1. Parse markdown file to identify sections and keypoints
2. Extract section information (id, name, introduction)
3. For each keypoint, extract:
   - ID (e.g., "1.1", "2.3")
   - Name (keypoint title)
   - Summary (one sentence summary from description)
   - Description (full text for full version)
4. Build JSON structure with all keypoints
5. Create summary version (without descriptions)
6. Validate both against schemas

### 3.2 Full JSON Structure
The complete JSON includes all information:

```json
{
  "project": "Component Name",
  "version": "1.0.0",
  "sections": [
    {
      "id": 1,
      "name": "Section Name",
      "keypoints": [
        {
          "id": "1.1",
          "name": "Keypoint Name",
          "summary": "One sentence summary",
          "description": "Full description text"
        }
      ]
    }
  ]
}
```

### 3.3 Summary JSON Structure
The lightweight version omits descriptions:

```json
{
  "project": "Component Name",
  "version": "1.0.0",
  "sections": [
    {
      "id": 1,
      "name": "Section Name",
      "keypoints": [
        {
          "id": "1.1",
          "name": "Keypoint Name",
          "summary": "One sentence summary"
        }
      ]
    }
  ]
}
```

### 3.4 Manual Generation Process
To manually create JSON from markdown:
1. Create empty JSON structure with project and version
2. Parse markdown section headers (##)
3. For each section, create section object
4. Parse keypoint headers (###) within section
5. Extract keypoint data
6. For summary: copy name and summary only
7. For full: include complete descriptions
8. Validate against schema
9. Save to appropriate filenames

### 3.5 Automation Tools
Consider creating scripts to automate conversion:
- Use markdown parsing libraries (markdown, ast)
- Extract structure programmatically
- Generate JSON automatically
- Validate during generation
- Save both full and summary versions

## 4. Creating Agent Specification

### 4.1 Agent.md Purpose
The `agent.md` file specifies the AI agent responsible for generating documentation in this format. It defines:
- Agent name and role
- Capabilities required
- Documentation standards
- Output formats
- Validation requirements

### 4.2 Agent.md Structure
```markdown
# Documentation Generation Agent

## Agent Specification

**Name:** Component Documentation Generator
**Role:** Generate structured documentation in multiple formats
**Version:** 1.0.0

## Capabilities

### Required Capabilities
- Markdown parsing and generation
- Hierarchical structure creation
- JSON schema generation
- Documentation validation

### Skills Required
- Documentation writing
- Technical explanation
- Markdown formatting
- JSON structure creation

## Standards

### Documentation Standards
- Maintain 15 sections, 3-5 keypoints per section
- One-sentence summaries (15-25 words)
- Descriptions 100-300 words
- Consistent formatting throughout
- Cross-reference related sections

### Output Standards
- Four synchronized formats (full/summary markdown/JSON)
- Validated against JSON schemas
- File naming conventions followed
- All content consistent across formats
```

### 4.3 Key Sections for Agent Specification
1. **Agent Identity** - Name, role, version
2. **Capabilities** - What the agent can do
3. **Skills** - Referenced from skills.md
4. **Standards** - Documentation and output standards
5. **Validation** - Schema validation requirements
6. **Error Handling** - How to handle inconsistencies

### 4.4 Agent Requirements
The agent specification should define:
- Minimum 15 sections for comprehensive coverage
- 3-5 keypoints per section
- Consistent structure across sections
- Clear, descriptive names
- Complete descriptions for all keypoints
- One-sentence summaries for all content

## 5. Creating Skills Definition

### 5.1 Skills.md Purpose
The `skills.md` file defines the specific skills required to generate documentation. These skills describe the capabilities and procedures the agent needs.

### 5.2 Skills Structure
```markdown
# Documentation Generation Skills

## Skill 1: Markdown Parsing
**Purpose:** Parse markdown documents and extract structure
**Required For:** Initial documentation analysis
**Procedure:**
1. Read markdown file
2. Identify headers (# ## ###)
3. Extract hierarchical structure
4. Validate section numbering
5. Group keypoints by section

## Skill 2: JSON Generation
**Purpose:** Generate structured JSON from markdown content
**Required For:** Creating machine-readable formats
**Procedure:**
1. Create JSON structure template
2. Populate with extracted data
3. Validate against schema
4. Generate summary version
5. Save both versions

...more skills...
```

### 5.3 Skills to Include
Document these essential skills:
1. **Markdown Parsing** - Extract structure from markdown
2. **Hierarchical Structure Creation** - Organize into sections/keypoints
3. **JSON Generation** - Create JSON formats from markdown
4. **Summary Creation** - Condense descriptions to one sentences
5. **Schema Validation** - Ensure JSON matches schema
6. **Format Synchronization** - Keep all formats consistent
7. **File Management** - Save and organize files
8. **Quality Assurance** - Validate completeness and accuracy

### 5.4 Skill Definition Format
Each skill should include:
- **Name** - Clear skill identifier
- **Purpose** - Why this skill is needed
- **Required For** - Which documentation generation steps
- **Procedure** - Step-by-step instructions
- **Inputs** - What data the skill works with
- **Outputs** - What the skill produces
- **Validation** - How to verify correctness

### 5.5 Skill Interdependencies
Show how skills depend on each other:
- Markdown Parsing → Hierarchical Structure
- Hierarchical Structure → JSON Generation
- JSON Generation → Schema Validation
- Summary Creation depends on Description Extraction
- Format Synchronization depends on all format generation

## 6. Creating JSON Schemas

### 6.1 Schema Purpose
JSON schemas validate the structure and content of generated JSON documents. They enforce:
- Required fields presence
- Correct data types
- Valid ID format (X.Y pattern)
- String length constraints
- Proper nesting structure

### 6.2 Full Schema Structure
For the complete documentation format:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "project": {"type": "string"},
    "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
    "sections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "integer", "minimum": 1, "maximum": 15},
          "name": {"type": "string"},
          "keypoints": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {"type": "string", "pattern": "^\\d+\\.\\d+$"},
                "name": {"type": "string"},
                "summary": {"type": "string", "maxLength": 200},
                "description": {"type": "string"}
              },
              "required": ["id", "name", "summary", "description"]
            }
          }
        },
        "required": ["id", "name", "keypoints"]
      }
    }
  },
  "required": ["project", "version", "sections"]
}
```

### 6.3 Summary Schema Structure
For the lightweight format (without descriptions):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "project": {"type": "string"},
    "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
    "sections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "integer", "minimum": 1, "maximum": 15},
          "name": {"type": "string"},
          "keypoints": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {"type": "string", "pattern": "^\\d+\\.\\d+$"},
                "name": {"type": "string"},
                "summary": {"type": "string", "maxLength": 200}
              },
              "required": ["id", "name", "summary"]
            }
          }
        },
        "required": ["id", "name", "keypoints"]
      }
    }
  },
  "required": ["project", "version", "sections"]
}
```

### 6.4 Key Schema Validations
Include these validation rules:
- Project name required and string type
- Version in semantic format (X.Y.Z)
- Sections array with 1-15 items
- Section IDs sequential integers
- Keypoint IDs in X.Y format
- Summaries max 200 characters
- All required fields present
- Proper type checking

## 7. Setting Up the Documentation Folder

### 7.1 Complete Folder Creation Checklist
```
documentation/component_name/
├── component_name_keypoints.md         (✓ Create source)
├── component_name_keypoints_full.json  (✓ Generate)
├── component_name_keypoints_summary.json (✓ Generate)
├── agent.md                            (✓ Create specification)
├── skills.md                           (✓ Create skills)
└── schemas/
    ├── component_name_keypoints_full.schema.json    (✓ Create)
    ├── component_name_keypoints_summary.schema.json (✓ Create)
    └── skills.schema.json                          (✓ Create)
```

### 7.2 Step-by-Step Setup Process
1. Create `documentation/component_name/` folder
2. Create markdown source document with 15 sections
3. Organize into 3-5 keypoints per section
4. Create agent.md specification
5. Create skills.md with required skills
6. Generate full JSON from markdown
7. Generate summary JSON from markdown
8. Create validation schemas
9. Validate JSON against schemas
10. Test with dashboard integration

### 7.3 File Creation Order
Recommended sequence:
1. **First**: Markdown source (foundation)
2. **Second**: Agent specification (define requirements)
3. **Third**: Skills definition (detail capabilities)
4. **Fourth**: JSON schema files (define validation)
5. **Fifth**: Generate JSON files (create formats)
6. **Sixth**: Validate JSON (ensure correctness)
7. **Seventh**: Test in dashboard (verify integration)

## 8. Validating Your Documentation

### 8.1 Markdown Validation
Check the markdown source:
- All sections numbered sequentially (## 1, ## 2, etc.)
- All keypoints numbered correctly (### 1.1, ### 1.2, etc.)
- No missing section numbers
- No keypoints without section
- Summaries are single sentences
- Descriptions are 100-300 words
- No deeper header levels (no ####)

### 8.2 JSON Validation
Validate generated JSON:
- Use JSON schema validators
- Check file is valid JSON
- Verify structure matches schema
- Ensure all required fields present
- Validate data types
- Check summary field constraints

```bash
# Validate JSON against schema
jsonschema -i component_name_keypoints_full.json \
  schemas/component_name_keypoints_full.schema.json
```

### 8.3 Format Consistency
Verify synchronization:
- Same sections in all formats
- Same keypoints in all formats
- Same names/IDs in all formats
- Summaries identical in all versions
- Full JSON has descriptions, summary doesn't

### 8.4 Quality Checklist
Before finalizing:
- ✓ All 15 sections present
- ✓ 3-5 keypoints per section
- ✓ Descriptive section names
- ✓ Clear keypoint titles
- ✓ One-sentence summaries
- ✓ Complete descriptions
- ✓ Code examples included
- ✓ JSON validates against schema
- ✓ All formats synchronized
- ✓ No broken cross-references

## 9. Integrating with Dashboard

### 9.1 Dashboard Integration Steps
Once documentation folder is created:
1. Place folder in `documentation/component_name/`
2. Ensure JSON files are properly formatted
3. Documentation auto-appears in dashboard
4. Update documentation index if needed
5. Test format selector with all 4 formats

### 9.2 API Integration
The documentation is automatically accessible via:
- `GET /api/documents` - Lists all available documents
- `GET /api/document?folder=component_name&document=component_name_keypoints&format=summary_json`

### 9.3 Dashboard Features
Once integrated, users can:
- Select documentation format from dropdown
- Toggle between compact and expanded views
- Download documentation in any format
- Expand/collapse JSON sections
- View all 4 synchronized formats

## 10. Best Practices

### 10.1 Documentation Standards
- Maintain consistent voice throughout
- Use active voice for clarity
- Explain the "why" not just "what"
- Include practical examples
- Group related concepts together
- Cross-reference when helpful
- Update when code changes

### 10.2 Structure Best Practices
- Organize by major concepts (15 sections)
- Group related details (3-5 keypoints per section)
- Use clear, searchable names
- Follow naming conventions consistently
- Maintain logical flow
- Group prerequisites at the beginning

### 10.3 Content Best Practices
- Write for your audience level
- Avoid unnecessary jargon
- Include code examples
- Provide procedures for tasks
- Show correct and incorrect patterns
- Keep examples focused (10-20 lines)
- Test all code examples

### 10.4 Maintenance Best Practices
- Review documentation quarterly
- Update when features change
- Keep examples current
- Track version numbers
- Maintain all 4 formats
- Validate regularly
- Document decision rationale

## 11. Common Issues and Solutions

### 11.1 Numbering Problems
**Issue**: Keypoint numbers don't follow X.Y pattern
**Solution**: Renumber systematically: 1.1, 1.2, 1.3, then 2.1, 2.2, etc.

**Issue**: Sections not numbered 1-15
**Solution**: Use ## 1, ## 2, ... ## 15 format exactly

### 11.2 JSON Generation Issues
**Issue**: JSON doesn't validate against schema
**Solution**:
- Check all required fields present
- Verify ID format (X.Y for keypoints)
- Ensure proper nesting
- Validate data types
- Run schema validation tool

### 11.3 Format Synchronization Issues
**Issue**: Summary and full formats have different keypoints
**Solution**:
- Ensure same sections in all formats
- Same keypoints in all formats
- Regenerate from single markdown source

### 11.4 Content Issues
**Issue**: Descriptions too long or too short
**Solution**: Aim for 100-300 words per description

**Issue**: Summaries longer than one sentence
**Solution**: Extract core concept into single sentence

## 12. Advanced Topics

### 12.1 Creating Custom Schemas
Extend base schema for custom properties:
- Add component-specific fields
- Define custom validation rules
- Create validation-specific schemas
- Document any custom fields

### 12.2 Automating Generation
Scripts to automate the process:
- Markdown parser
- JSON generator
- Schema validator
- Format synchronization checker

### 12.3 Multi-Language Support
Extending for multiple languages:
- Create translations of markdown
- Generate language-specific JSON
- Maintain consistency across languages
- Support language selection in dashboard

### 12.4 Versioning Strategy
Managing documentation versions:
- Use semantic versioning (X.Y.Z)
- Track changes in git
- Maintain version history
- Document breaking changes

## 13. Complete Example

### 13.1 Example Documentation Folder
Create `documentation/my_component/`:

**my_component_keypoints.md**:
- 15 sections (## 1 through ## 15)
- 3-5 keypoints per section (### 1.1, 1.2, etc.)
- Full descriptions for all keypoints
- Code examples where appropriate

**agent.md**:
- Agent specification for documentation generation
- Capability definitions
- Standards and requirements

**skills.md**:
- Markdown parsing skill
- JSON generation skill
- Schema validation skill
- And additional skills

**Schemas**:
- `my_component_keypoints_full.schema.json`
- `my_component_keypoints_summary.schema.json`
- `skills.schema.json`

### 13.2 Example Workflow
1. Write my_component_keypoints.md (100-300 words per keypoint)
2. Extract summaries to create summary version
3. Generate JSON structures from markdown
4. Validate against schemas
5. Place in documentation folder
6. Test in dashboard
7. Commit to version control

## 14. Version Management

### 14.1 Versioning Guidelines
Each documentation set has a version:
- Format: X.Y.Z (semantic versioning)
- X (major): Large structural changes
- Y (minor): Added sections/keypoints
- Z (patch): Content updates, fixes

### 14.2 Version Tracking
- Include version in JSON metadata
- Update in markdown header comments
- Track in git commits
- Document version history

### 14.3 Update Triggers
Update version when:
- Adding sections (minor version)
- Adding keypoints (minor version)
- Major restructuring (major version)
- Content updates (patch version)
- Bug fixes (patch version)

## 15. Documentation Quality Metrics

### 15.1 Completeness Metrics
- 15 sections: ✓ or count
- 3-5 keypoints per section: ✓ or gaps
- All keypoints described: ✓ or count
- Code examples present: ✓ or count
- JSON validates: ✓ or errors

### 15.2 Accuracy Metrics
- Code examples execute: ✓ or failures
- Procedures produce results: ✓ or issues
- Links work: ✓ or broken
- Version numbers current: ✓ or outdated
- Cross-references valid: ✓ or broken

### 15.3 Clarity Metrics
- Summaries one sentence: ✓ or need editing
- Descriptions explain "why": ✓ or unclear
- Examples are clear: ✓ or confusing
- Technical terms explained: ✓ or undefined
- Jargon minimized: ✓ or excessive

### 15.4 Consistency Metrics
- Style uniform: ✓ or varies
- Structure consistent: ✓ or inconsistent
- Terminology consistent: ✓ or mixed
- Formatting regular: ✓ or irregular
- Formats synchronized: ✓ or differences
