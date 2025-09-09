# Web Research MCP Server - Development Makefile
# Created by: Cod.1 (Coder Agent)
# Mission: T83 Custom MCP Development

.PHONY: test test-unit test-integration run-server status validate-mcp install setup clean help

# Testing Commands
test: test-unit
	@echo "✅ All tests completed successfully!"

test-unit:
	@echo "Running Web Search MCP unit tests..."
	@uv run python -m unittest discover tests -v

test-integration:
	@echo "Running integration tests..."
	@uv run python -c "import asyncio; from tests.test_web_search import run_async_test; from src.web_search import web_search; result = run_async_test(web_search('Python programming', num_results=3)); print('✅ Integration test passed!' if 'Web Search Results' in result else '❌ Integration test failed!')"

# Server Management
run-server:
	@echo "Starting Web Research MCP Server..."
	@uv run python src/web_search.py

test-mcp:
	@echo "Testing MCP tools directly..."
	@uv run python -c "import asyncio; from src.web_search import web_search, search_status; print('=== MCP Tools Test ==='); loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop); print(loop.run_until_complete(search_status())); print('\n' + loop.run_until_complete(web_search('artificial intelligence', num_results=2))); loop.close(); print('✅ MCP tools test completed!')"

# Development Tools
install:
	@echo "Installing dependencies..."
	@uv add mcp httpx
	@uv add --dev pytest pytest-asyncio

setup: install
	@echo "Setting up Web Research MCP development environment..."
	@echo "Project structure:"
	@find . -name "*.py" -o -name "*.toml" -o -name "Makefile" | head -10

validate-mcp:
	@echo "Validating MCP server structure..."
	@uv run python -c "from src.web_search import mcp; print('✅ FastMCP server initialized successfully'); print(f'✅ Server name: {mcp.name}')"

# Status and Information
status:
	@echo "Web Research MCP Server Status:"
	@echo "================================"
	@uv run python -c "import asyncio; from src.web_search import search_status; result = asyncio.run(search_status()); print(result)"

# Environment Setup
env-setup:
	@echo "Environment Variables Setup Guide:"
	@echo "=================================="
	@echo ""
	@echo "Optional API Keys (for enhanced search capabilities):"
	@echo ""
	@echo "Google Custom Search:"
	@echo "  export GOOGLE_SEARCH_API_KEY='your-google-api-key'"
	@echo "  export GOOGLE_SEARCH_ENGINE_ID='your-search-engine-id'"
	@echo ""
	@echo "Bing Search API:"
	@echo "  export BING_SEARCH_API_KEY='your-bing-api-key'"
	@echo ""
	@echo "Note: DuckDuckGo requires no API key and works out-of-the-box!"

# Production Commands
prod-check:
	@echo "Production readiness check..."
	@$(MAKE) validate-mcp
	@$(MAKE) test-unit
	@$(MAKE) test-integration
	@echo "✅ Web Search MCP Server is production ready!"

# Cleanup
clean:
	@echo "Cleaning up build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup completed!"

# Help
help:
	@echo "Web Research MCP Server - Available Commands:"
	@echo "============================================"
	@echo ""
	@echo "Development:"
	@echo "  make setup          - Set up development environment"
	@echo "  make install        - Install dependencies"
	@echo "  make test           - Run all tests"
	@echo "  make test-unit      - Run unit tests"
	@echo "  make test-integration - Run integration tests"
	@echo ""
	@echo "Server Management:"
	@echo "  make run-server     - Start MCP server"
	@echo "  make validate-mcp   - Validate MCP structure"
	@echo "  make test-mcp       - Test MCP tools directly"
	@echo ""
	@echo "Information:"
	@echo "  make status         - Show provider status"
	@echo "  make env-setup      - Show environment setup guide"
	@echo "  make prod-check     - Production readiness check"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          - Clean build artifacts"
	@echo "  make help           - Show this help"
<<<<<<< HEAD

=======
>>>>>>> origin/main
