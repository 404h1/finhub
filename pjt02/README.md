# PJT 02 · 넷플릭스 주가 데이터 분석

## 준비
1. [Kaggle](https://www.kaggle.com/datasets/akpmpr/netflix-stock-price-prediction) 에서 `NFLX.csv` 다운로드
2. `archive/NFLX.csv` 에 위치

## 실행
```bash
pip install -r requirements.txt
python netflix_analysis.py
```

## 요구사항
| 번호 | 내용 | 구분 |
|------|------|------|
| F202 | CSV 읽기 + 컬럼 선택 | 필수 |
| F203 | 2021년 이후 필터링 | 필수 |
| F204 | 최고/최저 종가 추출 | 필수 |
| F205 | 월별 평균 종가 시각화 | 필수 |
| F206 | High/Low/Close 복합 차트 | 필수 |
| F211 | AI 주가 예측 | 심화 |
