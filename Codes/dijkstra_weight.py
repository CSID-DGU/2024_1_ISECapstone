import pandas as pd
import numpy as np
import os
from weight_dic import weight_dic

print(os.getcwd())

class Graph:
    def __init__(self, distance_matrix, weight_matrix):
        self.graph = distance_matrix.to_numpy()
        self.nodes = distance_matrix.index
        self.columns = distance_matrix.columns
        self.weight_dicts = weight_matrix
        self.V = len(distance_matrix)
    
    def min_distance(self, dist, spt_set):
        min_val = float('inf')
        min_index = -1
        for v in range(self.V):
            if dist[v] < min_val and not spt_set[v]:
                min_val = dist[v]
                min_index = v
        return min_index

    def get_weight(self, u, v):
        weight_index = min(u // 2, 20)  # 40개 이후의 노드는 마지막 가중치 DataFrame을 사용
        if weight_index not in self.weight_dicts:
            return 1
        weight_matrix = self.weight_dicts[weight_index]
        node_u = self.nodes[u]
        node_v = self.columns[v]
        if node_u in weight_matrix.index and node_v in weight_matrix.columns:
            return weight_matrix.loc[node_u, node_v]
        return 1

    def dijkstra(self, src):
        dist = [float('inf')] * self.V
        dist[src] = 0
        spt_set = [False] * self.V
        prev = [None] * self.V

        for cout in range(self.V):
            u = self.min_distance(dist, spt_set)
            if u == -1:  # 모든 노드가 처리된 경우
                break
            spt_set[u] = True
            for v in range(self.V):
                if (self.graph[u][v] > 0 and not spt_set[v] and 
                    dist[v] > dist[u] + self.graph[u][v] * self.get_weight(u, v) and self.graph[u][v] != 99999):
                    dist[v] = dist[u] + self.graph[u][v] * self.get_weight(u, v)
                    prev[v] = u                
        return dist, prev
    
    def print_path(self, prev, j):
        if prev[j] is None:
            print(self.nodes[j], end=' ')
            return
        self.print_path(prev, prev[j])
        print(self.nodes[j], end=' ')

# 파일 경로
file_path = './ExcelFiles/DistanceBtwnNodes.xlsx'
data_DBN = pd.read_excel(file_path, index_col=0)
df_DBN = pd.DataFrame(data_DBN)

# Graph 객체 생성
graph_DBN = Graph(df_DBN, weight_dic)

# 출구 노드 분리를 위한 열 이름 문자열 변환
column_name_S = df_DBN.columns.map(str)
exits = [node for node in column_name_S if node.startswith('출구')]
exits_index = [df_DBN.columns.get_loc(col) for col in exits]
non_exit_indices = [i for i in range(graph_DBN.V) if i not in exits_index]

# Compute the shortest paths to each exit for each node excluding the exits themselves
shortest_paths = {}
for index_node in non_exit_indices:
    distances, predecessors = graph_DBN.dijkstra(index_node)
    valid_exits = [(distances[exit], exit) for exit in exits_index if distances[exit] < float('inf')]
    if not valid_exits:
        print(f"No valid path found from {df_DBN.index[index_node]} to any exit.")
        continue
    closer_exit = min(valid_exits)
    node_name = df_DBN.index[index_node]
    print(f"Shortest path from {node_name} to {df_DBN.columns[closer_exit[1]]} is {closer_exit[0]} units.", end="")
    print(" path : ", end="")
    graph_DBN.print_path(predecessors, closer_exit[1])
    print("\n")
    
# DataFrame으로 변환하고 CSV로 저장
df_paths = pd.DataFrame(list(shortest_paths.items()), columns=['Node', 'Path'])
df_paths.to_csv('shortest_paths_dijkstra_weight.csv', index=False, encoding='utf-8-sig')