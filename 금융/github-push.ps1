# =============================================
# K-FOOD AI Navigator - GitHub 업로드 스크립트
# =============================================
# 사용법: 이 스크립트를 PowerShell에서 실행하세요.
# GitHub Personal Access Token이 필요합니다.
# (https://github.com/settings/tokens 에서 생성)

$GITHUB_USER = "404h1"
$REPO_NAME   = "k-food-ai-marketing"
$BRANCH      = "ai-landing"

Write-Host "=== K-FOOD AI Navigator GitHub 업로드 ===" -ForegroundColor Cyan

# 토큰 입력
$token = Read-Host "GitHub Personal Access Token을 입력하세요" -AsSecureString
$BSTR  = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
$plain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# 임시 폴더에 클론
$tmpDir = "$env:TEMP\kfood-deploy-$(Get-Random)"
Write-Host "`n[1/4] 저장소 클론 중..." -ForegroundColor Yellow
git clone "https://${plain}@github.com/$GITHUB_USER/$REPO_NAME.git" $tmpDir

if (-not (Test-Path $tmpDir)) {
    Write-Host "클론 실패. 토큰을 확인해주세요." -ForegroundColor Red
    exit 1
}

Set-Location $tmpDir
git config user.email "hwlee139@gmail.com"
git config user.name "Hye"

Write-Host "[2/4] 브랜치 생성: $BRANCH" -ForegroundColor Yellow
git checkout -b $BRANCH 2>$null
if ($LASTEXITCODE -ne 0) { git checkout $BRANCH }

Write-Host "[3/4] 파일 복사 & 커밋..." -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item "$scriptDir\ai-navigator.html" "$tmpDir\ai-navigator.html" -Force
git add ai-navigator.html
git commit -m "Add AI-generated standalone landing page (ai-navigator.html)"

Write-Host "[4/4] GitHub에 푸시 중..." -ForegroundColor Yellow
git push "https://${plain}@github.com/$GITHUB_USER/$REPO_NAME.git" $BRANCH --force

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ 업로드 완료!" -ForegroundColor Green
    Write-Host "PR 주소: https://github.com/$GITHUB_USER/$REPO_NAME/compare/$BRANCH" -ForegroundColor Cyan
    Write-Host "파일 주소: https://github.com/$GITHUB_USER/$REPO_NAME/blob/$BRANCH/ai-navigator.html" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ 푸시 실패. 토큰 권한(repo)을 확인해주세요." -ForegroundColor Red
}

# 정리
Set-Location $env:TEMP
Remove-Item $tmpDir -Recurse -Force
