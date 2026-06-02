# Build SLIDES.pptx (editable) — 3 bước:
#   1) marp  : Markdown -> PPTX editable (qua LibreOffice)
#   2) add_links.py : gắn lại hyperlink (LibreOffice làm rớt)
#   3) fix_boxes.py : nới ô text bị cấp quá hẹp (chống wrap tiêu đề/bullet)
#
# Chạy:  .\slides\build.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$py   = Join-Path $root ".venv\Scripts\python.exe"
$env:PATH += ';C:\Program Files\LibreOffice\program'

Get-Process soffice*, soffice.bin -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Set-Location $root

npx --yes @marp-team/marp-cli@4.4.0 slides/SLIDES.md --pptx --pptx-editable --theme-set slides/theme.css --allow-local-files --no-stdin -o slides/SLIDES.pptx
& $py slides\add_links.py
& $py slides\fix_boxes.py

Write-Host "DONE -> slides\SLIDES.pptx"
