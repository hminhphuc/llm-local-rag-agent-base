# Pull models cần thiết cho workshop
# Chạy 1 lần duy nhất, mất ~5-10 phút tùy mạng

$ErrorActionPreference = "Stop"

Write-Host "=== Pull models cho workshop ===" -ForegroundColor Cyan
Write-Host ""

# Hỏi user muốn pull bộ nào
Write-Host "Chọn cấu hình model:" -ForegroundColor Yellow
Write-Host "  [1] Mặc định - Qwen3:1.7b + nomic-embed-text (~1.7GB) - khuyến nghị, output sạch + nhanh"
Write-Host "  [2] Mạnh hơn - Qwen3:4b + nomic-embed-text (~2.8GB) - cần RAM 16GB+"
Write-Host "  [3] Tốt nhất - Qwen3:8b + bge-m3 (~6GB) - cần GPU/RAM lớn"
Write-Host ""
$choice = Read-Host "Lựa chọn (1/2/3, mặc định 1)"

if ([string]::IsNullOrWhiteSpace($choice)) { $choice = "1" }

switch ($choice) {
    "1" {
        $llm = "qwen3:1.7b"
        $embed = "nomic-embed-text"
    }
    "2" {
        $llm = "qwen3:4b"
        $embed = "nomic-embed-text"
    }
    "3" {
        $llm = "qwen3:8b"
        $embed = "bge-m3"
    }
    default {
        Write-Host "Lựa chọn không hợp lệ" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Sẽ pull:" -ForegroundColor Yellow
Write-Host "  LLM:       $llm"
Write-Host "  Embedding: $embed"
Write-Host ""

# Kiểm tra Ollama đang chạy
try {
    Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 3 | Out-Null
} catch {
    Write-Host "Ollama chưa chạy. Đang start..." -ForegroundColor Yellow
    Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

Write-Host "[1/2] Pulling LLM: $llm" -ForegroundColor Yellow
ollama pull $llm

Write-Host ""
Write-Host "[2/2] Pulling embedding: $embed" -ForegroundColor Yellow
ollama pull $embed

# Ghi config để các script khác dùng đúng model
$config = @"
# Model config - do pull_models.ps1 tự sinh
# Sửa file này hoặc set biến môi trường để override
LLM_MODEL=$llm
EMBED_MODEL=$embed
OLLAMA_BASE_URL=http://localhost:11434/v1
"@

$repoRoot = Split-Path -Parent $PSScriptRoot
$config | Out-File -FilePath "$repoRoot\.env" -Encoding utf8 -Force

Write-Host ""
Write-Host "=== Hoàn tất ===" -ForegroundColor Cyan
Write-Host "Đã ghi config vào .env" -ForegroundColor Green
Write-Host ""
Write-Host "Test ngay:" -ForegroundColor Yellow
Write-Host "  ollama run $llm ""Giải thích RAG trong 3 câu"""
Write-Host ""
