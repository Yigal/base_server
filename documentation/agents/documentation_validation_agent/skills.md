# Documentation Validation Agent Skills

## Skill 1: Documentation Structure Validation

**Purpose:** Validate documentation folder and file organization
**Tools:** os, pathlib
**Complexity:** Basic

### Procedure

1. Check folder structure exists
2. Verify file organization
3. Validate naming conventions
4. Check for required files
5. Report structure issues

### Validation Checklist

- ✓ Folder structure correct
- ✓ File naming consistent
- ✓ Required files present
- ✓ No orphaned files
- ✓ Organization logical

## Skill 2: Content Completeness Check

**Purpose:** Ensure all required content sections are present
**Tools:** Content parser, regex
**Complexity:** Intermediate

### Procedure

1. Check for all required sections
2. Verify keypoint descriptions
3. Check code example presence
4. Validate example completeness
5. Report missing content

### Validation Checklist

- ✓ All sections present
- ✓ Keypoints documented
- ✓ Examples provided
- ✓ Descriptions complete
- ✓ No placeholder text

## Skill 3: Format Synchronization Verification

**Purpose:** Ensure content is synchronized across formats
**Tools:** Markdown/JSON parsers
**Complexity:** Advanced

### Procedure

1. Compare markdown and JSON formats
2. Verify content matches
3. Check metadata synchronization
4. Validate cross-references
5. Report discrepancies

### Validation Checklist

- ✓ Formats compared
- ✓ Content matches
- ✓ Metadata synchronized
- ✓ No conflicting data
- ✓ All formats current

## Skill 4: Link Validation

**Purpose:** Check all cross-references and external links
**Tools:** requests, link checker
**Complexity:** Intermediate

### Procedure

1. Extract all links from documentation
2. Check internal cross-references
3. Validate external links
4. Verify anchor references
5. Report broken links

### Validation Checklist

- ✓ All links found
- ✓ Internal links valid
- ✓ External links accessible
- ✓ Anchors exist
- ✓ No dead links

## Skill 5: Code Example Testing

**Purpose:** Execute and validate code examples
**Tools:** pytest, subprocess
**Complexity:** Advanced

### Procedure

1. Extract code examples
2. Create test files
3. Execute examples
4. Verify output
5. Report broken examples

### Validation Checklist

- ✓ Examples extracted
- ✓ Syntax valid
- ✓ Examples execute
- ✓ Output correct
- ✓ No errors

## Skill 6: Markdown Syntax Validation

**Purpose:** Validate markdown formatting
**Tools:** markdown parser, linters
**Complexity:** Intermediate

### Procedure

1. Check markdown syntax
2. Validate header hierarchy
3. Verify list formatting
4. Check code block syntax
5. Report formatting issues

### Validation Checklist

- ✓ Syntax valid
- ✓ Headers properly nested
- ✓ Lists consistent
- ✓ Code blocks valid
- ✓ No formatting errors

## Skill 7: JSON Schema Validation

**Purpose:** Validate JSON against schemas
**Tools:** jsonschema
**Complexity:** Advanced

### Procedure

1. Load JSON schema
2. Load JSON documents
3. Validate against schema
4. Check required fields
5. Report validation errors

### Validation Checklist

- ✓ Schema loaded
- ✓ JSON loads successfully
- ✓ All required fields present
- ✓ Data types correct
- ✓ Schema valid
