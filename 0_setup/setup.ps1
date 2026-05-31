# Setup script cho workshop - chạy 1 lần duy nhất
# Sử dụng: .\0_setup\setup.ps1

$ErrorActionPreference = "Stop"

Write-Host "=== Workshop Setup: Local LLM + RAG + Agent ===" -ForegroundColor Cyan
Write-Host ""

# 1. Kiểm tra & cài Ollama
Write-Host "[1/3] Kiểm tra Ollama..." -ForegroundColor Yellow
$ollama = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollama) {
    Write-Host "  Ollama đã cài: $($ollama.Source)" -ForegroundColor Green
} else {
    Write-Host "  Chưa có Ollama. Đang cài qua winget..." -ForegroundColor Yellow
    winget install Ollama.Ollama --accept-source-agreements --accept-package-agreements
    Write-Host "  Cài xong. CẦN KHỞI ĐỘNG LẠI POWERSHELL trước khi chạy tiếp." -ForegroundColor Red
    exit 0
}

# 2. Kiểm tra Python
Write-Host ""
Write-Host "[2/3] Kiểm tra Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "  CHƯA có Python. Cài Python 3.10+ trước rồi chạy lại script này." -ForegroundColor Red
    Write-Host "  Tải: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}
$pyver = python --version
Write-Host "  $pyver" -ForegroundColor Green

# 3. Tạo venv và cài deps
Write-Host ""
Write-Host "[3/3] Tạo virtualenv và cài dependencies..." -ForegroundColor Yellow

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "  Đã tạo .venv" -ForegroundColor Green
}

& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
Write-Host "  Đã cài xong Python dependencies" -ForegroundColor Green

Write-Host ""
Write-Host "=== Setup hoàn tất ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Bước tiếp theo:" -ForegroundColor Yellow
Write-Host "  1. Pull models:    .\0_setup\pull_models.ps1"
Write-Host "  2. Activate venv:  .\.venv\Scripts\Activate.ps1"
Write-Host "  3. Test:           ollama run qwen3:1.7b ""Xin chao"""
Write-Host ""
