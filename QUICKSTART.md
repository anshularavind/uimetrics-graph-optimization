# 🚀 Quick Start Guide

Get started with UI Metrics Graph Optimization in 3 steps!

## Installation

```bash
# 1. Install dependencies
pip install playwright

# 2. Install browser
playwright install chromium
```

That's it! No other dependencies needed.

---

## Usage: Analyze Your Website

### Step 1: Collect Navigation Data

**Option A: Use the AI Agent (Automated)**

Let the agent autonomously explore your website:

```bash
python -m agents.web_clicker_agent https://yoursite.com --max-clicks 100
```

This will:
- Open a browser and navigate your site
- Click through links intelligently
- Generate `navigation_graph.json`

**Option B: Use Your Analytics Data**

If you have PostHog or similar analytics, export your click data:

```bash
curl -X POST https://us.i.posthog.com/api/projects/YOUR_PROJECT/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d @query.json | jq '.results[] | {source: .[0], target: .[1], weight: .[2]}' > navigation_graph.json
```

### Step 2: Analyze Navigation Patterns

```bash
python3 graph_metrics.py navigation_graph.json
```

You'll get a comprehensive report with:
- ✅ Average Shortest Path Length (navigation efficiency)
- ✅ Closeness Centrality (most accessible pages)
- ✅ Clustering Coefficient (modularity & organization)

### Step 3: Optimize Your UI

Based on the metrics:
- **High path length?** Add shortcuts between related pages
- **Low centrality for important pages?** Make them more accessible
- **Low clustering?** Better interconnect related sections

---

## Quick Examples

### Explore a Site (Visible Browser)

```bash
python -m agents.web_clicker_agent https://example.com --max-clicks 50
```

### Fast Background Scan

```bash
python -m agents.web_clicker_agent https://example.com --headless --max-clicks 100 --output my_site.json
python3 graph_metrics.py my_site.json
```

### Compare Before/After a Redesign

```bash
# Before
python -m agents.web_clicker_agent https://staging.yoursite.com --output before.json
python3 graph_metrics.py before.json > before_metrics.txt

# After changes
python -m agents.web_clicker_agent https://staging.yoursite.com --output after.json
python3 graph_metrics.py after.json > after_metrics.txt

# Compare
diff before_metrics.txt after_metrics.txt
```

### Analyze Sample Data

```bash
# Good website example
python3 graph_metrics.py good_website.json

# Bad website example
python3 graph_metrics.py bad_website.json

# Compare both
python3 compare_sites.py
```

---

## Programmatic Usage

### Explore and Analyze in One Script

```python
import asyncio
from agents import WebClickerAgent
from graph_metrics import GraphMetrics

async def analyze_my_site():
    # 1. Collect data
    agent = WebClickerAgent(
        base_url="https://yoursite.com",
        max_clicks=100,
        headless=True
    )
    await agent.explore()
    
    # 2. Analyze
    graph_data = agent.get_graph_data()
    gm = GraphMetrics(graph_data)
    
    # 3. Get insights
    print(gm.get_summary_report())
    
    # 4. Export
    gm.export_metrics_json("metrics.json")

asyncio.run(analyze_my_site())
```

### Analyze Existing Data

```python
from graph_metrics import GraphMetrics

# Load from file
gm = GraphMetrics()
gm.load_from_json_file("navigation_graph.json")

# Or from data
edges = [
    {"source": "Home", "target": "Products", "weight": 100},
    {"source": "Products", "target": "Cart", "weight": 50}
]
gm = GraphMetrics(edges)

# Get metrics
avg_path = gm.average_shortest_path_length()
clustering = gm.average_clustering_coefficient()
centrality = gm.closeness_centrality()

print(f"Navigation efficiency: {avg_path:.2f} clicks")
print(f"Modularity: {clustering:.1%}")
```

---

## Understanding the Metrics

### 📏 Average Shortest Path Length

**What it means:** Average clicks to navigate between any two pages

**Ratings:**
- < 2.5 clicks: ✅ EXCELLENT
- 2.5-4.0 clicks: ✅ GOOD
- 4.0-6.0 clicks: ⚠️ FAIR
- \> 6.0 clicks: ❌ POOR

**How to improve:** Add shortcuts, flatten hierarchy, promote important pages

### 🎯 Closeness Centrality

**What it means:** How easily accessible each page is

**What you want:** High scores (>0.7) for important pages like:
- Homepage
- Product pages
- Checkout/Cart
- Dashboard

**How to improve:** Add more links to/from critical pages

### 🔗 Clustering Coefficient

**What it means:** How interconnected related pages are

**Ratings:**
- \> 0.6: ✅ HIGH - Well-organized modules
- 0.3-0.6: ✅ MODERATE - Decent structure
- < 0.3: ⚠️ LOW - Poor interconnection

**How to improve:** Add cross-links between related pages in each section

---

## Common Issues

**"Module not found: playwright"**
```bash
pip install playwright
playwright install chromium
```

**Agent doesn't click anything**
- Check URL is accessible
- Try `headless=False` to watch it work
- Increase `wait_time` parameter

**Metrics seem wrong**
- Ensure your graph data has the right format:
  ```json
  [{"source": "A", "target": "B", "weight": 5}]
  ```

**Browser won't open**
```bash
# Reinstall browser
playwright install --force chromium
```

---

## Next Steps

1. ✅ **Collect data** from your site (agent or analytics)
2. ✅ **Analyze metrics** with GraphMetrics
3. ✅ **Identify issues** (long paths, buried pages, poor clustering)
4. ✅ **Make changes** (add shortcuts, flatten hierarchy)
5. ✅ **Re-measure** to confirm improvements

**For more details:**
- See `README.md` for full documentation
- See `agents/README.md` for agent documentation
- See `COMPARISON.md` for good vs bad examples
- Run `python3 example_usage.py` for code examples

---

**Ready to optimize? Start here:**

```bash
python -m agents.web_clicker_agent https://yoursite.com --max-clicks 50
python3 graph_metrics.py navigation_graph.json
```

🎉 **Happy optimizing!**

