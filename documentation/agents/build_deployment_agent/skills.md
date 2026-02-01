# Build & Deployment Agent Skills

## Skill 1: Docker Build

**Purpose:** Build Docker image for deployment
**Tools:** Docker CLI
**Complexity:** Intermediate

### Procedure

1. Validate Dockerfile exists
2. Build Docker image with tags
3. Verify build succeeds
4. Check image size
5. Report build results

### Validation Checklist

- ✓ Dockerfile valid
- ✓ Build successful
- ✓ Image tagged correctly
- ✓ Image size reasonable
- ✓ Layers optimized

## Skill 2: Container Execution

**Purpose:** Start and run Docker container
**Tools:** Docker CLI
**Complexity:** Intermediate

### Procedure

1. Pull/prepare Docker image
2. Start container with config
3. Verify container started
4. Check running status
5. Monitor startup logs

### Validation Checklist

- ✓ Container starts
- ✓ No startup errors
- ✓ Ports exposed
- ✓ Environment vars set
- ✓ Health checks enabled

## Skill 3: Deployment Validation

**Purpose:** Verify deployment success
**Tools:** Deployment checks
**Complexity:** Intermediate

### Procedure

1. Verify all services running
2. Check configuration loaded
3. Validate data persistence
4. Test core functionality
5. Verify external services

### Validation Checklist

- ✓ Services running
- ✓ Configuration correct
- ✓ Data accessible
- ✓ APIs responding
- ✓ Database connected

## Skill 4: Health Check Verification

**Purpose:** Run comprehensive health checks
**Tools:** Health endpoints
**Complexity:** Intermediate

### Procedure

1. Call health check endpoints
2. Verify all components healthy
3. Check database connectivity
4. Monitor resource usage
5. Report health status

### Validation Checklist

- ✓ Health endpoints respond
- ✓ Status is healthy
- ✓ Database connected
- ✓ Memory usage normal
- ✓ No error conditions

## Skill 5: Version Management

**Purpose:** Track and manage versions
**Tools:** Git, version file
**Complexity:** Basic

### Procedure

1. Extract version from code
2. Tag release in git
3. Update version file
4. Create release notes
5. Document changes

### Validation Checklist

- ✓ Version number updated
- ✓ Git tag created
- ✓ Release notes written
- ✓ Changelog updated
- ✓ Version accessible
