# Định hướng giảng — Workshop: Local LLM · RAG

**Khớp với:** `slides/SLIDES.md` (47 slide) · **Giảng viên:** PGS.TS. Lê Anh Cường (NLP) · thời lượng ~2 giờ

> Tài liệu này tóm tắt theo từng slide: **các ý chính cần truyền đạt** và **thông tin/số liệu chốt** — để giảng viên tự định hướng, KHÔNG phải lời thoại đọc nguyên văn. Quy ước: `**Chốt / số liệu:**` = dữ kiện cần nêu chính xác · `**Chiếu / thao tác:**` = ảnh/diagram/lệnh cần trình. Slide chỉ có ảnh → nêu ảnh cho thấy gì + điểm cần chỉ ra.

## Thời lượng (lời giảng) ~108 phút — chưa tính thời gian học viên tự thao tác

| Phần | ~Thời lượng |
|---|---|
| Phần A — Mở đầu (Slide 1–6) | ~12' |
| Phần B — RAG lý thuyết · TRỤC CHÍNH (Slide 7–12) | ~26' |
| Phần C — Công cụ & chạy LLM local (Slide 13–20) | ~16' |
| Phần D — Open WebUI: nhu cầu · cài đặt · khởi động (Slide 21–30) | ~17' |
| Phần E — Open WebUI: nạp tài liệu → trợ lý → hỏi đáp (Slide 31–42) | ~28' |
| Phần F — Áp dụng & Tổng kết (Slide 43–47) | ~10' |

---

# Phần A — Mở đầu (Slide 1–6)

### Slide 1 — Local LLM · RAG (bìa)  ·  ~2 phút
- Định khung buổi học: tự xây trợ lý AI biết đọc tài liệu của chính mình, chạy 100% trên máy.
- Thông điệp xuyên suốt cần neo lại từ đầu: **dữ liệu của bạn không rời máy**.
- Không yêu cầu biết lập trình — chỉ cần làm theo từng bước.
- Có thể mở bằng câu hỏi gợi mở: ai từng dán tài liệu nội bộ vào ChatGPT để nhờ tóm tắt? (giữ lại để cuối buổi đối chiếu).

### Slide 2 — Mục tiêu buổi học  ·  ~2 phút
- Ba mục tiêu: **HIỂU** RAG + 6 thành phần hệ RAG local; **XÂY** RAG trên tài liệu của mình (không code); **CHỌN** model LLM phù hợp máy, chạy offline bằng Ollama.
- Nhấn ba động từ HIỂU – XÂY – CHỌN là ba việc lần lượt làm hôm nay.
- **Chốt:** thước đo thành công — hỏi 1 câu về tài liệu → trả lời **đúng** + **trích nguồn**.

### Slide 3 — Rủi ro khi gửi dữ liệu ra ngoài  ·  ~3 phút
- Gửi prompt = gửi luôn dữ liệu kèm theo ra ngoài tổ chức (câu chốt của slide).
- Rủi ro **rò rỉ**: Samsung (5/2023) cấm nhân viên dùng ChatGPT nội bộ sau khi lộ mã nguồn — ca thật, không giả định.
- Rủi ro **điều khoản**: nhiều dịch vụ ghi rõ *"data may be used to improve our models"* → cái gửi đi có thể thành nguyên liệu huấn luyện.
- Rủi ro **chi phí**: trả theo token, phụ thuộc đường mạng và nhà cung cấp.
- Có thể nêu câu hỏi gợi mở: tài liệu nhạy cảm nhất trong công việc là gì — có dám dán lên dịch vụ ngoài không?
- **Chiếu:** sơ đồ rủi ro bảo mật (`08_security_risks.png`); chỉ mũi tên dữ liệu đi từ "máy của bạn" ra "cloud".

### Slide 4 — Giải pháp: LLM local  ·  ~2-3 phút
- Giải pháp gói gọn: **dữ liệu KHÔNG rời máy** — chạy mô hình ngay trên máy.
- Kiến trúc 2 tầng: **LLM local (Ollama)** là nền tảng → **RAG** dựng lên trên.
- Không phải bài toán riêng của dân kỹ thuật — cùng công nghệ, nhiều nhu cầu: văn phòng (tra quy chế nội bộ), lập trình viên (trợ lý code offline), tổ chức/DN (chatbot không rò rỉ), y tế (hồ sơ bệnh nhân bảo mật).
- **Chiếu:** chỉ lần lượt từng dòng trong bảng nhóm nhu cầu; có thể hỏi nhanh ai thuộc nhóm nào để cá nhân hóa phần sau.

