import pandas as pd
import simpy
import ast

# CSV 파일에서 노드별 경로 데이터 로드
def load_paths_from_csv(filename):
    df = pd.read_csv(filename)
    paths = {}
    for _, row in df.iterrows():
        node = str(row['Node']).strip()
        path = ast.literal_eval(row['Path'])
        paths[node] = path
    return paths

# 엑셀 파일에서 노드 간 거리 데이터 로드
def load_excel_data(filename):
    df = pd.read_excel(filename, index_col=0)
    df.index = df.index.map(lambda x: str(x).strip())
    df.columns = df.columns.map(lambda x: str(x).strip())
    return df

# 엑셀 파일에서 노드별 인원 데이터 로드
def load_final_output_data(filename):
    return pd.read_excel(filename)

# 엑셀 파일에서 노드별 최대 인원 데이터 로드
def load_node_capacity(filename):
    df = pd.read_excel(filename, index_col=0)
    df.index = df.index.map(lambda x: str(x).strip())

    # NaN을 기본값으로 바꿔서 딕셔너리로 변환
    return df['optimum'].fillna(4).astype(int).to_dict()

# 시뮬레이션 결과 저장용 클래스
class SimulationRecorder:
    def __init__(self):
        self.records = []

    def record(self, day, time, total_time, from_node, to_node):
        self.records.append({"Day": day, "StartTime": time, "Time": total_time, "From": from_node, "To": to_node})

    def to_excel(self, filename):
        df = pd.DataFrame(self.records)
        df.to_excel(filename, index=False)

# 노드별 대기 시간 기록용 클래스
class NodeWaitRecorder:
    def __init__(self):
        self.records = {}

    def record_wait_time(self, node, wait_time):
        if node not in self.records:
            self.records[node] = []
        self.records[node].append(wait_time)

    def to_excel(self, filename):
        wait_time_averages = [{"Node": node, "Average Wait Time": sum(times) / len(times)} for node, times in self.records.items()]
        df = pd.DataFrame(wait_time_averages)
        df.to_excel(filename, index=False)

# 시뮬레이션 환경 설정 클래스
class BuildingEvacuation:
    def __init__(self, env, graph, recorder, wait_recorder, speed_m_per_s, node_capacity, exits):
        self.env = env
        self.graph = graph
        self.recorder = recorder
        self.wait_recorder = wait_recorder
        self.speed_m_per_s = speed_m_per_s
        self.node_capacity = node_capacity
        self.exits = exits  # 출구 목록

    def initialize_resources(self, paths):
        all_nodes = set()
        for path in paths.values():
            all_nodes.update(map(str, path))

        resources = {}
        for node in all_nodes:
            node = str(node).strip()
            if node in self.exits:
                # 출구는 용량을 크게 설정
                resources[node] = simpy.Resource(self.env, capacity=int(1e6))
            else:
                # 노드 용량 가져오고 NaN인 경우 기본 용량을 지정
                capacity = self.node_capacity.get(node, None)
                if pd.isna(capacity) or capacity is None:
                    capacity = 4  # 기본값을 4로 설정
                resources[node] = simpy.Resource(self.env, capacity=int(capacity))
        return resources

    def evacuate(self, day, start_time, people_count, path, resources):
        print(f"경로 이동 시작: {path} (요일: {day}, 시작 시간: {start_time}, 인원 수: {people_count})")
        from_node = str(path[0])
        if from_node not in resources:
            print(f"경고: 노드 '{from_node}'에 대한 리소스를 찾을 수 없습니다.")
            return

        total_time_s = 0

        for i in range(0, people_count, resources[from_node].capacity):
            remaining_people = min(resources[from_node].capacity, people_count - i)
            try:
                with resources[from_node].request() as req:
                    wait_start = self.env.now  # 대기 시작 시간
                    yield req
                    wait_time = self.env.now - wait_start  # 대기 시간
                    self.wait_recorder.record_wait_time(from_node, wait_time)

                    for j in range(len(path) - 1):
                        from_node, to_node = str(path[j]), str(path[j + 1])
                        try:
                            distance_mm = self.graph.at[from_node, to_node]
                            distance_m = distance_mm / 1000
                            travel_time_s = distance_m / self.speed_m_per_s
                            yield self.env.timeout(travel_time_s)
                            total_time_s = self.env.now
                        except KeyError as e:
                            print(f"경로에 오류가 있습니다. '{from_node}'에서 '{to_node}'으로 이동하려 했으나 키 에러 발생: {e}")
                            return
            except KeyError as e:
                print(f"리소스 요청에 문제가 발생했습니다: {e}")
                return

        total_time_min = total_time_s / 60
        final_destination = str(path[-1])
        self.recorder.record(day, start_time, total_time_min, path[0], final_destination)
        print(f"{total_time_min:.2f} 분: 요일 {day}, {start_time}에 {path[0]}에서 {final_destination}까지 이동 완료")

# 시계 시간 계산 함수
def next_half_hour_time(time):
    hours = time // 100
    minutes = time % 100
    minutes += 30
    if minutes >= 60:
        hours += 1
        minutes -= 60
    return hours * 100 + minutes

# 시뮬레이션 실행 함수
def simulate_time_intervals(graph_filename, paths_filename, final_output_filename, node_capacity_filename, output_filename, wait_time_filename, speed_m_per_s):
    env = simpy.Environment()
    distance_data = load_excel_data(graph_filename)
    paths = load_paths_from_csv(paths_filename)
    final_data = load_final_output_data(final_output_filename)
    node_capacity = load_node_capacity(node_capacity_filename)

    # 정확한 출구 노드 목록을 포함합니다.
    exits = ["출구1", "출구2-1", "출구2-2", "출구3", "출구4", "출구5", "출구6", "출구7"]

    recorder = SimulationRecorder()
    wait_recorder = NodeWaitRecorder()
    building = BuildingEvacuation(env, distance_data, recorder, wait_recorder, speed_m_per_s, node_capacity, exits)

    print("시뮬레이션 시작")
    for day in final_data['Day Number'].unique():
        day_data = final_data[final_data['Day Number'] == day]
        time = 900
        while time <= 2200:
            current_data = day_data[(day_data['Start Time'] <= time) & (day_data['End Time'] >= time)]
            resources = building.initialize_resources(paths)
            for _, row in current_data.iterrows():
                people_count = row['Adjusted People Count']
                node = str(row['Node']).strip()
                if node in paths:
                    path = paths[node]
                    print(f"노드 {node}에 대한 이동 경로 프로세스 시작 (요일: {day}, 시작 시간: {time}, 인원 수: {people_count})")
                    env.process(building.evacuate(day, time, people_count, path, resources))
            time = next_half_hour_time(time)

    env.run()
    print("시뮬레이션 완료")

    recorder.to_excel(output_filename)
    wait_recorder.to_excel(wait_time_filename)

# 시뮬레이션 실행
simulate_time_intervals('DistanceBtwnNodes.xlsx', 'shortest_paths.csv', 'Final_output.xlsx', 'NodeCapacity.xlsx', 'simulation_results_final.xlsx', 'node_wait_times.xlsx', 1.2)
