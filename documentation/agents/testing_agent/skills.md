# Testing Agent Skills

## Skill 1: Unit Test Execution

**Purpose:** Run all unit tests in the project
**Tools:** pytest
**Complexity:** Intermediate

### Procedure

1. Discover all test files matching test_*.py pattern
2. Execute pytest with verbose output
3. Collect test results and metrics
4. Report pass/fail status for each test
5. Track execution time per test

### Validation Checklist

- ✓ All tests discovered
- ✓ pytest configured
- ✓ Tests executed successfully
- ✓ Results reported
- ✓ Metrics collected

## Skill 2: Integration Test Execution

**Purpose:** Run integration tests for component interactions
**Tools:** pytest with integration markers
**Complexity:** Advanced

### Procedure

1. Identify integration test suite
2. Set up test environment
3. Execute integration tests
4. Verify component interactions
5. Report integration issues

### Validation Checklist

- ✓ Test environment ready
- ✓ All integration tests run
- ✓ Component interactions verified
- ✓ Data flow correct
- ✓ Issues reported

## Skill 3: API Test Execution

**Purpose:** Test all API endpoints functionality
**Tools:** pytest, requests
**Complexity:** Advanced

### Procedure

1. Extract all API endpoints from config
2. Create test cases for each endpoint
3. Test with various parameters
4. Verify response codes and formats
5. Check error handling

### Validation Checklist

- ✓ All endpoints tested
- ✓ Response codes validated
- ✓ Response formats correct
- ✓ Error handling verified
- ✓ Performance acceptable

## Skill 4: Coverage Measurement

**Purpose:** Measure code coverage and identify untested code
**Tools:** pytest-cov, coverage.py
**Complexity:** Intermediate

### Procedure

1. Run tests with coverage measurement
2. Generate coverage report
3. Identify uncovered lines
4. Calculate coverage percentage by file
5. Report coverage metrics

### Validation Checklist

- ✓ Coverage measured
- ✓ Report generated
- ✓ Percentages calculated
- ✓ Untested code identified
- ✓ Thresholds verified

## Skill 5: Test Report Generation

**Purpose:** Create comprehensive test reports
**Tools:** pytest, custom reporting
**Complexity:** Intermediate

### Procedure

1. Collect all test results
2. Generate test summary
3. Create coverage report
4. List failed tests with details
5. Provide improvement recommendations

### Validation Checklist

- ✓ Summary created
- ✓ All results included
- ✓ Coverage reported
- ✓ Failures documented
- ✓ Recommendations provided

## Skill 6: Performance Test Analysis

**Purpose:** Monitor test execution performance
**Tools:** pytest-benchmark, timing plugins
**Complexity:** Intermediate

### Procedure

1. Measure individual test execution time
2. Compare against baseline metrics
3. Identify slow tests
4. Report performance trends
5. Suggest optimization targets

### Validation Checklist

- ✓ Timing collected
- ✓ Baselines compared
- ✓ Slow tests identified
- ✓ Trends analyzed
- ✓ Issues reported

## Skill 7: Failure Diagnosis

**Purpose:** Analyze and report test failures
**Tools:** pytest, logging
**Complexity:** Advanced

### Procedure

1. Capture failure stack traces
2. Extract error messages
3. Analyze failure patterns
4. Categorize failure types
5. Suggest potential fixes

### Validation Checklist

- ✓ Failures captured
- ✓ Stack traces included
- ✓ Patterns identified
- ✓ Root causes analyzed
- ✓ Fixes suggested
