from __future__ import annotations

import csv
import argparse
from datetime import datetime
import logging
import sys
from typing import Generator
from dataclasses import dataclass

# 추가
import pandas as pd
import json
import simpy
from datetime import datetime, timedelta
import random, os, requests
import isodate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('read_nozzle_audit')

def iso8601_to_datetime(iso8601: str) -> datetime:
    # 밀리초 부분이 3자리가 아닌 경우 처리
    if '.' in iso8601:
        base, ms = iso8601.split('.')
        # 밀리초 부분을 3자리로 맞춤
        ms = ms.ljust(3, '0')
        iso8601 = f"{base}.{ms}"
    return datetime.fromisoformat(iso8601)
       
@dataclass
class NozzleProductionAudit:
    Timestamp: datetime
    QuantityProduced: int
    AvgProcessingTime: float
    AvgWaitingTime: float
    DefectVolume: int
    AvgDefectRate: float

    def __repr__(self):
        formatted_ts = self.Timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-5]
        return (
            f"NozzleProductionAudit: "
            f"Timestamp={formatted_ts}, "
            f"QuantityProduced={self.QuantityProduced}, "
            f"AvgProcessingTime={self.AvgProcessingTime:.2f}s, "
            f"AvgWaitingTime={self.AvgWaitingTime:.2f}s, "
            f"DefectVolume={self.DefectVolume}, "
            f"AvgDefectRate={self.AvgDefectRate:.3f} ({self.DefectVolume}/{self.QuantityProduced})"
        )

def define_args(parser):
    parser.add_argument("--nozzleProduction", type=str, required=True)
    parser.add_argument("--outputFile", type=str, required=True)
    
