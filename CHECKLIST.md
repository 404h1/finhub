# FinHub 프로젝트 체크리스트

> 필수 / 심화(선택) 요구사항 구현 현황  
> 마지막 업데이트: 2026-04-24

---

## PJT 01 — API 데이터 수집 (`pjt01/`)

### 필수 — 날씨 API (`pjt01/weather/weather.py`)

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F101 | OpenWeatherMap API 응답 Key 목록 출력 | ✅ | `weather.py` → `f101_print_keys()` | `list(data.keys())` 출력 |
| F102 | `main`, `weather` 키 딕셔너리로 추출 | ✅ | `weather.py` → `f102_extract_main_weather()` | dict 반환 |
| F103 | 추출 데이터 한글 키로 변환 | ✅ | `weather.py` → `f103_korean_keys()` | 온도·체감온도·습도·날씨상태 등 |
| F104 | 섭씨 온도 필드 추가 | ✅ | `weather.py` → `f104_add_celsius()` | `섭씨온도` 키 추가 |

### 심화(선택) — 금감원 정기예금 API (`pjt01/deposit/deposit.py`)

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F111 | FSS finlife API 응답 Key 목록 출력 | ✅ | `deposit.py` → `f111_print_keys()` | result 하위 키 포함 |
| F112 | 정기예금 상품 목록 출력 | ✅ | `deposit.py` → `f112_product_list()` | `baseList` 파싱 |
| F113 | 옵션(금리) 목록 출력 | ✅ | `deposit.py` → `f113_option_list()` | `optionList` 파싱 |
| F114 | 상품 + 옵션 통합 딕셔너리 생성 | ✅ | `deposit.py` → `f114_merge_product_option()` | `fin_prdt_cd` 기준 병합 |

**환경 설정**
- `.env.example` 제공 (`OPENWEATHER_API_KEY`, `FSS_API_KEY`)
- `requirements.txt`: `requests`, `python-dotenv`

---

## PJT 02 — 데이터 분석 (`pjt02/`)

### 필수 — 넷플릭스 주가 분석 (`pjt02/netflix_analysis.py`)

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F202 | CSV 파일 읽기 + 필요 컬럼 선택 | ✅ | `netflix_analysis.py` → `f202_load_data()` | Date·Open·High·Low·Close |
| F203 | 2021년 이후 데이터 필터링 | ✅ | `netflix_analysis.py` → `f203_filter_after_2021()` | `df["Date"] >= "2021-01-01"` |
| F204 | 최고/최저 종가 날짜·가격 추출 | ✅ | `netflix_analysis.py` → `f204_max_min_close()` | `idxmax()` / `idxmin()` |
| F205 | 월별 평균 종가 bar 차트 시각화 | ✅ | `netflix_analysis.py` → `f205_monthly_avg_close()` | `monthly_avg_close.png` 저장 |
| F206 | High / Low / Close 3개 지표 선 차트 | ✅ | `netflix_analysis.py` → `f206_high_low_close_chart()` | `high_low_close.png` 저장 |

**환경 설정**
- `requirements.txt`: `pandas`, `matplotlib`
- 데이터 파일: `archive/NFLX.csv` (Kaggle에서 별도 다운로드)
- `archive/.gitkeep`으로 빈 폴더 추적

---

## PJT 03 — Bootstrap 정적 페이지 (`pjt03/`)

### 필수 — 프로필 페이지 (`pjt03/profile.html`)

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F301 | Bootstrap 5 반응형 레이아웃 | ✅ | `profile.html` | CDN 방식 |
| F302 | 프로필 이미지 + 기본 정보 섹션 | ✅ | `profile.html` | 아바타 원형 카드 |
| F303 | 관심 종목 배지 목록 | ✅ | `profile.html` | badge 컴포넌트 |
| F304 | 내비게이션 바 | ✅ | `profile.html` + `portfolio.html` | navbar-expand-lg |
| F305 | 포트폴리오 페이지 링크 | ✅ | `profile.html` → `portfolio.html` 링크 | 별도 파일로 분리 |

### 심화(선택) — 포트폴리오 페이지 (`pjt03/portfolio.html`)

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F311 | 포트폴리오 카드 그리드 | ✅ | `portfolio.html` | row-cols-md-3 그리드 |
| F312 | 수익률 표시 (상승/하락 색상) | ✅ | `portfolio.html` | text-success / text-danger |

