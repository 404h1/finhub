# PJT 01 · Python API 데이터 수집

## 실행 방법
```bash
pip install -r requirements.txt
cp .env.example .env   # API 키 입력 후 저장

# 날씨 (필수)
python weather/weather.py

# 정기예금 (심화)
python deposit/deposit.py
```

## 요구사항
| 번호 | 내용 | 구분 |
|------|------|------|
| F101 | 날씨 응답 Key 출력 | 필수 |
| F102 | main/weather 값 추출 | 필수 |
| F103 | 한글 키 변환 | 필수 |
| F104 | 섭씨 온도 추가 | 필수 |
| F105 | 생성형 AI 활용 | 필수 |
| F111~F115 | 금감원 정기예금 API | 심화 |
