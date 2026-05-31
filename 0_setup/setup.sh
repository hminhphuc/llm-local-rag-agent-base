#!/usr/bin/env bash
# Setup script cho workshop - dùng cho macOS và Linux
# Chạy 1 lần duy nhất từ thư mục gốc repo:
#   chmod +x 0_setup/setup.sh
#   ./0_setup/setup.sh

set -euo pipefail

# Màu cho output (dễ đọc)
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'  # No Color

echo -e "${CYAN}=== Workshop Setup: Local LLM + RAG + Agent ===${NC}"
echo ""

# Phát hiện OS để dùng đúng cách cài Ollama
OS="$(uname -s)"
case "$OS" in
    Darwin*)  PLATFORM="macos" ;;
    Linux*)   PLATFORM="linux" ;;
    *)        echo -e "${RED}OS không hỗ trợ: $OS. Dùng Windows? Chạy setup.ps1 thay thế.${NC}"; exit 1 ;;
esac
echo -e "Phát hiện OS: ${GREEN}$PLATFORM${NC}"
echo ""

# ============================================
# [1/3] Kiểm tra và cài Ollama
# ============================================
echo -e "${YELLOW}[1/3] Kiểm tra Ollama...${NC}"

if command -v ollama &> /dev/null; then
    echo -e "  ${GREEN}Ollama đã cài: $(which ollama)${NC}"
else
    echo -e "  Chưa có Ollama. Đang cài đặt..."

    if [ "$PLATFORM" = "macos" ]; then
        # macOS: ưu tiên Homebrew (đa số dev đã có), fallback script chính thức
        if command -v brew &> /dev/null; then
            echo "  Cài qua Homebrew..."
            brew install ollama
        else
            echo "  Không có Homebrew, cài qua script chính thức..."
            curl -fsSL https://ollama.com/install.sh | sh
        fi
    elif [ "$PLATFORM" = "linux" ]; then
        # Linux: script chính thức của Ollama
        echo "  Cài qua script chính thức..."
        curl -fsSL https://ollama.com/install.sh | sh
    fi

    echo -e "  ${GREEN}Đã cài xong Ollama${NC}"
fi

# ============================================
# [2/3] Kiểm tra Python 3.10+
# ============================================
echo ""
echo -e "${YELLOW}[2/3] Kiểm tra Python...${NC}"

# Ưu tiên python3 (chuẩn trên macOS/Linux), fallback python
PYTHON_BIN=""
if command -v python3 &> /dev/null; then
    PYTHON_BIN="python3"
elif command -v python &> /dev/null; then
    PYTHON_BIN="python"
else
    echo -e "  ${RED}Chưa có Python. Cài Python 3.10+ trước rồi chạy lại script.${NC}"
    if [ "$PLATFORM" = "macos" ]; then
        echo -e "  ${RED}macOS: brew install python@3.11${NC}"
    else
        echo -e "  ${RED}Linux: sudo apt install python3 python3-venv python3-pip${NC}"
    fi
    exit 1
fi

PY_VERSION=$($PYTHON_BIN --version)
echo -e "  ${GREEN}$PY_VERSION (lệnh: $PYTHON_BIN)${NC}"

# ============================================
# [3/3] Tạo venv + cài Python dependencies
# ============================================
echo ""
echo -e "${YELLOW}[3/3] Tạo virtualenv và cài dependencies...${NC}"

# Đi đến thư mục gốc repo (script nằm trong 0_setup/)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if [ ! -d ".venv" ]; then
    $PYTHON_BIN -m venv .venv
    echo -e "  ${GREEN}Đã tạo .venv${NC}"
fi

# Activate venv (trên Unix: bin/activate, khác Windows: Scripts/Activate.ps1)
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo -e "  ${GREEN}Đã cài xong Python dependencies${NC}"

# ============================================
# Hoàn tất
# ============================================
echo ""
echo -e "${CYAN}=== Setup hoàn tất ===${NC}"
echo ""
echo -e "${YELLOW}Bước tiếp theo:${NC}"
echo "  1. Pull models:    ./0_setup/pull_models.sh"
echo "  2. Activate venv:  source .venv/bin/activate"
echo "  3. Test:           ollama run qwen3:1.7b \"Xin chào\""
echo ""