### Slide 5 — Local vs Cloud  ·  ~3 phút
- Trình bày sòng phẳng, không lựa chọn nào hoàn hảo — đối chiếu theo từng tiêu chí.
- **Bảo mật**: local ở lại máy / cloud gửi ra ngoài → local thắng.
- **Chi phí**: local trả 1 lần / cloud theo token → local thắng.
- **Chất lượng**: local model nhẹ / cloud có mô hình mạnh → cloud hơn.
- **Độ trễ**: local chậm trên CPU / cloud nhanh nhờ GPU lớn → cloud hơn.
- **Vận hành**: local tự bảo trì / cloud bấm là dùng → cloud tiện hơn.
- **Chốt:** local thắng **bảo mật & chi phí**, đổi lấy **chất lượng & tốc độ** — hiểu cái được/mất để chọn đúng việc đưa lên local.

### Slide 6 — Lộ trình buổi học  ·  ~2 phút
- Hai chặng: (1) **Nền tảng** — cài & chạy LLM local bằng Ollama + Docker; (2) **RAG — trọng tâm** — 6 thành phần → nạp tài liệu → trả lời kèm trích nguồn.
- Cả hai chặng đều có **thực hành làm theo**: GV làm trên màn hình, học viên làm song song trên máy mình.
- **Chiếu:** sơ đồ kiến trúc tổng thể (`01_overall_architecture.png`); lia từ khối "tài liệu" → "Ollama" → "câu trả lời có nguồn" — đây là bức tranh lớn học viên sẽ tự dựng được cuối buổi.

# Phần B — RAG lý thuyết · TRỤC CHÍNH (Slide 7–12)

### Slide 7 — RAG — Trục chính  ·  ~0.5 phút
- Slide divider: chốt rằng đây là trục chính, phần quan trọng nhất của buổi.
- Phần lý thuyết này trả lời 3 câu: RAG là gì · vận hành ra sao · làm sao biết một hệ RAG là tốt.
- Nắm vững lý thuyết ở đây → vào thực hành sẽ hiểu mình đang chỉnh thông số gì và tại sao.

### Slide 8 — RAG là gì  ·  ~5 phút
- Định nghĩa 1 câu: **tra tài liệu trước, trả lời sau**.
- LLM không có tài liệu riêng của bạn — chỉ học từ dữ liệu công khai lúc huấn luyện.
- Hỏi thẳng về quy chế nội bộ → mô hình **bịa** trơn tru (hallucination).
- Dán cả tập tài liệu vào prompt cũng hỏng: **vượt context window** + tốn token, chậm.
- Ẩn dụ: hỏi thẳng = làm bài thi **đóng sách** (nhớ gì nói nấy); RAG = **mở sách**, tra đúng trang rồi trả lời.
- Tên gọi = 3 bước: **R**etrieval (truy hồi) · **A**ugmented (bổ sung ngữ cảnh) · **G**eneration (sinh trả lời).
- Có thể nêu câu hỏi gợi mở: ai từng hỏi ChatGPT một con số trong quy định cơ quan và nhận câu trả lời sai mà nghe rất tự tin? — đó là "đóng sách".

### Slide 9 — Kiến trúc RAG: 6 bước  ·  ~5 phút
- 6 bước chia 2 nhóm theo tần suất chạy.
- **Offline** (làm 1 lần khi chuẩn bị kho): Load (nạp) → Chunk (cắt đoạn nhỏ) → Embed (đoạn → vector mang nghĩa) → Store (lưu vector vào DB) = dựng & sắp xếp thư viện.
- **Online** (chạy lại mỗi câu hỏi): Retrieve (truy hồi đoạn liên quan nhất) → Generate (đưa đoạn cho LLM sinh trả lời).
- **Chốt:** 4 bước đầu làm 1 lần · 2 bước cuối lặp mỗi câu hỏi.
- Lợi ích của ranh giới này: giải thích vì sao trong Open WebUI có thông số chỉnh 1 lần (offline) và thông số ảnh hưởng từng lần hỏi (online).
- **Chiếu / thao tác:** sơ đồ pipeline `02_rag_pipeline.png` — chỉ 4 ô trái = offline, 2 ô phải = online.

