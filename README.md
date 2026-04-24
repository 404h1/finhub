# FinHub · 금융 통합 플랫폼

> 정기예금 비교 · 주가 기술 분석 · 투자 토론을 한 곳에서

**[🌐 데모 보기](https://404h1.github.io/finhub/)**

---

## 주요 기능

| 기능 | 설명 |
|------|------|
| 🏦 금융상품 비교 | 금감원 API 기반 정기예금 금리 은행별·기간별 비교 |
| 📈 주가 기술 분석 | EMA / RSI / MACD / 볼린저밴드 / ADX + LONG·SHORT 신호 |
| 💬 투자 토론 | 자산별 커뮤니티 게시판 (AAPL, BTC, 삼성전자 등) |
| 👤 투자 프로필 | 커스텀 유저 모델 · 성향 설정 · 프로필 이미지 |

## 기술 스택

`Django 4.x` `Python` `SQLite` `yfinance` `Plotly.js` `Bootstrap 5` `금감원 API`

## 로컬 실행

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## URL 구조

| 경로 | 설명 |
|------|------|
| `/` | 홈 |
| `/products/` | 금융상품 비교 |
| `/stocks/` | 주가 분석 |
| `/boards/` | 투자 토론 |
| `/accounts/` | 로그인·회원가입·프로필 |
