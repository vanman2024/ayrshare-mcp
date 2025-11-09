# Production Configuration Guide

Complete guide to production features, logging, monitoring, and error handling for the Ayrshare MCP Server.

## Overview

The Ayrshare MCP server includes production-ready features:
- Structured JSON logging
- Rate limiting
- Error handling middleware
- Health check endpoint
- Environment-based configuration

## Production Modules

### 1. Production Configuration (`production_config.py`)

Central configuration module providing:
- **Structured logging** (JSON or text format)
- **Rate limiting** (per-minute and per-hour)
- **Error handling decorators**
- **Health check utilities**

### 2. Health Check Module (`health_check.py`)

Provides server health monitoring:
- Server status and version
- System information
- Rate limit statistics
- Configuration details

## Environment Variables

### Logging Configuration

```bash
# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Log format: json (production) or text (development)
LOG_FORMAT=json
```

**JSON Format** (Production):
```json
{
  "timestamp": "2025-11-09T12:00:00Z",
  "level": "INFO",
  "logger": "ayrshare-mcp",
  "message": "Tool completed: post_to_social",
  "module": "server",
  "function": "post_to_social",
  "line": 95,
  "tool": "post_to_social",
  "duration_seconds": 0.456,
  "success": true
}
```

**Text Format** (Development):
```
2025-11-09 12:00:00 - ayrshare-mcp - INFO - Tool completed: post_to_social
```

### Rate Limiting

```bash
# Maximum requests per minute (0 to disable)
RATE_LIMIT_PER_MINUTE=60

# Maximum requests per hour (0 to disable)
RATE_LIMIT_PER_HOUR=1000
```

**Recommended Limits by Plan**:

| Plan | Per Minute | Per Hour |
|------|------------|----------|
| Free | 10 | 100 |
| Business | 60 | 1000 |
| Enterprise | 120 | 5000 |

### Server Configuration

```bash
# Transport mode: stdio or http
TRANSPORT=stdio

# HTTP server host (when TRANSPORT=http)
HOST=0.0.0.0

# HTTP server port (when TRANSPORT=http)
PORT=8000
```

### Ayrshare Configuration

```bash
# API timeout in seconds
AYRSHARE_TIMEOUT=30

# Enable debug mode (verbose logging)
AYRSHARE_DEBUG=false

# API base URL (normally not needed)
AYRSHARE_BASE_URL=https://app.ayrshare.com/api
```

## Using Production Features

### 1. Enable Structured Logging

Set in environment or `.env` file:
```bash
LOG_FORMAT=json
LOG_LEVEL=INFO
```

The server will automatically use JSON logging with:
- ISO 8601 timestamps
- Structured fields
- Exception stack traces
- Performance metrics

### 2. Enable Rate Limiting

Set limits in environment:
```bash
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

Rate limiting is **automatic** for all tools. When exceeded:
```json
{
  "status": "error",
  "error": "Rate limit exceeded: 60 requests per minute",
  "error_type": "rate_limit"
}
```

### 3. Add Health Check Tool (Optional)

To add the health check tool to your server, add this to `server.py`:

```python
from health_check import health_check

@mcp.tool()
async def server_health() -> Dict[str, Any]:
    """
    Check server health status and configuration

    Returns comprehensive health information including server status,
    system details, rate limits, and configuration.
    """
    return await health_check()
```

Then restart the server. The health check will be available as a regular MCP tool.

### 4. Add Error Handling to Tools (Optional)

Wrap existing tools with error handling:

```python
from production_config import with_error_handling

@mcp.tool()
@with_error_handling
async def post_to_social(
    post_text: str,
    platforms: List[str],
    media_urls: Optional[List[str]] = None,
    shorten_links: bool = True,
) -> Dict[str, Any]:
    # Your existing code here
    pass
```

This adds:
- Automatic error logging
- Performance timing
- Rate limit checking
- Structured error responses

## Monitoring

### Health Check Endpoint

When deployed to FastMCP Cloud or running in HTTP mode, access health check at:

```bash
curl https://your-deployment.fastmcp.app/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-09T12:00:00Z",
  "server": {
    "name": "Ayrshare Social Media API",
    "version": "1.0.0",
    "transport": "stdio",
    "log_level": "INFO"
  },
  "system": {
    "python_version": "3.10.12",
    "platform": "Linux-5.15.0"
  },
  "rate_limits": {
    "per_minute": 60,
    "per_hour": 1000,
    "current_minute": 15,
    "current_hour": 234
  },
  "configuration": {
    "ayrshare_timeout": 30,
    "debug_mode": false
  }
}
```

### Log Analysis

#### View Recent Logs
```bash
# In FastMCP Cloud dashboard: Logs tab