### Slide 10 — Embedding: chữ thành nghĩa  ·  ~5 phút
- Embedding = biến chữ thành nghĩa — trái tim kỹ thuật của RAG.
- Mỗi đoạn → vector **~768 chiều** (gần 800 số mô tả ý nghĩa đoạn).
- Nguyên tắc: nghĩa gần nhau → vector gần nhau trong không gian (đo bằng **cosine nhỏ**).
- Hơn hẳn tìm từ khoá: "mã đăng nhập" vs "mật khẩu" khác hẳn về chữ → tìm từ khoá trượt, nhưng gần về nghĩa → embedding vẫn **khớp**.
- Model dùng trong buổi: **`nomic-embed-text`**; tính embedding chạy **hoàn toàn local** (đúng tinh thần dữ liệu không rời máy).
- Có thể nêu câu hỏi gợi mở: "đổi mật mã" với "thay password" có gần nhau không? — có, vì cùng nghĩa.
- **Chiếu / thao tác:** sơ đồ `04_embedding_space.png` — chỉ cụm điểm gần nhau = các đoạn cùng nghĩa tự co cụm.

### Slide 11 — Chunking, Vector DB, Top-k  ·  ~5 phút
- 3 khái niệm quyết định chất lượng truy hồi.
- **Chunk:** cắt tài liệu thành mẩu ~300–700 ký tự, 2 đoạn liền kề chồng lấn ~10–20% (overlap) để câu vắt ngang ranh giới không bị cắt cụt nghĩa.
- **Vector DB:** lưu đồng thời 3 thứ mỗi đoạn — vector + văn bản gốc + metadata (vd tên file); dùng **HNSW** tìm hàng xóm gần nhất cực nhanh dù nhiều đoạn.
- **Top-k:** mỗi câu hỏi chỉ lấy `k` đoạn gần nghĩa nhất đưa cho LLM.
- **Chốt / số liệu:** cấu hình thực hành — **Chunk Size 500 · Chunk Overlap 50 · Top K 3**; 3 con số này sẽ quay lại điền vào ô Settings của Open WebUI.
- **Chiếu / thao tác:** bảng thông số trên slide — gạch chân 3 dòng 500 / 50 / 3.

### Slide 12 — Giới hạn & Đánh giá RAG  ·  ~5 phút
- RAG không phải phép màu — vẫn sai trong 3 tình huống.
- (1) Retrieve **lấy nhầm đoạn** → LLM trả lời sai theo, "rác vào rác ra".
- (2) Câu hỏi **ngoài phạm vi tài liệu** → mô hình dễ bịa → cần **System Prompt** chặn, ép chỉ trả lời trong tài liệu.
- (3) **Chunking / embedding** kém ngay từ đầu → cả hệ kém theo (các bước sau xây trên nền đó).
- Đánh giá chất lượng — tiêu chí quan trọng nhất là **Faithfulness**: trả lời bám sát nguồn, có trích dẫn, không phịa thêm.
- Cách kiểm đơn giản ai cũng làm được: mở **Sources** đọc — nguồn trích không khớp câu trả lời = tín hiệu hệ đang sai.
- Đánh giá bài bản: khung **RAGAS** chấm điểm tự động.
- **Chốt:** đo lường được thì mới cải tiến được.
- Có thể nêu câu hỏi gợi mở: nhận một câu trả lời từ RAG, việc đầu tiên nên kiểm tra là gì? — gợi tới "mở Sources xem nguồn".

# Phần C — Công cụ & chạy LLM local (Slide 13–20)

### Slide 13 — Công cụ & chạy LLM local  ·  ~0.5 phút
- Slide divider, chuyển mục. Mục tiêu chặng này: dựng cái nền trước khi vào RAG — một LLM chạy ngay trên máy.
- Phạm vi 4 việc: làm quen Ollama → cài → lấy model → chạy thử.
- Trấn an mạch bài: dựng nền xong sẽ quay lại đúng RAG để thực hành, không bị đứt mạch.

### Slide 14 — Ollama là gì  ·  ~3 phút
- Định nghĩa: phần mềm mã nguồn mở chạy LLM ngay trên máy. Ẩn dụ "Docker cho LLM" — chỉ cần gọi tên model, nó lo phần cài đặt.
- Phổ biến: kho model cộng đồng, nhiều model hàng chục–trăm triệu lượt tải → gần như luôn có model phù hợp.
- Chuyên nghiệp: tự tối ưu GPU/CPU; API tương thích chuẩn OpenAI → dễ ghép vào app khác sau này.
- Bảo mật (điểm cốt lõi cả buổi): model + dữ liệu chạy 100% offline, không gửi gì lên cloud.
- Đơn giản: cài 1 lệnh, chạy/đổi model 1 dòng.

