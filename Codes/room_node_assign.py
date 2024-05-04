import pandas as pd

# 파일 경로 설정
file_path = 'ExcelFiles\Last_info_original - Copy.xlsx'

# 엑셀 파일 로드
data = pd.read_excel(file_path)

# 파일에서 'Node' 열이 실제로 존재하는지 확인하고, 필요하면 이름을 조정하세요
print(data.columns)  # 실제 열 이름을 확인

# 'Node'를 문자열로 변환 (엑셀 파일의 열 이름을 정확히 입력하세요)
data['Node'] = data['Node'].astype(str)

# 겹치는 시간 구간을 처리하는 함수
def process_intervals(df):
    df_sorted = df.sort_values('Start Time')
    result = []

    current = df_sorted.iloc[0].to_dict()
    for i in range(1, len(df_sorted)):
        next_row = df_sorted.iloc[i].to_dict()

        if current and current['End Time'] > next_row['Start Time']:  # Check overlap
            # Handle non-overlapping part before the overlap
            if current['Start Time'] < next_row['Start Time']:
                result.append({
                    'Node': current['Node'],
                    'Day Number': current['Day Number'],
                    'Start Time': current['Start Time'],
                    'End Time': next_row['Start Time'],
                    'Adjusted People Count': current['Adjusted People Count'],
                    'Connection Strength': current['Connection Strength']
                })

            # Overlapping part
            overlap_end = min(current['End Time'], next_row['End Time'])
            result.append({
                'Node': current['Node'],
                'Day Number': current['Day Number'],
                'Start Time': next_row['Start Time'],
                'End Time': overlap_end,
                'Adjusted People Count': current['Adjusted People Count'] + next_row['Adjusted People Count'],
                'Connection Strength': current['Connection Strength'] + next_row['Connection Strength']
            })

            # Prepare for the next comparison
            if next_row['End Time'] > overlap_end:
                next_row['Start Time'] = overlap_end
                current = next_row  # Continue with the modified next_row
            else:
                current['Start Time'] = overlap_end  # Modify current and compare with further rows

            if current['Start Time'] >= current['End Time']:  # No remaining part in current
                current = next_row if next_row['End Time'] > overlap_end else None
        else:
            if current:
                result.append(current)
            current = next_row

    if current:
        result.append(current)

    return pd.DataFrame(result)

# 'Node'와 'Day Number' 기준으로 그룹화하고 함수 적용
grouped_data = data.groupby(['Node', 'Day Number']).apply(process_intervals).reset_index(drop=True)

# 결과 데이터를 새 엑셀 파일로 저장
output_path = 'path_to_output_excel_file.xlsx'
grouped_data.to_excel(output_path, index=False)

print(f"Processed data saved to {output_path}")
