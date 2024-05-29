import pandas as pd
import ast

file_path_weight = './ExcelFiles/weight.xlsx'
data_weight = pd.read_excel(file_path_weight, index_col=0)
df_weight_dic = {}
for i in range(1, 51):
    df_weight_dic[i] = pd.DataFrame(data_weight)

file_path_weight = './ExcelFiles/test_weight.xlsx'
simulation_w = pd.read_excel(file_path_weight)
simulation_w_df = pd.DataFrame(simulation_w)

def load_and_update_weight(dic, df):
    results = []

    for idx, row in df.iterrows():
        df_to_use = dic[row['time']]
        # print(df_to_use)
        origin_value = df_to_use.loc[row['from'], row['to']]
        updated_value = origin_value*1.5
        df_to_use.at[row['from'], row['to']] = updated_value
        dic[row['time']] = df_to_use
        # print(dic[row['time']])
    

a = load_and_update_weight(df_weight_dic, simulation_w_df)

print(df_weight_dic[1])
print(df_weight_dic[2])