### Slide 15 — Cài đặt Ollama  ·  ~2.5 phút
- Windows: `winget install Ollama.Ollama` trong PowerShell — winget sẵn trên Win 10/11, tự tải và cài.
- macOS/Linux: `curl` tải script từ ollama.com rồi chạy, cũng 1 dòng.
- Kiểm tra cài thành công: `ollama --version` hiện số phiên bản = sẵn sàng.
- **Chốt / số liệu:** yêu cầu tối thiểu RAM ≥ 8GB (model cần bộ nhớ để nạp và chạy).
- **Chiều / thao tác:** mở PowerShell gõ thật `ollama --version` cho lớp thấy phiên bản. Có thể hỏi nhanh RAM máy học viên (8/16/hơn) để dẫn sang slide chọn model.

### Slide 16 — Lấy model  ·  ~3.5 phút
- Nguồn lấy model: trang ollama.com/library; chọn model theo đúng RAM máy.
- Tải bằng `ollama pull <tên model>`; lưu ý pull luôn `nomic-embed-text` — model embedding mà phần RAG cần sau.
- Con số "b" (tỷ tham số) càng lớn → càng thông minh nhưng càng nặng; đừng tham, cân với RAM.
- Qwen là dòng hợp tiếng Việt → chọn cho buổi học.
- **Chốt / số liệu:** bảng RAM↔model: 8GB → qwen3:1.7b (~1.4GB); 16GB → qwen3:4b (~2.5GB); GPU lớn → qwen3:8b (~5GB).
- **Chiều / thao tác:** gõ thật `ollama pull qwen3:1.7b` rồi `ollama pull nomic-embed-text` cho lớp thấy thanh tải. Có thể hỏi: theo bảng, máy mình pull bản nào?

### Slide 17 — Thư viện model Ollama  ·  ~1 phút
- Ảnh chụp thật trang ollama.com/library — đúng trang library vừa nhắc.
- Chỉ ra: ô tìm kiếm (gõ "qwen3" là ra) và các model phổ biến phía trên cùng.
- Thông điệp: kho rất nhiều model để chọn.

### Slide 18 — Model qwen3 — chọn cỡ theo RAM  ·  ~1.5 phút
- Ảnh chụp thật trang riêng của qwen3.
- Chỉ ra: danh sách các cỡ (tag) 1.7b / 4b / 8b và lệnh `ollama run` mà trang gợi ý.
- Thông điệp: mỗi cỡ ghi rõ dung lượng → đối chiếu bảng RAM mà chọn (8GB → 1.7b).

### Slide 19 — Chạy & test LLM local  ·  ~3 phút
- Test nhanh 1 câu: `ollama run qwen3:1.7b "Giải thích RAG trong 3 câu"`.
- Phiên chat nhiều lượt: `ollama run qwen3:1.7b` (không kèm câu hỏi) → dấu nhắc `>>>`, thoát bằng `/bye`.
- Lần đầu chưa có model → Ollama tự tải rồi trả lời luôn.
- **Chốt / số liệu:** chạy CPU có thể im 15–25s sau khi gõ (đang nạp model vào bộ nhớ, KHÔNG phải treo máy) → sau đó chữ stream ra dần.
- **Chiều / thao tác:** gõ thật `ollama run qwen3:1.7b "Giải thích RAG trong 3 câu"`; báo trước cho lớp về khoảng lặng nạp model trước khi chữ chạy ra. Kết quả thật xem ở slide sau.

### Slide 20 — Kết quả: LLM trả lời offline  ·  ~1 phút
- Ảnh chụp thật terminal: trên là dòng lệnh `ollama run`, dưới là đoạn trả lời của model.
- Chỉ ra: không có kết nối mạng nào — toàn bộ chạy trên máy.
- Chốt mạch: nền LLM local đã xong → bước tiếp dạy LLM đọc tài liệu của mình qua Open WebUI.

# Phần D — Open WebUI: nhu cầu · cài đặt · khởi động (Slide 21–30)

### Slide 21 — Thực hành — RAG qua Open WebUI  ·  ~0.5 phút
- Slide phân mục: khép phần nền tảng, mở phần thực hành xây hệ RAG hoàn chỉnh trên máy.
- Điểm nhấn: làm tất cả qua giao diện đồ họa Open WebUI — không gõ một dòng code.

