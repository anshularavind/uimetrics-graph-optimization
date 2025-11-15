"""
Example usage of the GraphMetrics class for UI navigation analysis.

This script demonstrates how to:
1. Load graph data from different sources
2. Calculate all three key metrics
3. Interpret the results for UI optimization
"""

from graph_metrics import GraphMetrics


def example_1_simple_hub_and_spoke():
    """
    Example 1: A simple hub-and-spoke UI pattern
    
    Structure: Homepage -> [Page1, Page2, Page3]
    All pages link back to homepage
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Hub-and-Spoke Pattern (Classic Website)")
    print("="*70)
    
    edges = [
        {"source": "Homepage", "target": "Page1", "weight": 10},
        {"source": "Homepage", "target": "Page2", "weight": 8},
        {"source": "Homepage", "target": "Page3", "weight": 5},
        {"source": "Page1", "target": "Homepage", "weight": 10},
        {"source": "Page2", "target": "Homepage", "weight": 8},
        {"source": "Page3", "target": "Homepage", "weight": 5},
    ]
    
    gm = GraphMetrics(edges)
    print(gm.get_summary_report())
    
    print("\n💡 INSIGHT:")
    print("   Hub-and-spoke has good centrality for the homepage but poor")
    print("   clustering. Users must return to the homepage to navigate")
    print("   between pages, which is inefficient.")


def example_2_well_connected_module():
    """
    Example 2: Well-connected settings module
    
    Structure: All settings pages link to each other
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Well-Connected Module (Settings Section)")
    print("="*70)
    
    edges = [
        # Settings hub links to all
        {"source": "Settings", "target": "Profile", "weight": 20},
        {"source": "Settings", "target": "Billing", "weight": 15},
        {"source": "Settings", "target": "Security", "weight": 10},
        
        # Cross-links between settings pages (high clustering)
        {"source": "Profile", "target": "Billing", "weight": 5},
        {"source": "Profile", "target": "Security", "weight": 3},
        {"source": "Billing", "target": "Profile", "weight": 4},
        {"source": "Billing", "target": "Security", "weight": 2},
        {"source": "Security", "target": "Profile", "weight": 2},
        {"source": "Security", "target": "Billing", "weight": 1},
        
        # Back to settings
        {"source": "Profile", "target": "Settings", "weight": 15},
        {"source": "Billing", "target": "Settings", "weight": 10},
        {"source": "Security", "target": "Settings", "weight": 8},
    ]
    
    gm = GraphMetrics(edges)
    print(gm.get_summary_report())
    
    print("\n💡 INSIGHT:")
    print("   High clustering coefficient shows this is a well-organized")
    print("   module. Users can navigate between related settings without")
    print("   returning to the hub. This is GOOD design.")


def example_3_inefficient_deep_hierarchy():
    """
    Example 3: Deep hierarchy with no shortcuts
    
    Structure: Home -> A -> B -> C -> D (linear chain)
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Deep Hierarchy (Poor Navigation)")
    print("="*70)
    
    edges = [
        {"source": "Home", "target": "LevelA", "weight": 100},
        {"source": "LevelA", "target": "LevelB", "weight": 50},
        {"source": "LevelB", "target": "LevelC", "weight": 25},
        {"source": "LevelC", "target": "LevelD", "weight": 10},
        {"source": "LevelC", "target": "ImportantPage", "weight": 5},
        
        # Back buttons
        {"source": "LevelA", "target": "Home", "weight": 30},
        {"source": "LevelB", "target": "LevelA", "weight": 20},
        {"source": "LevelC", "target": "LevelB", "weight": 15},
        {"source": "LevelD", "target": "LevelC", "weight": 8},
        {"source": "ImportantPage", "target": "LevelC", "weight": 4},
    ]
    
    gm = GraphMetrics(edges)
    print(gm.get_summary_report())
    
    print("\n💡 INSIGHT:")
    print("   High average path length indicates inefficient navigation.")
    print("   Users need too many clicks to reach important pages.")
    print("   RECOMMENDATION: Add direct links or breadcrumb shortcuts.")


def example_4_optimal_dashboard():
    """
    Example 4: Optimized dashboard with shortcuts
    
    Structure: Dashboard with both hub access and cross-links
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Optimized Dashboard (Best Practice)")
    print("="*70)
    
    edges = [
        # Dashboard to main sections
        {"source": "Dashboard", "target": "Analytics", "weight": 30},
        {"source": "Dashboard", "target": "Reports", "weight": 25},
        {"source": "Dashboard", "target": "Settings", "weight": 15},
        {"source": "Dashboard", "target": "Help", "weight": 10},
        
        # Cross-links (shortcuts between related pages)
        {"source": "Analytics", "target": "Reports", "weight": 20},
        {"source": "Reports", "target": "Analytics", "weight": 18},
        {"source": "Analytics", "target": "Settings", "weight": 5},
        {"source": "Settings", "target": "Help", "weight": 3},
        
        # Back to dashboard
        {"source": "Analytics", "target": "Dashboard", "weight": 25},
        {"source": "Reports", "target": "Dashboard", "weight": 20},
        {"source": "Settings", "target": "Dashboard", "weight": 12},
        {"source": "Help", "target": "Dashboard", "weight": 8},
    ]
    
    gm = GraphMetrics(edges)
    print(gm.get_summary_report())
    
    print("\n💡 INSIGHT:")
    print("   This design balances centrality (dashboard access) with")
    print("   moderate clustering (cross-links). Users can navigate")
    print("   efficiently both through the hub and via shortcuts.")
    print("   This is EXCELLENT design.")


def example_5_programmatic_usage():
    """
    Example 5: Using the API programmatically
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Programmatic API Usage")
    print("="*70)
    
    edges = [
        {"source": "A", "target": "B", "weight": 10},
        {"source": "B", "target": "C", "weight": 5},
        {"source": "A", "target": "C", "weight": 3},
    ]
    
    gm = GraphMetrics(edges)
    
    # Get individual metrics
    print("\n📊 Individual Metric Access:")
    print(f"   Average Path Length: {gm.average_shortest_path_length():.3f}")
    print(f"   Avg Clustering Coef: {gm.average_clustering_coefficient():.3f}")
    
    print("\n   Closeness Centrality by Node:")
    centrality = gm.closeness_centrality()
    for node, score in sorted(centrality.items(), key=lambda x: x[1], reverse=True):
        print(f"     {node}: {score:.4f}")
    
    print("\n   Clustering Coefficient by Node:")
    clustering = gm.clustering_coefficient()
    for node, score in clustering.items():
        print(f"     {node}: {score:.4f}")
    
    # Export to JSON for further analysis
    gm.export_metrics_json("example_metrics.json")
    print("\n   ✓ Exported to example_metrics.json for further analysis")


if __name__ == "__main__":
    print("\n🎯 GRAPH METRICS FOR UI OPTIMIZATION - EXAMPLES\n")
    print("This script demonstrates how to use graph theory metrics")
    print("to analyze and optimize UI navigation patterns.\n")
    
    example_1_simple_hub_and_spoke()
    example_2_well_connected_module()
    example_3_inefficient_deep_hierarchy()
    example_4_optimal_dashboard()
    example_5_programmatic_usage()
    
    print("\n" + "="*70)
    print("✅ ALL EXAMPLES COMPLETED")
    print("="*70)
    print("\nNow try running with your own data:")
    print("  python3 graph_metrics.py your_data.json")
    print("")

