# Module 0 — Setup môi trường

Chuẩn bị máy để chạy được toàn bộ workshop. Có script riêng cho Windows và macOS/Linux.
**Chọn đúng hệ điều hành của bạn bên dưới.**

## Cách chạy

### 🪟 Windows (PowerShell)

> 🛑 **Gặp lỗi "running scripts is disabled"? Chạy DÒNG NÀY TRƯỚC** (chỉ 1 lần):
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

```powershell
# Mở PowerShell (chuột phải Start → Windows PowerShell), cd vào thư mục repo
.\0_setup\setup.ps1         # Cài Ollama + tạo .venv + cài thư viện
.\0_setup\pull_models.ps1   # Tải model (Enter = mặc định qwen3:1.7b)
```

> ⚠️ **Nếu script báo "CẦN KHỞI ĐỘNG LẠI POWERSHELL"** (xảy ra ngay sau khi cài Ollama lần đầu):
> 1. Đóng cửa sổ PowerShell hiện tại — gõ `exit`.
> 2. Mở cửa sổ PowerShell **MỚI** (chuột phải Start → Windows PowerShell).
> 3. `cd` lại vào thư mục repo, rồi chạy lại `.\0_setup\setup.ps1`.
>
> Đừng chỉ bấm Enter trong cửa sổ cũ — biến môi trường mới chưa được nạp.

### 🍎 macOS / 🐧 Linux (Bash)
```bash
# Mở terminal tại thư mục gốc repo
chmod +x 0_setup/setup.sh 0_setup/pull_models.sh    # cấp quyền chạy
./0_setup/setup.sh                                  # Cài Ollama + tạo .venv + cài thư viện
./0_setup/pull_models.sh                            # Tải model (Enter = mặc định qwen3:1.7b)
```

> 💡 **`.venv` là gì?** Là môi trường Python riêng cho workshop (không đụng tới Python hệ thống). Script tự tạo nó. Trước **mọi** lệnh `python`, nhớ bật: `.\.venv\Scripts\Activate.ps1` (Windows) hoặc `source .venv/bin/activate` (macOS/Linux).

## Yêu cầu phần cứng

| Thành phần | Tối thiểu | Khuyến nghị |
|---|---|---|
| RAM | 8GB | 16GB |
| Ổ trống | 5GB | 10GB |
| OS | Win10 / macOS 12 / Ubuntu 20.04 | Bản mới nhất |
| Python | 3.10 | 3.11+ |
| GPU | Không bắt buộc | NVIDIA RTX 3050+, Apple Silicon M1+ |

### 👉 Cách kiểm tra máy bạn (Windows)

| Cần biết | Cách xem |
|---|---|
| **RAM** | Bấm `Windows` → gõ "About your PC" → dòng *Installed RAM* |
| **Python** | Mở PowerShell, gõ `python --version` (chưa có → cài [Python 3.11](https://www.python.org/downloads/), nhớ tick *Add to PATH*) |
| **GPU rời** | `Windows` → "Device Manager" → *Display adapters* (có NVIDIA/AMD = chạy nhanh hơn) |

**Chọn model lúc chạy `pull_models`:** dưới 14GB RAM hoặc không có GPU → chọn **[1] qwen3:1.7b** (mặc định). Từ 16GB RAM hoặc có GPU → có thể chọn [2]/[3].

## Trên macOS dùng Apple Silicon (M1/M2/M3)

Ollama tự dùng Metal (GPU của Apple Silicon) — không cần cấu hình gì. Tốc độ rất tốt cho model 3B-8B.

## Trên Linux có GPU NVIDIA

Ollama tự detect CUDA. Kiểm tra:
```bash
ollama serve  # log sẽ in: "using CUDA"
```

## Trên CPU (không GPU)

Vẫn chạy được, chỉ chậm hơn. Khuyến nghị dùng model nhỏ (Qwen3:1.7b hoặc Llama3.2:3b).

## Xử lý lỗi thường gặp

| Lỗi | Hệ | Cách xử lý |
|---|---|---|
| `cannot be loaded because running scripts is disabled` | Windows | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `winget không nhận diện` | Windows | Cài [App Installer](https://www.microsoft.com/store/productId/9NBLGGH4NNS1) |
| `python: command not found` | macOS/Linux | macOS: `brew install python@3.11`. Ubuntu: `sudo apt install python3 python3-venv python3-pip` |
| `Permission denied` khi chạy `.sh` | macOS/Linux | `chmod +x 0_setup/setup.sh` |
| `port 11434 already in use` | Mọi hệ | Đã có instance Ollama khác chạy, không sao — dùng luôn |

## Kiểm tra setup OK

### Windows
```powershell
ollama --version
ollama list
.\.venv\Scripts\Activate.ps1
python -c "import ollama, chromadb, pydantic_ai; print('OK')"
```

### macOS / Linux
```bash
ollama --version
ollama list
source .venv/bin/activate
python -c "import ollama, chromadb, pydantic_ai; print('OK')"
```

Nếu in `OK` là sẵn sàng vào [Module 1](../1_ollama_basics/).

> ❌ **Nếu báo lỗi `ModuleNotFoundError` ở bước này:** (1) chắc chắn đã **bật venv** (đầu dòng lệnh phải có `(.venv)`); (2) chạy lại `setup.ps1` / `setup.sh`; (3) vẫn lỗi → chụp màn hình tên lỗi để hỏi.

## Khởi động lại Ollama (nếu cần)

| Hệ | Lệnh |
|---|---|
| Windows | App Ollama chạy ở system tray, click chuột phải → Quit, mở lại |
| macOS (Homebrew) | `brew services restart ollama` |
| macOS (app) | Cmd+Q app Ollama, mở lại |
| Linux (systemd) | `sudo systemctl restart ollama` |
| Mọi hệ (manual) | `pkill ollama; ollama serve &` |