### Slide 22 — Nhu cầu giao diện  ·  ~2 phút
- Tình trạng hiện tại: LLM local đã chạy, 6 bước RAG đã hiểu về nguyên lý.
- Vấn đề: terminal/dòng lệnh không phù hợp người dùng hằng ngày — không ai muốn gõ lệnh mỗi lần hỏi tài liệu.
- Nhu cầu: giao diện lưu lịch sử chat, kéo-thả tài liệu, đổi model 1 click.
- Giải pháp: Open WebUI — không cần code.
- Có thể nêu câu hỏi gợi mở: ai thấy thoải mái gõ lệnh terminal hằng ngày?

### Slide 23 — 6 bước trong Open WebUI  ·  ~2.5 phút
- Slide bản lề: nối toàn bộ lý thuyết RAG với công cụ thực hành — mỗi khái niệm có 1 nút/ô tương ứng.
- Ánh xạ 1-1: Load → Upload/kéo-thả · Chunk → Chunk Size · Embed → Embedding Model · Store → tự động lưu · Retrieve → Top K · Generate → Model + System Prompt.
- Open WebUI có engine RAG riêng; mọi thứ lưu trong volume trên chính máy.
- **Chiếu / thao tác:** chỉ lần lượt từng dòng bảng, đối chiếu cột trái (6 bước) với cột phải (thao tác).

### Slide 24 — Open WebUI là gì  ·  ~1.5 phút
- Giao diện chat mã nguồn mở, nhìn/dùng giống ChatGPT, nhưng chạy hoàn toàn local.
- Tính năng: lưu lịch sử hội thoại, đổi model 1 click, kéo-thả tài liệu để hỏi.
- Quản trị RAG hoàn toàn qua giao diện — không cần code.
- Tài liệu + lịch sử chat lưu trong volume `open-webui-data` ngay trên máy → dữ liệu không rời máy.

### Slide 25 — Docker là gì  ·  ~2 phút
- Định nghĩa: nền tảng container — đóng gói phần mềm + mọi thứ nó cần, chạy y hệt trên mọi máy (hết cảnh "máy tôi chạy được, máy anh lỗi").
- 4 lý do dùng: chuẩn công nghiệp (hầu hết production hiện đại) · phổ biến (hàng triệu lập trình viên, kho image Docker Hub) · gọn & sạch (1 lệnh có Open WebUI, gỡ không để lại rác) · an toàn (chạy cách ly, không đụng hệ thống máy).
- Có thể dùng ẩn dụ "container như chiếc hộp niêm phong" cho học viên không chuyên kỹ thuật.

### Slide 26 — Cài đặt Docker  ·  ~2 phút
- Cài Docker Desktop (miễn phí cá nhân), tải tại docker.com.
- Windows: dùng `winget` (sẵn trên Win 10/11) → `winget install Docker.DockerDesktop`.
- macOS: cần Homebrew trước (mặc định Mac chưa có → cài tại brew.sh) → `brew install --cask docker`.
- Cài xong, dù hệ điều hành nào: mở Docker Desktop, đợi báo trạng thái "running" mới làm bước tiếp.
- **Chiếu / thao tác:** Docker Desktop ở trạng thái "running" — tín hiệu xanh để đi tiếp.

### Slide 27 — Cài đặt Open WebUI  ·  ~2.5 phút
- Quy tắc nghiêm: chọn 1 trong 2 cách, tuyệt đối không chạy cả hai cùng lúc.
- Cách 1 — Docker (khuyến nghị, cần Docker Desktop đang chạy): `docker compose up -d` → lần đầu tải image ~1GB → mở localhost:3000.
- Cách 2 — pip (không cần Docker): `pip install open-webui` rồi `open-webui serve` → mở localhost:8080.
- **Chốt / số liệu:** 2 cổng khác nhau — Docker = 3000, pip = 8080.
- Định hướng học viên: máy bị chặn Docker hoặc thấy Docker khó cài → đi đường pip, kết quả y hệt.

### Slide 28 — Khởi động & mở  ·  ~2 phút
- Kiểm tra trước khi mở: `ollama list` (model đã có chưa) và `docker ps` (container Open WebUI đang chạy chưa).
- Mở localhost:3000 → chọn model qwen3:1.7b.
- Open WebUI tự nối Ollama; kiểm tra tại Settings → Connections.
- Lưu ý nhánh pip: bỏ qua `docker ps`, mở cổng 8080 thay vì 3000.
- **Chiếu / thao tác:** gõ thật `ollama list` + `docker ps`, rồi mở localhost:3000 (giao diện & kết nối xem ở 2 slide ảnh sau).

