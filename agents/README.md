# Web Clicker AI Agent

An autonomous agent that takes control of a browser, navigates websites by clicking links, and generates navigation graphs for UI metrics analysis.

## 🚀 Quick Start

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install playwright
   ```

2. **Install browser:**
   ```bash
   playwright install chromium
   ```

### Basic Usage

```bash
# From the project root
python -m agents.web_clicker_agent https://example.com
```

This will:
- Open a browser (visible by default)
- Start at the given URL
- Autonomously click through links
- Generate `navigation_graph.json` with the navigation data

### Analyze Results

```bash
# Run the graph metrics analysis on the collected data
python graph_metrics.py navigation_graph.json
```

## 🎯 Features

- ✅ **Autonomous Navigation** - Agent clicks through website intelligently
- ✅ **Smart Link Detection** - Only clicks visible, valid links
- ✅ **Same-Domain Filtering** - Stays within the target site (configurable)
- ✅ **Depth Control** - Configurable exploration depth
- ✅ **Click Limiting** - Set maximum clicks to control runtime
- ✅ **Graph Generation** - Outputs data compatible with GraphMetrics
- ✅ **Visible or Headless** - Watch it work or run in background
- ✅ **Back Navigation** - Returns to previous page after each click

## 📖 Command Line Options

```bash
python -m agents.web_clicker_agent <url> [options]

Options:
  --max-clicks N       Maximum number of clicks (default: 100)
  --max-depth N        Maximum navigation depth (default: 5)
  --output FILE        Output JSON file (default: navigation_graph.json)
  --headless           Run browser in headless mode (no UI)
  --all-domains        Allow clicking external links (default: same domain only)
```

### Examples

**Explore a site with 50 clicks:**
```bash
python -m agents.web_clicker_agent https://example.com --max-clicks 50
```

**Run in headless mode (background):**
```bash
python -m agents.web_clicker_agent https://example.com --headless --max-clicks 30
```

**Deep exploration with custom output:**
```bash
python -m agents.web_clicker_agent https://example.com \
  --max-clicks 200 \
  --max-depth 10 \
  --output my_site_graph.json
```

**Allow external domains:**
```bash
python -m agents.web_clicker_agent https://example.com --all-domains
```

## 🐍 Programmatic Usage

```python
import asyncio
from agents import WebClickerAgent

async def explore_site():
    # Create agent
    agent = WebClickerAgent(
        base_url="https://example.com",
        max_clicks=100,
        max_depth=5,
        same_domain_only=True,
        headless=False,
        wait_time=1.0  # seconds between clicks
    )
    
    # Run exploration
    await agent.explore()
    
    # Save results
    agent.save_graph("output.json")
    
    # Get data programmatically
    graph_data = agent.get_graph_data()
    
    # Print summary
    print(agent.get_summary())

# Run it
asyncio.run(explore_site())
```

## 🔄 Integration with GraphMetrics

The agent outputs data in the exact format expected by GraphMetrics:

```python
from agents import WebClickerAgent
from graph_metrics import GraphMetrics
import asyncio

async def analyze_website():
    # 1. Collect navigation data
    agent = WebClickerAgent(
        base_url="https://yoursite.com",
        max_clicks=100,
        headless=True
    )
    await agent.explore()
    
    # 2. Get graph data
    graph_data = agent.get_graph_data()
    
    # 3. Analyze with GraphMetrics
    gm = GraphMetrics(graph_data)
    print(gm.get_summary_report())
    
    # 4. Export metrics
    gm.export_metrics_json("site_metrics.json")

