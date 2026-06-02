# Bảng tra lệnh: Cài Ollama + Open WebUI (Win / Mac)

> Tài liệu tra cứu nhanh phục vụ việc hỗ trợ cài đặt trên **máy cá nhân mới**, ở trạng thái **chưa cài đặt phần mềm**.
> Mục tiêu: vận hành **LLM local** cùng **giao diện RAG**. Mô hình: `qwen3:1.7b` và `nomic-embed-text`.
> Quy ước: dòng có `#` là phần giải thích. Thực hiện từng mục **lần lượt từ trên xuống**.

---

## A. WINDOWS — mở PowerShell (chuột phải nút Start → *Windows PowerShell*)

```powershell
# 1) Cài Ollama (winget có sẵn trên Win 10/11). Sau khi cài, ĐÓNG & MỞ LẠI PowerShell.
winget install Ollama.Ollama
ollama --version                     # kiểm tra cài xong (ra số phiên bản = OK)

# 2) Tải model (chạy 1 lần; sau đó offline)
ollama pull qwen3:1.7b               # LLM trả lời (~1.4GB)
ollama pull nomic-embed-text         # embedding cho RAG (BẮT BUỘC)

# 3) Cài Docker Desktop (để chạy Open WebUI)
winget install Docker.DockerDesktop
# → MỞ Docker Desktop, đợi tới khi báo "running" (icon cá voi hết nhấp nháy)

# 4) Chạy Open WebUI (1 lệnh, không cần repo)
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
# → mở trình duyệt: http://localhost:3000
```

---

## B. macOS — mở Terminal

```bash
# 0) Homebrew (máy Mac mới CHƯA có — cài trước)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
eval "$(/opt/homebrew/bin/brew shellenv)"   # Apple Silicon (M1–M4). Mac Intel: dùng /usr/local/bin/brew

# 1) Cài + khởi động Ollama  (hoặc tải .dmg tại ollama.com/download)
brew install --cask ollama
open -a Ollama                       # chạy Ollama nền
ollama --version

# 2) Tải model
ollama pull qwen3:1.7b
ollama pull nomic-embed-text

# 3) Docker Desktop + Open WebUI
brew install --cask docker
open -a Docker                       # mở, đợi báo "running"
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
# → mở: http://localhost:3000
```

---

## C. Trường hợp không sử dụng được Docker: cài bằng pip (cả 2 OS, cần Python 3.11+)

```bash
pip install open-webui
open-webui serve                     # → mở http://localhost:8080  (KHÔNG phải 8000)
```

---

## D. Lần đầu vào Open WebUI (BẮT BUỘC cho RAG)

1. Chọn mô hình **`qwen3:1.7b`** ở khung chọn model phía trên.
2. **Admin Panel → Settings → Documents**: đặt **Embedding Engine = Ollama**, **Model = `nomic-embed-text`** → Save.
   *(Mặc định OWUI dùng embedding khác. Nếu không đặt bước này thì RAG chạy sai.)*

---

## E. Xử lý lỗi thường gặp

| Triệu chứng | Lệnh / cách xử lý |
|---|---|
| PowerShell: `...running scripts is disabled` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (gõ `Y`) rồi chạy lại |
| `winget` không nhận diện | Cài **App Installer** từ Microsoft Store, hoặc tải Ollama tại **ollama.com/download** |
| Gõ `ollama` báo không tồn tại (vừa cài) | **Đóng & mở lại** terminal để nạp PATH, sau đó chạy lại `ollama --version` |
| `Connection refused` / OWUI không gọi được model | Ollama chưa chạy. Mở app Ollama; kiểm tra `ollama list`, hoặc mở `http://localhost:11434` (phải thấy *"Ollama is running"*) |
| Docker: `cannot connect to the Docker daemon` | Mở Docker Desktop, đợi *"running"*, rồi chạy lại lệnh docker |
| `port is already allocated` (cổng 3000 bận) | Đổi cổng: thay `-p 3000:8080` bằng `-p 3001:8080`, rồi mở `http://localhost:3001` |
| **Độ trễ cao ở câu trả lời** | qwen3 đang ở chế độ suy luận. Gõ **`/no_think`** trước câu hỏi, hoặc tắt nút **"Think"** (icon não) để giảm độ trễ đáng kể |
| Lần hỏi đầu chậm hơn các lần sau | Hiện tượng bình thường: mô hình đang được nạp vào RAM |
| Mac: `brew: command not found` | Cài Homebrew (mục B.0), rồi chạy lại |
| Gỡ và dựng lại Open WebUI | `docker rm -f open-webui` rồi chạy lại lệnh `docker run` ở mục A.4 / B.3 |

---

## F. Lệnh kiểm tra / quản lý nhanh

```bash
ollama list            # model đã tải
ollama ps              # model đang chạy (chiếm RAM)
ollama rm <model>      # xoá model, giải phóng ổ đĩa
docker ps              # container đang chạy (phải thấy 'open-webui')
docker logs open-webui # xem log nếu OWUI lỗi
```

> Yêu cầu tối thiểu: **RAM ≥ 8GB**, ổ trống ≥ 5GB. Ollama API chạy nền tại `localhost:11434`; Open WebUI ở `localhost:3000` (Docker) hoặc `localhost:8080` (pip).
