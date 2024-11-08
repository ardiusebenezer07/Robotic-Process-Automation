#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import yaml
import networkx as nx
import math
from scipy.spatial import KDTree

# Load parameters
with open("/home/faiz/PRM/src/prm_planner/config/params.yaml", 'r') as f:
    params = yaml.safe_load(f)

num_nodes = params['num_nodes']
connect_radius = params['connect_radius']
start = params['start']
goal = params['goal']
map_size = params['map_size']

# Fungsi untuk menghasilkan node acak
def generate_random_nodes(num_nodes, map_size, start, goal):
    nodes = np.random.rand(num_nodes, 2) * map_size
    nodes = np.vstack((start, nodes, goal))
    return nodes

# Fungsi untuk membentuk graf PRM
def construct_prm_graph(nodes, connect_radius):
    graph = nx.Graph()
    kdtree = KDTree(nodes)

    for i, node in enumerate(nodes):
        neighbors = kdtree.query_ball_point(node, connect_radius)
        for j in neighbors:
            if i != j:
                dist = np.linalg.norm(nodes[i] - nodes[j])
                graph.add_edge(i, j, weight=dist)

    return graph

# Fungsi untuk mencari jalur terpendek menggunakan algoritma Dijkstra
def shortest_path(graph, start_idx, goal_idx):
    try:
        path = nx.shortest_path(graph, source=start_idx, target=goal_idx, weight='weight')
        return path
    except nx.NetworkXNoPath:
        print("No path found!")
        return []

# Fungsi untuk visualisasi PRM
def visualize_prm(nodes, graph, path=None):
    plt.figure(figsize=(8, 8))
    plt.scatter(nodes[:, 0], nodes[:, 1], c='blue', s=30, label="Nodes")
    plt.scatter([nodes[0, 0]], [nodes[0, 1]], c='green', s=100, label="Start")
    plt.scatter([nodes[-1, 0]], [nodes[-1, 1]], c='red', s=100, label="Goal")

    for (i, j) in graph.edges:
        plt.plot([nodes[i, 0], nodes[j, 0]], [nodes[i, 1], nodes[j, 1]], 'gray', alpha=0.5)

    if path:
        path_coords = nodes[path]
        plt.plot(path_coords[:, 0], path_coords[:, 1], 'orange', linewidth=3, label="Shortest Path")

    plt.legend()
    plt.xlim(0, map_size[0])
    plt.ylim(0, map_size[1])
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Probabilistic Roadmap (PRM) Pathfinding")
    plt.grid()
    plt.show()

# Main program
def main():
    nodes = generate_random_nodes(num_nodes, map_size, start, goal)
    graph = construct_prm_graph(nodes, connect_radius)
    path = shortest_path(graph, 0, len(nodes) - 1)  # Indeks 0 untuk start dan indeks -1 untuk goal
    visualize_prm(nodes, graph, path)

if __name__ == "__main__":
    main()
