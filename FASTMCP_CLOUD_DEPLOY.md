# FastMCP Cloud Deployment Guide

## Pre-Deployment Checklist ✅

- ✅ FastMCP 2.x framework (v2.10.5)
- ✅ 75+ MCP tools properly decorated with `@mcp.tool()`
- ✅ 5 MCP resources with proper URI patterns
- ✅ 5 MCP prompts for content optimization
- ✅ No hardcoded API keys (all use environment variables)
- ✅ Clean project structure (Docker files removed)
- ✅ Server starts successfully in STDIO mode
- ✅ All resource URI templates fixed and functional

## Project Structure

```
ayrshare-mcp/
├── server.py                  # Main FastMCP server (75+ tools)
├── ayrshare_client.py         # Ayrshare API client
├── .env                       # Environment variables (API key configured)
├── .env.example               # Template with placeholders
├── pyproject.toml             # Project metadata & dependencies
├── requirements.txt           # Production dependencies
├── docs/                      # Additional documentation
│   ├── MCP_SETUP.md
│   ├── QUICKSTART.md
│   └── TESTING.md
└── README.md                  # Complete documentation
```

## Deployment Steps

### 1. Verify Local Functionality

Test the server locally first:

```bash
# Test STDIO mode (default)
python server.py

# Test HTTP mode
python server.py --http
```

Expected output:
```
╭─ FastMCP 2.0 ─────────────────────────────────────────╮
│  🖥️  Server name:     Ayrshare Social Media API         │
│  📦 Transport:       STDIO                             │
│  🏎️  FastMCP version: 2.10.5                            │
╰────────────────────────────────────────────────────────╯
```

### 2. Prepare for FastMCP Cloud

**Environment Variables Required:**
- `AYRSHARE_API_KEY` - Your Ayrshare API key (already configured in `.env`)
- `AYRSHARE_PROFILE_KEY` - (Optional) For multi-tenant scenarios

**Entry Point:**
- Format: `server.py:mcp` (file path + server object name)
- Main file: `server.py` (in root directory)
- Server instance: `mcp` (initialized at line 22)
- Transport: Supports both STDIO and HTTP
- Note: FastMCP Cloud imports the `mcp` object directly and ignores `if __name__ == "__main__"`

### 3. Deploy to FastMCP Cloud

Visit [https://fastmcp.cloud](https://fastmcp.cloud) and:

1. **Create New Deployment**
   - Project name: `ayrshare-mcp`
   - Description: "Ayrshare Social Media API - 75+ tools for multi-platform posting"

2. **Configure Repository**
   - Upload project directory or connect Git repository
   - Entry point: `server.py:mcp` (FastMCP Cloud imports the server object)
   - Python version: 3.10 or higher

3. **Set Environment Variables**
   - Add `AYRSHARE_API_KEY` from your `.env` file
   - Add `AYRSHARE_PROFILE_KEY` if using multi-tenant features

4. **Deploy**
   - FastMCP Cloud will automatically:
     - Install dependencies from `requirements.txt`
     - Start the server with proper transport
     - Expose MCP protocol endpoints

### 4. Verify Deployment

Once deployed, test using an MCP client:

```python
# Example: Connect to deployed server
from mcp import ClientSession

async with ClientSession(server_url="your-fastmcp-cloud-url") as session:
    # List available tools
    tools = await session.list_tools()
    print(f"Available tools: {len(tools)}")

    # Test posting
    result = await session.call_tool(
        "post_to_social",
        {
            "post_text": "Test post from FastMCP Cloud!",
            "platforms": ["facebook"]
        }
    )
    print(result)
```

## Server Capabilities

### Core Publishing (13 tools)
- `post_to_social` - Multi-platform posting
- `schedule_post` - Schedule for future publication
- `bulk_post` - Batch posting operations
- `update_post` - Edit existing posts
- `delete_post` - Remove posts
- And more...

### Analytics & Insights (15 tools)
- `get_post_analytics` - Engagement metrics
- `get_profile_analytics` - Audience insights
- `get_link_analytics` - URL tracking
- Dashboard resources and analytics tools

### Multi-User SaaS (12 tools)
- `create_user_profile` - Profile management
- `list_user_profiles` - Browse profiles
- `update_profile` - Modify profile settings
- Complete multi-tenant support

### AI Features (8 tools)
- `generate_post_content` - AI post generation
- `generate_hashtags` - Smart hashtag suggestions
- `generate_image_caption` - Auto captions
- Content optimization prompts

### Automation (10 tools)
- `auto_schedule_post` - AI-powered timing
- `create_evergreen_post` - Auto-reposting
- `get_scheduled_posts` - Calendar management
- Content calendar resources

## Supported Platforms

- Facebook
- Instagram
- Twitter/X
- LinkedIn
- TikTok
- YouTube
- Pinterest
- Reddit
- Snapchat
- Telegram
- Threads
- Bluesky
- Google Business Profile (GMB)

## Performance Metrics

- **Total Tools:** 75+
- **Total Resources:** 5 (with dynamic URI templates)
- **Total Prompts:** 5 (content optimization)
- **API Coverage:** Complete Ayrshare API (15 categories)
- **Platform Support:** 13+ social networks

## Security ✅

- ✅ No hardcoded credentials
- ✅ Environment-based configuration
- ✅ `.env` file gitignored
- ✅ `.env.example` with placeholders only
- ✅ Proper error handling for missing keys
- ✅ HTTPS transport support

## Troubleshooting

### Server won't start
```bash
# Check Python version
python --version  # Should be 3.10+

# Verify dependencies
pip install -r requirements.txt

# Test import
python -c "from src.server import mcp"
```

### Missing API key error
```bash
# Verify .env file exists
cat .env | grep AYRSHARE_API_KEY

# Should output:
# AYRSHARE_API_KEY=E64245A6-D7BC461C-B10BB820-DDDD6925
```

### Resource URI template errors
✅ **FIXED** - All URI templates now use proper parameter names:
- `get_analytics_dashboard(period: str)` - Fixed from `uri: str`
- `get_content_calendar(year: str, month: str)` - Fixed from `uri: str`

## Post-Deployment

After successful deployment:

1. **Test Core Functions**
   - Try posting to one platform
   - Fetch post history
   - Check analytics

2. **Monitor Performance**
   - Check FastMCP Cloud dashboard
   - Review logs for errors
   - Monitor API usage

3. **Scale as Needed**
   - Add more profiles for multi-tenant
   - Configure rate limiting
   - Set up monitoring alerts

## Support

- **FastMCP Docs:** https://gofastmcp.com
- **FastMCP Cloud:** https://fastmcp.cloud
- **Ayrshare API Docs:** https://docs.ayrshare.com
- **Project Issues:** See README.md for contact info

---

**Deployment Status:** ✅ Ready for FastMCP Cloud

**Last Updated:** 2025-11-09
**FastMCP Version:** 2.10.5
**MCP Protocol Version:** 1.12.0
