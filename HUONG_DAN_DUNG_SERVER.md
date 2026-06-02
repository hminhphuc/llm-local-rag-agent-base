# Dựng server RAG dùng chung (Open WebUI + Ollama) — runbook cho Claude Code

> **Mục tiêu:** Trên một server **Ubuntu có GPU**, dựng **một** Open WebUI + **một** Ollama, ra **link công khai qua ngrok**, để ~8 học viên **mở trình duyệt là dùng được ngay** — mỗi người có một workspace RAG **riêng tư, không xung đột**. Model dùng tạm **`qwen3:1.7b`** + embedding **`nomic-embed-text`** (model lớn hơn tải sau).
>
> **Cách dùng tài liệu này:** đưa cho **Claude Code chạy trên server**. Claude **thực thi Phần A–E** (lệnh terminal, cần `sudo`). **Phần F** là thao tác trên **trình duyệt** do **người** (giảng viên) làm — Claude hướng dẫn, không tự bấm được. **Làm tuần tự, qua được "✅ Kiểm tra" mới sang bước sau.**

---

## Quy ước & thông tin cần hỏi người dùng trước khi bắt đầu

Claude hãy hỏi giảng viên 3 thứ sau (điền vào khi cần), KHÔNG ghi vào file công khai:
1. **ngrok authtoken** — lấy ở https://dashboard.ngrok.com (Your Authtoken).
2. **Email + mật khẩu admin** sẽ dùng để đăng nhập (mật khẩu mạnh).
3. **(Tuỳ chọn) Domain riêng + bản ngrok trả phí?** Nếu có → dùng domain riêng; nếu không → dùng domain ngrok-free cố định (vẫn chạy tốt).

Giả định: có quyền `sudo`, server vào được Internet. GPU là tuỳ chọn — `qwen3:1.7b` chạy được cả trên CPU (chỉ chậm hơn).

---

## Phần A — Chuẩn bị hệ thống

```bash
# A1. Cập nhật + công cụ cơ bản
sudo apt update && sudo apt install -y curl ca-certificates tmux

# A2. Cài Docker (script chính thức) + bật service
curl -fsSL https://get.docker.com | sudo sh
sudo systemctl enable --now docker

# A3. Cài Ollama (tự cài thành systemd service 'ollama')
curl -fsSL https://ollama.com/install.sh | sh
```

```bash
# A4. (Tuỳ chọn) Kiểm tra GPU NVIDIA
nvidia-smi || echo "Khong thay GPU -> se chay CPU, van OK voi qwen3:1.7b"
```
> Nếu có GPU nhưng `nvidia-smi` báo lỗi: cài driver `sudo ubuntu-drivers autoinstall` rồi `sudo reboot`, sau đó chạy lại từ A3. Bỏ qua nếu chỉ dùng CPU.

**✅ Kiểm tra A:** `docker --version` và `docker compose version` ra số; `ollama --version` ra số.

---

## Phần B — Tải model

```bash
ollama pull qwen3:1.7b        # LLM trả lời (dùng tạm cho workshop)
ollama pull nomic-embed-text  # embedding cho RAG (bắt buộc)
```

**✅ Kiểm tra B:** `ollama list` thấy **cả hai** dòng `qwen3:1.7b` và `nomic-embed-text`.

---

## Phần C — Cấu hình Ollama (cho nhiều người + giữ model nạp sẵn)

Ollama mặc định chỉ nghe `127.0.0.1` → container Open WebUI gọi **không tới**. Ta cho nó nghe mọi card mạng + giữ model thường trú.

```bash
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo tee /etc/systemd/system/ollama.service.d/override.conf >/dev/null <<'EOF'
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_KEEP_ALIVE=-1"
Environment="OLLAMA_NUM_PARALLEL=4"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_KV_CACHE_TYPE=q8_0"
EOF
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

> `OLLAMA_HOST=0.0.0.0` mở cổng 11434 ra ngoài → **bắt buộc bật tường lửa** (Phần E) để chỉ chừa SSH, không lộ Ollama ra Internet.

**✅ Kiểm tra C:** `curl -s http://localhost:11434` trả về `Ollama is running`.