### Slide 29 — Giao diện Open WebUI  ·  ~1 phút
- Ảnh `open_webui_rag_real.png`: giao diện thật, gần như giống hệt ChatGPT.
- Chỉ ra: ô chọn model ở góc trên, ô nhập câu hỏi phía dưới, vùng hội thoại ở giữa, lịch sử chat bên trái.
- Khác biệt duy nhất: toàn bộ đang chạy trên máy local.

### Slide 30 — Kết nối Ollama với Open WebUI  ·  ~1 phút
- Ảnh `owui_30_connections.png`: màn Settings → Connections — nơi khai báo kết nối tới Ollama.
- Chỉ ra: ô địa chỉ Ollama đã tự dò và điền sẵn → không phải cấu hình thủ công.
- Khi hiển thị đúng địa chỉ Ollama = hai phần liên thông, danh sách model đã tải sẽ hiện ra để chọn.

# Phần E — Open WebUI: nạp tài liệu → trợ lý → hỏi đáp (Slide 31–42)

### Slide 31 — Nạp tài liệu · Bước 1: Load  ·  ~3 phút
- Đây là bước Load (bước 1/6 RAG) thực hiện trong giao diện.
- Knowledge base = kho tài liệu riêng của người dùng; tạo 1 lần, dùng lại nhiều lần.
- Quy trình: Workspace → Knowledge → + New Knowledge → đặt tên → Create → mở kho → bấm **+** → upload file.
- Định dạng nhận: .md, .pdf, .docx.
- File nằm trong volume trên máy, không gửi đi đâu — nhấn lại thông điệp "không rời máy".
- Có thể nêu câu gợi mở: tài liệu của tổ chức các bạn thường ở định dạng gì?

### Slide 32 — Tạo Knowledge base  ·  ~1.5 phút
- Ảnh màn tạo kho: cần chỉ ra ô đặt tên kho và nút **Create**.
- Khai báo một Knowledge base mới chỉ gồm 2 thao tác đó.
- Toàn bộ bằng giao diện, không gõ lệnh.
- **Chiếu / thao tác:** ảnh `owui_22a_create_kb.png` — chỉ ô tên + nút Create.

### Slide 33 — Kho "Quy chế ATTT" — 6 tài liệu  ·  ~1.5 phút
- Kho mẫu của buổi: "Quy chế An toàn thông tin", chứa sẵn 6 tài liệu.
- Mỗi file nạp vào sẽ được tự cắt nhỏ + mã hóa thành vector ở các bước sau; người dùng chỉ thấy danh sách file.
- Nhìn thấy 6 file trong kho = bước Load đã hoàn tất.
- **Chiếu / thao tác:** ảnh `owui_22b_kb_6files.png` — chỉ danh sách 6 file.

### Slide 34 — Chỉnh thông số · Bước 2–3–5  ·  ~4 phút
- Một màn hình gói 3/6 bước RAG; đường dẫn: Admin Panel → Settings → Documents.
- **Chunk Size ~500 · Chunk Overlap ~50** = bước Chunk (cắt đoạn có chồng lấn để không đứt mạch ý).
- **Embedding Model → nomic-embed-text** = bước Embed (biến chữ thành nghĩa, chạy 100% local).
- **Top K = 3** = bước Retrieve (số đoạn gần nhất lấy cho mỗi câu hỏi).
- Hybrid Search: bật khi tài liệu nhiều mã / từ khóa hiếm.
- Phải bấm **Save** + nạp lại tài liệu thì thay đổi mới có hiệu lực.
- Có thể hỏi kiểm tra: Top K = 3 nghĩa là lấy mấy đoạn? (nối thông số với khái niệm Retrieve).

### Slide 35 — Settings → Documents (mặc định)  ·  ~1.5 phút
- Ảnh Settings Documents ở trạng thái mặc định.
- Chỉ vị trí các ô: Chunk Size, Chunk Overlap, Top K, Embedding Model.
- Lưu ý ô Embedding Model còn giá trị mặc định — đây là điểm sắp đổi ở slide sau.
- **Chiếu / thao tác:** ảnh `owui_23a_settings.png` — chỉ ô Embedding Model mặc định.

