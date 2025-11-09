# Deployment Checklist - Ayrshare MCP Server

Use this checklist to ensure a successful deployment to FastMCP Cloud.

## Pre-Deployment Validation

### Code & Configuration
- [ ] Server file exists: `server.py`
- [ ] Server instance defined: `mcp = FastMCP("Ayrshare Social Media API")`
- [ ] All tools decorated with `@mcp.tool()`
- [ ] All resources defined with proper URIs
- [ ] All prompts defined correctly
- [ ] `fastmcp.json` configuration file created
- [ ] `requirements.txt` includes all dependencies
- [ ] `.env.example` has placeholders only (no real API keys)

### Security
- [ ] No hardcoded API keys in code
- [ ] `.env` file in `.gitignore`
- [ ] API key obtained from https://app.ayrshare.com/api-key
- [ ] Environment variables documented
- [ ] Rate limiting configured

### Testing
- [ ] Server starts successfully locally: `python server.py`
- [ ] STDIO mode tested
- [ ] HTTP mode tested: `python server.py --http`
- [ ] All critical tools tested
- [ ] Error handling verified

## GitHub Repository Setup

- [ ] Git repository initialized
- [ ] Remote repository created: `gh repo create ayrshare-mcp --public`
- [ ] Initial commit created
- [ ] Code pushed to GitHub
- [ ] Repository URL saved: `https://github.com/<username>/ayrshare-mcp`
- [ ] README.md updated with deployment info

## FastMCP Cloud Configuration

### Account & Project Setup
- [ ] FastMCP Cloud account created
- [ ] Signed in with GitHub
- [ ] New project created: "ayrshare-mcp"
- [ ] Repository selected from GitHub

### Server Configuration
- [ ] Entrypoint set: `server.py:mcp` (exact)
- [ ] Python version: 3.10 or higher
- [ ] Framework: FastMCP (auto-detected)

### Environment Variables
**Required**:
- [ ] `AYRSHARE_API_KEY` = `<your-actual-key>`

**Optional (Recommended)**:
- [ ] `LOG_LEVEL` = `INFO`
- [ ] `LOG_FORMAT` = `json`
- [ ] `RATE_LIMIT_PER_MINUTE` = `60`
- [ ] `RATE_LIMIT_PER_HOUR` = `1000`
- [ ] `AYRSHARE_TIMEOUT` = `30`

### Additional Configuration
- [ ] `AYRSHARE_PROFILE_KEY` (if using multi-tenant)
- [ ] `AYRSHARE_BASE_URL` (if custom)

## Deployment

- [ ] "Deploy" button clicked
- [ ] Deployment logs monitored
- [ ] No errors in deployment logs
- [ ] Deployment completed successfully
- [ ] Deployment URL saved: `https://ayrshare-mcp.fastmcp.app/mcp`

## Post-Deployment Verification

### Health Check
- [ ] Health endpoint accessible: `curl https://ayrshare-mcp.fastmcp.app/health`
- [ ] Health check returns "healthy" status
- [ ] Server version correct
- [ ] Rate limits showing correct values

### Functionality Testing
- [ ] MCP endpoint accessible: `https://ayrshare-mcp.fastmcp.app/mcp`
- [ ] Tools list returned (75+ tools)
- [ ] Resources list returned (5 resources)
- [ ] Prompts list returned (5 prompts)
- [ ] Test posting to one platform successful
- [ ] Error handling working correctly

### IDE Integration
- [ ] Claude Desktop configuration added
- [ ] Claude Code configuration added
- [ ] Server appears in MCP servers list
- [ ] Tools accessible from IDE
- [ ] Sample operation tested successfully

### Monitoring
- [ ] Logs accessible in FastMCP Cloud dashboard
- [ ] Log format is JSON (structured logging)
- [ ] Log level is INFO
- [ ] No errors in recent logs
- [ ] Rate limit counters working

## Documentation

- [ ] Deployment URL documented
- [ ] Environment variables documented
- [ ] Configuration guide updated
- [ ] Troubleshooting section added
- [ ] IDE integration examples provided
- [ ] Monitoring instructions documented

## Production Readiness

### Performance
- [ ] Rate limiting configured appropriately
- [ ] Timeout settings optimized
- [ ] Log level set to INFO (not DEBUG)
- [ ] Structured logging enabled (JSON format)

### Security
- [ ] API keys secured in environment variables
- [ ] No secrets in repository
- [ ] GitHub repository secrets configured (if needed)
- [ ] Rate limiting enabled
- [ ] Error messages don't expose sensitive data

### Reliability
- [ ] Health check endpoint working
- [ ] Error handling comprehensive
- [ ] Logging captures important events
- [ ] Dependencies pinned in requirements.txt

### Maintainability
- [ ] Documentation complete and accurate
- [ ] Configuration clearly documented
- [ ] Troubleshooting guide available
- [ ] Contact/support information provided

## Optional Enhancements

- [ ] Custom domain configured
- [ ] SSL certificate verified
- [ ] Monitoring alerts set up
- [ ] Backup strategy defined
- [ ] Disaster recovery plan documented
- [ ] Performance monitoring enabled
- [ ] Usage analytics configured

---

## Rollback Plan

If deployment fails or issues occur:

1. **Immediate Actions**:
   - [ ] Check FastMCP Cloud dashboard logs
   - [ ] Verify environment variables
   - [ ] Check GitHub repository state

2. **Common Fixes**:
   - [ ] Update entrypoint configuration
   - [ ] Verify API key is correct
   - [ ] Check dependencies versions
   - [ ] Review recent code changes

3. **Rollback Options**:
   - [ ] Revert to previous GitHub commit
   - [ ] Redeploy from known-good commit
   - [ ] Restore environment variables
   - [ ] Contact FastMCP Cloud support

---

## Success Criteria

Deployment is considered successful when:

- [ ] All pre-deployment checks passed
- [ ] GitHub repository created and accessible
- [ ] FastMCP Cloud deployment completed without errors
- [ ] Health check returns healthy status
- [ ] All 75+ tools accessible via MCP
- [ ] Sample operations work correctly
- [ ] IDE integration functional
- [ ] Logs showing normal operation
- [ ] No security issues detected
- [ ] Documentation complete and accurate

---

**Checklist Version**: 1.0
**Last Updated**: 2025-11-09
**For Server Version**: 1.0.0
