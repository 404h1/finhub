import requests
from django.conf import settings
from .models import DepositProduct, DepositOption

FSS_BASE = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'

MOCK_PRODUCTS = [
    {'fin_co_no':'0010927','kor_co_nm':'KB국민은행','fin_prdt_cd':'WR0001B','fin_prdt_nm':'KB Star 정기예금','join_way':'인터넷,스마트폰','spcl_cnd':'급여이체 실적 시 우대','join_member':'실명의 개인','etc_note':'자동해지 가능','max_limit':None,'dcls_month':'202601',
     'options':[{'intr_rate_type_nm':'단리','save_trm':6,'intr_rate':3.2,'intr_rate2':3.5},{'intr_rate_type_nm':'단리','save_trm':12,'intr_rate':3.5,'intr_rate2':3.8},{'intr_rate_type_nm':'단리','save_trm':24,'intr_rate':3.3,'intr_rate2':3.6}]},
    {'fin_co_no':'0010001','kor_co_nm':'우리은행','fin_prdt_cd':'WR0002B','fin_prdt_nm':'우리 으뜸 정기예금','join_way':'영업점,인터넷,스마트폰','spcl_cnd':'우리카드 실적 시 우대금리','join_member':'개인 및 개인사업자','etc_note':'중도해지 시 낮은 금리 적용','max_limit':None,'dcls_month':'202601',
     'options':[{'intr_rate_type_nm':'단리','save_trm':6,'intr_rate':3.0,'intr_rate2':3.3},{'intr_rate_type_nm':'단리','save_trm':12,'intr_rate':3.4,'intr_rate2':3.7},{'intr_rate_type_nm':'복리','save_trm':24,'intr_rate':3.2,'intr_rate2':3.5}]},
    {'fin_co_no':'0011625','kor_co_nm':'카카오뱅크','fin_prdt_cd':'WR0003B','fin_prdt_nm':'카카오뱅크 정기예금','join_way':'스마트폰','spcl_cnd':'없음','join_member':'실명의 개인','etc_note':'앱으로만 가입 가능','max_limit':None,'dcls_month':'202601',
     'options':[{'intr_rate_type_nm':'단리','save_trm':6,'intr_rate':3.5,'intr_rate2':3.5},{'intr_rate_type_nm':'단리','save_trm':12,'intr_rate':3.8,'intr_rate2':3.8},{'intr_rate_type_nm':'단리','save_trm':24,'intr_rate':3.6,'intr_rate2':3.6}]},
    {'fin_co_no':'0011001','kor_co_nm':'케이뱅크','fin_prdt_cd':'WR0004B','fin_prdt_nm':'케이뱅크 정기예금','join_way':'스마트폰','spcl_cnd':'케이뱅크 체크카드 실적 시 우대','join_member':'실명의 개인','etc_note':'비대면 전용 상품','max_limit':None,'dcls_month':'202601',
     'options':[{'intr_rate_type_nm':'단리','save_trm':6,'intr_rate':3.4,'intr_rate2':3.7},{'intr_rate_type_nm':'단리','save_trm':12,'intr_rate':3.7,'intr_rate2':4.0},{'intr_rate_type_nm':'단리','save_trm':24,'intr_rate':3.5,'intr_rate2':3.8}]},
    {'fin_co_no':'0013175','kor_co_nm':'토스뱅크','fin_prdt_cd':'WR0005B','fin_prdt_nm':'토스뱅크 정기예금','join_way':'스마트폰','spcl_cnd':'없음','join_member':'실명의 개인','etc_note':'토스 앱으로만 가입 가능','max_limit':None,'dcls_month':'202601',
     'options':[{'intr_rate_type_nm':'단리','save_trm':6,'intr_rate':3.6,'intr_rate2':3.6},{'intr_rate_type_nm':'단리','save_trm':12,'intr_rate':4.0,'intr_rate2':4.0},{'intr_rate_type_nm':'단리','save_trm':24,'intr_rate':3.8,'intr_rate2':3.8}]},
    {'fin_co_no':'0010927','kor_co_nm':'신한은행','fin_prdt_cd':'WR0006B','fin_prdt_nm':'신한 쏠(SOL) 정기예금','join_way':'인터넷,스마트폰','spcl_cnd':'신한카드 실적 또는 급여이체 시 우대','join_member':'실명의 개인','etc_note':'온라인 전용 우대금리 제공','max_limit':None,'dcls_month':'202601',
     'options':[{'intr_rate_type_nm':'단리','save_trm':6,'intr_rate':3.1,'intr_rate2':3.4},{'intr_rate_type_nm':'단리','save_trm':12,'intr_rate':3.5,'intr_rate2':3.85},{'intr_rate_type_nm':'복리','save_trm':36,'intr_rate':3.4,'intr_rate2':3.7}]},
]

def fetch_and_save_products():
    api_key = settings.FSS_API_KEY
    products_data = []
    if api_key:
        try:
            for page in range(1, 3):
                url = f'{FSS_BASE}?auth={api_key}&topFinGrpNo=020000&pageNo={page}'
                r = requests.get(url, timeout=10)
                data = r.json().get('result', {})
                base_list = data.get('baseList', [])
                option_list = data.get('optionList', [])
                for p in base_list:
                    p['options'] = [o for o in option_list if o['fin_prdt_cd'] == p['fin_prdt_cd']]
                products_data.extend(base_list)
                if not base_list:
                    break
        except Exception:
            products_data = MOCK_PRODUCTS
    else:
        products_data = MOCK_PRODUCTS

    saved = 0
    for p in products_data:
        prod, created = DepositProduct.objects.update_or_create(
            fin_prdt_cd=p['fin_prdt_cd'],
            defaults={
                'fin_co_no': p.get('fin_co_no',''),
                'kor_co_nm': p.get('kor_co_nm',''),
                'fin_prdt_nm': p.get('fin_prdt_nm',''),
                'join_way': p.get('join_way',''),
                'spcl_cnd': p.get('spcl_cnd',''),
                'join_member': p.get('join_member',''),
                'etc_note': p.get('etc_note',''),
                'max_limit': p.get('max_limit'),
                'dcls_month': p.get('dcls_month',''),
            }
        )
        if created:
            for o in p.get('options', []):
                DepositOption.objects.create(
                    product=prod,
                    fin_prdt_cd=o.get('fin_prdt_cd', p['fin_prdt_cd']),
                    intr_rate_type_nm=o.get('intr_rate_type_nm',''),
                    save_trm=int(o.get('save_trm', 12)),
                    intr_rate=o.get('intr_rate'),
                    intr_rate2=o.get('intr_rate2'),
                )
            saved += 1
    return saved
