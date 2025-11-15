# UI Metrics Graph Optimization

A Python tool for analyzing UI navigation patterns using graph theory metrics. This tool helps you identify inefficiencies in your user interface and optimize navigation paths.

## 📊 What It Does

This tool calculates three key graph metrics to analyze your UI:

### 1. **Average Shortest Path Length** (`L`)

The most direct measure of your UI's navigational efficiency.

**Formula:**

$$L = \frac{1}{N(N-1)} \sum_{u \neq v} d(u, v)$$

- **What it measures:** The average number of clicks it takes to get from any page to any other page
- **What you want:** A low average path length (< 3 clicks is excellent)
- **Example:** If users need 4 clicks to reach an important page, this metric will catch it

### 2. **Closeness Centrality** (`C(u)`)

Identifies which pages are the most "central" or easily accessible.

**Formula:**

$$C(u) = \frac{N-1}{\sum_{v \neq u} d(u, v)}$$

- **What it measures:** How quickly a single page can reach all other pages
- **What you want:** High closeness centrality for your most important pages (Dashboard, Homepage, Checkout)
- **Example:** A homepage that links to everything in one click has maximum centrality (1.0)

### 3. **Clustering Coefficient** (`C_u`)

Measures modularity and how well-organized your UI sections are.

**Formula:**

$$C_u = \frac{2T_u}{k_u(k_u - 1)}$$

Where:
- `T_u` = number of triangles (connections between neighbors)
- `k_u` = number of neighbors (degree)

- **What it measures:** The degree to which a node's neighbors are also connected to each other
- **What you want:** High clustering within modules (e.g., Settings pages), moderate clustering overall
- **Example:** If "Profile," "Billing," and "Security" all link to each other, they have high clustering (good!)

## 🚀 Quick Start

### Installation

No external dependencies required! Just Python 3.6+:

```bash
git clone <your-repo-url>
cd uimetrics-graph-optimization
```

### Basic Usage

1. **Prepare your data** - Create a JSON file with your graph edges:

```json
[
  {"source": "Homepage", "target": "Dashboard", "weight": 100},
  {"source": "Dashboard", "target": "Settings", "weight": 50},
  {"source": "Settings", "target": "Profile", "weight": 25}
]
```

2. **Run the analysis:**

```bash
python3 graph_metrics.py your_edges.json
```

3. **View results:**

The tool will output:
- Average shortest path length
- Top 10 most central pages
- Average clustering coefficient
- Most/least clustered nodes
- A JSON export with detailed metrics

### Example Output

```
======================================================================
UI NAVIGATION GRAPH METRICS REPORT
======================================================================

📊 GRAPH STRUCTURE
  Nodes (pages/elements): 5
  Edges (navigation paths): 12
  Total navigation events: 191

🛤️  AVERAGE SHORTEST PATH LENGTH
  L = 1.400 clicks
  Interpretation: On average, users need 1.4 clicks
                  to navigate between any two pages.
  ✓ EXCELLENT - Very efficient navigation

🎯 CLOSENESS CENTRALITY (Top 10 Most Central Pages)
   1. Dashboard
      Centrality: 1.0000
   2. Analytics
      Centrality: 0.8000
   ...

🔗 CLUSTERING COEFFICIENT
  Average: 0.6333
  Interpretation: 63.3% of possible neighbor
                  connections are realized.
  ✓ HIGH - Strong modularity, well-organized sections
```

## 📖 Usage Guide

### Command Line Interface

```bash
# Analyze a graph from JSON file
python3 graph_metrics.py edges.json

# The tool will automatically:
# 1. Load your graph data
# 2. Calculate all three metrics
# 3. Generate a comprehensive report
# 4. Export detailed metrics to edges_metrics.json
```

### Programmatic API

```python
from graph_metrics import GraphMetrics

# Create graph from edge list
edges = [
    {"source": "A", "target": "B", "weight": 10},
    {"source": "B", "target": "C", "weight": 5},
    {"source": "A", "target": "C", "weight": 3},
]

gm = GraphMetrics(edges)

# Get individual metrics
avg_path_length = gm.average_shortest_path_length()
closeness = gm.closeness_centrality()
clustering = gm.clustering_coefficient()
avg_clustering = gm.average_clustering_coefficient()

# Generate full report
print(gm.get_summary_report())

# Export to JSON
gm.export_metrics_json("output.json")
```

### Loading from Files

