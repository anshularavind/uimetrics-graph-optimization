#!/usr/bin/env python3
"""
Example usage of the Web Clicker Agent
"""

import asyncio
from web_clicker_agent import WebClickerAgent
import sys
import os

# Add parent directory to path to import graph_metrics
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from graph_metrics import GraphMetrics


async def example_1_basic_exploration():
    """
    Example 1: Basic website exploration
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Website Exploration")
    print("="*70)
    
    agent = WebClickerAgent(
        base_url="https://example.com",
        max_clicks=20,
        max_depth=3,
        headless=False,  # Watch it work!
        wait_time=1.0
    )
    
    await agent.explore()
    
    # Save and analyze
    agent.save_graph("example1_graph.json")
    print(agent.get_summary())


async def example_2_headless_mode():
    """
    Example 2: Fast exploration in headless mode
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Headless Mode (Background)")
    print("="*70)
    
    agent = WebClickerAgent(
        base_url="https://example.com",
        max_clicks=30,
        max_depth=4,
        headless=True,  # Run in background
        wait_time=0.5   # Faster
    )
    
    await agent.explore()
    
    # Get data and analyze
    graph_data = agent.get_graph_data()
    
    print(f"\n📊 Analyzing {len(graph_data)} navigation edges...")
    gm = GraphMetrics(graph_data)
    print(gm.get_summary_report())


async def example_3_with_analysis():
    """
    Example 3: Full workflow - explore and analyze
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Full Workflow (Explore + Analyze)")
    print("="*70)
    
    # Step 1: Explore website
    print("\n🤖 Step 1: Exploring website...")
    agent = WebClickerAgent(
        base_url="https://news.ycombinator.com",
        max_clicks=50,
        max_depth=3,
        headless=True,
        same_domain_only=True
    )
    
    await agent.explore()
    
    # Step 2: Save data
    print("\n💾 Step 2: Saving navigation data...")
    agent.save_graph("hacker_news_graph.json")
    
    # Step 3: Analyze with GraphMetrics
    print("\n📊 Step 3: Analyzing navigation patterns...")
    graph_data = agent.get_graph_data()
    gm = GraphMetrics(graph_data)
    
    # Get metrics
    avg_path = gm.average_shortest_path_length()
    clustering = gm.average_clustering_coefficient()
    centrality = gm.closeness_centrality()
    
    print(f"\n✨ KEY INSIGHTS:")
    print(f"   Average Path Length: {avg_path:.2f} clicks")
    print(f"   Clustering Coefficient: {clustering:.2%}")
    print(f"   Most Central Page: {max(centrality, key=centrality.get)}")
    print(f"   Centrality Score: {max(centrality.values()):.3f}")
    
    # Full report
    print("\n" + gm.get_summary_report())


async def example_4_compare_sites():
    """
    Example 4: Compare two websites
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Compare Two Websites")
    print("="*70)
    
    sites = [
        ("https://example.com", "site_a.json"),
        ("https://example.org", "site_b.json"),
    ]
    
    results = []
    
    for url, output_file in sites:
        print(f"\n🔍 Exploring {url}...")
        
        agent = WebClickerAgent(
            base_url=url,
            max_clicks=30,
            max_depth=3,
            headless=True
        )
        
        await agent.explore()
        agent.save_graph(output_file)
        
        # Analyze
        graph_data = agent.get_graph_data()
        gm = GraphMetrics(graph_data)
        
        results.append({
            'url': url,
            'path_length': gm.average_shortest_path_length(),
            'clustering': gm.average_clustering_coefficient(),
            'nodes': len(gm.nodes),
            'edges': len(gm.weights)
        })
    
    # Compare
    print("\n" + "="*70)
    print("📊 COMPARISON")
    print("="*70)
    print(f"\n{'Metric':<25} {'Site A':<15} {'Site B':<15}")
    print("-"*55)
    print(f"{'URL':<25} {results[0]['url']:<15} {results[1]['url']:<15}")
    print(f"{'Nodes':<25} {results[0]['nodes']:<15} {results[1]['nodes']:<15}")
    print(f"{'Edges':<25} {results[0]['edges']:<15} {results[1]['edges']:<15}")
    print(f"{'Avg Path Length':<25} {results[0]['path_length']:<15.2f} {results[1]['path_length']:<15.2f}")
    print(f"{'Clustering':<25} {results[0]['clustering']:<15.2%} {results[1]['clustering']:<15.2%}")


async def main():
    """Run all examples"""
    import sys
    
    if len(sys.argv) > 1:
        example = sys.argv[1]
        if example == "1":
            await example_1_basic_exploration()
        elif example == "2":
            await example_2_headless_mode()
        elif example == "3":
            await example_3_with_analysis()
        elif example == "4":
            await example_4_compare_sites()
        else:
            print("Unknown example. Use: 1, 2, 3, or 4")
    else:
        print("\n🎯 Web Clicker Agent Examples\n")
        print("Run specific examples:")
        print("  python example_usage.py 1  - Basic exploration")
        print("  python example_usage.py 2  - Headless mode")
        print("  python example_usage.py 3  - Full workflow with analysis")
        print("  python example_usage.py 4  - Compare two sites")
        print("\nOr run directly:")
        print("  python -m agents.web_clicker_agent https://example.com")


if __name__ == "__main__":
    asyncio.run(main())

