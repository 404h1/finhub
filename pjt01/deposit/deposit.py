"""
PJT 01 심화 - 금감원 정기예금 API 데이터 수집
FSS finlife API 활용
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FSS_API_KEY", "YOUR_FSS_API_KEY_HERE")
BASE_URL = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"


def get_deposit_raw():
    """정기예금 API 호출"""
    params = {
        "auth": API_KEY,
        "topFinGrpNo": "020000",  # 은행
        "pageNo": 1,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()


def f111_print_keys(data):
    """F111: 전체 응답 Key 값 출력"""
    print("=== F111: 응답 Key 목록 ===")
    print(list(data.keys()))
    print(list(data["result"].keys()))


def f112_product_list(data):
    """F112: 정기예금 상품 리스트 추출"""
    print("\n=== F112: 정기예금 상품 목록 ===")
    products = data["result"]["baseList"]
    for p in products:
        print(f"{p['fin_prdt_nm']} ({p['kor_co_nm']})")
    return products


def f113_option_list(data):
    """F113: 옵션(금리) 정보 출력"""
    print("\n=== F113: 옵션 리스트 ===")
    options = data["result"]["optionList"]
    for o in options[:5]:
        print(o)
    return options


def f114_merge_product_option(products, options):
    """F114: 상품 + 옵션 통합 딕셔너리"""
    print("\n=== F114: 상품+옵션 통합 ===")
    product_map = {p["fin_prdt_cd"]: p for p in products}
    merged = []
    for opt in options:
        code = opt["fin_prdt_cd"]
        if code in product_map:
            merged.append({**product_map[code], "option": opt})
    for item in merged[:3]:
        print(f"{item['fin_prdt_nm']} | {item['option']['save_trm']}개월 | {item['option']['intr_rate']}%")
    return merged


if __name__ == "__main__":
    data = get_deposit_raw()
    f111_print_keys(data)
    products = f112_product_list(data)
    options = f113_option_list(data)
    f114_merge_product_option(products, options)
