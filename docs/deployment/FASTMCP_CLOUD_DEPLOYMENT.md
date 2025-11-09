# FastMCP Cloud Deployment Guide - Ayrshare MCP Server

Complete guide for deploying the Ayrshare MCP server to FastMCP Cloud with production-ready configuration.

## Server Information

- **Server Name**: Ayrshare Social Media API
- **Server File**: `server.py` (root directory)
- **Server Instance**: `mcp` (line 21)
- **Entry Point**: `server.py:mcp`
- **Tools**: 75+
- **Resources**: 5
- **Prompts**: 5
- **Platforms Supported**: 13+ (Facebook, Instagram, Twitter/X, LinkedIn, TikTok, YouTube, Pinterest, Reddit, Snapchat, Telegram, Threads, Bluesky, GMB)

## Prerequisites

- GitHub account for repository hosting
- Ayrshare API account and API key from https://app.ayrshare.com/api-key
- FastMCP Cloud account (sign up at https://fastmcp.cloud)

---

## FastMCP Cloud Configuration

### Server Entrypoint

```
server.py:mcp
```

This tells FastMCP Cloud to:
1. Import the `server.py` file
2. Use the `mcp` object as the FastMCP server instance

### Required Environment Variables

```bash
AYRSHARE_API_KEY=<your-api-key-here>
```

Get your API key from: https://app.ayrshare.com/api-key

### Optional Environment Variables

```bash
# Multi-tenant profile management
AYRSHARE_PROFILE_KEY=<your-profile-key>

# API Configuration
AYRSHARE_BASE_URL=https://app.ayrshare.com/api
AYRSHARE_TIMEOUT=30
AYRSHARE_DEBUG=false

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

---

## Deployment Steps

### 1. Create GitHub Repository

```bash
# Navigate to project directory
cd /home/gotime2022/Projects/mcp-servers/business-productivity/ayrshare-mcp

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit - Ayrshare MCP Server"

# Create GitHub repository
gh repo create ayrshare-mcp --public --source=. --remote=origin --push
```

**Repository URL**: `https://github.com/<your-username>/ayrshare-mcp`

### 2. Deploy to FastMCP Cloud

Visit: https://fastmcp.cloud

#### Step 1: Sign in with GitHub
- Click "Sign in with GitHub"
- Authorize FastMCP Cloud to access your repositories

#### Step 2: Create New Project
- Click "New Project"
- Project name: `ayrshare-mcp`
- Description: "Ayrshare Social Media API - 75+ tools for multi-platform posting"

#### Step 3: Select Repository
- Choose repository: `<your-username>/ayrshare-mcp`
- Branch: `main` (or your default branch)

#### Step 4: Configure Server
- **Entrypoint**: `server.py:mcp` (exact value)
- **Python Version**: 3.10 or higher
- **Framework**: FastMCP (auto-detected)

#### Step 5: Add Environment Variables

Click "Add Environment Variable" and add:

**Required**:
- `AYRSHARE_API_KEY` = `<your-actual-api-key>`

**Optional (Recommended for Production)**:
- `LOG_LEVEL` = `INFO`
- `LOG_FORMAT` = `json`
- `RATE_LIMIT_PER_MINUTE` = `60`
- `RATE_LIMIT_PER_HOUR` = `1000`

#### Step 6: Deploy
- Click "Deploy"
- Wait for deployment to complete (usually 1-2 minutes)
- Monitor deployment logs in the dashboard

---

## Expected Deployment URL

After successful deployment, your server will be available at:

```
https://ayrshare-mcp.fastmcp.app/mcp
```

Or your custom URL if configured.

---

## Verification & Testing

### 1. Check Health Endpoint

```bash
curl https://ayrshare-mcp.fastmcp.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-09T12:00:00Z",
  "server": {
    "name": "Ayrshare Social Media API",
    "version": "1.0.0",
    "transport": "stdio",
    "log_level": "INFO"
  }
}
```

### 2. Test with Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ayrshare": {
      "url": "https://ayrshare-mcp.fastmcp.app/mcp"
    }
  }
}
```

### 3. Test with Claude Code

Add to your `.claude/mcp.json`:

```json
{
  "servers": {
    "ayrshare": {
      "url": "https://ayrshare-mcp.fastmcp.app/mcp",
      "description": "Ayrshare Social Media API - Multi-platform posting"
    }
  }
}
```

### 4. Test Core Functionality

Use any MCP client to test:

```python
# Example: Test posting capability
tools = await client.list_tools()
print(f"Available tools: {len(tools)}")  # Should be 75+

# Test posting
result = await client.call_tool(
    "post_to_social",
    {
        "post_text": "Test post from FastMCP Cloud deployment!",
        "platforms": ["facebook"]
    }
)
```

---

## Monitoring & Maintenance

### View Logs

In FastMCP Cloud dashboard:
1. Navigate to your project
2. Click "Logs" tab
3. Filter by log level (INFO, WARNING, ERROR)

### Monitor Rate Limits

Check health endpoint for current rate limit usage:
```bash
curl https://ayrshare-mcp.fastmcp.app/health | jq '.rate_limits'
```

### Update Environment Variables

1. Go to FastMCP Cloud dashboard
2. Select your project
3. Click "Settings" → "Environment Variables"
4. Update values
5. Redeploy if necessary

---

## Troubleshooting

### Deployment Fails

**Check entrypoint**:
- Must be exactly: `server.py:mcp`
- Case-sensitive
- No spaces

**Check dependencies**:
- Verify `requirements.txt` includes all dependencies
- FastMCP version should be `>=2.0.0`

**View deployment logs**:
- Check FastMCP Cloud dashboard logs for errors

### API Key Errors

```
Error: AYRSHARE_API_KEY not configured
```

**Solution**:
1. Add `AYRSHARE_API_KEY` in environment variables
2. Redeploy the server
3. Verify key is correct from https://app.ayrshare.com/api-key

### Rate Limit Issues

```
Error: Rate limit exceeded
```

**Solution**:
1. Increase `RATE_LIMIT_PER_MINUTE` or `RATE_LIMIT_PER_HOUR`
2. Set to `0` to disable rate limiting
3. Redeploy

---

## Production Optimization

### Enable Structured Logging

```bash
LOG_FORMAT=json
LOG_LEVEL=INFO
```

### Configure Rate Limits

Based on your Ayrshare plan:

**Free Plan**:
```bash
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_PER_HOUR=100
```

**Business Plan**:
```bash
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

**Enterprise Plan**:
```bash
RATE_LIMIT_PER_MINUTE=120
RATE_LIMIT_PER_HOUR=5000
```

### Increase Timeout for Large Media

```bash
AYRSHARE_TIMEOUT=60  # For video uploads
```

---

## Security Best Practices

1. **Never commit API keys** - Always use environment variables
2. **Use GitHub Secrets** - Store sensitive values in GitHub repository secrets
3. **Enable rate limiting** - Protect against abuse
4. **Monitor logs** - Watch for unusual activity
5. **Rotate API keys** - Regularly update keys in environment variables

---

## Support & Resources

- **FastMCP Documentation**: https://gofastmcp.com
- **FastMCP Cloud**: https://fastmcp.cloud
- **Ayrshare API Docs**: https://docs.ayrshare.com
- **Ayrshare Dashboard**: https://app.ayrshare.com

---

**Deployment Status**: Ready for FastMCP Cloud
**Last Updated**: 2025-11-09
**FastMCP Version**: 2.10.5
**MCP Protocol**: 1.12.0
