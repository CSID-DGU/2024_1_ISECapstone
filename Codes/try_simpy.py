import simpy
import random
import pandas as pd

def move_people(env, path_containers, start, end, people):
    """ 승객이 특정 통로를 이용하는 프로세스 """
    with path_containers[start][end].get(people) as req:
        yield req  # 통로에 자리가 날 때까지 기다림
        print(f"{env.now:.2f}: {people} people start moving from {start} to {end}.")
        yield env.timeout(time_df[start][end])  # 통과 시간
        yield path_containers[start][end].put(people)  # 통과 완료 후 자원 반환
        print(f"{env.now:.2f}: {people} people finished moving from {start} to {end}.")

def schedule_movement(env, path_containers, route, intervals, people_range):
    """ 랜덤 간격으로 승객을 생성하고 지정된 경로로 이동시킴 """
    while True:
        yield env.timeout(random.randint(*intervals))
        people = random.randint(*people_range)
        for i in range(len(route) - 1):
            env.process(move_people(env, path_containers, route[i], route[i + 1], people))

# 데이터 프레임 설정
capacity_df = pd.DataFrame({
    'A': [0, 4, 0, 0, 0],
    'B': [4, 0, 3, 10, 0],
    'C': [0, 3, 0, 0, 8],
    'D': [0, 10, 0, 0, 13],
    'E': [0, 0, 8, 13, 0]
}, index=['A', 'B', 'C', 'D', 'E'])
time_df = pd.DataFrame({
    'A': [0, 1, 0, 0, 0],
    'B': [1, 0, 3, 4, 0],
    'C': [0, 3, 0, 0, 3],
    'D': [0, 4, 0, 0, 5],
    'E': [0, 0, 3, 5, 0]
}, index=['A', 'B', 'C', 'D', 'E'])

env = simpy.Environment()
path_containers = {node: {} for node in capacity_df.columns}
for col in capacity_df.columns:
    for idx in capacity_df.index:
        if capacity_df[col][idx] > 0:
            path_containers[col][idx] = simpy.Container(env, capacity=capacity_df[col][idx], init=capacity_df[col][idx])

routes = {
    (1): ('A', 'B', 'C', (3, 5), (6, 12)),
    (2): ('A', 'B', 'D', (3, 5), (4, 17)),
    (3): ('C', 'E', (3, 5), (9, 10))
}

for key, value in routes.items():
    env.process(schedule_movement(env, path_containers, value[0:-2], value[-2], value[-1]))

env.run(until=30)