### Slide 36 — Đổi Embedding → nomic-embed-text  ·  ~1.5 phút
- Ảnh sau khi đổi Embedding Model sang nomic-embed-text.
- Đây là model biến chữ thành nghĩa cho cả kho; chạy local nên dữ liệu không rời máy.
- Sau khi đổi phải nạp lại tài liệu để các đoạn được mã hóa lại bằng model mới.
- **Chiếu / thao tác:** ảnh `owui_23b_embedding_nomic.png` — chỉ ô Embedding Model nay là nomic-embed-text.

### Slide 37 — Trợ lý RAG · Bước 6: Generate  ·  ~4 phút
- Bước cuối (6/6) — Generate, sinh câu trả lời; tạo model trợ lý riêng: Workspace → Models → **+**.
- Base model `qwen3:1.7b` + System Prompt = phần Generate.
- System Prompt (van an toàn chống bịa, đã nêu ở slide Giới hạn RAG): chỉ dùng tài liệu · thiếu → trả lời "không đề cập" · luôn trích nguồn.
- Gắn thẳng Knowledge base vào model → khỏi gõ `#` gọi kho mỗi lần.
- Lưu thành trợ lý → chọn 1 click, dùng lại mọi lúc.
- **Chiếu / thao tác:** demo gắn Knowledge base vào trợ lý trong Workspace → Models.

### Slide 38 — Trợ lý "Quy chế ATTT": Prompt + Knowledge  ·  ~1.5 phút
- Ảnh trợ lý hoàn chỉnh: ghép System Prompt (cách trả lời) + Knowledge (kho 6 tài liệu đã gắn).
- Hai thứ đi cùng nhau: trợ lý vừa tra đúng kho, vừa trả lời có kỷ luật.
- **Chiếu / thao tác:** ảnh `owui_model_chat.png` — chỉ vùng System Prompt + vùng Knowledge gắn kèm.

### Slide 39 — Hỏi đáp có trích nguồn  ·  ~3 phút
- Chọn trợ lý vừa tạo → hỏi câu thật: "Quy trình xử lý sự cố ATTT gồm những bước nào?".
- Câu trả lời bám sát tài liệu, không bịa.
- Trích nguồn: hiện tên file, bấm vào xem đúng đoạn gốc.
- Nhờ trích nguồn → kiểm chứng được; đây là khác biệt cốt lõi với ChatGPT thường.
- Có thể hỏi gợi mở: vì sao trích nguồn lại quan trọng với tài liệu nội bộ?
- **Chiếu / thao tác:** gõ thật câu hỏi vào trợ lý cho lớp xem chạy trực tiếp.

### Slide 40 — Retrieve: truy hồi đúng nguồn  ·  ~1.5 phút
- Pha Retrieve diễn ra ngay khi bấm gửi câu hỏi.
- Hệ thống đã kéo ra đúng các đoạn liên quan nhất = Top K đoạn đã đặt ở phần thông số.
- Bằng chứng Retrieve hoạt động trước khi model sinh câu trả lời.
- **Chiếu / thao tác:** ảnh `owui_24c_retrieved.png` — chỉ danh sách nguồn được truy hồi.

### Slide 41 — Trả lời kèm trích nguồn  ·  ~1.5 phút
- Ảnh thành quả: câu trả lời tiếng Việt mạch lạc, kèm trích nguồn ngay bên dưới.
- Bấm vào nguồn → nhảy thẳng về đoạn gốc trong tài liệu để đối chiếu.
- Đúng thước đo đặt ra đầu buổi: hỏi 1 câu về tài liệu → trả lời đúng + có trích nguồn.
- **Chiếu / thao tác:** ảnh `owui_24a_answer_vi.png` — chỉ câu trả lời + phần trích nguồn.

### Slide 42 — Tinh chỉnh & kiểm chứng  ·  ~3 phút
- Top K 3 → 5: câu trả lời đầy đặn hơn nhưng chậm hơn (xử lý nhiều đoạn hơn).
- Model qwen3:1.7b → 4b: câu chữ mạch lạc hơn.
- Khi hỏi nên dùng từ tự nhiên thay vì mã ngắn (viết rõ thay vì P1, MFA) — embedding khớp nghĩa tốt hơn khớp ký tự.
- Kiểm chứng quan trọng nhất: hỏi câu ngoài tài liệu → trợ lý đáp "Tài liệu không đề cập" = RAG đang chạy đúng, không bịa.
- Có thể hỏi gợi mở: nếu trợ lý vẫn trả lời câu ngoài tài liệu thì sửa ở đâu? (gợi về System Prompt).
- **Chiếu / thao tác:** demo nâng Top K lên 5 + đặt một câu hỏi cố tình ngoài phạm vi để lớp thấy trợ lý từ chối đúng cách.

