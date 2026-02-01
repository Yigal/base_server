# Documentation Generation Skills

Complete skill definitions for creating multi-format documentation systems following the base_server architecture.

## Skill 1: Markdown Document Creation

**Skill Name:** Markdown Document Creation
**Purpose:** Write comprehensive markdown documentation with proper hierarchical structure
**Required For:** Creating the source documentation that all formats derive from
**Complexity:** Intermediate
**Time Typical:** 2-4 hours per component

### Procedure

**Step 1: Plan the 15 Sections**
1. Identify major topic areas for the component
2. Create list of 15 logical sections
3. Ensure each section covers distinct topic
4. Order sections from foundational to advanced
5. Group related concepts together
6. Verify no overlap between sections

**Step 2: Design Keypoints per Section**
1. For each section, identify 3-5 key topics
2. Write brief description of each keypoint
3. Plan code examples or procedures
4. Ensure keypoints are independent but related
5. Verify keypoints cover section comprehensively
6. Number keypoints X.1, X.2, X.3, etc.

**Step 3: Write Markdown Document**
1. Create file: `component_name_keypoints.md`
2. Add document title with single # header
3. Add brief document description (2-3 sentences)
4. For each section:
   - Add `## N. Section Name` header
   - Write section introduction (1-2 paragraphs)
5. For each keypoint:
   - Add `### N.K Keypoint Name` header
   - Write one-sentence summary (15-25 words)
   - Write full description (100-300 words)
   - Include code examples if applicable
   - Add best practices or warnings