```python
from graph_metrics import GraphMetrics

# Method 1: JSON array file
gm = GraphMetrics()
gm.load_from_json_file("edges.json")

# Method 2: JSON Lines file (one edge per line)
gm = GraphMetrics()
gm.load_from_jsonl_file("edges.jsonl")

# Method 3: Direct data
gm = GraphMetrics(edge_list)
```

## 🎯 Examples

Run the included examples to see different UI patterns analyzed:

```bash
python3 example_usage.py
```

This demonstrates:
1. **Hub-and-Spoke Pattern** - Classic website with central homepage
2. **Well-Connected Module** - Settings section with cross-links
3. **Deep Hierarchy** - Inefficient linear navigation
4. **Optimized Dashboard** - Best practice design
5. **Programmatic Usage** - Using the API in your code

## 📥 Getting Your Data from PostHog

If you're using PostHog for analytics, you can extract navigation graphs using HogQL:

```bash
curl -X POST https://us.i.posthog.com/api/projects/YOUR_PROJECT/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d @query.json | jq '.results[] | {source: .[0], target: .[1], weight: .[2]}' > edges.json
```

See `query.json` for the HogQL query that extracts click navigation patterns.

## 🔧 Input Format

Your graph data should be a JSON array of edge objects:

```json
[
  {
    "source": "node_name_1",
    "target": "node_name_2",
    "weight": 42
  }
]
```

Or JSON Lines format (one object per line):

```json
{"source": "A", "target": "B", "weight": 10}
{"source": "B", "target": "C", "weight": 5}
```

**Fields:**
- `source` (string): The starting node/page
- `target` (string): The destination node/page  
- `weight` (number): Navigation frequency (click count)

## 📊 Interpreting Results

### Average Shortest Path Length

- **< 2.5 clicks**: ✓ EXCELLENT - Very efficient navigation
- **2.5-4.0 clicks**: ✓ GOOD - Reasonable efficiency
- **4.0-6.0 clicks**: ⚠️ FAIR - Consider shortening paths
- **> 6.0 clicks**: ❌ POOR - Significant optimization needed

### Closeness Centrality

- **High scores (> 0.7)**: Pages that are easy to reach from anywhere
- **Low scores (< 0.3)**: Buried pages that are hard to access
- **Action:** Ensure important pages have high centrality

### Clustering Coefficient

- **> 0.6**: ✓ HIGH - Strong modularity, well-organized
- **0.3-0.6**: ✓ MODERATE - Decent local connectivity
- **< 0.3**: ⚠️ LOW - Pages could be better interconnected
- **Within modules:** Aim for high clustering
- **Between modules:** Moderate clustering is fine

## 🛠️ Advanced Usage

### Analyzing Disconnected Graphs

The tool handles disconnected graphs gracefully:
- Reports unreachable node pairs
- Uses normalized centrality measures
- Excludes infinite distances from calculations

### Working with Large Graphs

The tool uses BFS for shortest path computation, which is efficient for sparse graphs typical in UI navigation:
- Time complexity: O(N² × (V + E))
- Space complexity: O(N²)
- Handles thousands of nodes efficiently

### Export Format

The JSON export includes:

```json
{
  "graph_info": {
    "num_nodes": 5,
    "num_edges": 12,
    "total_weight": 191
  },
  "average_shortest_path_length": 1.4,
  "average_clustering_coefficient": 0.6333,
  "closeness_centrality": {
    "Dashboard": 1.0,
    "Analytics": 0.8,
    ...
  },
  "clustering_coefficient": {
    "Dashboard": 0.5,
    "Analytics": 0.667,
    ...
  }
}
```

## 🎓 Theory & Background

These metrics come from graph theory and network analysis:

- **Average Shortest Path Length**: Measures network diameter and efficiency (Watts & Strogatz, 1998)
- **Closeness Centrality**: Node importance metric from social network analysis (Freeman, 1978)
- **Clustering Coefficient**: Local cohesion measure (Watts & Strogatz, 1998)

Applied to UI navigation, they reveal:
- Navigation bottlenecks
- Hard-to-reach pages
- Poorly organized modules
- Opportunities for shortcuts

## 🤝 Contributing

Contributions welcome! Some ideas:
- Add weighted shortest paths (Dijkstra's algorithm)
- Implement betweenness centrality
- Add visualization with networkx/matplotlib
- Create CI/CD pipeline
- Add unit tests

## 📝 License

MIT License - feel free to use in your projects!

## 🙋 Support

For questions or issues:
1. Check the examples in `example_usage.py`
2. Review this README
3. Open an issue on GitHub

---

**Made with ❤️ for better UI/UX**
