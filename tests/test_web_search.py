"""
Comprehensive test suite for Web Research MCP Server
Testing multi-provider search, fallback mechanisms, and error handling.

Created by: Cod.1 (Coder Agent)
Mission: T83 Custom MCP Development
"""

from web_search import (
    DuckDuckGoProvider,
    BingSearchProvider,
    GoogleSearchProvider,
    WebSearchCoordinator,
    web_search,
    research_topic,
    search_status
)
import unittest
import asyncio
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestWebSearchProviders(unittest.TestCase):
    """Test individual search providers."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_query = "Python programming"
        self.ddg_provider = DuckDuckGoProvider()
        self.bing_provider = BingSearchProvider()
        self.google_provider = GoogleSearchProvider()

    def test_duckduckgo_availability(self):
        """Test DDG provider is always available (no API key required)."""
        self.assertTrue(self.ddg_provider.is_available())

    def test_provider_rate_limits(self):
        """Test rate limit configuration."""
        self.assertGreater(self.ddg_provider.rate_limit_delay, 0)
        self.assertGreater(self.bing_provider.rate_limit_delay, 0)
        self.assertGreater(self.google_provider.rate_limit_delay, 0)

    async def test_duckduckgo_search(self):
        """Test DuckDuckGo search functionality."""
        result = await self.ddg_provider.search(self.test_query, num_results=5)

        # Verify response structure
        self.assertIn('provider', result)
        self.assertIn('query', result)
        self.assertIn('results', result)
        self.assertIn('status', result)
        self.assertEqual(result['provider'], 'DuckDuckGo')
        self.assertEqual(result['query'], self.test_query)

        # Should either succeed or fail gracefully
        self.assertIn(result['status'], ['success', 'error'])

    def test_api_key_detection(self):
        """Test API key detection for premium providers."""
        # These should reflect actual environment configuration
        bing_available = bool(os.getenv('BING_SEARCH_API_KEY'))
        google_available = bool(
            os.getenv('GOOGLE_SEARCH_API_KEY') and os.getenv('GOOGLE_SEARCH_ENGINE_ID'))

        self.assertEqual(self.bing_provider.is_available(), bing_available)
        self.assertEqual(self.google_provider.is_available(), google_available)


class TestWebSearchCoordinator(unittest.TestCase):
    """Test the web search coordinator."""

    def setUp(self):
        """Set up test fixtures."""
        self.coordinator = WebSearchCoordinator()
        self.test_query = "artificial intelligence"

    def test_coordinator_initialization(self):
        """Test coordinator has providers."""
        self.assertGreater(len(self.coordinator.providers), 0)

        # Should include DDG as fallback
        provider_names = [p.name for p in self.coordinator.providers]
        self.assertIn('DuckDuckGo', provider_names)

    async def test_multi_provider_search(self):
        """Test multi-provider search with fallback."""
        result = await self.coordinator.search_multi_provider(self.test_query, num_results=5)

        # Verify response structure
        self.assertIn('query', result)
        self.assertIn('results', result)
        self.assertIn('providers_used', result)
        self.assertIn('status', result)
        self.assertEqual(result['query'], self.test_query)

        # Should at least try DDG (always available)
        self.assertGreater(len(result['providers_used']), 0)

    async def test_single_provider_search(self):
        """Test targeting specific provider."""
        result = await self.coordinator.search_single_provider(self.test_query, "duckduckgo", num_results=3)

        self.assertIn('provider', result)
        self.assertEqual(result['provider'], 'DuckDuckGo')

    async def test_invalid_provider_handling(self):
        """Test handling of invalid provider names."""
        result = await self.coordinator.search_single_provider(self.test_query, "invalid_provider", num_results=3)

        self.assertEqual(result['status'], 'error')
        self.assertIn('not found', result['error'])


class TestMCPTools(unittest.TestCase):
    """Test the MCP tool functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_query = "machine learning"

    async def test_web_search_tool(self):
        """Test web_search MCP tool."""
        result = await web_search(self.test_query, num_results=3, provider="auto")

        # Should return formatted string
        self.assertIsInstance(result, str)
        self.assertIn(self.test_query, result)

        # Should include results or error message
        self.assertTrue(
            "Web Search Results" in result or
            "No search results found" in result or
            "Search failed" in result
        )

    async def test_research_topic_tool(self):
        """Test research_topic MCP tool."""
        result = await research_topic("Python", depth="quick")

        self.assertIsInstance(result, str)
        self.assertIn("Research Report", result)
        self.assertIn("Python", result)

    async def test_search_status_tool(self):
        """Test search_status MCP tool."""
        result = await search_status()

        self.assertIsInstance(result, str)
        self.assertIn("Provider Status", result)
        self.assertIn("DuckDuckGo", result)  # Should always be present
        self.assertIn("Available:", result)

    async def test_research_depth_variations(self):
        """Test different research depths."""
        for depth in ["quick", "standard", "deep"]:
            result = await research_topic("blockchain", depth=depth)

            self.assertIn("Research Report", result)
            self.assertIn(f"Research Depth: {depth.title()}", result)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""

    async def test_empty_query_handling(self):
        """Test handling of empty queries."""
        result = await web_search("", num_results=5)

        # Should handle gracefully
        self.assertIsInstance(result, str)

    async def test_network_error_resilience(self):
        """Test resilience to network errors."""
        # This will test the actual error handling in providers
        # Results may vary based on network conditions

        coordinator = WebSearchCoordinator()
        result = await coordinator.search_multi_provider("test query", num_results=1)

        # Should return structured response even on errors
        self.assertIn('status', result)


def run_async_test(coro):
    """Helper to run async tests."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


class AsyncTestCase(unittest.TestCase):
    """Base class for async tests."""

    def run_async(self, coro):
        """Run async coroutine in test."""
        return run_async_test(coro)


# Make async tests work with unittest
def make_async_test_methods():
    """Convert async test methods to sync for unittest."""
    test_classes = [TestWebSearchProviders,
                    TestWebSearchCoordinator, TestMCPTools, TestErrorHandling]

    for test_class in test_classes:
        for attr_name in dir(test_class):
            attr = getattr(test_class, attr_name)
            if (attr_name.startswith('test_') and
                    asyncio.iscoroutinefunction(attr)):

                # Create sync wrapper
                def make_sync_test(async_method):
                    def sync_test(self):
                        return run_async_test(async_method(self))
                    return sync_test

                # Replace async method with sync wrapper
                sync_method = make_sync_test(attr)
                sync_method.__name__ = attr_name
                setattr(test_class, attr_name, sync_method)


# Apply async test conversion
make_async_test_methods()


if __name__ == '__main__':
    # Run tests
    print("Running Web Research MCP Server Tests...")
    print("=" * 50)

    # Test with verbose output
    unittest.main(verbosity=2, exit=False)

    print("\n" + "=" * 50)
    print("Web Search MCP Testing Complete!")
<<<<<<< HEAD

=======
>>>>>>> origin/main