**Step 4: Format the Content**
1. Use proper markdown syntax:
   - Headers: `#`, `##`, `###` only
   - Code blocks: ` ``` ` with language
   - Inline code: Single backticks
   - Bold: `**text**`
   - Lists: `-` for bullets, `1.` for numbered
2. Ensure consistent indentation
3. Add blank lines between sections
4. Verify all code blocks have language specification

**Step 5: Validate Structure**
1. Count sections: should be exactly 15
2. Check section numbering: ## 1, ## 2, ..., ## 15
3. Count keypoints per section: should be 3-5
4. Verify keypoint numbering: ### X.1, X.2, X.3, etc.
5. No keypoints without parent section
6. No sections without introduction

### Inputs
- Component specification and features
- Knowledge of component architecture
- Use cases and workflows
- Best practices and standards
- Example code and procedures

### Outputs
- `component_name_keypoints.md` file
- Well-structured markdown document
- 15 sections with clear organization
- 45-75 keypoints across all sections
- Validated hierarchical structure

### Validation Checklist
- [ ] File created with correct name
- [ ] Exactly 15 sections (## 1-15)
- [ ] 3-5 keypoints per section
- [ ] All headers follow format (##, ###)
- [ ] Code blocks properly formatted
- [ ] Summaries are one sentence max
- [ ] Descriptions are 100-300 words
- [ ] No header levels deeper than ###
- [ ] Cross-references valid
- [ ] Consistent style throughout

### Common Issues and Fixes

**Issue:** Sections are not numbered sequentially
**Fix:** Use ## 1, ## 2, ## 3, etc. format precisely

**Issue:** Keypoint summary is longer than one sentence
**Fix:** Extract the core concept into single sentence

**Issue:** Descriptions are too short (< 100 words)
**Fix:** Add more detail about purpose, implementation, examples

**Issue:** Descriptions are too long (> 300 words)
**Fix:** Condense to essential information

---

## Skill 2: Markdown Parsing and Structure Extraction

**Skill Name:** Markdown Parsing and Structure Extraction
**Purpose:** Parse markdown files and extract hierarchical structure
**Required For:** Converting markdown to JSON, validating structure
**Complexity:** Intermediate
**Time Typical:** 30 minutes - 1 hour

### Procedure

**Step 1: Read the Markdown File**
1. Open `component_name_keypoints.md`
2. Read entire file to understand structure
3. Identify document title (# header)
4. Identify document description
5. Note overall organization

**Step 2: Extract Sections**
1. Identify all `## N.` headers (sections)
2. For each section, record:
   - Section number (integer 1-15)
   - Section name (text after ##)
   - Section introduction text
   - Starting line number
3. Verify numbering is sequential (1-15)
4. Create sections array with all data

**Step 3: Extract Keypoints**
1. For each section, identify all `### N.K` headers
2. For each keypoint, record:
   - Keypoint ID (string "N.K", e.g., "1.1")
   - Keypoint name (text after ###)
   - Full description text until next header
3. Extract one-sentence summary from description
   - Usually first sentence
   - May need to condense if longer
   - Should be 15-25 words

**Step 4: Structure the Data**
1. Create hierarchical object:
   ```
   Document
   ├── Title
   ├── Description
   └── Sections[]
       ├── id: integer
       ├── name: string
       └── keypoints[]
           ├── id: "X.K"
           ├── name: string
           ├── summary: string
           └── description: string
   ```
2. Verify all parent-child relationships
3. Ensure no orphaned keypoints or sections

**Step 5: Validate Extracted Structure**
1. Count sections: exactly 15
2. Check all sections numbered 1-15
3. Count keypoints per section: 3-5 range
4. Verify keypoint numbering format (X.K)
5. No gaps in section numbers
6. No gaps in keypoint numbers within sections
7. All required fields populated

### Inputs
- `component_name_keypoints.md` file
- Knowledge of markdown format
- Understanding of hierarchical structure

### Outputs
- Extracted section array with:
  - Section IDs (1-15)
  - Section names
  - Section introductions
- Extracted keypoint array with:
  - Keypoint IDs (X.K format)
  - Keypoint names
  - Keypoint summaries
  - Full descriptions
- Validation report

### Validation Checklist
- [ ] All sections extracted (15 total)
- [ ] All keypoints extracted (45-75 total)
- [ ] Section numbering correct (1-15)
- [ ] Keypoint numbering correct (X.K)
- [ ] No missing data fields
- [ ] Summaries extracted correctly
- [ ] Descriptions are complete
- [ ] Hierarchical structure valid

### Common Issues and Fixes

**Issue:** Summary is longer than one sentence
**Fix:** Take first sentence only, or condense to core concept

**Issue:** Keypoints missing (count is wrong)
**Fix:** Review markdown, find missing ### headers

**Issue:** Section numbering has gaps
**Fix:** Verify original markdown has all ## 1 through ## 15

---

## Skill 3: JSON Document Generation

**Skill Name:** JSON Document Generation
**Purpose:** Convert extracted markdown structure into valid JSON documents
**Required For:** Creating full and summary JSON versions
**Complexity:** Intermediate
**Time Typical:** 30 minutes per document

### Procedure

**Step 1: Create Full JSON Structure**
1. Start with base JSON template:
   ```json
   {
     "project": "Component Name",
     "version": "1.0.0",
     "sections": []
   }
   ```
2. Set project to component name
3. Set version to "1.0.0" (or appropriate version)

**Step 2: Add Sections to JSON**
1. For each extracted section:
   - Create section object
   - Set "id" to section number (integer)
   - Set "name" to section name (string)
   - Initialize "keypoints" array
2. Add section to sections array
3. Maintain section order (1-15)

**Step 3: Add Keypoints to JSON**
1. For each keypoint in section:
   - Create keypoint object
   - Set "id" to "X.K" format (string)
   - Set "name" to keypoint name
   - Set "summary" to one-sentence summary
   - Set "description" to full description text
2. Add keypoint to section's keypoints array
3. Maintain keypoint order within section

**Step 4: Generate Summary JSON**
1. Create copy of full JSON structure
2. Keep all sections and keypoints
3. Remove "description" field from all keypoints
4. Keep only: id, name, summary
5. Result: lightweight version for quick reference

**Step 5: Validate JSON Syntax**
1. Test with JSON validator (e.g., `jq .`)
2. Verify:
   - Proper bracket/brace nesting
   - All strings quoted
   - All commas in correct places
   - No trailing commas
   - Valid JSON syntax
3. If syntax errors, fix and retest

**Step 6: Save JSON Files**
1. Save full version as `component_name_keypoints_full.json`
2. Save summary version as `component_name_keypoints_summary.json`
3. Use 2-space indentation for readability
4. Ensure UTF-8 encoding
5. Verify files can be read

### Inputs
- Extracted markdown structure (from Skill 2)
- Component name and version
- All keypoint names, IDs, summaries, descriptions

### Outputs
- `component_name_keypoints_full.json` (35-50 KB typical)
- `component_name_keypoints_summary.json` (15-25 KB typical)
- Both in valid JSON format
- Proper indentation and formatting

### Validation Checklist
- [ ] Full JSON is valid (no syntax errors)
- [ ] Summary JSON is valid (no syntax errors)
- [ ] All sections present in both
- [ ] All keypoints present in both
- [ ] Section IDs are integers 1-15
- [ ] Keypoint IDs are "X.K" format
- [ ] Full JSON has descriptions
- [ ] Summary JSON doesn't have descriptions
- [ ] File encoding is UTF-8
- [ ] Files are readable

### Common Issues and Fixes

**Issue:** JSON syntax error (invalid structure)
**Fix:** Check bracket/brace matching, remove trailing commas

**Issue:** Summary and full have different keypoints
**Fix:** Ensure both generated from same source

**Issue:** Missing descriptions in full JSON
**Fix:** Add all description fields during generation

---

## Skill 4: JSON Schema Creation

**Skill Name:** JSON Schema Creation
**Purpose:** Create validation schemas for generated JSON documents
**Required For:** Validating JSON structure and format
**Complexity:** Intermediate-Advanced
**Time Typical:** 1-2 hours

### Procedure

**Step 1: Create Full JSON Schema**
1. Start with schema template:
   ```json
   {
     "$schema": "http://json-schema.org/draft-07/schema#",
     "type": "object",
     "properties": {},
     "required": []
   }
   ```
2. Define top-level properties:
   - "project": string
   - "version": string (pattern: X.Y.Z)
   - "sections": array

**Step 2: Define Section Schema**
1. Create section object schema:
   ```json
   {
     "type": "object",
     "properties": {
       "id": {"type": "integer", "minimum": 1, "maximum": 15},
       "name": {"type": "string"},
       "keypoints": {"type": "array"}
     },
     "required": ["id", "name", "keypoints"]
   }
   ```
2. Add as items definition for sections array

**Step 3: Define Keypoint Schema for Full**
1. Create keypoint object schema (with description):
   ```json
   {
     "type": "object",
     "properties": {
       "id": {"type": "string", "pattern": "^\\d+\\.\\d+$"},
       "name": {"type": "string"},
       "summary": {"type": "string", "maxLength": 200},
       "description": {"type": "string"}
     },
     "required": ["id", "name", "summary", "description"]
   }
   ```
2. Add as items definition for keypoints array

**Step 4: Create Summary JSON Schema**
1. Copy full schema
2. Modify keypoint schema:
   - Remove "description" from properties
   - Remove "description" from required fields
   - Keep only: id, name, summary
3. Save as separate schema file

**Step 5: Validate Schema Syntax**
1. Test schema with `jq .`
2. Verify:
   - Valid JSON syntax
   - Proper schema structure
   - All required properties defined
   - Type constraints correct
   - Pattern constraints valid
3. If errors, fix and retest

**Step 6: Save Schema Files**
1. Save full schema as `component_name_keypoints_full.schema.json`
2. Save summary schema as `component_name_keypoints_summary.schema.json`
3. Use 2-space indentation
4. Ensure UTF-8 encoding
5. Store in `schemas/` subdirectory

### Inputs
- Expected JSON structure (from Skill 3)
- Field definitions and constraints
- Type requirements
- Pattern constraints (e.g., "X.Y.Z" for version)

### Outputs
- `component_name_keypoints_full.schema.json`
- `component_name_keypoints_summary.schema.json`
- Valid JSON Schema Draft 7 format
- Comprehensive validation rules

### Validation Checklist
- [ ] Schema files are valid JSON
- [ ] Full schema includes description field
- [ ] Summary schema excludes description field
- [ ] All required fields specified
- [ ] Type constraints accurate
- [ ] Pattern constraints valid
- [ ] Section IDs: integer 1-15
- [ ] Keypoint IDs: "X.Y" pattern
- [ ] Summary max length 200 chars
- [ ] Version format X.Y.Z pattern

### Common Issues and Fixes

**Issue:** Schema syntax error
**Fix:** Validate with `jq .`, fix brackets/commas

**Issue:** Generated JSON fails validation
**Fix:** Check schema constraints, update schema or JSON

**Issue:** Summary schema has description requirement
**Fix:** Remove description from properties and required

---

## Skill 5: JSON Schema Validation

**Skill Name:** JSON Schema Validation
**Purpose:** Validate generated JSON documents against schemas
**Required For:** Quality assurance before deployment
**Complexity:** Intermediate
**Time Typical:** 15-30 minutes

### Procedure

**Step 1: Prepare for Validation**
1. Ensure JSON files exist:
   - `component_name_keypoints_full.json`
   - `component_name_keypoints_summary.json`
2. Ensure schema files exist:
   - `component_name_keypoints_full.schema.json`
   - `component_name_keypoints_summary.schema.json`
3. Have validation tool available (Python jsonschema, online validator, etc.)

**Step 2: Validate Full JSON**
1. Load full JSON file
2. Load full schema file
3. Run validation against schema
4. Check for errors:
   - Missing required fields
   - Wrong data types
   - Constraint violations
   - Pattern mismatches
5. Document any errors found

**Step 3: Validate Summary JSON**
1. Load summary JSON file
2. Load summary schema file
3. Run validation against schema
4. Verify:
   - No description fields present
   - All other fields match full version
   - Structure is consistent
5. Document any errors found

**Step 4: Cross-Validate Consistency**
1. Compare full and summary JSON:
   - Same sections (ids and names)
   - Same keypoints (ids and names)
   - Same summaries (if present in both)
   - Different: descriptions (full only)
2. Identify any inconsistencies
3. Report differences

**Step 5: Verify Constraints**
1. Check section IDs: integers 1-15
2. Check keypoint IDs: "X.Y" format
3. Check summaries: <= 200 characters
4. Check version: X.Y.Z format
5. Check all required fields present
6. Report any constraint violations

**Step 6: Generate Validation Report**
1. Create validation report with:
   - Status (Pass/Fail)
   - Validation date/time
   - Files validated
   - Errors found (if any)
   - Warnings (if any)
   - Pass criteria verification
2. Document for records

### Inputs
- Generated JSON files (full and summary)
- JSON schema files (full and summary)
- Validation tool
- Expected structure knowledge
- Access to config.json (for port configuration if needed)

### Outputs
- Validation report
- Error list (if any)
- Status: PASS or FAIL
- Constraints verification report

### Validation Checklist
- [ ] Full JSON syntax valid
- [ ] Summary JSON syntax valid
- [ ] Full JSON passes schema
- [ ] Summary JSON passes schema
- [ ] Sections present in both
- [ ] Keypoints identical in both
- [ ] Summaries match between versions
- [ ] No description in summary JSON
- [ ] Section IDs are integers 1-15
- [ ] Keypoint IDs are "X.K" format
- [ ] Version format is X.Y.Z
- [ ] All required fields present

### Common Issues and Fixes

**Issue:** JSON file is invalid (syntax error)
**Fix:** Use `jq .` to find syntax error, fix JSON

**Issue:** JSON fails schema validation
**Fix:** Check error message, update JSON or schema

**Issue:** Summary has description fields
**Fix:** Remove description field from all keypoints

---

## Skill 6: Format Synchronization Verification

**Skill Name:** Format Synchronization Verification
**Purpose:** Ensure all 4 documentation formats stay synchronized
**Required For:** Quality assurance, detecting format drift
**Complexity:** Intermediate
**Time Typical:** 30-45 minutes

### Procedure

**Step 1: Extract All Sections and Keypoints**
1. From markdown file, extract:
   - All sections (## headers)
   - All keypoints (### headers)
   - Section names and keypoint names
   - Keypoint summaries
2. From full JSON, extract:
   - All sections (from "sections" array)
   - All keypoints (from "keypoints" arrays)
   - Names and IDs
3. From summary JSON, extract:
   - All sections
   - All keypoints
   - Names and IDs

**Step 2: Compare Section Structure**
1. Verify same number of sections:
   - Markdown: count ## headers
   - Full JSON: count sections array items
   - Summary JSON: count sections array items
   - All should be 15
2. Verify section order and numbering:
   - Markdown: ## 1, ## 2, ... ## 15
   - JSON: "id": 1, "id": 2, ... "id": 15
3. Verify section names match:
   - Compare names across formats
   - All should be identical

**Step 3: Compare Keypoint Structure**
1. For each section, verify keypoints:
   - Same IDs (e.g., "1.1", "1.2")
   - Same names
   - Same count per section
2. Verify keypoint order within sections
3. No extra or missing keypoints

**Step 4: Compare Summaries**
1. For each keypoint, compare summaries:
   - Markdown summary
   - Full JSON summary
   - Summary JSON summary
2. All should be identical
3. Identify any discrepancies
4. Verify single-sentence format

**Step 5: Verify Content Differences**
1. Full JSON should have:
   - All field types
   - Description field
2. Summary JSON should NOT have:
   - Description field
   - Any other extra content
3. Markdown should have:
   - Full descriptions
   - Code examples
   - More detailed information

**Step 6: Generate Synchronization Report**
1. Create report documenting:
   - Sections: count and names
   - Keypoints: count per section
   - Summary consistency: same across formats
   - Content differences: expected vs. actual
   - Status: SYNCHRONIZED or DRIFT DETECTED
2. List any format inconsistencies found

### Inputs
- Markdown source document
- Full JSON file
- Summary JSON file
- Knowledge of expected structure

### Outputs
- Synchronization report
- List of inconsistencies (if any)
- Status: SYNCHRONIZED or DRIFT
- Recommendations for fixes

### Validation Checklist
- [ ] All formats have 15 sections
- [ ] Section IDs and names match
- [ ] All formats have 3-5 keypoints per section
- [ ] Keypoint IDs match across formats
- [ ] Keypoint names match across formats
- [ ] Summaries identical across formats
- [ ] Full JSON has descriptions
- [ ] Summary JSON doesn't have descriptions
- [ ] No extra fields in any format
- [ ] No missing fields in any format

### Common Issues and Fixes

**Issue:** Summary and full have different keypoint counts
**Fix:** Regenerate from single markdown source

**Issue:** Summaries differ between formats
**Fix:** Re-extract summaries to ensure consistency

**Issue:** Missing sections in JSON
**Fix:** Verify markdown has all ## 1-15, regenerate JSON

---

## Skill 7: File Organization and Naming

**Skill Name:** File Organization and Naming
**Purpose:** Organize documentation files in correct folder structure with proper naming
**Required For:** Dashboard integration, API discovery
**Complexity:** Basic-Intermediate
**Time Typical:** 15-30 minutes

### Procedure

**Step 1: Create Folder Structure**
1. Create main folder: `documentation/component_name/`
2. Create subdirectory: `documentation/component_name/schemas/`
3. Verify folder permissions allow read/write
4. Verify web server can access folders

**Step 2: Name Component Consistently**
1. Choose component name (e.g., "api_server", "user_auth")
2. Use lowercase with underscores
3. Use consistently in all file names
4. Create base name: `component_name_keypoints`
5. Document naming convention

**Step 3: Place Markdown File**
1. Name: `component_name_keypoints.md`
2. Location: `documentation/component_name/`
3. Full path: `documentation/component_name/component_name_keypoints.md`
4. Verify file can be read from web server

**Step 4: Place JSON Files**
1. Full JSON name: `component_name_keypoints_full.json`
2. Summary JSON name: `component_name_keypoints_summary.json`
3. Location: `documentation/component_name/`
4. Full paths:
   - `documentation/component_name/component_name_keypoints_full.json`
   - `documentation/component_name/component_name_keypoints_summary.json`
5. Verify files readable by web server

**Step 5: Place Schema Files**
1. Full schema: `component_name_keypoints_full.schema.json`
2. Summary schema: `component_name_keypoints_summary.schema.json`
3. Location: `documentation/component_name/schemas/`
4. Full paths:
   - `documentation/component_name/schemas/component_name_keypoints_full.schema.json`
   - `documentation/component_name/schemas/component_name_keypoints_summary.schema.json`
5. Verify files are valid JSON

**Step 6: Place Agent and Skills Files**
1. Agent file: `agent.md`
2. Skills file: `skills.md`
3. Location: `documentation/component_name/`
4. Full paths:
   - `documentation/component_name/agent.md`
   - `documentation/component_name/skills.md`
5. Verify Markdown is properly formatted

**Step 7: Verify Final Structure**
1. Expected structure:
   ```
   documentation/component_name/
   ├── component_name_keypoints.md
   ├── component_name_keypoints_full.json
   ├── component_name_keypoints_summary.json
   ├── agent.md
   ├── skills.md
   └── schemas/
       ├── component_name_keypoints_full.schema.json
       ├── component_name_keypoints_summary.schema.json
       └── skills.schema.json
   ```
2. Check all files present
3. Verify naming conventions
4. Verify file permissions (readable)
5. Verify folder structure correct

### Inputs
- All created files (markdown, JSON, schemas)
- Component name
- Folder path information

### Outputs
- Properly organized folder structure
- All files in correct locations
- Proper file naming
- Verified permissions

### Validation Checklist
- [ ] Folder `documentation/component_name/` exists
- [ ] Subfolder `schemas/` exists
- [ ] Markdown file named correctly
- [ ] Full JSON file named correctly
- [ ] Summary JSON file named correctly
- [ ] Full schema named correctly
- [ ] Summary schema named correctly
- [ ] Agent file named `agent.md`
- [ ] Skills file named `skills.md`
- [ ] All files in correct locations
- [ ] All files readable by web server
- [ ] No extra files or folders

### Common Issues and Fixes

**Issue:** Files in wrong locations
**Fix:** Move files to correct folders matching structure

**Issue:** Naming doesn't match convention
**Fix:** Rename files to follow component_name_keypoints pattern

**Issue:** Web server can't read files
**Fix:** Check file permissions, ensure 644 or better for files

---

## Skill 8: Agent and Skills Documentation Creation

**Skill Name:** Agent and Skills Documentation Creation
**Purpose:** Document the documentation generation agent and required skills
**Required For:** Understanding documentation system and execution
**Complexity:** Intermediate-Advanced
**Time Typical:** 2-3 hours

### Procedure

**Step 1: Create Agent Specification**
1. Create file: `agent.md` in `documentation/component_name/`
2. Include sections:
   - Agent Identity (name, version, role)
   - Agent Description (what it does)
   - Core Capabilities (8-10 major capabilities)
   - Required Skills (list from skills.md)
   - Standards and Requirements (documentation standards)
   - Validation Requirements (checklist)
   - Output Formats (types of documents)
   - Error Handling (procedures)
   - Integration Points (where agent fits)
   - Success Criteria (how to measure success)
3. Use markdown headers (## and ###)
4. Include detailed descriptions

**Step 2: Define Agent Capabilities**
1. List 8-10 major capabilities:
   - Documentation architecture understanding
   - Markdown source creation
   - JSON generation
   - Schema creation and validation
   - Format synchronization
   - Agent and skills definition
   - Dashboard integration
   - Quality assurance
   - (Additional as appropriate)
2. For each capability, describe:
   - What the agent can do
   - When the capability is used
   - Any dependencies

**Step 3: Create Skills Definition**
1. Create file: `skills.md` in `documentation/component_name/`
2. Include sections for each skill:
   - Skill Name
   - Purpose
   - Required For
   - Procedure (step-by-step)
   - Inputs
   - Outputs
   - Validation Checklist
   - Common Issues and Fixes
3. Include 8+ skills covering:
   - Markdown creation
   - Markdown parsing
   - JSON generation
   - Schema creation
   - Schema validation
   - Format synchronization
   - File organization
   - Documentation creation
   - (Additional as appropriate)

**Step 4: Define Skill Procedures**
1. For each skill, create detailed procedure:
   - Clear, numbered steps
   - Specific, actionable instructions
   - No ambiguous directions
   - Include decisions points
   - Show order dependencies
2. Include examples where helpful
3. Define inputs and outputs clearly

**Step 5: Document Skill Interdependencies**
1. Show which skills depend on others:
   - Markdown Parsing depends on Markdown Creation
   - JSON Generation depends on Markdown Parsing
   - Schema Validation depends on Schema Creation
   - Format Synchronization depends on JSON Generation
2. Create dependency diagram or description
3. Show execution order

**Step 6: Create Validation Sections**
1. For agent, include:
   - Validation requirements checklist
   - Success criteria
   - Quality metrics
2. For each skill, include:
   - Validation checklist
   - Common issues and fixes
   - Quality gates

### Inputs
- Completed documentation files
- Understanding of agent architecture
- Knowledge of skills required
- Documentation creation experience

### Outputs
- `agent.md` specification file
- `skills.md` definitions file
- Complete procedure documentation
- Clear skill interdependencies
- Validation criteria

### Validation Checklist
- [ ] Agent file created with correct name
- [ ] Skills file created with correct name
- [ ] Both files in `documentation/component_name/`
- [ ] Agent includes identity section
- [ ] Agent lists 8-10 capabilities
- [ ] Agent includes success criteria
- [ ] Skills file includes 8+ skills
- [ ] Each skill has procedure section
- [ ] Each skill has inputs/outputs defined
- [ ] Each skill has validation checklist
- [ ] Skill interdependencies documented
- [ ] Markdown properly formatted

### Common Issues and Fixes

**Issue:** Procedures are vague or unclear
**Fix:** Make steps more specific, add examples

**Issue:** Missing dependencies between skills
**Fix:** Document which skills require output from others

**Issue:** Agent capabilities don't match documentation
**Fix:** Ensure all capabilities are needed for documentation

---

## Skill 9: Documentation Quality Assessment

**Skill Name:** Documentation Quality Assessment
**Purpose:** Evaluate documentation completeness, accuracy, clarity, and consistency
**Required For:** Quality assurance before deployment
**Complexity:** Intermediate-Advanced
**Time Typical:** 1-2 hours

### Procedure

**Step 1: Assess Completeness**
1. Check section coverage:
   - Exactly 15 sections present?
   - All major topics covered?
   - No obvious gaps?
2. Check keypoint coverage:
   - 3-5 keypoints per section?
   - All keypoints have full descriptions?
   - All keypoints have code examples/procedures?
3. Verify all 4 formats present:
   - Markdown file exists?
   - Full JSON exists?
   - Summary JSON exists?
   - Schemas exist?

**Step 2: Assess Accuracy**
1. Code examples:
   - Can they be executed?
   - Do they produce expected results?
   - Are they tested?
2. Procedures:
   - Can they be followed?
   - Do they produce expected outcomes?
   - Are they tested?
3. Cross-references:
   - Do all references point to valid sections?
   - Are section numbers correct?
   - Do references match actual content?
4. Information:
   - Is it current with implementation?
   - No outdated information?
   - Matches actual behavior?

**Step 3: Assess Clarity**
1. Language:
   - Clear and accessible?
   - Active voice used?
   - Minimal jargon?
   - Technical terms explained?
2. Summaries:
   - One sentence each?
   - Capture essence?
   - Understandable?
3. Descriptions:
   - Explain the "why"?
   - Include "how" details?
   - Examples included?
   - Easy to follow?

**Step 4: Assess Consistency**
1. Style:
   - Consistent formatting throughout?
   - Same terminology used consistently?
   - Same structure in all sections/keypoints?
2. Terminology:
   - Same terms for same concepts?
   - No conflicting definitions?
   - Abbreviations consistent?
3. Structure:
   - All sections follow same pattern?
   - All keypoints follow same format?
   - Consistent depth of detail?

**Step 5: Assess Currency**
1. Implementation:
   - Matches current code?
   - No outdated references?
   - Features current?
2. Examples:
   - Run on current system?
   - Use current APIs?
   - Reflect current best practices?
3. Maintenance:
   - Updated recently?
   - Version number current?
   - Last update date known?

**Step 6: Create Quality Report**
1. Document findings for each area:
   - Completeness: ✓ or issues list
   - Accuracy: ✓ or errors list
   - Clarity: ✓ or improvements needed
   - Consistency: ✓ or inconsistencies
   - Currency: ✓ or updates needed
2. Rate overall quality: Good/Acceptable/Needs Work
3. List recommendations for improvement
4. Create action items if needed

### Inputs
- Completed documentation (all files)
- Knowledge of actual implementation
- Quality standards
- Component expertise

### Outputs
- Quality assessment report
- Ratings for each dimension
- List of issues found
- Recommendations for improvement
- Action items (if any)

### Validation Checklist
- [ ] 15 sections present
- [ ] 3-5 keypoints per section
- [ ] All sections have introductions
- [ ] All keypoints have descriptions
- [ ] Code examples are executable
- [ ] Procedures are testable
- [ ] Cross-references are valid
- [ ] Information is current
- [ ] Language is clear
- [ ] Summaries are one sentence
- [ ] Style is consistent
- [ ] Terminology is consistent
- [ ] All 4 formats present
- [ ] Formats are synchronized

### Common Issues and Fixes

**Issue:** Code examples don't execute
**Fix:** Test and fix code, or replace with correct version

**Issue:** Information is outdated
**Fix:** Update to match current implementation

**Issue:** Summaries are too long
**Fix:** Condense to single, essential sentence

**Issue:** Inconsistent terminology
**Fix:** Standardize on single term, update all instances

---

## Skill 10: Dashboard Integration Testing

**Skill Name:** Dashboard Integration Testing
**Purpose:** Verify documentation displays correctly in dashboard and API
**Required For:** User acceptance, deployment verification
**Complexity:** Basic-Intermediate
**Time Typical:** 30-45 minutes

### Procedure

**Step 1: Get Port Configuration**
1. Read config.json to get ports:
   ```bash
   python3 -c "import json; cfg=json.load(open('config.json')); \
     root=cfg['run_details']['root_port']; \
     api_offset=cfg['run_details']['port_offsets']['api']; \
     print(f'Dashboard: {root}, API: {root + api_offset}')"
   ```
2. Note the root_port and API port offset
3. Calculate actual ports:
   - Dashboard port = root_port + port_offsets.dashboard
   - API port = root_port + port_offsets.api

**Step 2: Verify File Placement**
1. Check documentation folder exists:
   - `documentation/component_name/`
2. Verify all required files present:
   - `component_name_keypoints.md`
   - `component_name_keypoints_full.json`
   - `component_name_keypoints_summary.json`
   - `agent.md`
   - `skills.md`
   - `schemas/` folder with schema files
3. Verify file permissions allow reading

**Step 3: Test API Endpoints**
1. Get API port from config.json (see Step 1)
2. Open terminal and test:
   ```bash
   curl http://localhost:$API_PORT/api/documents | jq .
   ```
3. Verify response includes:
   - Your component's document listed
   - All 4 formats (full_markdown, summary_markdown, full_json, summary_json)
   - File names and sizes

**Step 4: Test Document Retrieval**
1. Test each format using API_PORT from config:
   ```bash
   curl "http://localhost:$API_PORT/api/document?folder=component_name\
     &document=component_name_keypoints&format=summary_json" | jq .
   ```
2. For each format:
   - summary_markdown: Should return markdown text
   - full_markdown: Should return markdown with full descriptions
   - summary_json: Should return JSON without descriptions
   - full_json: Should return complete JSON with descriptions

**Step 5: Test Dashboard Display**
1. Get dashboard port from config.json (root_port + dashboard offset)
2. Open dashboard: `http://localhost:$DASHBOARD_PORT/ui/`
3. Scroll to "Project Documentation" section
4. Verify format selector shows your document
5. Select each format:
   - Content displays correctly?
   - Markdown renders as text?
   - JSON expands/collapses?
6. Test view toggles:
   - Compact mode limits height?
   - Expanded shows full content?

**Step 5: Test Download Functionality**
1. In dashboard, click Download button
2. For each format:
   - File downloads?
   - Correct filename?
   - Correct file type?
   - Content complete?

**Step 6: Test Content Accuracy**
1. Compare dashboard display with source:
   - All sections present?
   - All keypoints present?
   - Content matches source?
   - Formatting correct?
2. Verify JSON rendering:
   - Sections expandable?
   - Keypoints visible?
   - Data displayed correctly?

### Inputs
- Completed documentation files
- Running server (ports 9000, 9001)
- Browser for dashboard testing
- curl or API client

### Outputs
- Test results report
- Status: PASS or FAIL
- Screenshots (optional)
- Issues found (if any)

### Validation Checklist
- [ ] Files in correct location
- [ ] All files present
- [ ] /api/documents endpoint works
- [ ] /api/document endpoint works
- [ ] All 4 formats retrievable
- [ ] Dashboard displays documentation
- [ ] Format selector works
- [ ] View toggle works
- [ ] Download function works
- [ ] Content matches source
- [ ] JSON expands/collapses
- [ ] No console errors

### Common Issues and Fixes

**Issue:** Documentation not appearing in /api/documents
**Fix:** Check file location, ensure folder name matches configuration

**Issue:** API returns 404 error
**Fix:** Verify folder name and document name in query parameters

**Issue:** Dashboard doesn't load content
**Fix:** Check browser console for errors, verify API endpoints working

**Issue:** Downloaded file has wrong content
**Fix:** Verify API is returning correct format

---

## Skill Execution Order

When creating new documentation, execute skills in this order:

1. **Skill 1**: Markdown Document Creation (source)
2. **Skill 2**: Markdown Parsing and Structure Extraction
3. **Skill 3**: JSON Document Generation (both formats)
4. **Skill 4**: JSON Schema Creation
5. **Skill 5**: JSON Schema Validation
6. **Skill 7**: File Organization and Naming (set up folder)
7. **Skill 8**: Agent and Skills Documentation Creation
8. **Skill 6**: Format Synchronization Verification
9. **Skill 9**: Documentation Quality Assessment
10. **Skill 10**: Dashboard Integration Testing

This order ensures each skill has the dependencies it needs from previous skills.

## Skill Dependencies Summary

```
Skill 1: Markdown Creation
  ↓
Skill 2: Markdown Parsing (uses markdown from Skill 1)
  ↓
Skill 3: JSON Generation (uses parsed data from Skill 2)
  ↓
Skill 4: Schema Creation (validates structure from Skill 3)
  ↓
Skill 5: Schema Validation (validates JSON using Skill 4)
  ↓
Skill 7: File Organization (organizes all files)
  ↓
Skill 8: Agent/Skills Documentation
  ↓
Skill 6: Format Synchronization (verifies all formats match)
  ↓
Skill 9: Quality Assessment (comprehensive evaluation)
  ↓
Skill 10: Dashboard Integration Testing (user verification)
```

## Total Time Investment

- Markdown Creation: 2-4 hours
- Markdown Parsing: 1 hour
- JSON Generation: 1 hour
- Schema Creation: 1-2 hours
- Schema Validation: 30 min
- File Organization: 30 min
- Agent/Skills Documentation: 2-3 hours
- Format Synchronization: 1 hour
- Quality Assessment: 1-2 hours
- Dashboard Testing: 1 hour

**Total: 12-18 hours for complete documentation system**
