"""
Production Configuration for Ayrshare MCP Server

This module provides production-ready logging, error handling, and monitoring
configurations for the Ayrshare MCP server.
"""

import os
import sys
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps
import time


class ProductionConfig:
    """Production configuration settings"""

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FORMAT = os.getenv("LOG_FORMAT", "json").lower()

    # Rate limiting
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    RATE_LIMIT_PER_HOUR = int(os.getenv("RATE_LIMIT_PER_HOUR", "1000"))

    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    TRANSPORT = os.getenv("TRANSPORT", "stdio")

    # Ayrshare
    AYRSHARE_TIMEOUT = int(os.getenv("AYRSHARE_TIMEOUT", "30"))
    AYRSHARE_DEBUG = os.getenv("AYRSHARE_DEBUG", "false").lower() == "true"


class JsonFormatter(logging.Formatter):
    """JSON log formatter for structured logging"""

    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            log_data["stack_trace"] = self.formatStack(record.stack_info) if record.stack_info else None

        return json.dumps(log_data)


def setup_logging(name: str = "ayrshare-mcp") -> logging.Logger:
    """
    Configure production logging

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(ProductionConfig.LOG_LEVEL)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    if ProductionConfig.LOG_FORMAT == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        )

    logger.addHandler(handler)
    logger.propagate = False

    return logger


# Global logger instance
logger = setup_logging()


class RateLimiter:
    """Simple in-memory rate limiter"""

    def __init__(self):
        self.minute_calls = []
        self.hour_calls = []

    def check_limit(self) -> tuple[bool, Optional[str]]:
        """
        Check if request is within rate limits

        Returns:
            Tuple of (allowed, error_message)
        """
        now = time.time()

        # Clean old entries
        minute_ago = now - 60
        hour_ago = now - 3600

        self.minute_calls = [t for t in self.minute_calls if t > minute_ago]
        self.hour_calls = [t for t in self.hour_calls if t > hour_ago]

        # Check limits
        if ProductionConfig.RATE_LIMIT_PER_MINUTE > 0:
            if len(self.minute_calls) >= ProductionConfig.RATE_LIMIT_PER_MINUTE:
                return False, f"Rate limit exceeded: {ProductionConfig.RATE_LIMIT_PER_MINUTE} requests per minute"

        if ProductionConfig.RATE_LIMIT_PER_HOUR > 0:
            if len(self.hour_calls) >= ProductionConfig.RATE_LIMIT_PER_HOUR:
                return False, f"Rate limit exceeded: {ProductionConfig.RATE_LIMIT_PER_HOUR} requests per hour"

        # Record this call
        self.minute_calls.append(now)
        self.hour_calls.append(now)

        return True, None


# Global rate limiter instance
rate_limiter = RateLimiter()


def with_error_handling(func):
    """
    Decorator to add error handling and logging to tool functions
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        tool_name = func.__name__

        try:
            logger.debug(f"Calling tool: {tool_name}", extra={
                "extra_fields": {
                    "tool": tool_name,
                    "args_count": len(args),
                    "kwargs_keys": list(kwargs.keys())
                }
            })

            # Check rate limits
            allowed, error_msg = rate_limiter.check_limit()
            if not allowed:
                logger.warning(f"Rate limit exceeded for {tool_name}", extra={
                    "extra_fields": {"tool": tool_name, "error": error_msg}
                })
                return {
                    "status": "error",
                    "error": error_msg,
                    "error_type": "rate_limit"
                }

            # Execute the tool
            result = await func(*args, **kwargs)

            duration = time.time() - start_time
            logger.info(f"Tool completed: {tool_name}", extra={
                "extra_fields": {
                    "tool": tool_name,
                    "duration_seconds": round(duration, 3),
                    "success": True
                }
            })

            return result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Tool error: {tool_name}", exc_info=True, extra={
                "extra_fields": {
                    "tool": tool_name,
                    "duration_seconds": round(duration, 3),
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                }
            })

            return {
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__,
                "tool": tool_name
            }

    return wrapper


def get_health_status() -> Dict[str, Any]:
    """
    Get server health status

    Returns:
        Dictionary with health check information
    """
    import platform

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "server": {
            "name": "Ayrshare MCP Server",
            "version": "1.0.0",
            "transport": ProductionConfig.TRANSPORT,
            "log_level": ProductionConfig.LOG_LEVEL
        },
        "system": {
            "python_version": platform.python_version(),
            "platform": platform.platform()
        },
        "rate_limits": {
            "per_minute": ProductionConfig.RATE_LIMIT_PER_MINUTE,
            "per_hour": ProductionConfig.RATE_LIMIT_PER_HOUR,
            "current_minute": len(rate_limiter.minute_calls),
            "current_hour": len(rate_limiter.hour_calls)
        },
        "configuration": {
            "ayrshare_timeout": ProductionConfig.AYRSHARE_TIMEOUT,
            "debug_mode": ProductionConfig.AYRSHARE_DEBUG
        }
    }


def log_startup():
    """Log server startup information"""
    logger.info("Starting Ayrshare MCP Server", extra={
        "extra_fields": {
            "version": "1.0.0",
            "transport": ProductionConfig.TRANSPORT,
            "log_level": ProductionConfig.LOG_LEVEL,
            "log_format": ProductionConfig.LOG_FORMAT,
            "rate_limit_minute": ProductionConfig.RATE_LIMIT_PER_MINUTE,
            "rate_limit_hour": ProductionConfig.RATE_LIMIT_PER_HOUR
        }
    })


def log_shutdown():
    """Log server shutdown information"""
    logger.info("Shutting down Ayrshare MCP Server")
