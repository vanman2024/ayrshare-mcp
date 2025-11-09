"""
Health Check Tool for Ayrshare MCP Server

This module provides a health check tool that can be added to the FastMCP server.
"""

from typing import Dict, Any
from production_config import get_health_status, logger


async def health_check() -> Dict[str, Any]:
    """
    Check server health status

    Returns comprehensive health information including:
    - Server status and version
    - System information
    - Rate limit statistics
    - Configuration details

    Returns:
        Dictionary with health check results

    Example:
        health_check()
        # Returns:
        # {
        #     "status": "healthy",
        #     "timestamp": "2025-11-09T12:00:00Z",
        #     "server": {...},
        #     "system": {...},
        #     "rate_limits": {...}
        # }
    """
    try:
        health_data = get_health_status()
        logger.debug("Health check completed successfully")
        return health_data
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return {
            "status": "unhealthy",
            "error": str(e),
            "error_type": type(e).__name__
        }


# To add this to your server.py, add this tool:
"""
from health_check import health_check

@mcp.tool()
async def server_health() -> Dict[str, Any]:
    '''
    Check server health status and configuration

    Returns comprehensive health information including server status,
    system details, rate limits, and configuration.

    Returns:
        Dictionary with health check results
    '''
    return await health_check()
"""
