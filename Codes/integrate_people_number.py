import pandas as pd
import re
import os
from collections import Counter

# 현재 작업 디렉토리 확인
print(os.getcwd())

# 파일 경로
lecture_file_path = './ExcelFiles/LectureByClass.xlsx'
people_file_path = './ExcelFiles/PeopleByRoom.xlsx'

# 엑셀 파일 읽기
lecture_data = pd.read_excel(lecture_file_path)
people_data = pd.read_excel(people_file_path)

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
        start_time = int(start_hr) * 100 + int(start_min)
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

# 데이터 통합
lecture_info = organize_data_with_code(lecture_data)
people_info = organize_data_with_code(people_data)

# # 최종 데이터 구조 생성
# for code in lecture_info:
#     if code in people_info:
#         for slot in lecture_info[code]['time_slots']:
#             slot.append(people_info[code])  # 인원수 추가

people_info.update(lecture_info)
print(people_info.keys())
print(len(people_info.keys()))