# Phần F — Áp dụng & Tổng kết (Slide 43–47)

### Slide 43 — Áp dụng & Tổng kết  ·  ~0.5 phút
- Slide divider: chuyển từ phần thực hành sang phần đúc kết + áp dụng thực tế.
- Khung phần cuối: tổng kết thành quả → khi nào dùng local/cloud → checklist bảo mật để đưa vào tổ chức.
- Thông điệp gói: "từ làm được sang dùng được" — đã dựng xong hệ, giờ bàn cách triển khai an toàn, đúng nơi đúng chỗ.

### Slide 44 — Thành quả buổi học  ·  ~2.5 phút
- 3 thành quả cụ thể trong ~2 giờ: (1) chạy LLM offline — câu hỏi & câu trả lời ở lại máy; (2) xây RAG local trên chính tài liệu của mình — máy "biết đọc kho của bạn", không chỉ "biết nói"; (3) trả lời có trích nguồn, không cần viết dòng code nào.
- Trích nguồn = phần chứng minh đúng thước đo đã hứa ở Slide 2 (hỏi 1 câu → đúng + có nguồn).
- **Chiếu / thao tác:** sơ đồ kiến trúc tổng thể (`01_overall_architecture.png`) — đây chính là hệ học viên vừa dựng: tài liệu → embedding → vector DB → LLM trả lời có nguồn. Lia nhanh từ đầu vào tới đầu ra.
- Có thể hỏi gợi mở: trong 3 việc này, việc nào ban đầu tưởng khó nhất mà hóa ra làm được?

### Slide 45 — Áp dụng trong tổ chức  ·  ~3 phút
- Ma trận quyết định theo độ nhạy dữ liệu; nguyên tắc cốt lõi: dữ liệu càng nhạy → càng ưu tiên local.
- Dữ liệu nhạy + tra cứu nội bộ → Local.
- Dữ liệu nhạy + tác vụ phức tạp → vẫn Local, nâng model lớn hơn (4b/8b) cho đủ sức.
- Dữ liệu công khai + cần chất lượng tối đa → Cloud hợp lý (không rủi ro lộ, lại tận dụng model mạnh nhất).
- Use case áp dụng ngay: HR (hồ sơ nhân sự) · Pháp chế (hợp đồng, quy định) · R&D (tài liệu kỹ thuật nội bộ) · CSKH (kho tri thức).
- Có thể hỏi gợi mở: bộ phận nào ở đơn vị đang giữ dữ liệu nhạy nhất — đó là nơi nên triển khai local đầu tiên.

### Slide 46 — Checklist bảo mật  ·  ~3 phút
- Điểm chốt mở đầu: "không rời máy" chưa đồng nghĩa "an toàn tuyệt đối" — cần thêm 4 lớp phòng vệ.
- Phân loại tài liệu trước khi nạp — biết rõ cái gì được đưa vào kho, cái gì không.
- Redact PII trước khi index — che/xóa thông tin cá nhân (số căn cước, số điện thoại) trước khi đưa vào hệ thống.
- Phân quyền — bật `WEBUI_AUTH`, mỗi người 1 tài khoản riêng (không dùng chung) để kiểm soát ai truy cập gì.
- Audit log — ghi lại ai hỏi gì, truy vấn vào tài liệu nào, để truy vết khi cần.
- Thông điệp: 4 việc này biến một bản demo thành hệ thống dùng được nghiêm túc trong tổ chức.
- **Chiếu / thao tác:** sơ đồ rủi ro bảo mật (`08_security_risks.png`) — mỗi mục checklist là một lớp phòng vệ tương ứng.
- Có thể hỏi gợi mở: trong 4 việc này, việc nào đơn vị đã có sẵn quy trình, việc nào còn thiếu?

### Slide 47 — Cảm ơn!  ·  ~1 phút
- Slide kết: chốt lại thông điệp xuyên suốt — học viên hoàn toàn tự xây được hệ RAG local cho riêng mình, và dữ liệu không rời máy.
- Điều mang về không phải vài thao tác lẻ, mà là niềm tin tự dựng được hệ thống của chính mình.
- Mở phần hỏi đáp.
