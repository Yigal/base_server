# API Endpoint Validation Agent Skills

## Skill 1: Endpoint Availability Test

**Purpose:** Test all API endpoints for accessibility
**Tools:** requests, curl
**Complexity:** Intermediate

### Procedure

1. Discover all API endpoints from config
2. Send request to each endpoint
3. Check HTTP status codes
4. Measure response time
5. Report unavailable endpoints

### Validation Checklist

- ✓ All endpoints discovered
- ✓ Requests sent
- ✓ Status codes checked
- ✓ Response times measured
- ✓ Availability reported

## Skill 2: Response Validation

**Purpose:** Validate API response format and content
**Tools:** requests, jsonschema
**Complexity:** Intermediate

### Procedure

1. Send test requests to each endpoint
2. Check response content type
3. Validate response structure
4. Verify data types
5. Check for required fields

### Validation Checklist

- ✓ Content-Type correct
- ✓ Response structure valid
- ✓ JSON valid
- ✓ Data types correct
- ✓ No malformed responses

## Skill 3: Parameter Validation

**Purpose:** Test required and optional parameters
**Tools:** requests
**Complexity:** Intermediate

### Procedure

1. Test required parameters present
2. Test with missing parameters
3. Test invalid parameter values
4. Test optional parameters
5. Report parameter issues

### Validation Checklist

- ✓ Required parameters enforced
- ✓ Missing param errors correct
- ✓ Invalid values handled
- ✓ Optional params work
- ✓ Parameter types validated

## Skill 4: Error Handling Test

**Purpose:** Validate error responses
**Tools:** requests
**Complexity:** Intermediate

### Procedure

1. Send invalid requests
2. Check error response codes
3. Verify error messages
4. Check error details
5. Report error handling issues

### Validation Checklist

- ✓ Error codes correct (4xx, 5xx)
- ✓ Error messages present
- ✓ Messages are descriptive
- ✓ No sensitive data in errors
- ✓ Error format consistent

## Skill 5: Performance Testing

**Purpose:** Measure endpoint response times
**Tools:** requests, timing
**Complexity:** Intermediate

### Procedure

1. Send requests to each endpoint
2. Measure response latency
3. Calculate average times
4. Identify slow endpoints
5. Compare against SLAs

### Validation Checklist

- ✓ Latency measured
- ✓ Baselines established
- ✓ Slow endpoints identified
- ✓ SLAs defined
- ✓ Performance acceptable

## Skill 6: Security Testing

**Purpose:** Test endpoint security
**Tools:** requests
**Complexity:** Advanced

### Procedure

1. Test without authentication
2. Verify auth required
3. Test with invalid credentials
4. Check authorization
5. Verify secure data handling

### Validation Checklist

- ✓ Auth required for protected endpoints
- ✓ Invalid auth rejected
- ✓ Authorization working
- ✓ Sensitive data not logged
- ✓ HTTPS enforced

## Skill 7: Documentation Accuracy Check

**Purpose:** Verify API documentation matches implementation
**Tools:** requests, documentation parser
**Complexity:** Advanced

### Procedure

1. Extract endpoints from documentation
2. Compare with actual endpoints
3. Verify parameter documentation
4. Check response examples
5. Report documentation issues

### Validation Checklist

- ✓ All endpoints documented
- ✓ Parameters match docs
- ✓ Response formats accurate
- ✓ Examples match behavior
- ✓ Docs up to date