asyncio.run(analyze_website())
```

## 🛠️ How It Works

1. **Initialization**
   - Launches Playwright browser (Chromium)
   - Navigates to base URL
   - Sets up tracking structures

2. **Exploration**
   - Extracts all visible links from current page
   - Filters valid links (same domain, no files, etc.)
   - Clicks each link and records navigation
   - Returns to previous page via back button
   - Adds new pages to exploration queue

3. **Graph Building**
   - Records each navigation as an edge: `(source_page, target_page)`
   - Weights represent click frequency
   - Generates readable page labels from titles/URLs

4. **Output**
   - Saves JSON file with format: `[{"source": "A", "target": "B", "weight": 5}, ...]`
   - Compatible with GraphMetrics tool

## 🎯 Use Cases

### 1. Analyze Your Own Website
```bash
python -m agents.web_clicker_agent https://yoursite.com --max-clicks 200
python graph_metrics.py navigation_graph.json
```

### 2. Compare Competitors
```bash
# Your site
python -m agents.web_clicker_agent https://yoursite.com --output your_site.json
python graph_metrics.py your_site.json

# Competitor site
python -m agents.web_clicker_agent https://competitor.com --output competitor.json
python graph_metrics.py competitor.json
```

### 3. Test Navigation Changes
```bash
# Before redesign
python -m agents.web_clicker_agent https://staging.yoursite.com --output before.json

# After redesign  
python -m agents.web_clicker_agent https://staging.yoursite.com --output after.json

# Compare metrics
python graph_metrics.py before.json
python graph_metrics.py after.json
```

### 4. Monitor Over Time
```bash
# Run weekly and compare path lengths
python -m agents.web_clicker_agent https://yoursite.com --output week_$(date +%Y%m%d).json
python graph_metrics.py week_$(date +%Y%m%d).json
```

## ⚙️ Configuration

### Agent Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `base_url` | (required) | Starting URL to explore |
| `max_clicks` | 100 | Stop after this many clicks |
| `max_depth` | 5 | Maximum depth from start page |
| `same_domain_only` | True | Only click same-domain links |
| `headless` | False | Run browser without UI |
| `wait_time` | 1.0 | Seconds to wait between clicks |

### Link Filtering

The agent automatically skips:
- External domains (if `same_domain_only=True`)
- Non-HTTP protocols (javascript:, mailto:, etc.)
- File downloads (.pdf, .zip, .exe, etc.)
- Media files (.jpg, .png, .mp4, etc.)
- Hidden or invisible links
- Already-visited URLs (but records repeat clicks)

## 🐛 Troubleshooting

**Browser doesn't open:**
```bash
# Make sure Playwright is installed
playwright install chromium
```

**"Module not found" error:**
```bash
# Install from project root
pip install playwright
```

**Agent gets stuck:**
- Reduce `max_clicks` and `max_depth`
- Increase `wait_time` for slow-loading sites
- Use `--headless` to see if UI rendering is causing issues

**Too many external links clicked:**
- Use `--same-domain` flag (default)
- Check that your site doesn't redirect to external domain

**Output file empty:**
- Check that website is accessible
- Try with `headless=False` to watch what happens
- Increase `wait_time` for slow sites

## 🔒 Ethical Considerations

**Be Respectful:**
- Don't overwhelm servers with rapid requests
- Respect robots.txt
- Don't use on sites that prohibit automation
- Use reasonable `wait_time` (1+ seconds)
- Limit `max_clicks` for production sites

**Legal:**
- Only use on sites you own or have permission to test
- Don't scrape copyrighted content
- Don't bypass authentication without authorization

## 🚧 Limitations

- **JavaScript-heavy sites:** May miss dynamically loaded links
- **Authentication:** Doesn't handle login flows
- **Single-page apps (SPAs):** May have issues with client-side routing
- **Infinite scrolling:** Won't scroll to load more content
- **CAPTCHAs:** Cannot solve captchas
- **Rate limiting:** May trigger if too aggressive

## 🔮 Future Enhancements

Potential improvements:
- [ ] Login flow support
- [ ] Scroll and infinite loading handling
- [ ] Form filling and submission
- [ ] Screenshot capture at each page
- [ ] A/B path testing
- [ ] Heatmap generation
- [ ] Performance metrics (load times)
- [ ] Mobile viewport simulation
- [ ] Multi-browser support (Firefox, Safari)

## 📝 License

MIT License - Use freely in your projects!

---

**Ready to explore?**

```bash
python -m agents.web_clicker_agent https://example.com --max-clicks 50
```

