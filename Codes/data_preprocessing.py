import pandas as pd

# 파일 경로
file_path = './ExcelFiles/LectureByClass.xlsx'

# 엑셀 파일 읽기
data = 0
data = pd.read_excel(file_path)

# 데이터의 첫 몇 줄을 출력하여 구조 파악
data.head(), data.columns

import re

# 요일을 숫자로 변환하는 함수
def day_to_number(day):
    days = {'월': 1, '화': 2, '수': 3, '목': 4, '금': 5, '토': 6, '일': 7}
    return days.get(day, 0)

# 시간 정보 분리 및 정리 함수
def parse_time_info(time_str):
    pattern = r'(\w)(\d{2}):(\d{2})-(\d{2}):(\d{2})'
    matches = re.findall(pattern, time_str)
    time_info = []
    for match in matches:
        day, start_hr, start_min, end_hr, end_min = match
        start_time = int(start_hr + start_min)
        duration = (int(end_hr) * 60 + int(end_min)) - (int(start_hr) * 60 + int(start_min))
        time_info.append([day_to_number(day), start_time, duration])
    return time_info

# 강의실별로 데이터 정리 (강의 코드를 '호수' 열의 뒷 3자리를 사용)
def organize_data_with_code(df):
    time_table = {}
    for _, row in df.iterrows():
        # '호수' 열에서 강의 코드 추출 (뒷 3자리)
        classroom_code = int(row['호수'].split('-')[-1])
        time_slots = parse_time_info(row['요일/시간'])
        for slot in time_slots:
            if classroom_code not in time_table:
                time_table[classroom_code] = []
            time_table[classroom_code].append(slot + [row['인원수']])
    return time_table

# 강의 데이터 정리
organized_time_table = organize_data_with_code(data)
organized_time_table[127][:5]  # 예시 출력 (강의실 '127'의 첫 5개 강의 정보 확인)

organized_time_table
