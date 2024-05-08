import pandas as pd
import numpy as np

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
    
    def get_path(self, prev, j):
        path = []
        while j is not None:
            path.append(j)
            j = prev[j]
        path.reverse()
        return path

# 예제 데이터 불러오기
file_path = 'DistanceBtwnNodes.xlsx'
data_DBN = pd.read_excel(file_path, index_col=0)
df_DBN = pd.DataFrame(data_DBN)
distance_matrix = df_DBN.to_numpy()

graph_DBN = Graph(distance_matrix)
column_name_S = df_DBN.columns.map(str)
exits = [node for node in column_name_S if node.startswith('출구')]
exits_index = [df_DBN.columns.get_loc(col) for col in exits]
non_exit_indices = [i for i in range(df_DBN.shape[0]) if i not in exits_index]

shortest_paths = {}

for index_node in non_exit_indices: 
    node_name = df_DBN.index[index_node]
    distances, predecessors = graph_DBN.dijkstra(index_node)
    closer_exit = min((distances[exit], exit) for exit in exits_index)
    exit_name = df_DBN.columns[closer_exit[1]]
    path = graph_DBN.get_path(predecessors, closer_exit[1])
    path_names = [df_DBN.index[node_index] for node_index in path]  # 인덱스를 노드 이름으로 변환
    shortest_paths[node_name] = path_names

# DataFrame으로 변환하고 CSV로 저장
df_paths = pd.DataFrame(list(shortest_paths.items()), columns=['Node', 'Path'])
df_paths.to_csv('shortest_paths.csv', index=False, encoding='utf-8-sig')


'''example_paths = {
    '노드1': ['노드1', '노드2', '노드3', '출구'],
    '노드2': ['노드2', '노드3', '출구'],
    '노드3': ['노드3', '출구']
}'''