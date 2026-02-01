# Code Quality Agent Skills

## Skill 1: Python Linting Validation

**Purpose:** Validate Python code against PEP 8 style guidelines
**Tools:** flake8
**Complexity:** Intermediate

### Procedure

1. Run flake8 on all Python files in the project
2. Collect violations and errors
3. Report results with line numbers and error codes
4. Calculate violation density (violations per 1000 lines)
5. Compare against baseline metrics

### Validation Checklist

- ✓ flake8 installed
- ✓ .flake8 configuration present
- ✓ All files scanned
- ✓ Violations reported
- ✓ Metrics calculated

## Skill 2: Code Formatting Check

**Purpose:** Verify code is properly formatted
**Tools:** black, isort
**Complexity:** Intermediate

### Procedure

1. Check code formatting with black
2. Verify import organization with isort
3. Report formatting issues
4. Suggest fixes

### Validation Checklist

- ✓ black check run
- ✓ isort check run
- ✓ Issues reported
- ✓ Suggestions provided

## Skill 3: Complexity Analysis

**Purpose:** Measure code complexity and identify problematic areas
**Tools:** radon
**Complexity:** Intermediate

### Procedure

1. Measure cyclomatic complexity for all functions
2. Calculate maintainability index
3. Identify overly complex functions
4. Report metrics and recommendations

### Validation Checklist

- ✓ radon metrics calculated
- ✓ Complex functions identified
- ✓ Recommendations provided

## Skill 4: Dead Code Detection

**Purpose:** Find unused variables, functions, and imports
**Tools:** vulture, manual analysis
**Complexity:** Advanced

### Procedure

1. Identify unused variables
2. Find unreachable code
3. Detect unused functions
4. Report code smell patterns

### Validation Checklist

- ✓ Unused code detected
- ✓ False positives verified
- ✓ Report generated

## Skill 5: Import Organization

**Purpose:** Ensure imports are properly organized and sorted
**Tools:** isort
**Complexity:** Basic

### Procedure

1. Check import grouping (stdlib, third-party, local)
2. Verify alphabetical sorting
3. Report import issues
4. Suggest organization changes

### Validation Checklist

- ✓ Import groups correct
- ✓ Sorting verified
- ✓ Issues reported

## Skill 6: Docstring Validation

**Purpose:** Ensure all public functions have proper documentation
**Tools:** pydocstyle
**Complexity:** Intermediate

### Procedure

1. Check for docstring presence
2. Validate docstring format
3. Verify parameter documentation
4. Check return value documentation

### Validation Checklist

- ✓ All public functions documented
- ✓ Format validated
- ✓ Parameters documented
- ✓ Return values documented

## Skill 7: Type Hint Validation

**Purpose:** Verify type hints are present and correct
**Tools:** mypy
**Complexity:** Advanced

### Procedure

1. Run mypy type checker
2. Identify missing type hints
3. Report type errors
4. Verify against actual usage

### Validation Checklist

- ✓ mypy run successfully
- ✓ Type hints present
- ✓ No type errors
- ✓ Coverage complete