# With jq (if accessing via API):
curl https://your-deployment.fastmcp.app/logs | jq '.[] | select(.level == "ERROR")'
```

#### Track Performance
```bash
# Filter for slow operations (>1 second):
cat logs.json | jq 'select(.duration_seconds > 1)'

# Average duration by tool:
cat logs.json | jq -s 'group_by(.tool) | map({tool: .[0].tool, avg_duration: (map(.duration_seconds) | add / length)})'
```

#### Monitor Rate Limits
```bash
# Check current rate limit usage:
curl https://your-deployment.fastmcp.app/health | jq '.rate_limits'
```

### Error Tracking

#### Common Error Patterns

**Rate Limit Exceeded**:
```json
{
  "status": "error",
  "error": "Rate limit exceeded: 60 requests per minute",
  "error_type": "rate_limit"
}
```

**API Key Missing**:
```json
{
  "status": "error",
  "error": "AYRSHARE_API_KEY not configured",
  "error_type": "configuration_error"
}
```

**API Request Failed**:
```json
{
  "status": "error",
  "error": "Ayrshare API error: Insufficient balance",
  "error_type": "AyrshareError"
}
```

## Performance Optimization

### 1. Adjust Timeout for Large Media

For video uploads or large images:
```bash
AYRSHARE_TIMEOUT=60  # Increase from default 30
```

### 2. Enable Debug Logging Temporarily

For troubleshooting:
```bash
LOG_LEVEL=DEBUG
AYRSHARE_DEBUG=true
```

**Warning**: Debug mode generates verbose logs. Use only for troubleshooting.

### 3. Optimize Rate Limits

Match your rate limits to your Ayrshare plan:
```bash
# Check your plan limits at: https://app.ayrshare.com/settings

# Set slightly below API limits to avoid rejections
RATE_LIMIT_PER_MINUTE=55  # If API allows 60
RATE_LIMIT_PER_HOUR=950   # If API allows 1000
```

## Security Considerations

### 1. Protect API Keys

Never log API keys:
```python
# Good - logs don't show key
logger.info("API key configured: %s", "***")

# Bad - exposes key in logs
logger.info(f"API key: {api_key}")
```

### 2. Sanitize Error Messages

Error messages shouldn't expose sensitive data:
```python
# Good
return {"error": "Authentication failed"}

# Bad
return {"error": f"Invalid API key: {api_key}"}
```

### 3. Rate Limit Protection

Always enable rate limiting in production:
```bash
# Never disable in production
RATE_LIMIT_PER_MINUTE=60  # Not 0
RATE_LIMIT_PER_HOUR=1000  # Not 0
```

## Troubleshooting

### Logs Not Appearing

Check log level:
```bash
LOG_LEVEL=INFO  # Not ERROR or CRITICAL
```

Verify log format:
```bash
LOG_FORMAT=json  # or text
```

### Rate Limits Too Restrictive

Temporarily increase limits:
```bash
RATE_LIMIT_PER_MINUTE=120
RATE_LIMIT_PER_HOUR=2000
```

Or disable for testing:
```bash
RATE_LIMIT_PER_MINUTE=0
RATE_LIMIT_PER_HOUR=0
```

### Performance Issues

Enable debug logging:
```bash
LOG_LEVEL=DEBUG
```

Check duration_seconds in logs:
```bash
cat logs.json | jq '.duration_seconds'
```

Increase timeout:
```bash
AYRSHARE_TIMEOUT=60
```

## Best Practices

### Development Environment

```bash
# .env for development
LOG_LEVEL=DEBUG
LOG_FORMAT=text
RATE_LIMIT_PER_MINUTE=0
RATE_LIMIT_PER_HOUR=0
AYRSHARE_DEBUG=true
TRANSPORT=stdio
```

### Production Environment

```bash
# .env.production
LOG_LEVEL=INFO
LOG_FORMAT=json
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
AYRSHARE_DEBUG=false
TRANSPORT=stdio  # or http for FastMCP Cloud
```

### Staging Environment

```bash
# .env.staging
LOG_LEVEL=DEBUG
LOG_FORMAT=json
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=500
AYRSHARE_DEBUG=false
TRANSPORT=http
```

---

## Additional Resources

- **FastMCP Logging Docs**: https://gofastmcp.com/production/logging
- **FastMCP Monitoring**: https://gofastmcp.com/production/monitoring
- **Ayrshare API Limits**: https://docs.ayrshare.com/rate-limits

---

**Configuration Version**: 1.0
**Last Updated**: 2025-11-09
**Compatible With**: FastMCP 2.0+