---

## Phần D — Triển khai Open WebUI (đa người dùng, có đăng nhập)

```bash
# D1. Thư mục triển khai
sudo mkdir -p /opt/owui && cd /opt/owui

# D2. Sinh secret key cố định (ký phiên đăng nhập) và tạo file .env
#     -> Claude thay <ADMIN_EMAIL>, <ADMIN_PASSWORD> bằng giá trị giảng viên cung cấp.
SECRET=$(openssl rand -base64 32)
sudo tee /opt/owui/.env >/dev/null <<EOF
WEBUI_SECRET_KEY=$SECRET
EOF
echo ".env da tao (chua secret key)."
```

Tạo file `/opt/owui/docker-compose.yml`:

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main   # workshop ổn định nên ghim 1 version cụ thể, vd :v0.6.x
    container_name: open-webui
    restart: always
    ports:
      - "127.0.0.1:3000:8080"        # chỉ mở nội bộ; ngrok sẽ trỏ vào đây
    extra_hosts:
      - "host.docker.internal:host-gateway"
    env_file: .env
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
      - WEBUI_AUTH=True                              # BẮT BUỘC: bật đăng nhập
      - DEFAULT_USER_ROLE=user                       # học viên đăng ký xong dùng được ngay
      - DEFAULT_MODELS=qwen3:1.7b                    # model chọn sẵn
      - USER_PERMISSIONS_WORKSPACE_KNOWLEDGE_ACCESS=True   # cho học viên tạo Knowledge base
      - USER_PERMISSIONS_WORKSPACE_MODELS_ACCESS=True      # cho học viên tạo Model RAG
      - RAG_EMBEDDING_ENGINE=ollama                  # embedding chạy local qua Ollama
      - RAG_EMBEDDING_MODEL=nomic-embed-text
      - RAG_OLLAMA_BASE_URL=http://host.docker.internal:11434
      - ENABLE_COMMUNITY_SHARING=False
      - ENABLE_ADMIN_EXPORT=False
      - WEBUI_SESSION_COOKIE_SAME_SITE=lax
      - WEBUI_SESSION_COOKIE_SECURE=True
    volumes:
      - open-webui-data:/app/backend/data
volumes:
  open-webui-data:
```

```bash
# D3. Khởi động
cd /opt/owui && sudo docker compose up -d
sudo docker compose logs -f --tail=20   # xem tới khi thấy 'Uvicorn running' rồi Ctrl+C
```

**✅ Kiểm tra D:** `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000` trả về `200`.

---

## Phần E — Tường lửa + ra link công khai bằng ngrok

```bash
# E1. Tường lửa: chỉ chừa SSH, KHÔNG mở 3000/11434 ra ngoài (ngrok đi hướng ra)
sudo ufw allow OpenSSH
sudo ufw --force enable
sudo ufw status
```
> Open WebUI bind `127.0.0.1:3000` và Ollama được ufw chặn từ ngoài → chỉ truy cập được qua link ngrok. An toàn.

```bash
# E2. Cài ngrok
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install -y ngrok

# E3. Nạp authtoken (thay <TOKEN> bằng token giảng viên cung cấp)
ngrok config add-authtoken <TOKEN>

# E4. Chạy ngrok trong tmux để nó sống độc lập với phiên SSH
tmux new -d -s ngrok 'ngrok http 3000'
sleep 3
curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | head -1
```

Lệnh cuối in ra **link công khai** dạng `https://xxxx.ngrok-free.dev` → **đây là link phát cho học viên**.

> **Có domain riêng + ngrok trả phí?** Thay E4 bằng: thêm domain trong ngrok Dashboard (Domains) + tạo bản ghi CNAME theo hướng dẫn của ngrok, rồi:
> `tmux new -d -s ngrok 'ngrok http --url=https://chat.<domain-cua-ban> 3000'`

