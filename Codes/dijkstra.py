import pandas as pd
import numpy as np

class Graph:
    def __init__(self, distance_matrix):
        self.graph = distance_matrix
        self.V = len(distance_matrix)
    
    def min_distance(self, dist, spt_set):
        # Initialize minimum distance for next node
        min = float('inf')
        min_index = -1

        # Search not nearest vertex not in the shortest path tree
        for v in range(self.V):
            if dist[v] < min and not spt_set[v]:
                min = dist[v]
                min_index = v
        return min_index

    def dijkstra(self, src):
        dist = [float('inf')] * self.V  # The output array. dist[i] will hold the shortest distance from src to i
        dist[src] = 0
        spt_set = [False] * self.V  # sptSet[i] will be True if vertex i is included in shortest path tree or shortest distance from src to i is finalized
        prev = [None] * self.V  # To store the path

        for cout in range(self.V):
            u = self.min_distance(dist, spt_set)  # Pick the minimum distance vertex from the set of vertices not yet processed
            spt_set[u] = True  # Put the minimum distance vertex in the shortest path tree

            # Update dist value of the adjacent vertices of the picked vertex only if the current
            # distance is greater than new distance and the vertex in not in the shortest path tree
            for v in range(self.V):
                if (self.graph[u][v] > 0 and not spt_set[v] and 
                    dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]
                    prev[v] = u
        
        return dist, prev

    def print_path(self, prev, j):
        # Base Case : If j is source
        if prev[j] is None:
            print(j, end=' ')
            return
        self.print_path(prev, prev[j])
        print(j, end=' ')

# Create a 10x10 DataFrame for distance matrix
data = np.random.randint(1, 142884, size=(378, 378))
np.fill_diagonal(data, 0)
distance_df = pd.DataFrame(data)

# Convert the DataFrame to a numpy array for processing
distance_matrix = distance_df.to_numpy()

# Assuming node 9 is the destination
destination = 9

g = Graph(distance_matrix)

# Print shortest paths from each node to the destination node
for i in range(378):  # Excluding the destination itself
    distances, predecessors = g.dijkstra(i)
    print(f"Shortest Path from Node {i} to Node {destination}: ", end='')
    g.print_path(predecessors, destination)
    print(f" with total distance: {distances[destination]}")
