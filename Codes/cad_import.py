import ezdxf
import os

def extract_building_structure(file_path):
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()
    
    # 건물 구조를 저장할 데이터 구조
    building_structure = {
        'floors': [],
        'walls': [],
        'doors': [],
        'windows': []
    }
    
    # 층(floor) 정보 추출
    for entity in msp:
        if entity.dxftype() == 'LINE':
            start_point = entity.dxf.start
            end_point = entity.dxf.end
            # 층을 나타내는 선분의 길이를 이용하여 층 높이 추정 가능
            floor_height = abs(start_point[2] - end_point[2])
            building_structure['floors'].append({
                'height': floor_height
            })
        elif entity.dxftype() == 'LWPOLYLIN E':
            # 벽 정보 추출
            vertices = list(entity.points())
            building_structure['walls'].append({
                'vertices': vertices
            })
        # 추가적으로 문, 창문 정보도 추출 가능
        
    return building_structure

def main():
    dwg_file_path = os.path.join(os.getcwd(), './CADfiles/test1.dxf')
    # 파일 존재 여부 확인
    if not os.path.exists(dwg_file_path):
        print(f"Error: 파일이 존재하지 않습니다 - {dwg_file_path}")
        return
    
    building_structure = extract_building_structure(dwg_file_path)
    print(building_structure)

if __name__ == "__main__":
    main()