# FinHub GitHub 업로드 스크립트
# 사용법: PowerShell에서 이 파일이 있는 폴더로 이동 후 실행
#   cd C:\Users\SSAFY\Desktop\hwlee\03_pjts\금융\finhub
#   .\github_push.ps1

# ─── 설정 ────────────────────────────────────────────────
$GITHUB_USERNAME = "404h1"          # GitHub 유저명
$REPO_NAME       = "finhub"        # 생성할 레포 이름
# ─────────────────────────────────────────────────────────

Write-Host "=== FinHub GitHub 업로드 ===" -ForegroundColor Cyan

# 혹시 이전에 실패한 .git 폴더가 있으면 삭제
if (Test-Path ".git") {
    Write-Host "기존 .git 폴더 삭제 중..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force ".git"
}

# git 초기화
Write-Host "git 초기화 중..." -ForegroundColor Green
git init
git branch -M main

# git config (로컬)
git config user.email "hwlee154@gmail.com"
git config user.name "hwlee154"

# 파일 추가 및 커밋
Write-Host "파일 스테이징 및 커밋 중..." -ForegroundColor Green
git add .
git commit -m "feat: FinHub 금융 통합 플랫폼 초기 커밋

- accounts: 커스텀 유저 모델, 로그인/회원가입/프로필
- products: 금감원 API 기반 정기예금 비교
- stocks: yfinance + 기술적 분석 (EMA, RSI, MACD, 볼린저밴드)
- boards: 자산별 커뮤니티 게시판
- 모던 다크 네이비 UI (Pretendard, Bootstrap5)
- docs/: GitHub Pages 데모 페이지"

# 원격 추가 및 push
$REMOTE_URL = "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
Write-Host "원격 레포 연결: $REMOTE_URL" -ForegroundColor Green
git remote add origin $REMOTE_URL
git push -u origin main

Write-Host ""
Write-Host "=== 완료! ===" -ForegroundColor Cyan
Write-Host "GitHub 레포: https://github.com/$GITHUB_USERNAME/$REPO_NAME" -ForegroundColor Green
Write-Host ""
Write-Host "[ GitHub Pages 데모 활성화 방법 ]" -ForegroundColor Yellow
Write-Host "1. https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/pages 접속"
Write-Host "2. Source → 'Deploy from a branch' 선택"
Write-Host "3. Branch: main / Folder: /docs 선택 후 Save"
Write-Host "4. 잠시 후 https://$GITHUB_USERNAME.github.io/$REPO_NAME/ 에서 데모 확인"
