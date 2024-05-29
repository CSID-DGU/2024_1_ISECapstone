import pandas as pd
import numpy as np
import os
from make_weight_df import df_weight_dic

print(os.getcwd())

class Graph:
    def __init__(self, distance_matrix, weight_matrix):
        self.graph = distance_matrix
        self.weight_dicts = weight_matrix
        self.V = len(distance_matrix)
    
    def min_distance(self, dist, spt_set):
        # 최소 거리를 찾는 함수
        min = float('inf')
        min_index = -1
        for v in range(self.V):
            if dist[v] < min and not spt_set[v]:
                min = dist[v]
                min_index = v
        return min_index

    def dijkstra(self, src):
        # Dijkstra 알고리즘을 사용하여 최단 경로를 계산하는 함수
        dist = [float('inf')] * self.V
        dist[src] = 0
        spt_set = [False] * self.V
        prev = [None] * self.V

        weight_index = src//10
        weight_matrix = self.weight_dicts[weight_index].to_numpy() if weight_index in self.weight_dicts else np.ones((self.V, self.V))

        for cout in range(self.V):
            u = self.min_distance(dist, spt_set)
            spt_set[u] = True
            for v in range(self.V):
                if (self.graph[u][v] > 0 and not spt_set[v] and 
                    dist[v] > dist[u] + self.graph[u][v] * weight_matrix[u][v] and self.graph[u][v] != 99999):
                    dist[v] = dist[u] + self.graph[u][v] * weight_matrix[u][v]
                    prev[v] = u                
        return dist, prev
    
    def print_path(self, prev, j):
        # 경로를 출력하는 함수
        if prev[j] is None:
            print(j, end=' ')
            return
        self.print_path(prev, prev[j])
        print(j, end=' ')

# 파일 경로
file_path = './ExcelFiles/DistanceBtwnNodes.xlsx'
data_DBN = pd.read_excel(file_path, index_col=0)
df_DBN = pd.DataFrame(data_DBN)

# Graph 객체 생성
graph_DBN = Graph(df_DBN.to_numpy(), df_weight_dic)

# 출구 노드 분리를 위한 열 이름 문자열 변환
column_name_S = df_DBN.columns.map(str)
exits = [node for node in column_name_S if node.startswith('출구')]
exits_index = [df_DBN.columns.get_loc(col) for col in exits]
non_exit_indices = [i for i in range(graph_DBN.V) if i not in exits_index]

# Compute the shortest paths to each exit for each node excluding the exits themselves
shortest_paths = {}
for index_node in non_exit_indices:
    distances, predecessors = graph_DBN.dijkstra(index_node)
    closer_exit = min((distances[exit], exit) for exit in exits_index)
    node_name = df_DBN.index[index_node]
    print(f"Shortest path from {node_name} to {df_DBN.columns[closer_exit[1]]} is {closer_exit[0]} units.", end="")
    print(" path : ", end="")
    graph_DBN.print_path(predecessors, closer_exit[1])
    print("\n")