---

## PJT 04 — Django 커뮤니티 (`pjt04/`)

### 필수 — 커뮤니티 CRUD (`pjt04/community/`)

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F401 | 게시글 목록 조회 | ✅ | `views.py` → `board()` | `Post.objects.all()` |
| F402 | 게시글 상세 조회 | ✅ | `views.py` → `post_detail()` | `get_object_or_404` |
| F403 | 게시글 작성 | ✅ | `views.py` → `post_create()` | ModelForm 처리 |
| F404 | 게시글 수정 | ✅ | `views.py` → `post_update()` | `instance=post` |
| F405 | 게시글 삭제 | ✅ | `views.py` → `post_delete()` | POST only |
| F406 | 자산 목록 메인 페이지 | ✅ | `views.py` → `asset_list()` | `data/assets.json` 로드 |

### 심화(선택) — LLM 투자성향 분석 (`pjt04/community/llm.py`)

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F411 | OpenAI API 연동 | ✅ | `llm.py` | `openai` 라이브러리 |
| F412 | 투자성향 분석 기능 | ✅ | `llm.py` + `utils.py` | 게시글 기반 분석 |

---

## PJT 05 — Django 회원 인증 (`pjt05/`)

### 필수 — 커스텀 유저 모델 (`pjt05/accounts/`)

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F501 | AbstractUser 기반 커스텀 유저 모델 | ✅ | `accounts/models.py` → `class User(AbstractUser)` | `AUTH_USER_MODEL = "accounts.User"` 설정 |
| F501 | nickname 필드 | ✅ | `accounts/models.py` | `CharField(max_length=50)` |
| F501 | interest_stocks 필드 (관심 종목) | ✅ | `accounts/models.py` | 쉼표 구분 문자열, `get_interest_stocks_list()` 메서드 포함 |
| F501 | profile_image 필드 | ✅ | `accounts/models.py` | `ImageField(upload_to="profiles/")`, pillow 필요 |

### 필수 — 회원가입 (`accounts/views.py`, `accounts/forms.py`)

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F502 | 회원가입 폼 + 뷰 | ✅ | `views.py` → `signup()` | `CustomUserCreationForm` 사용 |
| F502 | 가입 후 자동 로그인 | ✅ | `views.py` → `signup()` | `login(request, user)` 즉시 호출 |
| F502 | 관심 종목 다중 선택 (MultipleChoiceField) | ✅ | `forms.py` → `CustomUserCreationForm` | CheckboxSelectMultiple → 쉼표 join 저장 |
| F502 | 프로필 이미지 업로드 | ✅ | `forms.py` | `request.FILES` 처리 |

### 필수 — 로그인 / 로그아웃

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F503 | 로그인 뷰 | ✅ | `views.py` → `login_view()` | `AuthenticationForm` 사용 |
| F503 | 로그인 후 next 파라미터 redirect | ✅ | `views.py` | `request.GET.get("next", ...)` |
| F504 | 로그아웃 뷰 (POST only) | ✅ | `views.py` → `logout_view()` | GET 접근 시 redirect만 |

### 필수 — 비밀번호 변경

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F505 | 비밀번호 변경 뷰 (`@login_required`) | ✅ | `views.py` → `password_change()` | `update_session_auth_hash` 포함 |
| F505 | 한글 에러 메시지 | ✅ | `forms.py` → `CustomPasswordChangeForm` | 현재/새 비밀번호 오류 메시지 한글화 |

### 필수 — 프로필 페이지

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F506 | 프로필 조회 (`@login_required`) | ✅ | `views.py` → `profile()` | 닉네임·관심종목·작성글 표시 |
| F506 | 내가 작성한 게시글 목록 | ✅ | `views.py` → `profile()` | `Post.objects.filter(author=request.user.username)` |

