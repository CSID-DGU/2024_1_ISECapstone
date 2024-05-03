import pandas as pd
import numpy as np
import os

print(os.getcwd)

class Graph:
    def __init__(self, distance_matrix):
        self.graph = distance_matrix
        self.V = len(distance_matrix)
    
    def min_distance(self, dist, spt_set):
        min = float('inf')
        min_index = -1
        for v in range(self.V):
            if dist[v] < min and not spt_set[v]:
                min = dist[v]
                min_index = v
        return min_index

    def dijkstra(self, src):
        dist = [float('inf')] * self.V
        dist[src] = 0
        spt_set = [False] * self.V
        prev = [None] * self.V

        for cout in range(self.V):
            u = self.min_distance(dist, spt_set)
            spt_set[u] = True
            for v in range(self.V):
                if (self.graph[u][v] > 0 and not spt_set[v] and 
                    dist[v] > dist[u] + self.graph[u][v] and self.graph[u][v] != 99999):
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

# Create a DataFrame from the provided distance matrix
file_path = './ExcelFiles/DistanceBtwnNodes.xlsx'
data_DBN = pd.read_excel(file_path, index_col=0)
df_DBN = pd.DataFrame(data_DBN)

# Convert the DataFrame to a numpy array for graph processing
distance_matrix = df_DBN.to_numpy()

# 출구의 index 추출하기&출구노드 분리를 위한 열 이름 문자열 변환
graph_DBN = Graph(distance_matrix)
column_name_S = df_DBN.columns.map(str)

#출구와 출구가 아닌 노드의 index 분리
exits = [node for node in column_name_S if node.startswith('출구')]
exits_index = [df_DBN.columns.get_loc(col) for col in exits]
non_exit_indices = [i for i in range(380) if i not in exits_index]

#경로를 저장할 위치
shortest_paths = {}

# Compute the shortest paths to each exit for each node excluding the exits themselves
for index_node in non_exit_indices: 
    node_name = df_DBN.index[index_node]
    distances, predecessors = graph_DBN.dijkstra(index_node)
    closer_exit = min((distances[exit], exit) for exit in exits_index)
    shortest_paths[df_DBN.columns[index_node]] = closer_exit
    print(f"Shortest path from {node_name} to {closer_exit[1]} is {closer_exit[0]} units.", end="")
    print(" path : ", end="")
    graph_DBN.print_path(predecessors, closer_exit[1])
    print("\n")