def estimate_throughput(audit: NozzleProductionAudit) -> float: 
    # JSON 파일을 읽고 DataFrame으로 변환하는 함수
    def read_json_file(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        # 데이터를 DataFrame으로 변환
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame([data])
        return df

    # 각 JSON 파일을 DataFrame으로 읽어오기 (audit 값으로 대체할 것들은 아래에서 대체)
    planwork_df = read_json_file('planwork.json')
    planoperation_df = read_json_file('planoperation.json')
    product_df = read_json_file('product.json')
    resourceinven_df = read_json_file('resourceinven.json')

    # audit 값으로 DataFrame 생성 (기존 json 파일 대신)
    simul_quantity_produced_df = pd.DataFrame([{"Quantity": audit.QuantityProduced}])
    simul_defect_rate_df = pd.DataFrame([{"AvgDefectRate": audit.AvgDefectRate}])
    simul_defect_volume_df = pd.DataFrame([{"Volume": audit.DefectVolume}])
    simul_processing_time_df = pd.DataFrame([{"AvgProcessingTime": audit.AvgProcessingTime}])
    simul_waiting_time_df = pd.DataFrame([{"AvgWaitingTime": audit.AvgWaitingTime}])

    # simulation_time.txt 파일에서 날짜 읽기 대신 audit.Timestamp 사용
    now = audit.Timestamp
    simulation_time_str = now.strftime('%Y-%m-%d %H:%M:%S')

    # 운영 시작 시간 결정
    work_start_time = datetime(now.year, now.month, now.day, 8, 0, 0)
    if now < work_start_time:
        start_time = work_start_time
    else:
        start_time = now

    operating_time_hours = int(planwork_df.loc[planwork_df['WK_SHOP_CD'] == 'XD-01', 'WK_TIME'].values[0])
    end_time = start_time + timedelta(hours=operating_time_hours)
    remaining_time_seconds = (end_time - start_time).total_seconds()

    # 이미 생산된 수량 차감 (O)
    def adjust_quantities(planoperation_df, simul_quantity_produced_df):
        produced_qty = simul_quantity_produced_df['Quantity'].astype(int).sum()
        planoperation_df = planoperation_df.sort_values(by='WK_ORD_NO')
        produced_by_product = {}
        for index, row in planoperation_df.iterrows():
            if produced_qty <= 0:
                break
            product_id = row['PRODUCT_ID']
            if product_id not in produced_by_product:
                produced_by_product[product_id] = 0
            if row['QTY'] <= produced_qty:
                produced_by_product[product_id] += row['QTY']
                produced_qty -= row['QTY']
                planoperation_df.at[index, 'QTY'] = 0
            else:
                produced_by_product[product_id] += produced_qty
                planoperation_df.at[index, 'QTY'] -= produced_qty
                produced_qty = 0
        return planoperation_df[planoperation_df['QTY'] > 0], produced_by_product

    adjusted_planoperation_df, produced_by_product = adjust_quantities(planoperation_df, simul_quantity_produced_df)

    # 불량 제품 수량 반영 (O)
    def calculate_defects(produced_by_product, simul_defect_volume_df):
        total_defects_volume = simul_defect_volume_df['Volume'].sum()
        total_produced_qty = sum(produced_by_product.values())
        defect_ratio = total_defects_volume / total_produced_qty if total_produced_qty > 0 else 0
        defects_by_product = {}
        for product_id, qty in produced_by_product.items():
            defects_by_product[product_id] = int(qty * defect_ratio)
        return defects_by_product

    defects_by_product = calculate_defects(produced_by_product, simul_defect_volume_df)

    # 현재 시간, 제품 ID, 정상 제품 생산량, 불량 제품 생산량 처리
    def process_produced_by_product(produced_by_product, defects_by_product):
        processed_data = []
        current_time = datetime.strptime(simulation_time_str, '%Y-%m-%d %H:%M:%S')
        for product_id, qty in produced_by_product.items():
            defect_qty = defects_by_product.get(product_id, 0)
            normal_qty = qty - defect_qty
            processed_data.append({
                "현재 시간": current_time,
                "Product_ID": product_id,
                "정상 제품 생산량": normal_qty,
                "불량 제품 생산량": defect_qty
            })
        return processed_data

    processed_produced_data = process_produced_by_product(produced_by_product, defects_by_product)

    # 초기 재고 업데이트
    def initial_inventory_update(produced_by_product, product_df, resourceinven_df):
        for product_id, qty in produced_by_product.items():
            parts_needed = product_df[product_df['PRODUCT_ID'] == product_id]['Part_ID']
            for part in parts_needed:
                resourceinven_df.loc[resourceinven_df['PART_ID'] == part, 'GOOD_INV_QTY'] -= qty
        return resourceinven_df

    resourceinven_df = initial_inventory_update(produced_by_product, product_df, resourceinven_df)

    # 시뮬레이션 매개변수
    avg_defect_rate = simul_defect_rate_df['AvgDefectRate'].values[0]
    avg_processing_time = simul_processing_time_df['AvgProcessingTime'].values[0]  # 초 단위
    avg_waiting_time = simul_waiting_time_df['AvgWaitingTime'].values[0]  # 초 단위

    # 시뮬레이션 결과 저장용 변수
    cumulative_production = []
    total_production = {}
    total_defects = {}
    equipment_utilization = []
    total_operating_time = 0
    productive_time = 0

    # 초기 누적 생산량 설정
    for data in processed_produced_data:
        cumulative_production.append((
            data["현재 시간"], 
            data["Product_ID"], 
            data["정상 제품 생산량"], 
            data["불량 제품 생산량"]
        ))
        if data["Product_ID"] not in total_production:
            total_production[data["Product_ID"]] = {"정상 제품 생산량": data["정상 제품 생산량"], "불량 제품 생산량": data["불량 제품 생산량"]}
        else:
            total_production[data["Product_ID"]]["정상 제품 생산량"] += data["정상 제품 생산량"]
            total_production[data["Product_ID"]]["불량 제품 생산량"] += data["불량 제품 생산량"]

    # 부품 소요 추적 및 재고 업데이트 함수
    def update_inventory(product_df, resourceinven_df, product_id, produced_qty):
        parts_needed = product_df[product_df['PRODUCT_ID'] == product_id]['Part_ID']
        for part in parts_needed:
            resourceinven_df.loc[resourceinven_df['PART_ID'] == part, 'GOOD_INV_QTY'] -= produced_qty

    # 추가된 10분 단위 결과 저장용 변수
    incremental_production = []
    incremental_utilization = []
    total_production_at_noon = []  # 12:00:00 시점의 생산량을 기록할 리스트
    overall_total_production_at_noon = []  # 12:00:00 시점의 전체 총 생산량을 기록할 리스트
    # 초기화 코드 추가
    last_incremental_normal_production = 0
    last_incremental_defective_production = 0
    # 추가된 22:00:00 시점 결과 저장용 변수
    total_production_at_10pm = []  # 22:00:00 시점의 생산량을 기록할 리스트
    overall_total_production_at_10pm = []  # 22:00:00 시점의 전체 총 생산량을 기록할 리스트
    ten_pm_logged = False  # 22:00:00 시점에서의 기록 여부
    # 추가된 24:00:00 시점 결과 저장용 변수
    total_production_at_24pm = []  # 24:00:00 시점의 생산량을 기록할 리스트
    overall_total_production_at_24pm = []  # 24:00:00 시점의 전체 총 생산량을 기록할 리스트
    zero_pm_logged = False  # 24:00:00 시점에서의 기록 여부



    # SimPy 환경 설정
    def machine(env, remaining_time_seconds, adjusted_planoperation_df, product_df, resourceinven_df, start_time):
        nonlocal total_operating_time, productive_time
        last_logged_time = 0
        last_incremental_log_time = 0
        noon_logged = False
        ten_pm_logged = False
        zero_pm_logged = False

        def get_current_sim_time():
            return start_time + timedelta(seconds=int(env.now))

        for index, row in adjusted_planoperation_df.iterrows():
            qty_to_produce = row['QTY']
            product_id = row['PRODUCT_ID']
            total_production[product_id] = total_production.get(product_id, {"정상 제품 생산량": 0, "불량 제품 생산량": 0})
            total_defects[product_id] = total_defects.get(product_id, 0)
            last_incremental_normal_production = total_production[product_id]["정상 제품 생산량"]
            last_incremental_defective_production = total_production[product_id]["불량 제품 생산량"]

            while qty_to_produce > 0 and env.now < remaining_time_seconds:
                current_time = get_current_sim_time()
                current_hour = current_time.hour
                current_minute = current_time.minute
                current_second = current_time.second

   
                if (current_hour == 11 and current_minute >= 50) or (current_hour == 21 and current_minute >= 50) or (current_hour == 23 and current_minute >= 50):
                    yield env.timeout(10)
                else:
                    yield env.timeout(38)

                current_time = get_current_sim_time()

                # 12:00:00 시점에 기록
                if not noon_logged and current_hour == 12 and current_minute == 0 and current_second <= 10:
                    total_qty_all_products = 0
                    for pid, production_data in total_production.items():
                        total_qty = production_data["정상 제품 생산량"] + production_data["불량 제품 생산량"]
                        total_qty_all_products += total_qty
                        total_production_at_noon.append((get_current_sim_time(), pid, total_qty))
                    overall_total_production_at_noon.append((get_current_sim_time(), total_qty_all_products))
                    noon_logged = True

                # 22:00:00 시점에 기록
                if not ten_pm_logged and current_hour == 22 and current_minute == 0 and current_second <= 10:
                    print(f"[22:00 기록] {get_current_sim_time()} | total_production: {total_production}")
                    total_qty_all_products = 0
                    for pid, production_data in total_production.items():
                        total_qty = production_data["정상 제품 생산량"] + production_data["불량 제품 생산량"]
                        total_qty_all_products += total_qty
                        total_production_at_10pm.append((get_current_sim_time(), pid, total_qty))
                    overall_total_production_at_10pm.append((get_current_sim_time(), total_qty_all_products))
                    ten_pm_logged = True

                # 24:00:00 시점에 기록
                if not zero_pm_logged and current_hour == 23 and current_minute == 58 and current_second <= 50:
                    total_qty_all_products = 0
                    for pid, production_data in total_production.items():
                        total_qty = production_data["정상 제품 생산량"] + production_data["불량 제품 생산량"]
                        total_qty_all_products += total_qty
                        total_production_at_24pm.append((get_current_sim_time(), pid, total_qty))
                    overall_total_production_at_24pm.append((get_current_sim_time(), total_qty_all_products))
                    zero_pm_logged = True

                # 휴게 시간 체크
                if (current_hour == 12 and current_minute >= 0) or (current_hour == 17 and current_minute < 30):
                    if current_hour == 12:
                        yield env.timeout(1 * 3600)  # 1시간 대기
                    else:
                        yield env.timeout(0.5 * 3600)  # 30분 대기
                else:
                    # 설비 운영 및 생산
                    qty_to_produce -= 2  # 생산마다 제품 2개 출력
                    productive_time += avg_processing_time

                    # 정상 및 불량 제품에 대해 부품 재고 차감
                    update_inventory(product_df, resourceinven_df, product_id, 1)
                    if random.random() < avg_defect_rate:
                        total_production[product_id]["불량 제품 생산량"] += 2
                    else:
                        total_production[product_id]["정상 제품 생산량"] += 2

                    # 다음 제품 생산을 위한 대기 시간
                    yield env.timeout(avg_waiting_time)

                    # 누적 생산량 기록
                    if env.now - last_logged_time >= 10 * 60:  # 10분 간격
                        cumulative_production.append((get_current_sim_time(), product_id, total_production[product_id]["정상 제품 생산량"], total_production[product_id]["불량 제품 생산량"]))
                        utilization = productive_time / env.now
                        equipment_utilization.append((get_current_sim_time(), utilization))
                        last_logged_time = env.now

                    # 10분 간격으로 기록
                    if env.now - last_incremental_log_time >= 10 * 60:
                        incremental_production.append((
                            get_current_sim_time(),
                            product_id,
                            total_production[product_id]["정상 제품 생산량"] - last_incremental_normal_production,
                            total_production[product_id]["불량 제품 생산량"] - last_incremental_defective_production
                        ))
                        # 가동률 계산
                        utilization = productive_time / env.now
                        incremental_utilization.append((get_current_sim_time(), utilization))
                        # 마지막 기록 값 업데이트
                        last_incremental_normal_production = total_production[product_id]["정상 제품 생산량"]
                        last_incremental_defective_production = total_production[product_id]["불량 제품 생산량"]
                        last_incremental_log_time = env.now
                    if qty_to_produce == 0:
                        print(f"[Sim] {get_current_sim_time()} | {product_id} 생산 완료")
        total_operating_time = env.now

    env = simpy.Environment()
    env.process(machine(env, remaining_time_seconds, adjusted_planoperation_df, product_df, resourceinven_df, start_time))
    env.run(until=remaining_time_seconds)


    # 시뮬레이션 종료 후, 22:00:00 시점의 생산량이 기록되지 않았다면 강제로 기록
    if not overall_total_production_at_10pm:
        target_time = start_time.replace(hour=22, minute=0, second=0, microsecond=0)
        total_qty_all_products = 0
        for pid, production_data in total_production.items():
            total_qty = production_data["정상 제품 생산량"] + production_data["불량 제품 생산량"]
            total_qty_all_products += total_qty
            total_production_at_10pm.append((target_time, pid, total_qty))
        overall_total_production_at_10pm.append((target_time, total_qty_all_products))

    # 22:00:00 시점의 전체 제품 총 생산량 저장
    if overall_total_production_at_10pm:
        overall_total_production_10pm_df = pd.DataFrame(overall_total_production_at_10pm, columns=['DATETIME', '총 생산량'])
        return overall_total_production_10pm_df['총 생산량'].iloc[-1]
    else:
        return 0

def read_audit_csv(file_path: str, delimiter: str = ",") -> Generator[NozzleProductionAudit, None, None]:
    """
    CSV 파일을 읽어서 NozzleProductionAudit 객체를 생성하는 제너레이터
    
    Args:
        file_path: CSV 파일 경로
        delimiter: CSV 구분자 (기본값: 쉼표)
        
    Yields:
        NozzleProductionAudit: CSV의 각 행을 변환한 객체
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            try:
                # CSV의 각 필드를 NozzleProductionAudit 객체의 필드에 맞게 변환
                audit_data = {
                    'Timestamp': datetime.fromisoformat(row['timestamp']),
                    'QuantityProduced': int(row['quantity_produced']),
                    'AvgProcessingTime': float(row['avg_processing_time'])/1000,
                    'AvgWaitingTime': float(row['avg_waiting_time'])/1000,
                    'DefectVolume': int(row['defect_volume']),
                    'AvgDefectRate': float(row['avg_defect_rate'])
                }
                audit = NozzleProductionAudit(**audit_data)
                yield audit
            except (KeyError, ValueError) as e:
                logger.error(f"Error processing row: {row}, Error: {e}")
                continue

def run(args):
    print(f'input[nozzleProduction]: {args.nozzleProduction}')
    print('--------------------------------------------------')

    input = json.loads(args.nozzleProduction)
    ts = input['Timestamp']
    input['Timestamp'] = iso8601_to_datetime(ts)
    input['AvgProcessingTime'] = isodate.parse_duration(input['AvgProcessingTime']).total_seconds()
    input['AvgWaitingTime'] = isodate.parse_duration(input['AvgWaitingTime']).total_seconds()
    input['AvgDefectRate'] = float(input['AvgDefectRate'])
    input['QuantityProduced'] = int(input['QuantityProduced'])
    input['DefectVolume'] = int(input['DefectVolume'])
    audit = NozzleProductionAudit(**input)
    print(f"Processing audit: {audit}")

    throughput = estimate_throughput(audit)
    with open(args.outputFile, 'w') as f:
        result = json.dumps({ 'Value': f'{throughput}', 'Timestamp':  ts })
        f.write(result)
        print(f"Estimated throughput: {result}")

def main():
    parser = argparse.ArgumentParser(description="Read nozzle production audit records from CSV")
    define_args(parser)
    args = parser.parse_args()
    run(args)

if __name__ == '__main__':
    main() 

    
