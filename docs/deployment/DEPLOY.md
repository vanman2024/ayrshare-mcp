# Quick Deployment Guide

Deploy the Ayrshare MCP Server to FastMCP Cloud in 5 minutes.

## Prerequisites

- Ayrshare API key from https://app.ayrshare.com/api-key
- GitHub account
- FastMCP Cloud account (sign up at https://fastmcp.cloud)

## Deployment Steps

### 1. Create GitHub Repository (2 minutes)

```bash
cd /home/gotime2022/Projects/mcp-servers/business-productivity/ayrshare-mcp

# Create and push to GitHub
gh repo create ayrshare-mcp --public --source=. --remote=origin --push
```

### 2. Deploy to FastMCP Cloud (3 minutes)

Visit: **https://fastmcp.cloud**

1. **Sign in** with GitHub
2. Click **"New Project"**
3. **Configure**:
   - Project name: `ayrshare-mcp`
   - Repository: `<your-username>/ayrshare-mcp`
   - **Entrypoint**: `server.py:mcp` (exact value)
   - Python: `3.10+`

4. **Add Environment Variables**:
   ```
   AYRSHARE_API_KEY = <your-api-key>
   LOG_LEVEL = INFO
   LOG_FORMAT = json
   RATE_LIMIT_PER_MINUTE = 60
   RATE_LIMIT_PER_HOUR = 1000
   ```

5. Click **"Deploy"**

### 3. Verify Deployment

Your server will be at: `https://ayrshare-mcp.fastmcp.app/mcp`

Test health:
```bash
curl https://ayrshare-mcp.fastmcp.app/health
```

## IDE Integration

### Claude Desktop

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "ayrshare": {
      "url": "https://ayrshare-mcp.fastmcp.app/mcp"
    }
  }
}
```

### Claude Code

Add to `.claude/mcp.json`:
```json
{
  "servers": {
    "ayrshare": {
      "url": "https://ayrshare-mcp.fastmcp.app/mcp"
    }
  }
}
```

## What's Included

- 75+ social media tools
- 5 resources (dashboard, calendar, etc.)
- 5 content optimization prompts
- 13+ platform support
- Production logging (JSON)
- Rate limiting
- Health checks
- Error handling

## Documentation

- **Complete Guide**: `FASTMCP_CLOUD_DEPLOYMENT.md`
- **Checklist**: `DEPLOYMENT_CHECKLIST.md`
- **Production Config**: `PRODUCTION_CONFIG.md`
- **Quick Reference**: `DEPLOYMENT_SUMMARY.md`

## Need Help?

- Check `DEPLOYMENT_CHECKLIST.md` for detailed steps
- Review `PRODUCTION_CONFIG.md` for configuration options
- See `FASTMCP_CLOUD_DEPLOYMENT.md` for troubleshooting

---

**Status**: Ready to deploy
**Estimated Time**: 5 minutes
**Last Updated**: 2025-11-09
