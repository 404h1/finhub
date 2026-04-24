# FinHub - 금융 통합 플랫폼

## 실행 방법
```bash
cd finhub
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

서버 실행 후 → http://127.0.0.1:8000

| 경로 | 기능 |
|------|------|
| /products/ | 정기예금 비교 |
| /stocks/ | 주가 기술적 분석 |
| /boards/ | 투자 토론 게시판 |
| /accounts/ | 회원 인증·프로필 |
| /admin/ | 관리자 |
