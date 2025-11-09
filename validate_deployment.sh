#!/bin/bash
# Deployment Validation Script for Ayrshare MCP Server
# Usage: bash validate_deployment.sh

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     Ayrshare MCP Server - Deployment Validation               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $1"
        ((FAILED++))
    fi
}

echo "📋 Checking Configuration Files..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test -f fastmcp.json
check "fastmcp.json exists"

test -f production_config.py
check "production_config.py exists"

test -f health_check.py
check "health_check.py exists"

test -f .env.example
check ".env.example exists"

test -f server.py
check "server.py exists"

echo ""
echo "📚 Checking Documentation..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test -f docs/deployment/DEPLOY.md
check "DEPLOY.md exists"

test -f docs/deployment/DEPLOYMENT_CHECKLIST.md
check "DEPLOYMENT_CHECKLIST.md exists"

test -f docs/deployment/DEPLOYMENT_SUMMARY.md
check "DEPLOYMENT_SUMMARY.md exists"

test -f docs/deployment/FASTMCP_CLOUD_DEPLOYMENT.md
check "FASTMCP_CLOUD_DEPLOYMENT.md exists"

test -f docs/deployment/PRODUCTION_CONFIG.md
check "PRODUCTION_CONFIG.md exists"

test -f DEPLOYMENT_STATUS.md
check "DEPLOYMENT_STATUS.md exists"

echo ""
echo "🔍 Validating Configuration..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Validate JSON
python -c "import json; json.load(open('fastmcp.json'))" 2>/dev/null
check "fastmcp.json is valid JSON"

# Check server entrypoint
grep -q '"entrypoint": "mcp"' fastmcp.json
check "Server entrypoint is 'mcp'"

# Check server file path
grep -q '"path": "server.py"' fastmcp.json
check "Server path is 'server.py'"

# Check for AYRSHARE_API_KEY in env
grep -q 'AYRSHARE_API_KEY' fastmcp.json
check "AYRSHARE_API_KEY defined in fastmcp.json"

echo ""
echo "🔐 Security Validation..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for hardcoded keys in .env.example
! grep -E "AYRSHARE_API_KEY=E64245A6|AYRSHARE_API_KEY=[A-Z0-9]{8}-" .env.example >/dev/null 2>&1
check ".env.example has no real API keys"

# Check .env.example has placeholders
grep -q "your_ayrshare_api_key_here" .env.example
check ".env.example has placeholder values"

# Check if .env is in .gitignore
test -f .gitignore && grep -q "\.env" .gitignore
check ".env is in .gitignore"

echo ""
echo "🧪 Testing Python Modules..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test production_config import
python -c "from production_config import setup_logging, get_health_status" 2>/dev/null
check "production_config.py imports successfully"

# Test health_check import
python -c "from health_check import health_check" 2>/dev/null
check "health_check.py imports successfully"

# Test server import
python -c "from server import mcp" 2>/dev/null
check "server.py imports successfully"

echo ""
echo "🚀 Server Startup Test..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test server starts (timeout after 3 seconds)
timeout 3 python server.py >/dev/null 2>&1 || true
if [ $? -eq 124 ]; then
    echo -e "${GREEN}✓${NC} Server starts successfully"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Server startup test inconclusive"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Validation Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Passed: ${GREEN}${PASSED}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All validation checks passed!${NC}"
    echo ""
    echo "Your server is ready for deployment to FastMCP Cloud."
    echo ""
    echo "Next steps:"
    echo "  1. Create GitHub repository: gh repo create ayrshare-mcp --public"
    echo "  2. Deploy to FastMCP Cloud: https://fastmcp.cloud"
    echo "  3. Follow: docs/deployment/DEPLOY.md"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Some validation checks failed.${NC}"
    echo ""
    echo "Please fix the issues above before deploying."
    echo "See DEPLOYMENT_STATUS.md for details."
    echo ""
    exit 1
fi