**✅ Kiểm tra E:** mở link `https://...` trên máy khác → hiện trang đăng nhập Open WebUI. (ngrok free hiện 1 trang cảnh báo, bấm **Visit Site** để qua — bình thường.)

---

## Phần F — Cấu hình lần đầu trên trình duyệt *(GIẢNG VIÊN làm, không phải Claude)*

> Thứ tự quan trọng. **Giảng viên phải là người MỞ LINK ĐẦU TIÊN** — tài khoản đăng ký đầu tiên tự động thành **Admin**.

**F1. Tạo tài khoản Admin (làm NGAY, trước khi phát link):**
- Mở link ngrok → **Sign up** → dùng email + mật khẩu admin đã chuẩn bị → tài khoản này là Admin.

**F2. Khoá embedding (nếu chưa đúng):** **Admin Panel → Settings → Documents**
- **Embedding Model Engine = Ollama**, **Embedding Model = `nomic-embed-text`** → **Save**.
- ⚠️ Phải đúng **TRƯỚC KHI** học viên upload tài liệu. Đổi sau khi đã có dữ liệu sẽ **gãy RAG**, phải Reindex lại.

**F3. Kiểm tra quyền cho học viên:** **Admin Panel → Settings → Users → Permissions**
- Bật **Knowledge Access** và **Models Access** (nếu chưa bật). Đây là thứ cho phép học viên **tự tạo RAG**.
- **Không** bật các mục "Allow Public Sharing" cho user → tránh học viên đè dữ liệu của nhau.

**F4. Mở đăng ký cho học viên (cửa sổ ngắn):** **Admin Panel → Settings → General** (hoặc **Users**)
- Bật **Enable New Sign Ups** → phát link → học viên tự **Sign up** (mỗi người một tài khoản, vào dùng được ngay).
- Khi đủ người → **tắt** Enable New Sign Ups lại (đừng để mở trên link công khai).

**F5. (Tuỳ chọn) RAG có sẵn cho người chỉ muốn thử nhanh:**
- Admin tạo **Workspace → Knowledge** (nạp tài liệu mẫu) → **Workspace → Models → New Model**: Base = `qwen3:1.7b`, gắn Knowledge vừa tạo, đặt **Visibility = Public** (hoặc share Read cho nhóm).
- Trong ô **System Prompt** của model, đặt dòng đầu là **`/no_think`** (xem F6) để trả lời nhanh.
- Người chỉ muốn thử: vào chat **chọn model đó** → hỏi luôn, không cần tự dựng.

**F6. ⚠️ Bắt buộc với qwen3 — tắt chế độ "thinking":** qwen3 mặc định sinh một đoạn lý luận dài trước khi trả lời → câu trả lời chậm 15–60s, nhìn như **treo**. Khắc phục (chọn 1):
- Thêm **`/no_think`** vào **đầu System Prompt** của mọi Model RAG (cách bền nhất cho cả lớp), hoặc
- Dặn học viên gõ `/no_think` ở đầu câu hỏi, hoặc tắt nút **"Think"** (biểu tượng não) cạnh ô gửi.

---

## Phần G — Nghiệm thu (định nghĩa "chạy được")

Một học viên (hoặc admin) thử đủ luồng RAG:
1. **Workspace → Knowledge → + New** → tạo kho → upload 1 file `.txt`/`.md`/`.pdf`.
   *(Cần file mẫu? Clone repo workshop để lấy `2_rag/data/`:* `git clone <repo> /tmp/ws`*)*
2. Chat: chọn `qwen3:1.7b`, gõ **`#`** chọn kho vừa tạo → hỏi 1 câu về nội dung tài liệu.
3. ✅ **Đạt** khi: trả lời bám tài liệu **và** dưới câu trả lời có mục **Sources/trích nguồn** trỏ đúng tên file.

Mỗi học viên đăng nhập tài khoản riêng → Knowledge/Model của họ **chỉ họ thấy** → 4+ workspace data khác nhau, không xung đột. Xong.

---

## Phần H — Tải model mạnh hơn (sau, khi cần chất lượng cao hơn)

