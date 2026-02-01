# Configuration Validation Agent Skills

## Skill 1: JSON Syntax Validation

**Purpose:** Validate JSON configuration files
**Tools:** json module, jsonschema
**Complexity:** Basic

### Procedure

1. Load config.json file
2. Parse with JSON parser
3. Validate JSON structure
4. Check for required fields
5. Report any syntax errors

### Validation Checklist

- ✓ File readable
- ✓ JSON parses successfully
- ✓ Structure valid
- ✓ Required fields present
- ✓ No duplicate keys

## Skill 2: Port Configuration Validation

**Purpose:** Verify port configuration is correct
**Tools:** Configuration parser
**Complexity:** Intermediate

### Procedure

1. Extract root_port from config
2. Verify port_offsets defined
3. Calculate all derived ports
4. Check port ranges (1024-65535)
5. Verify no port conflicts

### Validation Checklist

- ✓ root_port defined
- ✓ port_offsets present
- ✓ Port values valid
- ✓ No negative values
- ✓ Port ranges appropriate

## Skill 3: Route Configuration Validation

**Purpose:** Validate API route definitions
**Tools:** Configuration validation
**Complexity:** Intermediate

### Procedure

1. Read all route definitions
2. Verify required fields present
3. Validate HTTP methods
4. Check function references exist
5. Report missing or invalid routes

### Validation Checklist

- ✓ All routes present
- ✓ Methods valid (GET, POST, etc.)
- ✓ Function files exist
- ✓ Function names correct
- ✓ Path syntax valid

## Skill 4: Environment Variables Validation

**Purpose:** Verify required environment variables
**Tools:** os, dotenv
**Complexity:** Intermediate

### Procedure

1. List required environment variables
2. Check .env file for variables
3. Verify values are set
4. Validate variable format
5. Report missing variables

### Validation Checklist

- ✓ .env file exists
- ✓ All required vars present
- ✓ Values properly formatted
- ✓ No empty values
- ✓ Secrets not logged

## Skill 5: Security Settings Validation

**Purpose:** Verify security configuration
**Tools:** Configuration validation
**Complexity:** Intermediate

### Procedure

1. Check CORS configuration
2. Verify authentication settings
3. Validate security headers
4. Check API key configuration
5. Report security gaps

### Validation Checklist

- ✓ CORS configured
- ✓ Auth enabled
- ✓ Headers present
- ✓ Keys configured
- ✓ Debug mode disabled

## Skill 6: Docker Configuration Validation

**Purpose:** Validate Docker configuration
**Tools:** Dockerfile parser, docker-compose validator
**Complexity:** Advanced

### Procedure

1. Validate Dockerfile syntax
2. Check docker-compose format
3. Verify image names
4. Check port mappings
5. Validate volume configurations

### Validation Checklist

- ✓ Dockerfile valid
- ✓ docker-compose.yml valid
- ✓ Images available
- ✓ Ports mapped correctly
- ✓ Volumes configured
