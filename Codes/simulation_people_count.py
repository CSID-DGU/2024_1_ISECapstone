import pandas as pd
import numpy as np
import os

directory = './ExcelFiles/pathfinder_people_count'
i = 0
people_count_dic = {}

file_path = './ExcelFiles/NodeCapacity.xlsx'
capacity_data = pd.read_excel(file_path)
capacity_df = pd.DataFrame(capacity_data)
time_list = []

def transform_value(x):
    if x < 1:
        return 1
    else:
        return x

def calculate_max_intervals(dfs, interval=4):
    interval_results = {}
    
    for key, df in dfs.items():
        for start in range(1, len(df), interval):
            if start < 80:
                end = min(start + interval, len(df) + 1)
                interval_label = f"{start}초~{end-1}초"
            else:
                end = len(df) + 1
                interval_label = f"{start}초~"

            max_values = df.iloc[start:end, :].max(axis=0)  # 첫 번째 열(t)를 포함하여 계산
            if interval_label not in interval_results:
                interval_results[interval_label] = []
            interval_results[interval_label].append(max_values)
            if start >= 80:
                break

    # 각 구간별로 평균을 계산하여 새로운 DataFrame으로 저장
    result_dict = {col: [] for col in df.columns}  # 첫 번째 열(t)를 포함한 열로 dict 초기화

    for interval_label, max_values_list in interval_results.items():
        df_max_values = pd.DataFrame(max_values_list)
        for col in df.columns:  # 첫 번째 열(t)를 포함한 열에 대해 평균 계산
            result_dict[col].append(df_max_values[col].mean())

    result_df = pd.DataFrame(result_dict)

    # 원래 df의 첫 번째 행 추가 (첫 번째 열(t) 포함)
    first_row = list(dfs.values())[0].iloc[0, :]
    result_df.loc[-1] = first_row
    result_df.index = result_df.index + 1
    result_df = result_df.sort_index()

    return result_df

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)

        df = None
        df = pd.read_csv(file_path, header=None)

        df.iloc[1] = df.iloc[1].replace('Floor 6.0 m->25', 'Floor 6.0 m->38')
        df.iloc[1] = df.iloc[1].replace('Floor 10.0 m->38', 'Floor 10.0 m->49')
        df.iloc[1] = df.iloc[1].replace('Floor 14.0 m->49', 'Floor 14.0 m->59')
        df.iloc[1] = df.iloc[1].replace('Floor 18.0 m->59', 'Floor 18.0 m->68')

        df.drop(index=[0, 2, 3, 4], inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df = df.T.reset_index(drop=True).T

        for column in df.columns:
            value = df.loc[0, column]
            if isinstance(value, str):
                if 'room' in value or 'Room' in value:
                    df.drop(column, axis=1, inplace=True)
                elif '->' in value:
                    df[column] = df[column].apply(lambda x: x.split('->')[1] if '->' in x else x)

        for column in df.columns:
            try:
                df[column] = pd.to_numeric(df[column], errors='coerce')
            except ValueError:
                pass
        
        df.reset_index(drop=True, inplace=True)
        df = df.T.reset_index(drop=True).T

        df.iloc[0] = df.iloc[0].replace(559, 657)
        df.iloc[0] = df.iloc[0].replace(461, 559)
        df.iloc[0] = df.iloc[0].replace(350, 461)
        df.iloc[0] = df.iloc[0].replace(245, 350)
        df.iloc[0] = df.iloc[0].replace(142, 245)
        df.iloc[0] = df.iloc[0].replace(553, 652)
        df.iloc[0] = df.iloc[0].replace(455, 553)

        col_352_index = df.iloc[0][df.iloc[0]==352]
        col_352 = col_352_index.index[0]
        df['352_copy'] = df.iloc[:, col_352]

        df.at[0, '352_copy'] = 455
            
        people_count_dic[i] = df
        i += 1

for j in range(0, 90):
    df = None
    df = people_count_dic[j]
    max_people = df.iloc[1, 1]*0.8
    filtered_df = df[df.iloc[:, 2] >= max_people]

    min_time = filtered_df.iloc[:, 0].tolist()
    if min_time:
        min_value = min(min_time)
        time_list.append(min_value)

results_dic = {}
l=0
results = []
for k in range(0, 90):
    df = None
    df = people_count_dic[k]
    for idx, row in capacity_df.iterrows():
        inx_node = df.iloc[0][df.iloc[0]==idx]
        if not inx_node.empty:
            index_node = inx_node.index[0]
            df.iloc[1:, index_node] = df.iloc[1:, index_node]/row['optimum']
    for column in df.columns:
        value = df.loc[0, column]
        if np.isnan(value):
            df.drop(columns=column, inplace=True)  
    df.reset_index(drop=True, inplace=True)
    df = df.T.reset_index(drop=True).T
    df.iloc[1:, :] = df.iloc[1:, :].applymap(transform_value)
    people_count_dic[k] = df

# print(people_count_dic[0])
    
results_df = calculate_max_intervals(people_count_dic)
print(results_df)

output_file = 'output.xlsx'
results_df.to_excel(output_file)

# for m in range(0, 21):
#     print(results_df.iloc[:, 0])

# average_time = np.mean(time_list)
# print(results)
    
#일단 101이 비어있는 이유가 101부분이 index라고 취급되어서인거같은데 어떻게 처리해야할지는...