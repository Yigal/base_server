# Security Audit Agent Skills

## Skill 1: Dependency Vulnerability Scan

**Purpose:** Check dependencies for known CVEs
**Tools:** safety, snyk, pip-audit
**Complexity:** Intermediate

### Procedure

1. Extract all dependencies from requirements.txt
2. Check against National Vulnerability Database (NVD)
3. Use safety or snyk to identify vulnerabilities
4. Report vulnerable packages with severity levels
5. Suggest package upgrades or alternatives

### Validation Checklist

- ✓ All dependencies listed
- ✓ NVD checked
- ✓ Vulnerabilities identified
- ✓ Severity levels assigned
- ✓ Upgrade paths suggested

## Skill 2: Code Vulnerability Detection

**Purpose:** Scan for common code vulnerabilities
**Tools:** bandit, semgrep
**Complexity:** Advanced

### Procedure

1. Scan all Python files with bandit
2. Check for hardcoded values
3. Identify dangerous function usage
4. Detect vulnerable patterns
5. Report findings with line numbers

### Validation Checklist

- ✓ bandit scan complete
- ✓ All patterns checked
- ✓ Dangerous functions reported
- ✓ Line numbers provided
- ✓ Severity assessed

## Skill 3: Secret Detection

**Purpose:** Find hardcoded secrets and credentials
**Tools:** detect-secrets, git-secrets, truffleHog
**Complexity:** Advanced

### Procedure

1. Scan codebase for API keys
2. Check for database credentials
3. Identify password patterns
4. Scan environment configurations
5. Report all discovered secrets

### Validation Checklist

- ✓ Secret patterns detected
- ✓ All file types scanned
- ✓ False positives verified
- ✓ Secrets reported
- ✓ Remediation steps provided

## Skill 4: API Security Validation

**Purpose:** Validate API endpoints for security issues
**Tools:** Custom validation scripts
**Complexity:** Advanced

### Procedure

1. Check endpoint authentication requirements
2. Verify input validation
3. Check rate limiting implementation
4. Validate error handling
5. Report security gaps

### Validation Checklist

- ✓ Authentication verified
- ✓ Input validation checked
- ✓ Rate limiting present
- ✓ Error messages safe
- ✓ Security headers present

## Skill 5: Configuration Security Check

**Purpose:** Review configuration files for security issues
**Tools:** Custom validation, config linters
**Complexity:** Intermediate

### Procedure

1. Validate config.json structure
2. Check environment variable usage
3. Verify debug mode disabled in production
4. Review CORS settings
5. Report security misconfigurations

### Validation Checklist

- ✓ Config reviewed
- ✓ Env vars validated
- ✓ Debug mode checked
- ✓ CORS settings verified
- ✓ Secure defaults applied

## Skill 6: Authentication Verification

**Purpose:** Validate authentication implementation
**Tools:** Custom validation scripts
**Complexity:** Advanced

### Procedure

1. Check authentication middleware
2. Verify token validation
3. Review session management
4. Check password handling
5. Report authentication issues

### Validation Checklist

- ✓ Auth middleware present
- ✓ Token validation working
- ✓ Session secure
- ✓ Passwords hashed
- ✓ Auth flows tested

## Skill 7: CORS Configuration Validation

**Purpose:** Ensure CORS is properly configured
**Tools:** Custom validation
**Complexity:** Intermediate

### Procedure

1. Verify allowed origins are specific
2. Check allowed HTTP methods
3. Validate allowed headers
4. Verify credentials handling
5. Report CORS misconfigurations

### Validation Checklist

- ✓ Origins whitelist reviewed
- ✓ Methods restricted
- ✓ Headers validated
- ✓ Credentials properly configured
- ✓ Security implications assessed
