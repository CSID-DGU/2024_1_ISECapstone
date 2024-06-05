import pandas as pd
import numpy as np
import os

file_path_distance = './ExcelFiles/output_일부열제외.xlsx'
weight_data = pd.read_excel(file_path_distance, index_col=0)
weight_df = pd.DataFrame(weight_data)

weight_dic = {}

nodes = weight_df.iloc[0, 0:]

for i in range(1, 22):
    df = pd.DataFrame(index = nodes, columns = nodes)
    for j in range(0, 361):
        for k in range(0, 361):
            if j == k:
                df.iloc[j, k] = 0
            else:
                df.iloc[j, k] = (weight_df.iloc[i, j]+ weight_df.iloc[i, k])/2
    weight_dic[i] = df

# output_file = 'output_weight.xlsx'
# weight_dic[1].to_excel(output_file)
