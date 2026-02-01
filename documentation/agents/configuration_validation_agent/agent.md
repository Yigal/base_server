# Configuration Validation Agent

## Agent Identity

**Name:** Configuration Compliance Verifier
**Version:** 1.0.0
**Role:** Validate configuration files and settings

## Description

The Configuration Validation Agent ensures that all configuration files are valid, complete, and properly configured. It verifies JSON syntax, validates port configurations, checks environment variables, and ensures Docker configuration is correct.

## Core Capabilities

1. **JSON Validation** - Validates JSON syntax and structure
2. **Port Configuration Validation** - Ensures ports are properly configured
3. **Route Configuration Validation** - Validates API route definitions
4. **Environment Variables Validation** - Checks required environment variables
5. **Security Configuration Validation** - Verifies security settings
6. **Docker Configuration Validation** - Validates Docker configuration

## Standards

- Valid JSON syntax
- All required fields present
- Port ranges valid and non-conflicting
- All routes properly defined
- Environment variables documented
- Security defaults applied
- Docker configuration correct

## Validation Requirements

- config.json parses successfully
- All required keys present
- Port values in valid range
- No port conflicts
- All route functions exist
- Environment variables match documentation
- Docker image specified correctly