`qwen3:1.7b` là model tạm. Khi muốn trả lời tiếng Việt tốt hơn (tận dụng GPU), pull thêm rồi học viên tự chọn trong khung model:
```bash
ollama pull qwen2.5:14b     # ~10GB, hợp GPU ~20GB/card
# hoặc
ollama pull qwen2.5:32b     # ~20GB, cần VRAM lớn (vd 2x40GB)
```
> Không cần khởi động lại gì — Open WebUI tự thấy model mới. Muốn đổi mặc định: sửa `DEFAULT_MODELS` trong compose rồi `docker compose up -d`.

---

## Phần I — Dọn dẹp sau buổi học

```bash
tmux kill-session -t ngrok            # tắt link công khai
cd /opt/owui && sudo docker compose down   # tắt Open WebUI
# Quyết định dữ liệu (chat + tài liệu học viên còn trong volume):
# sudo docker volume rm owui_open-webui-data   # XOÁ HẲN (cẩn thận, không hồi lại được)
```

---

## Xử lý lỗi nhanh

| Triệu chứng | Nguyên nhân | Xử lý |
|---|---|---|
| Open WebUI báo không kết nối được model / `Connection refused` | Ollama chưa nghe `0.0.0.0`, hoặc container gọi sai host | Kiểm tra Phần C (`curl localhost:11434`); compose có `extra_hosts: host.docker.internal:host-gateway` và `OLLAMA_BASE_URL=http://host.docker.internal:11434` |
| Upload tài liệu lỗi / không có Sources khi hỏi | Embedding chưa trỏ Ollama, hoặc chưa pull `nomic-embed-text` | `ollama list` xem có `nomic-embed-text`; F2 đặt Engine=Ollama, Model=nomic-embed-text |
| Hỏi xong **đợi rất lâu** mới trả lời / như **treo** | qwen3 bật chế độ "thinking" (sinh lý luận dài trước khi trả lời) | Thêm **`/no_think`** vào đầu System Prompt của Model (F6) hoặc đầu câu hỏi; hoặc tắt nút **"Think"** cạnh ô gửi |
| Học viên **không thấy** mục tạo Knowledge/Model | Quyền workspace đang tắt | F3: bật Knowledge Access + Models Access |
| Học viên đăng ký nhưng **không vào được** | `DEFAULT_USER_ROLE` đang là `pending` | Admin Panel → Users → duyệt user, hoặc đảm bảo `DEFAULT_USER_ROLE=user` |
| Người lạ chiếm mất quyền admin | Có người mở link trước giảng viên | Phải để giảng viên đăng ký **đầu tiên**; lỡ rồi thì xoá volume làm lại (I) |
| Đăng nhập xong bị đá ra liên tục | `WEBUI_SECRET_KEY` đổi mỗi lần restart (không cố định) | Đảm bảo `.env` có `WEBUI_SECRET_KEY` cố định và volume `open-webui-data` được giữ |
| Mở link báo trang cảnh báo ngrok | Bình thường ở bản free | Bấm **Visit Site** (cookie nhớ 7 ngày) |
| Link ngrok đổi sau khi restart | Chạy lại tunnel | Bản free có 1 domain cố định; ghim bằng `ngrok http --url=<domain-cua-ban> 3000` |

---

## Tóm tắt kiến trúc (để rõ "tại sao")

- **1** Open WebUI + **1** Ollama trên cùng server. Không cần nhiều instance.
- **1 Admin** (giảng viên) + **N user** (mỗi học viên 1 tài khoản). **Không** tạo nhiều admin (admin thấy/sửa được dữ liệu mọi người → mất cô lập).
- Mỗi user có **Workspace riêng tư mặc định** → Knowledge base & Model của ai người nấy thấy ⇒ **các workspace data khác nhau, không xung đột** mà không cần cấu hình gì thêm.
- Ra ngoài bằng **ngrok** (hướng ra, không mở port firewall); Ollama/3000 bị ufw chặn từ Internet.