### 필수 — 게시글 권한 관리

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F507 | 게시글 작성 시 `@login_required` | ✅ | `community/views.py` → `post_create()` | `LOGIN_URL` 설정으로 자동 redirect |
| F507 | 작성자만 수정/삭제 가능 | ✅ | `community/views.py` → `post_update()` / `post_delete()` | `post.author == request.user.username` 체크 |
| F507 | 비작성자 수정/삭제 버튼 숨김 | ✅ | `community/templates/community/post_detail.html` | `{% if is_author %}` 조건부 렌더링 |
| F507 | 비작성자 접근 시 에러 메시지 | ✅ | `community/views.py` | "본인이 작성한 게시글만 수정·삭제할 수 있습니다" |

### 심화(선택) — UI/UX

| ID | 요구사항 | 상태 | 구현 위치 | 비고 |
|----|---------|------|-----------|------|
| F511 | 헤더 인증 상태 분기 | ✅ | `community/templates/community/base.html` | 로그인 시 닉네임+프로필+로그아웃 / 비로그인 시 로그인+회원가입 |
| F511 | 기존 디자인 유지 (Noto Sans KR + teal #0d9488) | ✅ | `base.html` + 모든 accounts 템플릿 | 사용자 디자인 보존 |

**Django 설정 (`pjt05/config/settings.py`)**
- `AUTH_USER_MODEL = "accounts.User"` ✅
- `MEDIA_URL`, `MEDIA_ROOT` ✅
- `LOGIN_URL = "accounts:login"` ✅
- `LOGIN_REDIRECT_URL = "community:asset_list"` ✅

**URL 설정 (`pjt05/config/urls.py`)**
- `path("accounts/", include("accounts.urls"))` ✅
- `static(MEDIA_URL, document_root=MEDIA_ROOT)` ✅

> ⚠️ **실행 전 필수**: `python manage.py makemigrations accounts` → `python manage.py migrate` 실행 필요  
> ⚠️ **pillow 설치 필요**: `pip install pillow` (profile_image ImageField 사용 시)

---

## 공통 — 데모 페이지 (`docs/`)

| 항목 | 상태 | 위치 | 비고 |
|------|------|------|------|
| 메인 타임라인 (PJT01~05) | ✅ | `docs/index.html` | 5열 그리드, 각 PJT 컬러 테마 |
| PJT01 데모 페이지 | ✅ | `docs/pjt01/index.html` | 파란 테마 |
| PJT02 데모 페이지 | ✅ | `docs/pjt02/index.html` | 보라 테마 |
| PJT03 데모 페이지 | ✅ | `docs/pjt03/index.html` | 초록 테마 |
| PJT04 데모 페이지 | ✅ | `docs/pjt04/index.html` | 인디고 테마 |
| PJT05 데모 페이지 | ✅ | `docs/pjt05/index.html` | 앰버 테마 |
| file:// 직접 열기 지원 | ✅ | 모든 docs HTML | `href="pjtXX/index.html"` 명시 |

---

## 폴더 구조

```
finhub-1524/
├── pjt01/              # API 데이터 수집 (날씨 + 정기예금)
│   ├── weather/weather.py
│   ├── deposit/deposit.py
│   ├── .env.example
│   └── requirements.txt
├── pjt02/              # 데이터 분석 (넷플릭스 주가)
│   ├── netflix_analysis.py
│   ├── archive/.gitkeep
│   └── requirements.txt
├── pjt03/              # Bootstrap 정적 페이지
│   ├── profile.html
│   └── portfolio.html
├── pjt04/              # Django 커뮤니티 (인증 없음)
│   ├── community/
│   ├── config/
│   └── manage.py
├── pjt05/              # Django 커뮤니티 + 회원 인증
│   ├── accounts/
│   ├── community/
│   ├── config/
│   └── manage.py
├── docs/               # GitHub Pages 데모
│   ├── index.html
│   └── pjt01~05/index.html
├── README.md
└── CHECKLIST.md        ← 이 파일
```

---

## 요약

| PJT | 필수 | 심화(선택) |
|-----|------|-----------|
| PJT01 | F101~F104 ✅ (4/4) | F111~F114 ✅ (4/4) |
| PJT02 | F202~F206 ✅ (5/5) | — |
| PJT03 | F301~F305 ✅ (5/5) | F311~F312 ✅ (2/2) |
| PJT04 | F401~F406 ✅ (6/6) | F411~F412 ✅ (2/2) |
| PJT05 | F501~F507 ✅ (전체) | F511 ✅ |
