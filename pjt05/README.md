# PJT 05 · 사용자 인증 & 게시판 권한

## 실행
```bash
pip install -r requirements.txt
pip install pillow  # 프로필 이미지용
python manage.py makemigrations accounts
python manage.py migrate
python manage.py runserver
```

## 요구사항
| 번호 | 내용 | 구분 |
|------|------|------|
| F501 | 커스텀 유저 모델 (nickname, interest_stocks, profile_image) | 필수 |
| F502 | 회원가입 (자동 로그인) | 필수 |
| F503 | 로그인 | 필수 |
| F504 | 로그아웃 | 필수 |
| F505 | 비밀번호 변경 (한글 오류 메시지) | 필수 |
| F506 | 게시글 작성 권한 (로그인 필수 + 작성자 검증) | 필수 |
| F507 | 프로필 페이지 (내 게시글 목록) | 필수 |
| F511 | LLM 투자 성향 분석 | 심화 |

## URL 구조
| 경로 | 설명 |
|------|------|
| `/` | 자산 목록 |
| `/asset/<id>/` | 게시판 |
| `/accounts/signup/` | 회원가입 |
| `/accounts/login/` | 로그인 |
| `/accounts/logout/` | 로그아웃 |
| `/accounts/profile/` | 프로필 |
| `/accounts/password/change/` | 비밀번호 변경 |
