# Dependency Management Agent Skills

## Skill 1: Dependency Scanning

**Purpose:** List and verify all project dependencies
**Tools:** pip, poetry, requirements.txt
**Complexity:** Basic

### Procedure

1. Read requirements.txt or poetry.lock
2. Extract all dependencies
3. Check installed versions
4. Verify integrity
5. Report dependency tree

### Validation Checklist

- ✓ All dependencies listed
- ✓ Versions recorded
- ✓ Installed correctly
- ✓ No conflicts
- ✓ Dependencies documented

## Skill 2: Update Checking

**Purpose:** Find available updates for packages
**Tools:** pip, poetry, online package index
**Complexity:** Intermediate

### Procedure

1. Check for available updates
2. Compare versions
3. Identify outdated packages
4. Check release dates
5. Report available updates

### Validation Checklist

- ✓ Updates checked
- ✓ New versions identified
- ✓ Release notes available
- ✓ Changelog reviewed
- ✓ Update timeline noted

## Skill 3: Security Scanning

**Purpose:** Check dependencies for vulnerabilities
**Tools:** safety, pip-audit, snyk
**Complexity:** Intermediate

### Procedure

1. Check against CVE database
2. Scan for vulnerabilities
3. Identify severity levels
4. Check for security patches
5. Report security issues

### Validation Checklist

- ✓ CVEs checked
- ✓ Vulnerabilities identified
- ✓ Severity assigned
- ✓ Patches available
- ✓ Issues reported

## Skill 4: Compatibility Testing

**Purpose:** Test dependency updates for compatibility
**Tools:** pytest, test suite
**Complexity:** Advanced

### Procedure

1. Plan dependency updates
2. Update in test environment
3. Run full test suite
4. Check for breaking changes
5. Report compatibility issues

### Validation Checklist

- ✓ Tests run successfully
- ✓ No breaking changes
- ✓ API compatibility verified
- ✓ Data integrity checked
- ✓ Performance acceptable

## Skill 5: License Verification

**Purpose:** Check package licenses for compliance
**Tools:** pip-licenses, SPDX
**Complexity:** Intermediate

### Procedure

1. Extract licenses from packages
2. Check against company policy
3. Verify compatibility
4. Track license changes
5. Report license issues

### Validation Checklist

- ✓ All licenses identified
- ✓ Compliance checked
- ✓ No conflicts
- ✓ Compatible licenses
- ✓ Issues reported
