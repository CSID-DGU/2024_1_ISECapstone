import simpy
import pandas as pd
import numpy as np

file_path_distance = './ExcelFiles/NodeCapacity.xlsx'
capacity_data = pd.read_excel(file_path_distance, index_col=0)
capacity_df = pd.DataFrame(capacity_data)

file_path_people = './ExcelFiles/pathfinder_people_count/금0900.csv'
people_data = pd.read_csv(file_path_people, header=None)
df = pd.DataFrame(people_data)

df.iloc[1] = df.iloc[1].replace('Floor 6.0 m->25', 'Floor 6.0 m->38')
df.iloc[1] = df.iloc[1].replace('Floor 10.0 m->38', 'Floor 10.0 m->49')
df.iloc[1] = df.iloc[1].replace('Floor 14.0 m->49', 'Floor 14.0 m->59')
df.iloc[1] = df.iloc[1].replace('Floor 18.0 m->59', 'Floor 18.0 m->68')

df.drop(index=[0, 2, 3, 4], inplace=True)
df.drop(df.columns[0], axis=1, inplace=True)
df.reset_index(drop=True, inplace=True)

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
index = col_352_index.index[0]


df['352_copy'] = df.iloc[:, index]

df.at[0, '352_copy'] = 455

df.reset_index(drop=True, inplace=True)
df = df.T.reset_index(drop=True).T

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

def transform_value(x):
    if x < 1:
        return 1
    else:
        return x

# print(df)    
df.iloc[1:, :] = df.iloc[1:, :].applymap(transform_value)
output_file = '금0900_output.xlsx'
df.to_excel(output_file, index=False)

# num_rows = len(df)
# max_in_intervals = []