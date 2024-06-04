import pandas as pd
import numpy as np
import os

file_path_distance = './ExcelFiles/output.xlsx'
weight_data = pd.read_excel(file_path_distance, index_col=0)
weight_df = pd.DataFrame(weight_data)

print(weight_df.iloc[:, 1])