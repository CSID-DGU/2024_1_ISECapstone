import os
import pandas as pd

# 디렉토리 경로
directory_path = 'ExcelFiles/시간별혼잡도/'

# 결과를 저장할 리스트
results = []

# 디렉토리의 모든 CSV 파일 처리
for filename in os.listdir(directory_path):
    if filename.endswith(".csv"):
        # CSV 파일 경로
        file_path = os.path.join(directory_path, filename)
        
        # CSV 파일 읽기 (header=None으로 모든 행을 데이터로 읽기)
        df_raw = pd.read_csv(file_path, header=None)
        
        # 새로운 열 이름 만들기 (1행과 4행의 텍스트를 concatenate)
        new_column_names = df_raw.iloc[0] + ' ' + df_raw.iloc[3]
        
        # 필요한 데이터 선택 (6행부터 시작, B~D열만 사용)
        df = df_raw.iloc[5:, 1:4]
        
        # 새로운 열 이름 지정
        df.columns = new_column_names[1:4]
        
        # 인덱스 리셋
        df.reset_index(drop=True, inplace=True)
        
        # 3열의 값을 이전 행과의 차이로 변경
        df.iloc[:, 2] = df.iloc[:, 2].astype(int).diff().fillna(0).astype(int)
        
        # 마지막 행 제외
        df_excluding_last = df.iloc[:-1, :]
        
        # 1열과 3열의 값을 곱해서 더한 값 계산 (마지막 행 제외)
        product_sum_excluding_last = (df_excluding_last.iloc[:, 0].astype(float) * df_excluding_last.iloc[:, 2]).sum()
        
        # 2열의 첫 번째 데이터를 float로 변환
        first_value_col2 = float(df.iloc[0, 1])
        
        # 2열의 첫 번째 데이터로 나눈 값 계산
        result_excluding_last = product_sum_excluding_last / first_value_col2
        
        # df.iloc[-1, 0] 값
        last_value_first_col = df.iloc[-1, 0]
        
        # 결과를 리스트에 저장
        results.append([filename, result_excluding_last, last_value_first_col])

# 결과를 데이터프레임으로 변환
results_df = pd.DataFrame(results, columns=['Filename', 'Result', 'Last Time Value'])

# 결과를 CSV 파일로 저장
results_df.to_csv('ExcelFiles/processed_results.csv', index=False)

print("Results have been saved to 'processed_results.csv'.")
