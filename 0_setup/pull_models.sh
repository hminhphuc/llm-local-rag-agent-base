#!/usr/bin/env bash
# Pull models cần thiết cho workshop - dùng cho macOS và Linux
# Chạy 1 lần duy nhất, mất ~5-10 phút tùy mạng:
#   ./0_setup/pull_models.sh

set -euo pipefail

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}=== Pull models cho workshop ===${NC}"
echo ""

# ============================================
# Cho user chọn bộ model theo cấu hình máy
# ============================================
echo -e "${YELLOW}Chọn cấu hình model:${NC}"
echo "  [1] Mặc định - Qwen3:1.7b + nomic-embed-text (~1.7GB) - khuyến nghị, output sạch + nhanh"
echo "  [2] Mạnh hơn - Qwen3:4b + nomic-embed-text (~2.8GB) - cần RAM 16GB+"
echo "  [3] Tốt nhất - Qwen3:8b + bge-m3 (~6GB) - cần GPU/RAM lớn"
echo ""
read -rp "Lựa chọn (1/2/3, mặc định 1): " choice
choice="${choice:-1}"

case "$choice" in
    1)
        LLM="qwen3:1.7b"
        EMBED="nomic-embed-text"
        ;;
    2)
        LLM="qwen3:4b"
        EMBED="nomic-embed-text"
        ;;
    3)
        LLM="qwen3:8b"
        EMBED="bge-m3"
        ;;
    *)
        echo -e "${RED}Lựa chọn không hợp lệ${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${YELLOW}Sẽ pull:${NC}"
echo "  LLM:       $LLM"
echo "  Embedding: $EMBED"
echo ""

# ============================================
# Đảm bảo Ollama daemon đang chạy
# ============================================
# Trên macOS/Linux, Ollama serve qua background process hoặc systemd.
# Ta check qua API endpoint /api/tags. Nếu không reachable, tự start.
if ! curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo -e "${YELLOW}Ollama chưa chạy. Đang start trong background...${NC}"
    # nohup để Ollama không chết khi script này thoát
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
fi

# ============================================
# Pull từng model
# ============================================
echo -e "${YELLOW}[1/2] Pulling LLM: $LLM${NC}"
ollama pull "$LLM"

echo ""
echo -e "${YELLOW}[2/2] Pulling embedding: $EMBED${NC}"
ollama pull "$EMBED"

# ============================================
# Ghi config cho các script Python đọc
# ============================================
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cat > "$REPO_ROOT/.env" <<EOF
# Model config - do pull_models.sh tự sinh
# Sửa file này hoặc set biến môi trường để override
LLM_MODEL=$LLM
EMBED_MODEL=$EMBED
OLLAMA_BASE_URL=http://localhost:11434/v1
EOF

echo ""
echo -e "${CYAN}=== Hoàn tất ===${NC}"
echo -e "${GREEN}Đã ghi config vào .env${NC}"
echo ""
echo -e "${YELLOW}Test ngay:${NC}"
echo "  ollama run $LLM \"Giải thích RAG trong 3 câu\""
echo ""
