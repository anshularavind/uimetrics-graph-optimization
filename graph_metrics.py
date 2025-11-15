"""
Graph Metrics Calculator for UI Navigation Analysis

This module provides a GraphMetrics class that calculates:
1. Average Shortest Path Length - measures overall navigational efficiency
2. Closeness Centrality - identifies most accessible pages
3. Clustering Coefficient - measures modularity and interconnectedness
"""

import json
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Set
import sys


class GraphMetrics:
    """
    A class to analyze UI navigation graphs using graph theory metrics.
    
    The graph is represented as a directed, weighted graph where:
    - Nodes represent UI elements/pages
    - Edges represent navigation paths (clicks)
    - Weights represent frequency of navigation
    """
    
    def __init__(self, graph_data: List[Dict[str, any]] = None):
        """
        Initialize the GraphMetrics calculator.
        
        Args:
            graph_data: List of dicts with 'source', 'target', 'weight' keys
        """
        self.nodes: Set[str] = set()
        self.edges: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.weights: Dict[Tuple[str, str], int] = {}
        
        if graph_data:
            self.load_from_data(graph_data)
    
    def load_from_data(self, graph_data: List[Dict[str, any]]):
        """
        Load graph from a list of edge dictionaries.
        
        Args:
            graph_data: List of dicts with 'source', 'target', 'weight' keys
        """
        for edge in graph_data:
            source = edge['source']
            target = edge['target']
            weight = edge['weight']
            
            self.nodes.add(source)
            self.nodes.add(target)
            self.edges[source][target] = weight
            self.weights[(source, target)] = weight
        
        print(f"✓ Loaded graph with {len(self.nodes)} nodes and {len(self.weights)} edges")
    
    def load_from_json_file(self, filepath: str):
        """
        Load graph data from a JSON file containing an array of edge objects.
        
        Args:
            filepath: Path to JSON file with format:
                     [{"source": "A", "target": "B", "weight": 5}, ...]
        """
        with open(filepath, 'r') as f:
            graph_data = json.load(f)
        
        self.load_from_data(graph_data)
    
    def load_from_jsonl_file(self, filepath: str):
        """
        Load graph data from a JSON Lines file (one edge object per line).
        
        Args:
            filepath: Path to JSONL file where each line is:
                     {"source": "A", "target": "B", "weight": 5}
        """
        graph_data = []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    graph_data.append(json.loads(line))
        
        self.load_from_data(graph_data)
    
    def _compute_shortest_paths_bfs(self) -> Dict[str, Dict[str, float]]:
        """
        Compute shortest paths between all pairs of nodes using BFS.
        
        For unweighted graphs or when we only care about hop count (not weight),
        BFS gives us the shortest path in terms of number of edges.
        
        Returns:
            Dict mapping source -> target -> shortest distance (number of hops)
            Uses float('inf') for unreachable pairs
        """
        distances = {}
        
        for start_node in self.nodes:
            distances[start_node] = {}
            visited = {start_node: 0}
            queue = deque([start_node])
            
            while queue:
                current = queue.popleft()
                current_dist = visited[current]
                
                # Explore neighbors
                if current in self.edges:
                    for neighbor in self.edges[current]:
                        if neighbor not in visited:
                            visited[neighbor] = current_dist + 1
                            queue.append(neighbor)
            
            # Store distances for all nodes
            for node in self.nodes:
                distances[start_node][node] = visited.get(node, float('inf'))
        
        return distances
    
    def average_shortest_path_length(self) -> float:
        """
        Calculate the average shortest path length L.
        
        Formula: L = (1 / (N(N-1))) * Σ d(u,v) for all u ≠ v
        
        This measures the average number of clicks needed to navigate
        between any two pages in the UI.
        
        Returns:
            Average shortest path length (lower is better)
            Returns None if graph is disconnected or has < 2 nodes
        """
        if len(self.nodes) < 2:
            return None
        
        distances = self._compute_shortest_paths_bfs()
        
        total_distance = 0
        reachable_pairs = 0
        unreachable_pairs = 0
        
        for source in self.nodes:
            for target in self.nodes:
                if source != target:
                    dist = distances[source][target]
                    if dist != float('inf'):
                        total_distance += dist
                        reachable_pairs += 1
                    else:
                        unreachable_pairs += 1
        
        if reachable_pairs == 0:
            return None  # Completely disconnected graph
        
        N = len(self.nodes)
        avg_path_length = total_distance / (N * (N - 1))
        
        if unreachable_pairs > 0:
            print(f"⚠️  Warning: {unreachable_pairs} unreachable node pairs in graph")
        
        return avg_path_length
    
    def closeness_centrality(self) -> Dict[str, float]:
        """
        Calculate closeness centrality for each node.
        
        Formula: C(u) = (N-1) / Σ d(u,v) for all v ≠ u
        
        Measures how quickly a page can reach all other pages.
        High scores indicate central, easily accessible pages.
        
        Returns:
            Dict mapping node -> closeness centrality score
            Returns 0.0 for nodes that cannot reach other nodes
        """
        if len(self.nodes) < 2:
            return {node: 0.0 for node in self.nodes}
        
        distances = self._compute_shortest_paths_bfs()
        centrality = {}
        
        N = len(self.nodes)
        
        for node in self.nodes:
            # Sum distances from this node to all others
            total_distance = 0
            reachable_count = 0
            
            for target in self.nodes:
                if target != node:
                    dist = distances[node][target]
                    if dist != float('inf'):
                        total_distance += dist
                        reachable_count += 1
            
            # Closeness centrality (normalized)
            if total_distance > 0 and reachable_count > 0:
                # Normalize by the fraction of reachable nodes
                centrality[node] = (reachable_count / (N - 1)) * (reachable_count / total_distance)
            else:
                centrality[node] = 0.0
        
        return centrality
    
    def clustering_coefficient(self) -> Dict[str, float]:
        """
        Calculate local clustering coefficient for each node.
        
        Formula: C_u = (2 * T_u) / (k_u * (k_u - 1))
        
        Where:
        - T_u = number of triangles (connections between neighbors)
        - k_u = number of neighbors (degree)
        
        Measures how interconnected a node's neighbors are.
        High scores indicate modular, well-organized sections.
        
        Returns:
            Dict mapping node -> clustering coefficient (0.0 to 1.0)
        """
        clustering = {}
        
        for node in self.nodes:
            # Get neighbors (nodes this node points to)
            if node not in self.edges or len(self.edges[node]) < 2:
                clustering[node] = 0.0
                continue
            
            neighbors = list(self.edges[node].keys())
            k = len(neighbors)
            
            # Count triangles: connections between neighbors
            triangles = 0
            for i, neighbor1 in enumerate(neighbors):
                for neighbor2 in neighbors[i+1:]:
                    # Check if neighbor1 connects to neighbor2 (or vice versa)
                    if (neighbor1 in self.edges and neighbor2 in self.edges[neighbor1]) or \
                       (neighbor2 in self.edges and neighbor1 in self.edges[neighbor2]):
                        triangles += 1
            
            # Calculate coefficient
            max_possible = k * (k - 1) / 2
            clustering[node] = triangles / max_possible if max_possible > 0 else 0.0
        
        return clustering
    
    def average_clustering_coefficient(self) -> float:
        """
        Calculate the average clustering coefficient across all nodes.
        
        Returns:
            Average clustering coefficient for the entire graph (0.0 to 1.0)
        """
        clustering = self.clustering_coefficient()
        if not clustering:
            return 0.0
        return sum(clustering.values()) / len(clustering)
    
    def get_summary_report(self) -> str:
        """
        Generate a comprehensive summary report of all metrics.
        
        Returns:
            Formatted string with all calculated metrics
        """
        report = []
        report.append("=" * 70)
        report.append("UI NAVIGATION GRAPH METRICS REPORT")
        report.append("=" * 70)
        report.append("")
        
        # Basic graph info
        report.append("📊 GRAPH STRUCTURE")
        report.append(f"  Nodes (pages/elements): {len(self.nodes)}")
        report.append(f"  Edges (navigation paths): {len(self.weights)}")
        report.append(f"  Total navigation events: {sum(self.weights.values())}")
        report.append("")
        
        # Average Shortest Path Length
        report.append("🛤️  AVERAGE SHORTEST PATH LENGTH")
        avg_path = self.average_shortest_path_length()
        if avg_path is not None:
            report.append(f"  L = {avg_path:.3f} clicks")
            report.append(f"  Interpretation: On average, users need {avg_path:.1f} clicks")
            report.append(f"                  to navigate between any two pages.")
            if avg_path < 2.5:
                report.append("  ✓ EXCELLENT - Very efficient navigation")
            elif avg_path < 4.0:
                report.append("  ✓ GOOD - Reasonable navigation efficiency")
            elif avg_path < 6.0:
                report.append("  ⚠️  FAIR - Consider shortening some paths")
            else:
                report.append("  ❌ POOR - UI has very long navigation paths")
        else:
            report.append("  ⚠️  Unable to calculate (disconnected graph or < 2 nodes)")
        report.append("")
        
        # Closeness Centrality
        report.append("🎯 CLOSENESS CENTRALITY (Top 10 Most Central Pages)")
        centrality = self.closeness_centrality()
        sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        
        for i, (node, score) in enumerate(sorted_centrality[:10], 1):
            # Truncate long node names for display
            display_node = node[:50] + "..." if len(node) > 50 else node
            report.append(f"  {i:2d}. {display_node}")
            report.append(f"      Centrality: {score:.4f}")
        
        if len(sorted_centrality) > 10:
            report.append(f"  ... and {len(sorted_centrality) - 10} more nodes")
        report.append("")
        
        # Clustering Coefficient
        report.append("🔗 CLUSTERING COEFFICIENT")
        avg_clustering = self.average_clustering_coefficient()
        report.append(f"  Average: {avg_clustering:.4f}")
        report.append(f"  Interpretation: {avg_clustering*100:.1f}% of possible neighbor")
        report.append(f"                  connections are realized.")
        
        if avg_clustering > 0.85:
            report.append("  ✓ HIGH - Strong modularity, well-organized sections")
        elif avg_clustering > 0.6:
            report.append("  ✓ MODERATE - Decent local connectivity")
        else:
            report.append("  ⚠️  LOW - Pages could be better interconnected")
        report.append("")
        
        # Top/Bottom clustered nodes
        clustering = self.clustering_coefficient()
        sorted_clustering = sorted(clustering.items(), key=lambda x: x[1], reverse=True)
        
        report.append("  Most Clustered Nodes (Top 5):")
        for i, (node, score) in enumerate(sorted_clustering[:5], 1):
            if score > 0:
                display_node = node[:45] + "..." if len(node) > 45 else node
                report.append(f"    {i}. {display_node}: {score:.3f}")
        
        report.append("")
        report.append("  Least Clustered Nodes (Bottom 5):")
        for i, (node, score) in enumerate(reversed(sorted_clustering[-5:]), 1):
            display_node = node[:45] + "..." if len(node) > 45 else node
            report.append(f"    {i}. {display_node}: {score:.3f}")
        
        report.append("")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def export_metrics_json(self, filepath: str):
        """
        Export all metrics to a JSON file for further analysis.
        
        Args:
            filepath: Path where JSON file should be written
        """
        metrics = {
            "graph_info": {
                "num_nodes": len(self.nodes),
                "num_edges": len(self.weights),
                "total_weight": sum(self.weights.values())
            },
            "average_shortest_path_length": self.average_shortest_path_length(),
            "average_clustering_coefficient": self.average_clustering_coefficient(),
            "closeness_centrality": self.closeness_centrality(),
            "clustering_coefficient": self.clustering_coefficient()
        }
        
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"✓ Metrics exported to {filepath}")


def main():
    """
    Command-line interface for the GraphMetrics calculator.
    """
    if len(sys.argv) < 2:
        print("Usage: python graph_metrics.py <input_file.json>")
        print("")
        print("Input file formats supported:")
        print("  1. JSON array: [{\"source\": \"A\", \"target\": \"B\", \"weight\": 5}, ...]")
        print("  2. JSON Lines: One edge object per line")
        print("")
        print("Example:")
        print("  python graph_metrics.py edges.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    print(f"\n📈 Loading graph from {input_file}...")
    
    # Create metrics calculator
    gm = GraphMetrics()
    
    # Try loading as JSON array first, then JSONL
    try:
        gm.load_from_json_file(input_file)
    except json.JSONDecodeError:
        try:
            gm.load_from_jsonl_file(input_file)
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            sys.exit(1)
    
    # Calculate and display metrics
    print("\n" + gm.get_summary_report())
    
    # Export to JSON
    output_file = input_file.rsplit('.', 1)[0] + '_metrics.json'
    gm.export_metrics_json(output_file)


if __name__ == "__main__":
    main()

