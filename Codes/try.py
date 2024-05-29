import simpy
import pandas as pd

file_path_distance = './ExcelFiles/DistanceBtwnNodes.xlsx'
distance_data = pd.read_excel(file_path_distance, index_col=0)
distance_df = pd.DataFrame(distance_data)

file_path_routes = './ExcelFiles/shortestpaths.csv'
routes_data = pd.read_csv(file_path_routes)
routes_df = pd.DataFrame(routes_data)

file_path_people = './ExcelFiles/Last_info_original.xlsx'
people_data = pd.read_excel(file_path_people)
people_df = pd.DataFrame(people_data)

people_routes_df = pd.merge(people_df, routes_df, on='Node', how='left')

# 0이 아닌 값만 선택
non_zero_values = distance_df[(distance_df != 0) & (distance_df != 9999999999)]

# 0이 아닌 값들의 평균 계산
mean_value = non_zero_values.stack().mean()
max_value = non_zero_values.max().max()
min_value = non_zero_values.min().min()
mid_value = non_zero_values.stack().median()
print("평균:", mean_value, "max", max_value, "min", min_value, "mid", mid_value)