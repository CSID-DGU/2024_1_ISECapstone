import pandas as pd

# 업로드된 파일 경로
file_path = 'ExcelFiles/processed_results.csv'

# CSV 파일 읽기
results_df = pd.read_csv(file_path)

# Filename에서 요일과 시간 정보를 추출하는 함수
def extract_day_and_time(filename):
    try:
        day_time = filename.split('.')[0]
        day = day_time[0]  # 요일
        time = day_time[1:]  # 시간
        return day, time
    except IndexError:
        return None, None

# 요일과 시간 정보 추출
results_df['Day'], results_df['Time'] = zip(*results_df['Filename'].apply(extract_day_and_time))

# 시간 형식을 맞추기 위해 'Time' 열을 4자리 문자열로 변환
results_df['Time'] = results_df['Time'].apply(lambda x: f"{int(x):04d}" if pd.notnull(x) else x)

# 요일과 시간 테이블 만들기
days = ['월', '화', '수', '목', '금']
times = [f'{hour:02d}{minute:02d}' for hour in range(9, 18) for minute in [0, 30]]

# 빈 데이터프레임 생성
timetable_result_df = pd.DataFrame(index=times, columns=days)
timetable_last_time_value_df = pd.DataFrame(index=times, columns=days)

# 결과를 테이블에 채우기
for _, row in results_df.iterrows():
    day = row['Day']
    time = row['Time']
    result = row['Result']
    last_time_value = row['Last Time Value']
    if day in timetable_result_df.columns and time in timetable_result_df.index:
        timetable_result_df.at[time, day] = result
        timetable_last_time_value_df.at[time, day] = last_time_value

# Excel 파일로 저장
output_file = 'ExcelFiles/timetable_results.xlsx'
with pd.ExcelWriter(output_file) as writer:
    timetable_result_df.to_excel(writer, sheet_name='Result')
    timetable_last_time_value_df.to_excel(writer, sheet_name='Last Time Value')

# 결과 파일 경로 출력
output_file
