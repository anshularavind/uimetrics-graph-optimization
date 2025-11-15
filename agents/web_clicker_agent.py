"""
Web Clicker AI Agent

This agent takes control of a browser, navigates a website by clicking links,
and generates a navigation graph for UI metrics analysis.

Features:
- Autonomous exploration of websites
- Click tracking and graph generation
- Intelligent navigation (avoids external links, respects same-domain)
- Configurable exploration depth and breadth
- Generates graph data compatible with GraphMetrics
"""

import json
import time
import hashlib
from collections import defaultdict
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Set, Tuple, Optional
import asyncio


class WebClickerAgent:
    """
    An autonomous agent that explores websites by clicking links
    and generates navigation graphs for UI analysis.
    """
    
    def __init__(
        self,
        base_url: str,
        max_clicks: int = 100,
        max_depth: int = 5,
        same_domain_only: bool = True,
        headless: bool = False,
        wait_time: float = 1.0,
        keep_open: bool = False,
        pause_before_close: float = 0.0
    ):
        """
        Initialize the Web Clicker Agent.
        
        Args:
            base_url: Starting URL to explore
            max_clicks: Maximum number of clicks to perform
            max_depth: Maximum navigation depth from start page
            same_domain_only: Only click links within the same domain
            headless: Run browser in headless mode
            wait_time: Seconds to wait between clicks
            keep_open: Keep browser open after exploration (requires manual close)
            pause_before_close: Seconds to wait before closing browser (0 = close immediately)
        """
        self.base_url = base_url
        self.max_clicks = max_clicks
        self.max_depth = max_depth
        self.same_domain_only = same_domain_only
        self.headless = headless
        self.wait_time = wait_time
        self.keep_open = keep_open
        self.pause_before_close = pause_before_close
        
        # Parse base domain
        parsed = urlparse(base_url)
        self.base_domain = parsed.netloc
        
        # Tracking
        self.visited_urls: Set[str] = set()
        self.navigation_graph: Dict[Tuple[str, str], int] = defaultdict(int)
        self.page_labels: Dict[str, str] = {}  # URL -> readable label
        self.click_count = 0
        
        # Browser instances (will be initialized)
        self.browser = None
        self.page = None
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL by removing fragments and trailing slashes."""
        parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        return normalized.rstrip('/')
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL should be explored."""
        if not url:
            return False
        
        parsed = urlparse(url)
        
        # Skip non-HTTP protocols
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Skip external domains if configured
        if self.same_domain_only and parsed.netloc != self.base_domain:
            return False
        
        # Skip common file types
        skip_extensions = ['.pdf', '.zip', '.exe', '.dmg', '.jpg', '.png', '.gif', '.mp4', '.mp3']
        if any(url.lower().endswith(ext) for ext in skip_extensions):
            return False
        
        return True
    
    def _get_page_label(self, url: str, page_title: str = None) -> str:
        """
        Generate a readable label for a page.
        Uses page title or URL path.
        """
        if page_title and page_title.strip():
            return page_title.strip()[:100]
        
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        
        if not path:
            return f"{parsed.netloc} - Home"
        
        # Use last segment of path
        segments = path.split('/')
        label = segments[-1].replace('-', ' ').replace('_', ' ').title()
        return label[:100] if label else path[:100]
    
    async def _init_browser(self):
        """Initialize Playwright browser."""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            raise ImportError(
                "Playwright not installed. Install with:\n"
                "  pip install playwright\n"
                "  playwright install chromium"
            )
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        
        # Create browser context with reasonable settings
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        
        self.page = await self.context.new_page()
        
        print(f"✓ Browser initialized ({'headless' if self.headless else 'visible'})")
    
    async def _close_browser(self):
        """Close browser and cleanup."""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def _get_clickable_links(self) -> List[Dict]:
        """
        Extract all clickable links from the current page.
        Returns list of {url, text, selector} dicts.
        """
        try:
            # Get all links
            links = await self.page.evaluate("""
                () => {
                    const links = [];
                    const elements = document.querySelectorAll('a[href]');
                    
                    elements.forEach((el, idx) => {
                        const rect = el.getBoundingClientRect();
                        const isVisible = rect.width > 0 && rect.height > 0 &&
                                        window.getComputedStyle(el).visibility !== 'hidden' &&
                                        window.getComputedStyle(el).display !== 'none';
                        
                        if (isVisible) {
                            links.push({
                                url: el.href,
                                text: el.innerText.trim().substring(0, 100),
                                selector: `a[href="${el.getAttribute('href')}"]`
                            });
                        }
                    });
                    
                    return links;
                }
            """)
            
            return links
        except Exception as e:
            print(f"  ⚠️  Error extracting links: {e}")
            return []
    
    async def _click_link(self, link: Dict) -> Optional[str]:
        """
        Click a link and return the new URL if successful.
        
        Args:
            link: Dict with 'url', 'text', 'selector'
        
        Returns:
            New URL if navigation succeeded, None otherwise
        """
        try:
            current_url = self.page.url
            
            # Try to click the link
            try:
                await self.page.click(link['selector'], timeout=3000)
            except:
                # If clicking fails, try navigating directly
                await self.page.goto(link['url'], timeout=10000, wait_until='domcontentloaded')
            
            # Wait for navigation
            await self.page.wait_for_load_state('domcontentloaded', timeout=5000)
            await asyncio.sleep(self.wait_time)
            
            new_url = self.page.url
            
            # Record navigation
            if current_url != new_url:
                return new_url
            
            return None
            
        except Exception as e:
            print(f"  ⚠️  Click failed: {str(e)[:100]}")
            return None
    
    async def explore(self):
        """
        Main exploration method. Autonomously clicks through the website.
        """
        print(f"\n🤖 Web Clicker Agent Starting")
        print(f"   Base URL: {self.base_url}")
        print(f"   Max clicks: {self.max_clicks}")
        print(f"   Max depth: {self.max_depth}")
        print(f"   Same domain only: {self.same_domain_only}")
        print()
        
        await self._init_browser()
        
        try:
            # Navigate to base URL
            print(f"📍 Navigating to {self.base_url}...")
            await self.page.goto(self.base_url, timeout=30000, wait_until='domcontentloaded')
            await asyncio.sleep(self.wait_time)
            
            start_url = self._normalize_url(self.page.url)
            self.visited_urls.add(start_url)
            
            # Get page title
            try:
                title = await self.page.title()
                self.page_labels[start_url] = self._get_page_label(start_url, title)
            except:
                self.page_labels[start_url] = self._get_page_label(start_url)
            
            print(f"✓ Started at: {self.page_labels[start_url]}")
            print()
            
            # Exploration queue: (url, depth)
            to_explore = [(start_url, 0)]
            
            while to_explore and self.click_count < self.max_clicks:
                current_url, depth = to_explore.pop(0)
                
                if depth >= self.max_depth:
                    continue
                
                # Navigate to URL if not already there
                if self._normalize_url(self.page.url) != current_url:
                    try:
                        await self.page.goto(current_url, timeout=10000, wait_until='domcontentloaded')
                        await asyncio.sleep(self.wait_time)
                    except:
                        continue
                
                # Get current page info
                current_label = self.page_labels.get(current_url, current_url)
                
                # Get all links on page
                links = await self._get_clickable_links()
                valid_links = [
                    link for link in links
                    if self._is_valid_url(link['url'])
                ]
                
                print(f"🔍 [{self.click_count}/{self.max_clicks}] Exploring: {current_label}")
                print(f"   Found {len(valid_links)} valid links (depth {depth})")
                
                # Click through links
                clicked_this_page = 0
                for link in valid_links[:10]:  # Limit links per page
                    if self.click_count >= self.max_clicks:
                        break
                    
                    target_url = self._normalize_url(link['url'])
                    
                    # Record the edge (even if already visited)
                    source_label = self.page_labels[current_url]
                    
                    # Get target label
                    if target_url not in self.page_labels:
                        self.page_labels[target_url] = self._get_page_label(
                            target_url,
                            link['text'] if link['text'] else None
                        )
                    target_label = self.page_labels[target_url]
                    
                    # Record edge
                    self.navigation_graph[(source_label, target_label)] += 1
                    
                    print(f"   → Clicking: {link['text'][:50] if link['text'] else target_label}")
                    
                    # Click the link
                    new_url = await self._click_link(link)
                    self.click_count += 1
                    clicked_this_page += 1
                    
                    if new_url:
                        new_url_normalized = self._normalize_url(new_url)
                        
                        # Update label if we got a better one
                        if new_url_normalized not in self.visited_urls:
                            try:
                                title = await self.page.title()
                                self.page_labels[new_url_normalized] = self._get_page_label(
                                    new_url_normalized, title
                                )
                            except:
                                pass
                        
                        # Add to exploration queue if not visited
                        if new_url_normalized not in self.visited_urls:
                            self.visited_urls.add(new_url_normalized)
                            to_explore.append((new_url_normalized, depth + 1))
                        
                        # Go back to continue exploring current page
                        try:
                            await self.page.go_back(timeout=5000, wait_until='domcontentloaded')
                            await asyncio.sleep(self.wait_time)
                        except:
                            # If back fails, navigate directly
                            try:
                                await self.page.goto(current_url, timeout=10000, wait_until='domcontentloaded')
                                await asyncio.sleep(self.wait_time)
                            except:
                                break
                
                print(f"   ✓ Clicked {clicked_this_page} links from this page")
                print()
            
            print(f"🏁 Exploration Complete!")
            print(f"   Total clicks: {self.click_count}")
            print(f"   Unique pages: {len(self.visited_urls)}")
            print(f"   Navigation edges: {len(self.navigation_graph)}")
            print()
            
        finally:
            # Pause before closing if configured
            if self.pause_before_close > 0:
                print(f"⏸️  Pausing {self.pause_before_close} seconds before closing browser...")
                await asyncio.sleep(self.pause_before_close)
            
            # Keep browser open if configured
            if self.keep_open:
                print("🔓 Browser will remain open. Close it manually when done.")
                print("   Press Ctrl+C to exit and close the browser.")
                try:
                    # Keep the script running
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    print("\n👋 Closing browser...")
            
            await self._close_browser()
    
    def get_graph_data(self) -> List[Dict]:
        """
        Get navigation graph in format compatible with GraphMetrics.
        
        Returns:
            List of {"source": str, "target": str, "weight": int}
        """
        return [
            {
                "source": source,
                "target": target,
                "weight": weight
            }
            for (source, target), weight in self.navigation_graph.items()
        ]
    
    def save_graph(self, filepath: str):
        """Save navigation graph to JSON file."""
        data = self.get_graph_data()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Graph saved to {filepath}")
    
    def get_summary(self) -> str:
        """Get a summary of the exploration."""
        lines = []
        lines.append("="*70)
        lines.append("WEB CLICKER AGENT - EXPLORATION SUMMARY")
        lines.append("="*70)
        lines.append(f"Base URL: {self.base_url}")
        lines.append(f"Total clicks: {self.click_count}")
        lines.append(f"Unique pages visited: {len(self.visited_urls)}")
        lines.append(f"Navigation edges recorded: {len(self.navigation_graph)}")
        lines.append(f"Total navigation events: {sum(self.navigation_graph.values())}")
        lines.append("")
        lines.append("Top Navigation Paths:")
        
        # Sort by weight
        sorted_edges = sorted(
            self.navigation_graph.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        for (source, target), weight in sorted_edges:
            source_short = source[:30] + "..." if len(source) > 30 else source
            target_short = target[:30] + "..." if len(target) > 30 else target
            lines.append(f"  {source_short} → {target_short} ({weight}x)")
        
        lines.append("="*70)
        return "\n".join(lines)


async def main():
    """Example usage of the Web Clicker Agent."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m agents.web_clicker_agent <url> [options]")
        print("")
        print("Options:")
        print("  --max-clicks N       Maximum clicks (default: 100)")
        print("  --max-depth N        Maximum depth (default: 5)")
        print("  --output FILE        Output file (default: navigation_graph.json)")
        print("  --headless           Run in headless mode")
        print("  --all-domains        Allow external domains")
        print("  --keep-open          Keep browser open after exploration")
        print("  --pause N            Pause N seconds before closing browser")
        print("")
        print("Example:")
        print("  python -m agents.web_clicker_agent https://example.com --max-clicks 50")
        print("  python -m agents.web_clicker_agent https://example.com --pause 10")
        print("  python -m agents.web_clicker_agent https://example.com --keep-open")
        sys.exit(1)
    
    # Parse arguments
    url = sys.argv[1]
    max_clicks = 100
    max_depth = 5
    output = "navigation_graph.json"
    headless = False
    same_domain = True
    keep_open = False
    pause_before_close = 0.0
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--max-clicks':
            max_clicks = int(sys.argv[i+1])
            i += 2
        elif sys.argv[i] == '--max-depth':
            max_depth = int(sys.argv[i+1])
            i += 2
        elif sys.argv[i] == '--output':
            output = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == '--headless':
            headless = True
            i += 1
        elif sys.argv[i] == '--all-domains':
            same_domain = False
            i += 1
        elif sys.argv[i] == '--keep-open':
            keep_open = True
            i += 1
        elif sys.argv[i] == '--pause':
            pause_before_close = float(sys.argv[i+1])
            i += 2
        else:
            i += 1
    
    # Create and run agent
    agent = WebClickerAgent(
        base_url=url,
        max_clicks=max_clicks,
        max_depth=max_depth,
        same_domain_only=same_domain,
        headless=headless,
        keep_open=keep_open,
        pause_before_close=pause_before_close
    )
    
    await agent.explore()
    
    # Save results
    agent.save_graph(output)
    print(agent.get_summary())


if __name__ == "__main__":
    asyncio.run(main())

