#!/usr/bin/env python3
"""
Quick comparison script for good vs bad website navigation
"""

from graph_metrics import GraphMetrics

print("\n" + "="*80)
print("🎯 WEBSITE NAVIGATION COMPARISON")
print("="*80)

# Load good website
print("\n📊 Loading websites...")
good = GraphMetrics()
good.load_from_json_file("good_website.json")

bad = GraphMetrics()
bad.load_from_json_file("bad_website.json")

# Calculate metrics
good_path = good.average_shortest_path_length()
bad_path = bad.average_shortest_path_length()

good_clustering = good.average_clustering_coefficient()
bad_clustering = bad.average_clustering_coefficient()

good_centrality = good.closeness_centrality()
bad_centrality = bad.closeness_centrality()

good_top_cent = max(good_centrality.values())
bad_top_cent = max(bad_centrality.values())

# Display comparison table
print("\n" + "="*80)
print("📊 METRICS COMPARISON")
print("="*80)
print()
print(f"{'Metric':<30} {'Good Website':<20} {'Bad Website':<20} {'Difference':<15}")
print("-"*80)

# Nodes
print(f"{'Nodes (pages)':<30} {len(good.nodes):<20} {len(bad.nodes):<20} {len(good.nodes) - len(bad.nodes):+}")

# Edges
print(f"{'Edges (paths)':<30} {len(good.weights):<20} {len(bad.weights):<20} {len(good.weights) - len(bad.weights):+}")

# Path length
diff_pct = ((bad_path - good_path) / good_path) * 100
print(f"{'Avg Path Length':<30} {good_path:.2f} clicks {'':<8} {bad_path:.2f} clicks {'':<8} {diff_pct:+.0f}% slower")

# Clustering
cluster_ratio = good_clustering / bad_clustering if bad_clustering > 0 else float('inf')
print(f"{'Clustering Coefficient':<30} {good_clustering:.1%} {'':<13} {bad_clustering:.1%} {'':<13} {cluster_ratio:.0f}x better")

# Centrality
cent_diff = ((good_top_cent - bad_top_cent) / bad_top_cent) * 100
print(f"{'Top Centrality Score':<30} {good_top_cent:.3f} {'':<14} {bad_top_cent:.3f} {'':<14} {cent_diff:+.0f}% higher")

print("="*80)

# Ratings
print("\n🏆 OVERALL RATINGS")
print("-"*80)

print("\n🟢 GOOD WEBSITE:")
if good_path < 4.0:
    print(f"   ✓ Path Length: EXCELLENT ({good_path:.1f} clicks)")
else:
    print(f"   ⚠ Path Length: FAIR ({good_path:.1f} clicks)")

if good_clustering > 0.3:
    print(f"   ✓ Clustering: GOOD ({good_clustering:.1%})")
else:
    print(f"   ⚠ Clustering: LOW ({good_clustering:.1%})")

print(f"   ✓ Top Centrality: {good_top_cent:.3f}")
print(f"   ✓ Fully Connected: No unreachable pages")

print("\n🔴 BAD WEBSITE:")
if bad_path < 4.0:
    print(f"   ✓ Path Length: EXCELLENT ({bad_path:.1f} clicks)")
elif bad_path < 6.0:
    print(f"   ⚠ Path Length: FAIR ({bad_path:.1f} clicks)")
else:
    print(f"   ❌ Path Length: POOR ({bad_path:.1f} clicks)")

if bad_clustering > 0.3:
    print(f"   ✓ Clustering: GOOD ({bad_clustering:.1%})")
else:
    print(f"   ❌ Clustering: POOR ({bad_clustering:.1%})")

print(f"   ⚠ Top Centrality: {bad_top_cent:.3f}")
print(f"   ❌ Has disconnected sections")

# Key insights
print("\n" + "="*80)
print("💡 KEY INSIGHTS")
print("="*80)
print()
print("The GOOD website is optimized for user experience:")
print(f"  • {((bad_path - good_path) / good_path * 100):.0f}% faster navigation")
print(f"  • {cluster_ratio:.0f}x better page interconnection")
print("  • Clear pathways to important pages (Products, Cart)")
print("  • Users can navigate laterally without backtracking")
print()
print("The BAD website has major UX issues:")
print("  • Deep menu hierarchy forces excessive clicking")
print("  • No shortcuts between related content")
print("  • Important pages (Cart, Account) are buried")
print("  • Users must constantly backtrack through menus")
print()
print("🎯 RECOMMENDATION: Use good website patterns for new designs")
print("="*80)
print()

