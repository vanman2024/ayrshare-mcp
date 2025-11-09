# Deployment Section for README.md

Add this section to the main README.md file to document deployment options.

---

## Deployment

The Ayrshare MCP Server supports multiple deployment options with production-ready features.

### Quick Deployment to FastMCP Cloud (5 minutes)

```bash
# 1. Create GitHub repository
gh repo create ayrshare-mcp --public --source=. --remote=origin --push

# 2. Visit https://fastmcp.cloud and deploy with:
#    Entrypoint: server.py:mcp
#    Env: AYRSHARE_API_KEY=<your-key>
```

See [Quick Deployment Guide](docs/deployment/DEPLOY.md) for full instructions.

### Deployment Options

| Option | Use Case | Documentation |
|--------|----------|---------------|
| **FastMCP Cloud** | Production hosting | [FASTMCP_CLOUD_DEPLOYMENT.md](docs/deployment/FASTMCP_CLOUD_DEPLOYMENT.md) |
| **STDIO Mode** | Local IDE integration | [MCP_SETUP.md](docs/MCP_SETUP.md) |
| **HTTP Mode** | Remote access/testing | Run with `--http` flag |

### Production Features

- **Structured Logging**: JSON or text format with configurable levels
- **Rate Limiting**: Per-minute and per-hour request limits
- **Error Handling**: Comprehensive error handling and recovery
- **Health Checks**: Built-in health monitoring endpoint
- **Environment Config**: Full environment-based configuration

### Configuration Files

- `fastmcp.json` - FastMCP Cloud configuration
- `production_config.py` - Production logging and rate limiting
- `health_check.py` - Health monitoring tool
- `.env.example` - Environment variable template

### Documentation

- [Quick Start](docs/deployment/DEPLOY.md) - 5-minute deployment guide
- [Checklist](docs/deployment/DEPLOYMENT_CHECKLIST.md) - Complete deployment checklist
- [Summary](docs/deployment/DEPLOYMENT_SUMMARY.md) - Quick reference
- [Complete Guide](docs/deployment/FASTMCP_CLOUD_DEPLOYMENT.md) - Comprehensive deployment guide
- [Production Config](docs/deployment/PRODUCTION_CONFIG.md) - Production features guide
- [Status](DEPLOYMENT_STATUS.md) - Current deployment status

### Environment Variables

Required:
```bash
AYRSHARE_API_KEY=your_ayrshare_api_key_here
```

Optional (Production):
```bash
LOG_LEVEL=INFO
LOG_FORMAT=json
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

See `.env.example` for all available options.

---
