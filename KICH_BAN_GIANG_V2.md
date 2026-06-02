# Kịch bản giảng (V2) — Workshop: Local LLM · RAG

**Giảng viên:** PGS.TS. Lê Anh Cường (chuyên ngành NLP)
**Mục tiêu:** Học viên **nắm vững lý thuyết RAG** và xây được một hệ **RAG local** nhanh, hiệu quả — **hoàn toàn qua giao diện Open WebUI, không cần code**. RAG là **trục chính**; Local LLM/Ollama là nền tảng.
**Đối tượng:** đa dạng — có người không biết code (dân văn phòng, nghiên cứu) lẫn người code.
**Thời lượng dự kiến:** ~113 phút (xem bảng + ghi chú cắt gọn nếu cần khít 2h).

> Đây là **storyboard theo từng slide** để hình dung buổi học — CHƯA phải slide. Mỗi slide gồm: *nội dung trên slide · hình/diagram · GV làm · HV làm · lời giảng · chuyển cảnh*.

## Quy ước
- "..." = câu nói gần nguyên văn cho giảng viên đọc.
- **CẦN TẠO** = hình/asset chưa có trong repo, phải tạo trước khi lên slide.
- **[loại]** = phân loại slide (bìa / lý thuyết / công cụ / làm theo / kết quả / demo / kết bài).

## Chuẩn bị TRƯỚC buổi (bắt buộc)
- [ ] Pull sẵn model ở nhà: `ollama pull qwen3:1.7b` + `ollama pull nomic-embed-text`. **KHÔNG tải tại lớp** (~1.7GB dễ nghẽn Wi-Fi chung).
- [ ] `docker compose up -d` chạy sẵn → mở http://localhost:3000 kiểm tra OK; nạp sẵn 2-3 tài liệu mẫu từ `2_rag/data/` vào 1 Knowledge base; đổi **Embedding Model** về `nomic-embed-text` trong Settings.
- [ ] Smoke test 1 câu "chạy chắc": *"Quy trình xử lý sự cố ATTT gồm những bước nào?"*
- [ ] Tạo trước các hình **CẦN TẠO** (xem Phụ lục A).

## Bảng thời lượng (tổng ~113 phút)

| Phần | Thời lượng |
|---|---|
| Phần A — Mở đầu (Slide 1–6) | ~16' |
| Phần B — RAG lý thuyết, TRỤC CHÍNH (Slide 7–12) | ~30' |
| Phần C — Công cụ & chạy LLM local (Slide 13–17) | ~21' |
| Phần D — Quay lại RAG + Open WebUI · thực hành (Slide 18–25) | ~34' |
| Phần E — Kết bài (Slide 26–28) | ~12' |

> ⚠️ Tổng ~113 phút → **vừa khít 2h**. Phần A-C (Slide 1-17) ~67' là khối nghe/xem khá dài; Slide 16 đã có 1 lần gõ `ollama run` để học viên chạm máy sớm, còn thực hành RAG dồn ở Phần D.

## Ghi chú biên tập (từ vòng rà soát — nên xử lý khi dựng slide)
1. **Nhịp dạy:** chèn 1 "khoảnh khắc tay chạm máy" SỚM — cho cả lớp gõ `ollama run qwen3:1.7b` ngay sau Slide 16, đừng đợi đến Phần D mới thực hành.
2. **Cắt gọn để khít 2h:** cân nhắc gộp **Slide 4+5** (giải pháp + so sánh local/cloud) và **Slide 10+11**; nén **Slide 12** còn ~4'.
3. **Nhất quán xuyên suốt:** 1 model embedding = **nomic-embed-text (768 chiều)**; 1 thông điệp tải = "dùng `ollama run`, nó **tự tải**" (tránh lẫn `pull`/`run`).
4. **Diagram:** `08_security_risks` chỉ dùng ở **1 chỗ** đúng nội dung; `01_overall_architecture` diễn chính ở **Slide 6**, nơi khác chỉ khoanh ô nhỏ (tránh chiếu lại y nguyên 3 lần).
5. **Slide 11:** chốt **1 phương án** (đã-cài-trước HOẶC pull-nền), không để slide "tùy quyết tại lớp".

---

# Phần A — Mở đầu (Slide 1–6)

### Slide 1 — Local LLM · RAG  ·  ~2 phút  ·  [loại: bìa]
- **Trên slide (nội dung chữ):**
  - Tiêu đề lớn: **"Local LLM · RAG"**
  - Phụ đề giá trị: *"Xây trợ lý AI đọc tài liệu của bạn — chạy 100% trên máy, dữ liệu không rời máy"*
  - Dòng bắt buộc (đặt nổi bật phía dưới): **"Người trình bày: PGS.TS. Lê Anh Cường"** — *(chuyên ngành Xử lý ngôn ngữ tự nhiên — NLP)*
  - Góc dưới: tên đơn vị / ngày / thời lượng ~2 giờ
- **Hình/diagram:** CAN TAO: ảnh hero ngang gợi 2 lớp khái niệm LLM → RAG (ví dụ: một laptop ở giữa, bên trái icon "bộ não" = LLM, bên phải icon "tài liệu + kính lúp" = RAG nổi bật nhất/lớn nhất; nền tông xanh đậm, có hàng chữ nhỏ "offline · private · open-source"). Phải làm RAG là điểm nhấn thị giác trung tâm.
- **Giảng viên LÀM:** Chiếu slide bìa ngay khi học viên vào phòng (để sẵn trước giờ). Đứng cạnh màn hình, chào lớp, tự giới thiệu ngắn. Không thao tác máy.
- **Học viên LÀM:** Ổn định chỗ ngồi, mở máy (nếu mang theo), nghe. KHÔNG làm gì khác.
- **Lời giảng (nói gì):**
  - Chào và định khung: hôm nay không nghe lý thuyết suông mà cùng dựng một trợ lý AI chạy trên chính máy của mình.
  - Nhấn trọng tâm là RAG: *"Trọng tâm buổi hôm nay là RAG — cách cho AI đọc và trả lời dựa trên tài liệu của chính các bạn. Local LLM là nền móng để RAG chạy được offline."*
  - Trấn an đối tượng đa dạng: *"Lớp mình có cả người không code và người code — phần thực hành tôi sẽ dùng giao diện bấm chuột, nên không biết lập trình vẫn theo được."*
- **Chuyển cảnh → Slide 2:** *"Trước khi build, ta chốt nhanh: sau 2 giờ này các bạn sẽ làm được gì."*

---

### Slide 2 — Mục tiêu buổi học  ·  ~2 phút  ·  [loại: mục tiêu]
- **Trên slide (nội dung chữ):**
  - Tiêu đề: **"Sau buổi này, bạn sẽ…"**
  - 3 mục tiêu chính (đánh số, RAG đứng đầu):
    1. **HIỂU** RAG là gì và **6 thành phần** của một hệ RAG chạy local
    2. **XÂY** được một hệ RAG local trên tài liệu của chính mình (qua giao diện, không cần code)
    3. **BIẾT** cách chọn model LLM phù hợp (nhẹ vs mạnh) và chạy nó offline bằng Ollama
  - Khung nhỏ "Thước đo thành công": *"Cuối buổi, bạn hỏi 1 câu về tài liệu của bạn → trợ lý trả lời đúng + chỉ ra trích từ tài liệu nào."*
- **Hình/diagram:** CAN TAO: hình 3 ô checkbox xếp dọc (HIỂU / XÂY / BIẾT), ô "XÂY RAG local" tô đậm nổi bật; bên dưới một dải "thước đo thành công" hình đích ngắm (target). Đơn giản, ít chữ.
- **Giảng viên LÀM:** Chiếu slide, đọc lướt 3 mục tiêu, dừng lâu hơn ở mục 1 và 2. Chỉ tay vào khung "Thước đo thành công".
- **Học viên LÀM:** Nghe, đối chiếu kỳ vọng cá nhân. KHÔNG làm gì.
- **Lời giảng (nói gì):**
  - Nêu rõ trục: *"Mục tiêu số một là HIỂU RAG — vì đây là phần dùng được ngay cho công việc của các bạn: tra quy chế, tra tài liệu nội bộ, tra ghi chú nghiên cứu."*
  - Định nghĩa thành công cụ thể: *"Tôi coi buổi này thành công nếu cuối giờ bạn hỏi một câu về đúng tài liệu của bạn, và trợ lý trả lời đúng kèm câu 'trích từ file nào'. Đó là khác biệt căn bản giữa RAG và một chatbot bịa."*
- **Chuyển cảnh → Slide 3:** *"Nhưng tại sao phải tự build chạy local, trong khi ngoài kia ChatGPT, Gemini có sẵn? Câu trả lời nằm ở một chữ: dữ liệu."*

---

### Slide 3 — Đặt vấn đề: rủi ro khi gửi dữ liệu cho API bên thứ ba  ·  ~4 phút  ·  [loại: lý thuyết]
- **Trên slide (nội dung chữ):**
  - Tiêu đề: **"Khi bạn gõ vào ChatGPT/API — dữ liệu của bạn đi đâu?"**
  - 3 rủi ro chính (mỗi cái 1 dòng, có dẫn nguồn):
    - **Rò rỉ qua nhân viên:** *Samsung (5/2023) cấm nhân viên dùng ChatGPT nội bộ sau khi mã nguồn & ghi chú họp bị dán vào ChatGPT* — nguồn: Bloomberg / Reuters, 5/2023.
    - **Điều khoản sử dụng:** nhiều dịch vụ ghi rõ *"data may be used to improve our models"* → dữ liệu của bạn có thể thành dữ liệu huấn luyện.
    - **Chi phí & phụ thuộc:** trả tiền **theo từng lượt gọi (per-token)**, càng dùng nhiều càng tốn; phụ thuộc mạng & nhà cung cấp.
  - Câu nhấn (in đậm cuối slide): **"Gửi prompt đi = gửi dữ liệu ra khỏi tổ chức của bạn."**
  - Tag góc: **[HỎI LỚP]**
- **Hình/diagram:** docs/diagrams/08_security_risks.png — *(dùng làm hình minh họa nền nguy cơ; khi giảng chỉ chỉ vào, sẽ nói sâu hơn ở phần bảo mật cuối buổi).* Nếu thấy 08 thiên về rủi ro RAG hơn là rủi ro API → giữ làm phụ; điểm nhấn slide vẫn là 3 dòng dẫn nguồn ở trên.
- **Giảng viên LÀM:** Chiếu slide. Đọc ví dụ Samsung như một câu chuyện thật. Hỏi lớp và chờ vài giây lấy phản hồi (giơ tay). Chỉ vào diagram 08 lướt qua.
- **Học viên LÀM:** Nghe; trả lời câu hỏi tương tác (giơ tay / nói nhanh). Suy nghĩ về dữ liệu của chính cơ quan mình.
- **Lời giảng (nói gì):**
  - Kể ví dụ cụ thể: *"Tháng 5 năm 2023, Samsung phát hiện kỹ sư dán cả mã nguồn và biên bản họp vào ChatGPT để nhờ tóm tắt. Hệ quả: công ty cấm ChatGPT nội bộ. Dữ liệu một khi gửi đi, ta không kéo lại được."*
  - Điều khoản: *"Hãy đọc kỹ — nhiều dịch vụ ghi 'dữ liệu có thể dùng để cải thiện mô hình'. Nghĩa là câu hỏi nhạy cảm của bạn có thể nằm trong tập huấn luyện sau này."*
  - [HỎI LỚP]: *"Cơ quan các bạn có tài liệu nào mà tuyệt đối không được lọt ra ngoài không? Hợp đồng, hồ sơ nhân sự, bệnh án, đề tài chưa công bố?"* — chờ phản hồi.
- **Chuyển cảnh → Slide 4:** *"Vậy giải pháp là gì? Đơn giản: đừng gửi đi đâu cả — kéo nguyên cái LLM về máy mình."*

---

### Slide 4 — Giải pháp: LLM local + nhu cầu thực tế  ·  ~3 phút  ·  [loại: lý thuyết]
- **Trên slide (nội dung chữ):**
  - Tiêu đề: **"Giải pháp: đưa LLM về máy bạn + ứng dụng lên trên"**
  - Trục đậm xuyên suốt (banner trên cùng): **"Dữ liệu của bạn KHÔNG rời máy."**
  - Sơ đồ tầng: **LLM local (nền tảng)** → bên trên là **RAG** (làm nổi bật).
  - Bảng "Nhu cầu thực tế theo nhóm" (4 dòng):
    - **Văn phòng/hành chính:** tra quy định, quy chế nội bộ mà không lộ ra ngoài.
    - **Lập trình viên:** trợ lý code chạy offline, không gửi mã nguồn lên cloud.
    - **Tổ chức/DN:** chatbot nội bộ không rò rỉ dữ liệu khách hàng.
    - **Y tế:** xử lý hồ sơ bệnh nhân theo yêu cầu bảo mật (vd HIPAA).
- **Hình/diagram:** CAN TAO: sơ đồ tầng 2 lớp — đáy "LLM local (Ollama)" rộng, lớp trên "RAG — đọc tài liệu của bạn" (tô đậm, to nhất). Có thể tái dùng tinh thần của docs/diagrams/01_overall_architecture.png nhưng slide này nên là sơ đồ tầng đơn giản hơn để tránh trùng với Slide 6.
- **Giảng viên LÀM:** Chiếu slide. Chỉ vào banner "dữ liệu không rời máy". Đi qua từng dòng nhu cầu, dừng ở nhóm khớp với phần đông học viên trong phòng.
- **Học viên LÀM:** Nghe; tự nhận diện mình thuộc nhóm nào. KHÔNG làm gì.
- **Lời giảng (nói gì):**
  - Khẳng định trục: *"Cả buổi hôm nay xoay quanh đúng một câu: dữ liệu của bạn không rời máy. Mọi thứ ta build đều chạy offline."*
  - Định vị RAG: *"LLM local là cái nền. Nhưng LLM trống rỗng thì chỉ biết kiến thức chung — muốn nó trả lời theo tài liệu của bạn, ta cần RAG. Đó là lý do RAG là trục chính hôm nay."*
  - Cá nhân hóa: *"Bạn làm văn phòng thì đây là máy tra quy chế; bạn là dev thì đây là trợ lý code offline; bạn ngành y thì hồ sơ bệnh nhân không bao giờ ra khỏi phòng."*
- **Chuyển cảnh → Slide 5:** *"Nghe local là 'an toàn' thì hấp dẫn, nhưng công bằng mà nói nó cũng có cái giá. Ta so sánh thẳng local với cloud trước khi đi tiếp."*

---

### Slide 5 — So sánh nhanh: Local vs Cloud  ·  ~3 phút  ·  [loại: lý thuyết]
- **Trên slide (nội dung chữ):**
  - Tiêu đề: **"Local vs Cloud — cân bằng, không một chiều"**
  - Bảng so sánh 5 tiêu chí:

    | Tiêu chí | Local (tự chạy) | Cloud / API bên thứ ba |
    |---|---|---|
    | **Bảo mật** | ✅ Dữ liệu ở lại máy | ⚠️ Gửi ra ngoài |
    | **Chi phí** | ✅ Trả 1 lần (máy), không tính lượt | 💸 Tính theo token, dùng nhiều tốn nhiều |
    | **Chất lượng** | ⚠️ Model nhẹ, kém model top | ✅ Mô hình mạnh nhất (GPT, Gemini) |
    | **Độ trễ** | ⚠️ Chậm trên CPU | ✅ Nhanh (có GPU lớn) |
    | **Vận hành** | ⚠️ Tự cài, tự bảo trì | ✅ Bấm là dùng |
  - Câu chốt: **"Local KHÔNG thay thế hoàn toàn cloud — nó thắng ở bảo mật & chi phí, đánh đổi chất lượng & tốc độ."**
- **Hình/diagram:** CAN TAO: bảng cân (cán cân thăng bằng) 2 đĩa Local / Cloud, mỗi đĩa liệt kê ưu điểm — nhấn mạnh thông điệp "đánh đổi", không phải "local luôn thắng". (Bảng so sánh ở trên là asset chính của slide.)
- **Giảng viên LÀM:** Chiếu slide. Đi qua từng hàng. Chủ động thừa nhận điểm yếu của local (chậm, model nhẹ) để giữ uy tín, tránh framing một chiều.
- **Học viên LÀM:** Nghe, ghi chú nếu muốn. KHÔNG làm gì.
- **Lời giảng (nói gì):**
  - Đặt thẳng: *"Tôi đặt bảng này sớm để các bạn không nghĩ local là viên đạn bạc. Nó không phải."*
  - Thừa nhận đánh đổi: *"Model chạy local hôm nay — tôi dùng một model nhẹ khoảng 1.7 tỷ tham số — không thông minh bằng GPT mới nhất, và trên CPU thì chậm hơn. Bù lại: dữ liệu không đi đâu, và không tốn tiền theo từng câu hỏi."*
  - Định hướng chọn đúng việc: *"Việc nhạy cảm, lặp lại nhiều, tra tài liệu nội bộ → local rất hợp. Việc cần suy luận đỉnh cao, dữ liệu không nhạy cảm → cứ dùng cloud. Hiểu đánh đổi để chọn đúng."*
- **Chuyển cảnh → Slide 6:** *"Đã rõ tại sao và đánh đổi gì. Giờ xem lộ trình 2 giờ tới ta đi qua những gì."*

---

### Slide 6 — Lộ trình buổi học  ·  ~2 phút  ·  [loại: divider]
- **Trên slide (nội dung chữ):**
  - Tiêu đề: **"Lộ trình 2 giờ — RAG là trung tâm"**
  - 2 chặng (đánh số, chặng 2 tô đậm nhất):
    1. **Nền tảng:** Cài & chạy LLM local bằng Ollama + Docker *(công cụ)*
    2. **⭐ RAG — TRỌNG TÂM:** hiểu 6 thành phần → nạp tài liệu của bạn → hỏi & nhận câu trả lời có trích nguồn (qua Open WebUI)
  - Dòng dưới: *"Cả 2 chặng đều có thực hành."*
- **Hình/diagram:** docs/diagrams/01_overall_architecture.png — *(kiến trúc tổng thể: User → Open WebUI → RAG → Ollama, tất cả trong khung "Máy local offline"). Dùng để học viên thấy bức tranh lớn và vị trí của RAG ở giữa.*
- **Giảng viên LÀM:** Chiếu slide. Chỉ vào diagram 01: khoanh tay vào khối "Máy local (offline)" để nhấn mọi thứ chạy nội bộ; chỉ vào khối RAG và nói đây là phần ta dành nhiều thời gian nhất. Đếm "1-2" theo 2 chặng.
- **Học viên LÀM:** Nghe, nắm bản đồ tổng thể. KHÔNG làm gì.
- **Lời giảng (nói gì):**
  - Vẽ bản đồ: *"Đây là toàn bộ hệ thống ta sẽ dựng — và để ý: cả cái khung này nằm trong 'máy local, offline'. Không có mũi tên nào đi ra Internet."*
  - Nhấn trọng tâm: *"Chặng 1 là cài đặt nền tảng, làm nhanh. Chặng 2 — RAG — là nơi ta dừng lâu nhất, vì đây là thứ các bạn dùng được ngay."*
  - Cam kết thực hành: *"Hai chặng đầu các bạn sẽ tự gõ/tự bấm theo. Ai không quen code đừng lo — phần RAG ta làm qua giao diện Open WebUI, bấm chuột là chính."*
- **Chuyển cảnh → Slide 7:** *"Bắt đầu từ nền móng: làm sao kéo được một con LLM về chạy ngay trên máy bạn. Ta gặp hai công cụ — Ollama và Docker."*

# Phần B — RAG lý thuyết, TRỤC CHÍNH (Slide 7–12)

### Slide 7 — RAG là gì? · ~5 phút · [loại: lý thuyết]
- **Trên slide (nội dung chú):**
  - Tiêu đề lớn: **"RAG = cho LLM tra tài liệu TRƯỚC khi trả lời"**
  - Vấn đề: *LLM không biết tài liệu của BẠN.* Nó học từ Internet công khai tới một thời điểm cắt — không hề biết quy chế nội bộ, hợp đồng, email, sổ tay đơn vị bạn.
  - 2 lựa chọn tệ: (1) Hỏi thẳng → LLM **bịa** (hallucination); (2) Dán cả tập tài liệu vào prompt → quá dài, tốn token, vượt giới hạn context.
  - Giải pháp RAG: **Retrieval (tra) + Augmented (bổ sung) + Generation (sinh)** → tìm đúng vài đoạn liên quan → đưa cho LLM kèm câu hỏi → LLM trả lời dựa trên đoạn đó.
  - Ẩn dụ: *LLM = sinh viên giỏi nhưng KHÔNG được mang tài liệu vào phòng thi. RAG = mở thi, cho tra cứu sách trước khi viết bài.*
- **Hình/diagram:** CAN TAO: 1 hình ẩn dụ đơn giản 2 ô cạnh nhau — Ô trái "LLM một mình" (đầu người + dấu "?", mũi tên tới ô trả lời màu đỏ ghi "BỊA"); Ô phải "LLM + RAG" (đầu người + chồng tài liệu/kính lúp, mũi tên tới ô trả lời màu xanh ghi "ĐÚNG + trích nguồn"). Nếu không kịp tạo: dùng slide chỉ chữ với ẩn dụ "phòng thi".
- **Giảng viên LÀM:** Chiếu slide. Vẽ hoặc chỉ tay theo ẩn dụ phòng thi. Đặt 1 câu hỏi mở cho cả lớp: "Nếu hỏi ChatGPT 'Quy định mật khẩu đơn vị tôi là gì?' — nó trả lời được không, và nếu trả lời thì dựa vào đâu?" Chờ vài phản hồi.
- **Học viên LÀM:** Nghe, suy nghĩ, trả lời câu hỏi mở. KHÔNG gõ máy.
- **Lời giảng (nói gì):**
  - "Mô hình ngôn ngữ rất giỏi, nhưng nó chỉ biết những gì đã đọc trên Internet đến một thời điểm. Nó **không** biết tài liệu của riêng bạn — quy chế, hợp đồng, sổ tay nội bộ."
  - "Nếu bạn cứ hỏi thẳng, mô hình sẽ làm cái nó giỏi nhất: nói trôi chảy. Nhưng trôi chảy không có nghĩa là đúng — nó sẽ **bịa**, thuật ngữ gọi là hallucination."
  - "RAG giải quyết đúng một việc: trước khi để mô hình trả lời, ta **tra** đúng vài đoạn tài liệu liên quan, đưa cho nó, rồi mới bảo: trả lời dựa vào đây."
  - "Hãy nhớ ẩn dụ này suốt buổi: *LLM là sinh viên giỏi nhưng không được mang tài liệu. RAG biến nó thành thi mở — cho tra sách trước khi viết.*"
  - "Ba chữ R-A-G: Retrieval là tra, Augmented là bổ sung ngữ cảnh, Generation là sinh câu trả lời."
- **Chuyển cảnh → Slide 8:** "Vậy 'tra tài liệu rồi mới trả lời' diễn ra qua những bước nào? Đây là kiến trúc 6 thành phần — phần xương sống của cả buổi học."

---

### Slide 8 — Kiến trúc RAG: 6 thành phần · ~6 phút · [loại: lý thuyết]
- **Trên slide (nội dung chú):**
  - Tiêu đề: **"6 bước: Load → Chunk → Embed → Store → Retrieve → Generate"**
  - **OFFLINE — build index 1 lần** (làm sẵn, lặp lại khi tài liệu đổi):
    - **1. Load** — đọc file (.md, .pdf, .docx) thành text
    - **2. Chunk** — cắt nhỏ thành đoạn ~vài trăm ký tự
    - **3. Embed** — biến mỗi đoạn thành vector (dãy số)
    - **4. Store** — lưu vector vào Vector DB (ChromaDB)
  - **ONLINE — mỗi câu hỏi** (chạy lại mỗi lần hỏi):
    - **5. Retrieve** — embed câu hỏi, tìm top-k đoạn gần nghĩa nhất
    - **6. Generate** — đưa các đoạn đó + câu hỏi cho LLM → câu trả lời + nguồn
  - Khẩu quyết: *4 bước đầu làm 1 lần. 2 bước cuối chạy mỗi câu hỏi.*
- **Hình/diagram:** docs/diagrams/02_rag_pipeline.png (đã có sẵn — khung Offline dưới: Tài liệu → Loader → Chunker → Embedder → Vector DB; khung Online trên: Câu hỏi → Embed → Retrieve top-k → Generate → Câu trả lời + nguồn).
- **Giảng viên LÀM:** Chiếu diagram. Chỉ tay theo từng ô **theo đúng thứ tự 1→6**. Khoanh tay vào khung "Offline" nói "làm 1 lần", rồi khung "Online" nói "mỗi câu hỏi". Nhấn vào mũi tên đứt nét nối Vector DB lên Retrieve — "đây là chỗ câu hỏi gặp lại tài liệu".
- **Học viên LÀM:** Nghe, quan sát diagram, theo ngón tay GV. KHÔNG gõ máy. (Có thể chụp lại slide diagram làm bản đồ tham chiếu.)
- **Lời giảng (nói gì):**
  - "Cả hệ RAG chỉ gồm 6 hộp này thôi. Học thuộc 6 chữ là bạn nắm được kiến trúc: Load, Chunk, Embed, Store, Retrieve, Generate."
  - "Mấu chốt là tách làm hai pha. Bốn bước đầu — Load, Chunk, Embed, Store — gọi là **offline**, bạn làm **một lần** để dựng kho. Giống như sắp xếp thư viện."
  - "Hai bước cuối — Retrieve và Generate — là **online**, chạy lại **mỗi lần có câu hỏi**. Giống như đi vào thư viện đã sắp xếp sẵn để tìm sách."
  - "Để ý: câu hỏi cũng phải đi qua Embed — vì muốn so sánh câu hỏi với các đoạn tài liệu, cả hai phải cùng một 'ngôn ngữ số'. Đó là embedding, ta nói kỹ ngay slide sau."
  - "Lát nữa trên Open WebUI, đúng 6 bước này hiện ra thành các thông số bấm được — Upload, Chunk Size, Embedding Model, Top K, model chat — bạn chỉnh chứ không phải viết code."
- **Chuyển cảnh → Slide 9:** "Bước số 3 — Embed — là phép màu khiến RAG hơn hẳn tìm kiếm từ khóa. Ta mổ xẻ nó ngay bây giờ."

---

### Slide 9 — Embedding: biến chữ thành nghĩa · ~6 phút · [loại: lý thuyết]
- **Trên slide (nội dung chú):**
  - Tiêu đề: **"Embedding = biến chữ thành NGHĨA (vector ~768 chiều)"**
  - Mỗi đoạn text → một dãy ~768 số. Đoạn **nghĩa gần nhau → vector gần nhau** trong không gian.
  - Đo độ gần bằng **cosine similarity / distance** — *distance càng nhỏ → càng giống nghĩa.*
  - **Vì sao embedding > tìm từ khóa:** tìm từ khóa cần TRÙNG CHỮ. Hỏi "mã đăng nhập" mà tài liệu ghi "mật khẩu" → từ khóa **trượt**. Embedding hiểu chúng **cùng nghĩa** → vẫn tìm ra.
  - Ví dụ trực quan: similarity("xe đạp","xe máy") = CAO ↔ ("xe máy","rau muống xào tỏi") = THẤP.
  - **Chạy LOCAL** qua Ollama, model `nomic-embed-text` (768 chiều, 274MB). *Toàn bộ embedding tính trên máy bạn — KHÔNG gửi tài liệu đi đâu.*
- **Hình/diagram:** docs/diagrams/04_embedding_space.png (đã có — "xe máy" ở giữa, "xe đạp" d≈0.18, "ô tô" d≈0.30, "rau muống xào tỏi" d≈0.85 xa & khác nghĩa; chú thích "nghĩa gần → vector gần → distance nhỏ").
- **Giảng viên LÀM:** Chiếu diagram embedding. Chỉ vào 3 khoảng cách, nhấn "0.18 gần, 0.85 xa". Diễn giải bằng diagram: 'xe đạp/xe máy' sát nhau, 'rau muống xào tỏi' nằm xa — cho học viên thấy trực quan "nghĩa gần → vector gần". (Không chạy code; cả buổi thực hành RAG đều qua giao diện.)
- **Học viên LÀM:** Quan sát diagram, đối chiếu các khoảng cách. KHÔNG gõ máy.
- **Lời giảng (nói gì):**
  - "Máy tính không hiểu chữ, nó chỉ tính số. Embedding là phép biến mỗi đoạn chữ thành một dãy khoảng 768 con số — gọi là vector."
  - "Điều kỳ diệu: vector được học sao cho **nghĩa gần nhau thì số gần nhau**. 'Xe đạp' và 'xe máy' đứng sát nhau; 'rau muống xào tỏi' nằm tận đẩu đâu."
  - "Đây chính là lý do RAG thắng tìm từ khóa. Tìm từ khóa đòi **trùng chữ**: hỏi 'mã đăng nhập' nhưng tài liệu viết 'mật khẩu' là trượt ngay. Embedding hiểu hai cụm đó cùng nghĩa nên vẫn lôi ra được."
  - "Và rất quan trọng cho bài toán bảo mật của chúng ta: việc biến chữ thành vector này chạy **ngay trên máy bạn** bằng model nomic-embed-text qua Ollama. Tài liệu **không** rời khỏi máy."
- **Chuyển cảnh → Slide 10:** "Đã có vector, hai câu hỏi thực tế nảy ra: cắt tài liệu to bao nhiêu là vừa, và lưu/tìm vector ở đâu? Đó là chunking và vector DB."

---

### Slide 10 — Chunking, Vector DB & Top-k · ~6 phút · [loại: lý thuyết]
- **Trên slide (nội dung chú):**
  - **Chunking — cắt tài liệu thành đoạn:**
    - Quá NHỎ → mất ngữ cảnh (cắt ngang một ý)
    - Quá TO → loãng, lẫn nhiều thông tin thừa, tốn token
    - Sweet spot tiếng Việt: **~300–700 ký tự**, **overlap ~10–20%** để không cắt đứt ý ở rìa
    - Trong Open WebUI bạn đặt: **Chunk Size = 500**, **Chunk Overlap = 50** (Settings → Documents)
  - **Vector DB:** kho lưu vector + text gốc + metadata (tên file…); tìm "hàng xóm gần nhất" cực nhanh kể cả triệu vector (HNSW). *Open WebUI tự quản — bạn không phải dựng.*
  - **Retrieve top-k:** lấy `k` đoạn gần nhất (Open WebUI: **Top K = 3**). k cao → ngữ cảnh phong phú nhưng dễ nhiễu; k thấp → tập trung nhưng dễ sót
  - **"càng gần nghĩa càng liên quan"** — mỗi đoạn retrieve có điểm liên quan; Open WebUI hiển thị đoạn nguồn qua **citation/Sources** để bạn kiểm chứng
- **Hình/diagram:** docs/diagrams/02_rag_pipeline.png (chiếu lại, khoanh vào ô "2 Chunker" và "4 Vector DB / 5 Retrieve top-k"). Kèm minh họa khái niệm:
  - 3 thông số trong Settings: `Chunk Size = 500 / Chunk Overlap = 50 / Top K = 3`
  - ví dụ overlap: Chunk1 [0..500], Chunk2 [450..950]… (vẽ tay 2 thanh gối nhau)
- **Giảng viên LÀM:** Chiếu slide. Chỉ vào 3 thông số (Chunk Size / Chunk Overlap / Top K) — nói *"lát nữa ta sẽ chỉnh đúng 3 cái này trong Open WebUI"*. Vẽ tay 1 thanh ngang chia đoạn có phần gối nhau để giải thích overlap.
- **Học viên LÀM:** Quan sát diagram + 3 thông số. KHÔNG cần gõ gì.
- **Lời giảng (nói gì):**
  - "Vì sao phải cắt nhỏ? Vì nếu nhét cả tài liệu vào, vector sẽ là trung bình của quá nhiều ý — tìm kiếm sẽ mờ. Cắt nhỏ giúp mỗi vector mang một ý rõ ràng."
  - "Nhưng cắt quá nhỏ thì lại đứt ngữ cảnh. Cho nên có hai núm vặn: **kích thước chunk** và **overlap** — phần gối lên nhau giữa hai đoạn để không cắt ngang một ý ở rìa. Ở đây ta dùng 500 ký tự, gối 50."
  - "Vector lưu ở đâu? Vào **vector database** — Open WebUI tự quản (mặc định dùng ChromaDB). Nó giữ vector kèm text gốc và metadata như tên file, và tìm hàng xóm gần nhất rất nhanh."
  - "Mỗi câu hỏi, ta lấy **top-k** đoạn gần nhất. Ở đây k = 3. Open WebUI gắn các đoạn này thành **trích nguồn (Sources)** dưới câu trả lời — bấm vào là thấy đúng đoạn RAG đang dựa vào."
- **Chuyển cảnh → Slide 11:** "Trước khi sang phần giới hạn và đánh giá, một lưu ý vận hành quan trọng cho buổi học hôm nay về việc tải model."

---

### Slide 11 — [LƯU Ý VẬN HÀNH] Pull model trong lúc giảng · ~1 phút · [loại: lý thuyết / note quyết định]

> GHI CHÚ CHO GV: đây có thể là **một dòng lưu ý chèn vào cuối Slide 10** hoặc một slide cực ngắn. KHÔNG nhất thiết tách slide riêng. Quyết định ngay tại lớp tùy đã yêu cầu cài trước hay chưa.

- **Trên slide (nội dung chú):** (chỉ hiện nếu pull live)
  - "Trong lúc nghe lý thuyết, ai CHƯA tải model hãy chạy:"
  - `ollama pull qwen3:1.7b` (LLM, ~1.4GB)
  - `ollama pull nomic-embed-text` (embedding, ~274MB)
  - Lưu ý: **chỉ tải model NHỎ** trong lớp; model lớn (4b/8b) để tải ở nhà.
- **Hình/diagram:** không cần. (Tùy chọn CAN TAO: 1 dòng QR/đường dẫn `0_setup/pull_models.ps1`.)
- **Giảng viên LÀM:** **NẾU đã yêu cầu cài trước buổi → BỎ slide này, chỉ nói 1 câu.** NẾU pull live → bật slide, đọc 2 lệnh, dặn cả lớp chạy song song trong lúc GV giảng tiếp Slide 12, để model tải xong vừa kịp vào phần thực hành.
- **Học viên LÀM:** (nếu pull live) Mở terminal, dán 2 lệnh `ollama pull …`, để chạy nền, **vẫn nghe giảng**. (nếu đã cài trước) KHÔNG làm gì.
- **Lời giảng (nói gì):**
  - "Nếu hôm nay bạn chưa tải model, tranh thủ chạy ngay hai lệnh này trong lúc tôi giảng nốt phần lý thuyết — đến mục thực hành là vừa xong."
  - "Lưu ý: ta **chỉ** tải bản nhỏ qwen3:1.7b. Cả lớp cùng tải bản lớn một lúc sẽ **nghẽn Wi-Fi**, mất cả buổi. Bản lớn 4b/8b để về nhà tải."
  - (nếu đã cài trước) "May là buổi trước đã dặn cài rồi, nên ta đi tiếp ngay."
- **Chuyển cảnh → Slide 12:** "Cuối phần lý thuyết — và đây là phần dân NLP cần nắm nhất: RAG có giới hạn gì, và làm sao biết một hệ RAG là TỐT?"

---

### Slide 12 — Giới hạn RAG & Đánh giá chất lượng · ~6 phút · [loại: lý thuyết]
- **Trên slide (nội dung chú):**
  - **RAG vẫn có thể BỊA khi:**
    - Retrieve **sai** → đưa nhầm đoạn → LLM trả lời sai một cách tự tin ("rác vào → rác ra")
    - Câu hỏi **ngoài tài liệu** → không có đoạn nào đúng → cần **System Prompt** bắt LLM nói *"Tài liệu không đề cập"* (ta sẽ dán prompt này vào Open WebUI ở Slide 23)
    - Chất lượng phụ thuộc **chunking + embedding** — cắt dở / embed yếu → cả hệ kém theo
  - **Làm sao biết RAG TỐT?**
    - **Faithfulness (bám nguồn):** câu trả lời có **đúng** dựa trên đoạn đã retrieve không? (yêu cầu LLM **trích nguồn** → người dùng kiểm chứng được)
    - **Kiểm bằng Sources:** bấm vào trích nguồn — nếu đoạn nguồn không thật sự chứa câu trả lời → cảnh giác (câu hỏi có lẽ ngoài tài liệu)
    - **Khung đánh giá bài bản:** **RAGAS** — đo faithfulness, answer relevancy, context precision/recall (mức intuition, không demo)
- **Hình/diagram:** docs/diagrams/08_security_risks.png (rủi ro RAG — tận dụng cho khung "RAG sai thì hậu quả gì"). Kèm **System Prompt mẫu cho RAG**: nguyên tắc *"Chỉ trả lời dựa vào tài liệu / Nếu không đủ thông tin nói rõ / Trích nguồn"*.
- **Giảng viên LÀM:** Chiếu slide. (Demo thật sẽ ở Phần D trên Open WebUI.) Nêu trước điều cần để ý: phần **trích nguồn (Sources)** dưới câu trả lời. Báo trước thí nghiệm ở **Slide 25**: hỏi **một câu ngoài tài liệu** (vd "Lương trung bình ngành CNTT 2026?") → LLM nói "Tài liệu không đề cập" thay vì bịa → đó là RAG hoạt động ĐÚNG.
- **Học viên LÀM:** Nghe, quan sát. Suy nghĩ câu hỏi GV nêu: "câu trả lời này có thật sự nằm trong tài liệu không?" KHÔNG bắt buộc gõ.
- **Lời giảng (nói gì):**
  - "RAG không phải thuốc tiên. Nếu bước Retrieve lôi nhầm đoạn, LLM vẫn trả lời rất trôi chảy — nhưng sai. Quy tắc nhớ đời: **rác vào, rác ra**."
  - "Vậy làm sao đánh giá? Khái niệm quan trọng nhất là **faithfulness — độ bám nguồn**: câu trả lời có thật sự suy ra được từ đoạn đã tra không, hay LLM tự thêm thắt? Đây là lý do ta luôn bắt nó **trích nguồn** — để người đọc kiểm chứng."
  - "Một mẹo rẻ tiền nhưng hiệu quả: luôn **bấm vào phần trích nguồn (Sources)**. Nếu đoạn nguồn không thật sự chứa câu trả lời, khả năng cao câu hỏi nằm ngoài tài liệu — đừng tin câu trả lời vội."
  - "Muốn đo bài bản, giới chuyên môn dùng **RAGAS** — bộ chỉ số đo faithfulness, độ liên quan của câu trả lời, độ chính xác của ngữ cảnh. Hôm nay ta chỉ cần nắm tinh thần: **đo được thì cải tiến được.**"
  - "Lát nữa khi thực hành (Slide 25), thử hỏi một câu ngoài tài liệu — để ý nó nói 'Tài liệu không đề cập' chứ không bịa. **Đấy mới là một hệ RAG tốt.**"
- **Chuyển cảnh → Slide 13:** "Lý thuyết RAG đã đủ vững. Giờ ta đã có LLM local, có pipeline — nhưng gõ lệnh terminal thì khó cho người không code. Cần một GIAO DIỆN. Đó là Open WebUI."

# Phần C — Công cụ & chạy LLM local (Slide 13–17)

### Slide 13 — Ollama: "Docker cho LLM" + vai trò Docker  ·  ~4 phút  ·  [loại: công cụ]
- **Trên slide (nội dung chữ):**
  - Tiêu đề: **Ollama — chạy LLM local dễ như cài app**
  - Một dòng định vị: *"Ollama là Docker cho LLM"* — đóng gói model + cách chạy, ẩn hết phần khó.
  - 5 ưu điểm (mỗi ý 1 dòng, có icon):
    1. **Cài 1 lệnh** — `winget install Ollama.Ollama` là xong (không compile, không cấu hình CUDA).
    2. **Tự tối ưu phần cứng** — tự detect GPU/CPU, tự fallback. Không cần biết VRAM / quantization.
    3. **Đổi model 1 dòng** — `ollama run X` → `ollama run Y`, không tải/cài lại từ đầu.
    4. **API tương thích OpenAI** — code viết cho ChatGPT chỉ đổi `base_url` là chạy.
    5. **Offline 100%** — pull model 1 lần, tắt mạng vẫn chạy. Dữ liệu không rời máy.
  - Ghi chú nhỏ cuối slide: *Docker ở workshop này dùng cho phần GIAO DIỆN (Open WebUI) ở Phần D — không bắt buộc cho LLM.*
- **Hình/diagram:** docs/diagrams/01_overall_architecture.png (chỉ vào ô "Ollama (LLM runtime)" để định vị Ollama trong toàn bộ kiến trúc). Tận dụng diagram đang bỏ không.
- **Giảng viên LÀM:** Chiếu slide. Đọc lần lượt 5 ưu điểm, dừng ở mỗi ý 1 nhịp. Khi nói ý 1, mở sẵn một cửa sổ terminal nhỏ bên cạnh (chưa gõ gì) để lát Slide 16 dùng tiếp. Khi nói "Docker cho LLM" thì so sánh: *Docker đóng gói app — Ollama đóng gói model.* Phân biệt rõ Docker ở đây KHÁC vai trò Docker chạy Open WebUI (sẽ gặp lại sau).
- **Học viên LÀM:** Nghe + quan sát. KHÔNG gõ gì (chưa tới phần thực hành).
- **Lời giảng (nói gì):**
  - "Cách dễ nhất để chạy một mô hình ngôn ngữ trên máy của chính mình là dùng Ollama. Tôi hay nói **Ollama là Docker cho LLM** — nó đóng gói model lại, mình chỉ việc gọi tên ra dùng."
  - "Năm điểm cần nhớ: cài đúng một lệnh; nó tự lo phần cứng cho mình; đổi model chỉ một dòng; API y hệt OpenAI nên code cũ chạy ngay; và quan trọng nhất với bài hôm nay — **offline một trăm phần trăm**."
  - "Cái 'offline 100%' này chính là lý do chúng ta ngồi đây: tài liệu mật không gửi ra ngoài, không qua API bên thứ ba."
  - "Lưu ý: Docker trong slide trước có thể làm vài bạn lo. Để chạy LLM thì **không cần Docker**. Docker chỉ xuất hiện ở phần giao diện đẹp Open WebUI lát nữa, và cũng là tuỳ chọn thôi."
- **Chuyển cảnh → Slide 14:** "Vậy để bắt đầu, mỗi người trong phòng cần chuẩn bị những gì? Và nếu bạn không biết code thì đường nào ngắn nhất?"

### Slide 14 — Học viên cần gì + 3 cấp độ từ dễ đến khó  ·  ~5 phút  ·  [loại: công cụ]
- **Trên slide (nội dung chữ):**
  - Tiêu đề: **Bạn cần chuẩn bị gì? — Chọn đúng cấp độ cho mình**
  - Khối "Tối thiểu cần có":
    - **Ollama** (bắt buộc, mọi cấp độ).
    - **RAM ≥ 8GB** (chạy được qwen3:1.7b).
    - **Python 3.10+** — *chỉ cần nếu đi đường code (cấp 2)*.
    - **Docker** — *chỉ cần nếu dùng giao diện Open WebUI (cấp 3)*.
  - Bảng 3 cấp độ (từ dễ → khó):
    | Cấp | Cách dùng | Cần gì thêm | Hợp với ai |
    |---|---|---|---|
    | **1 — Dễ nhất** | Gõ thẳng `ollama run qwen3:1.7b` trong terminal | KHÔNG cần Python | Dân văn phòng, nghiên cứu, người không code |
    | **2 — Hiểu cơ chế** | Mở Jupyter notebook, chạy từng ô | Python + venv | Người muốn hiểu/đọc code |
    | **3 — Giao diện đẹp** | Open WebUI (chat như ChatGPT) | Docker | Ai muốn UI quen thuộc, dùng lâu dài |
  - Dòng nhấn (to, màu): *Không biết code? → Đi thẳng Cấp 1. Một lệnh là có ChatGPT riêng trên máy bạn.*
- **Hình/diagram:** CẦN TẠO: hình "thang 3 bậc" (bậc 1 = terminal `ollama run`, bậc 2 = biểu tượng Jupyter, bậc 3 = biểu tượng Open WebUI), mũi tên "dễ → khó" chạy dọc theo bậc thang. (Nếu không kịp tạo: dùng nguyên bảng 3 cấp ở trên là đủ.)
- **Giảng viên LÀM:** Chiếu slide. Chỉ tay vào khối "tối thiểu" trước, nhấn mạnh chỉ Ollama + RAM 8GB là bắt buộc. Sau đó chỉ vào bảng 3 cấp, đọc từng hàng. Hỏi nhanh cả lớp: *"Ai ở đây không quen gõ lệnh / không viết code?"* — giơ tay — rồi nói thẳng với nhóm đó: "Các bạn theo Cấp 1, chỉ một dòng."
- **Học viên LÀM:** Nghe + tự xác định mình ở cấp nào. Có thể giơ tay khi GV hỏi. Chưa gõ gì.
- **Lời giảng (nói gì):**
  - "Đừng lo về danh sách dài. Bắt buộc chỉ có hai thứ: **Ollama và 8GB RAM**. Python chỉ cần nếu bạn muốn đụng vào code; Docker chỉ cần nếu bạn muốn giao diện đẹp."
  - "Tôi chia thành ba cấp độ. **Cấp 1 là dễ nhất** — bạn chỉ gõ `ollama run qwen3:1.7b` vào terminal là đã chat được, không cần một dòng Python nào."
  - "**Cấp 2** là mở notebook để nhìn thấy cơ chế bên trong — dành cho ai muốn hiểu code. **Cấp 3** là Open WebUI, đẹp như ChatGPT, đổi lại cần Docker."
  - "Thông điệp quan trọng: **nếu bạn không code, hãy đi thẳng Cấp 1**. Hôm nay tôi sẽ làm mẫu Cấp 1 trước, rồi mới tới Cấp 2 và 3."
- **Chuyển cảnh → Slide 15:** "Nhưng trước khi gõ lệnh, ta phải có model trên máy. Model lấy ở đâu, và máy của bạn nên chọn model nào? Mở trang chính thức ra xem."

### Slide 15 — [MÀN HÌNH] Tải tài nguyên: ollama.com/library + chọn model theo RAM  ·  ~4 phút  ·  [loại: làm theo]
- **Trên slide (nội dung chữ):**
  - Tiêu đề: **Lấy model ở đâu? — ollama.com/library**
  - Quy tắc chọn model theo RAM (bảng):
    | RAM máy | Model LLM khuyến nghị | Lệnh pull |
    |---|---|---|
    | **8GB** | `qwen3:1.7b` (mặc định workshop) | `ollama pull qwen3:1.7b` |
    | **16GB** | `qwen3:4b` (chất lượng cao hơn) | `ollama pull qwen3:4b` |
    | **GPU / RAM lớn** | `qwen3:8b` | `ollama pull qwen3:8b` |
  - Đừng quên embedding cho RAG: `ollama pull nomic-embed-text`.
  - Kinh nghiệm chọn model (bullet):
    - Bắt đầu **NHỎ rồi tăng** — 1.7b chạy mượt mới thử 4b.
    - Ưu tiên model **đa ngôn ngữ** cho tiếng Việt (họ Qwen rất tốt).
    - Để ý đuôi **quantization** (q4 = nhẹ, nhanh; bản đầy đủ = chính xác hơn, nặng hơn).
    - Số "b" = tỷ tham số ≈ độ "thông minh" nhưng cũng ≈ độ nặng.
- **Hình/diagram:** CHIẾU THẬT trang web ollama.com/library trên trình duyệt (không phải ảnh tĩnh). Dự phòng nếu mạng yếu: CẦN TẠO ảnh chụp màn hình ollama.com/library (trang danh sách model) để chiếu offline.
- **Giảng viên LÀM:** Mở trình duyệt, gõ **ollama.com/library**. Click vào model **qwen3** → cho thấy danh sách các size (1.7b, 4b, 8b...) và lệnh `ollama pull` mà trang tự gợi ý ở bên phải. Chỉ vào con số dung lượng từng bản. Quay lại slide chỉ bảng "RAM → model". Nhắc: đã có script `0_setup\pull_models.ps1` tự hỏi chọn bộ 1/2/3 và pull giúp.
- **Học viên LÀM:** Quan sát. Ai mang máy có thể tự mở ollama.com/library xem song song. Chưa pull (để tiết kiệm thời gian/mạng lớp — pull đã làm ở khâu chuẩn bị).
- **Lời giảng (nói gì):**
  - "Tất cả model nằm ở một chỗ: **ollama.com/library**. Đây giống như 'kho ứng dụng' cho LLM."
  - "Click vào Qwen3, các bạn thấy nhiều phiên bản theo kích thước. Bên phải nó cho sẵn luôn lệnh `ollama pull` — copy là chạy."
  - "Chọn theo RAM thôi: **8GB thì 1.7b, 16GB thì 4b, có GPU thì 8b**. Nguyên tắc vàng — bắt đầu nhỏ, chạy mượt rồi mới tăng."
  - "Với tiếng Việt, họ Qwen làm rất tốt nên tôi chọn làm mặc định. Và đừng quên một model nữa cho RAG là `nomic-embed-text` — lát phần RAG sẽ dùng."
- **Chuyển cảnh → Slide 16:** "Giả sử model đã nằm trên máy. Bây giờ là phần được chờ đợi nhất — gõ một lệnh và nói chuyện với LLM chạy ngay trên máy mình."

### Slide 16 — [LÀM THEO] Lệnh chạy LLM local  ·  ~4 phút  ·  [loại: làm theo]
- **Trên slide (nội dung chữ):**
  - Tiêu đề: **Chạy LLM local — gõ theo tôi**
  - **Cấp 1 (không cần Python) — chạy thẳng:**
    ```powershell
    ollama run qwen3:1.7b
    ```
    → hiện dấu nhắc `>>>`, gõ câu hỏi, Enter. Thoát: `/bye`.
  - **Cấp 2 (notebook) — chuẩn bị môi trường trước:**
    ```powershell
    # Windows PowerShell
    .\.venv\Scripts\Activate.ps1
    jupyter lab 1_ollama_basics\notebook.ipynb
    ```
    ```bash
    # macOS / Linux
    source .venv/bin/activate
    jupyter lab 1_ollama_basics/notebook.ipynb
    ```
  - Kiểm tra trước khi chạy (2 dòng nhỏ):
    - Đầu dòng lệnh có `(.venv)` chưa? (chỉ cần cho Cấp 2)
    - Ollama đang chạy? (Windows: icon Ollama ở khay hệ thống). Nếu báo `Connection refused` → mở app Ollama.
- **Hình/diagram:** CẦN TẠO: ảnh chụp dấu nhắc `>>>` của `ollama run qwen3:1.7b` (terminal trống vừa khởi động). Tạm thời có thể tái dùng docs/screenshots/terminal_ollama_chat.png nhưng nói rõ đó là kết quả sau khi hỏi.
- **Giảng viên LÀM:** Chuyển sang terminal đã mở sẵn từ Slide 13. Gõ trực tiếp **`ollama run qwen3:1.7b`** trước cả lớp. Khi hiện `>>>`, gõ một câu thật, ví dụ: *"Giải thích RAG trong 3 câu"*. Bấm Enter và **báo trước cho lớp sẽ phải chờ**. Trong lúc chờ, mở thêm tab nói về Cấp 2: bật venv → `jupyter lab`. Chỉ rõ dòng `(.venv)` ở đầu prompt.
- **Học viên LÀM:** Ai mang máy: GÕ THEO `ollama run qwen3:1.7b` rồi hỏi một câu của riêng mình. Ai không có máy: quan sát màn hình GV. Người theo Cấp 2 thì bật venv + mở Jupyter.
- **Lời giảng (nói gì):**
  - "Đây là cả bí mật của Cấp 1: một lệnh duy nhất — `ollama run qwen3:1.7b`. Gõ xong các bạn thấy ba dấu lớn hơn `>>>`, đó là chỗ mình hỏi."
  - "Tôi gõ thử: 'Giải thích RAG trong 3 câu'. Bấm Enter… **giờ ta chờ một chút**, tôi sẽ giải thích tại sao ở slide sau."
  - "Ai đi đường code thì hai dòng: bật môi trường ảo `.venv` rồi `jupyter lab`. Nhìn đầu dòng lệnh, phải thấy chữ `(.venv)` thì mới đúng."
  - "Nếu máy báo `Connection refused`, không phải lỗi của bạn — chỉ là app Ollama chưa bật. Tìm icon Ollama ở khay hệ thống, mở lên là xong."
- **Chuyển cảnh → Slide 17:** "Trong lúc model đang nghĩ — và nó sẽ im lặng vài chục giây — hãy xem kết quả phải trông như thế nào để các bạn đối chiếu."

### Slide 17 — [KẾT QUẢ DỰ KIẾN] Đối chiếu màn hình thật  ·  ~4 phút  ·  [loại: kết quả]
- **Trên slide (nội dung chữ):**
  - Tiêu đề: **Kết quả phải trông như thế này**
  - Hai ảnh đặt cạnh nhau:
    - Trái — **Cấp 1 (terminal):** câu trả lời RAG + dòng STATUS *qwen3:1.7b · ~73 tok/s · 100% offline · output sạch*.
    - Phải — **Cấp 2 (Jupyter):** notebook Module 1 chạy từng ô.
  - Hộp **LƯU Ý KHI DEMO** (màu nổi):
    - Trên CPU, model **im lặng 15–25 giây là BÌNH THƯỜNG** — đang nạp + suy nghĩ, không phải treo máy.
    - Sau đó chữ sẽ **stream ra dần** (hoặc hiện cả khối).
    - Có GPU thì nhanh hơn nhiều.
  - Câu chốt (to): *"Bạn vừa thấy: tải về và dùng model open-source KHÔNG hề khó."*
- **Hình/diagram:** docs/screenshots/terminal_ollama_chat.png (Cấp 1) + docs/screenshots/jupyter_m1.png (Cấp 2). Cả hai là ảnh THẬT có sẵn trong repo.
- **Giảng viên LÀM:** Quay lại terminal Slide 16 — lúc này nhiều khả năng câu trả lời ĐÃ hiện. So nó với ảnh terminal_ollama_chat.png trên slide: "y như nhau". Chỉ vào dòng STATUS (~73 tok/s, 100% offline). Sau đó chuyển sang ảnh jupyter_m1.png, đối chiếu với Jupyter đang mở (nếu đã bật). Nếu model vẫn đang chạy, dùng đúng khoảng chờ này để chỉ vào hộp "LƯU Ý KHI DEMO".
- **Học viên LÀM:** Đối chiếu màn hình của mình với ảnh trên slide. Ai khác kết quả thì giơ tay. Quan sát + cảm nhận "à, ra là chạy được thật".
- **Lời giảng (nói gì):**
  - "Đây là cái các bạn nên thấy. Bên trái là terminal — câu trả lời về RAG, và dòng trạng thái: khoảng 73 token mỗi giây trên CPU, **một trăm phần trăm offline**."
  - "Quan trọng nhất là cái hộp này: **trên CPU, máy im lặng 15 đến 25 giây là hoàn toàn bình thường**. Nó đang nạp model và suy nghĩ, đừng tưởng treo. Sau đó chữ sẽ tuôn ra."
  - "Bên phải là cùng nội dung nhưng trong Jupyter — cho ai đi đường code. Hai bên cho kết quả như nhau."
  - "Và đây là điều tôi muốn các bạn mang về từ phần này: **tải về và dùng một model open-source không hề khó**. Vừa nãy chúng ta chỉ gõ đúng một dòng."
- **Chuyển cảnh → Slide 18:** "Giờ ta đã có một LLM chạy ngay trên máy. Nhưng gõ lệnh trong terminal chưa tiện, và LLM một mình thì chưa biết về tài liệu của bạn. Quay lại trục chính — RAG — ta còn thiếu gì?"

---

Ghi chú tài nguyên cho người dựng slide (đường dẫn tuyệt đối):
- Ảnh dùng lại (Slide 17): `c:\Users\Minh Phuc\Downloads\project-2026\bai-giang-localLLM-RAG-Agent\docs\screenshots\terminal_ollama_chat.png` và `...\docs\screenshots\jupyter_m1.png`.
- Diagram dùng lại (Slide 13): `...\docs\diagrams\01_overall_architecture.png`.
- CẦN TẠO: (S14) hình thang 3 bậc cấp độ; (S15) ảnh dự phòng chụp ollama.com/library; (S16) ảnh dấu nhắc `>>>` của `ollama run` lúc trống.
- Lệnh đã đối chiếu với repo: setup/pull tại `...\0_setup\pull_models.ps1` (bộ 1=qwen3:1.7b+nomic-embed-text, 2=qwen3:4b, 3=qwen3:8b+bge-m3); lệnh chạy notebook/script tại `...\1_ollama_basics\README.md`.

# Phần D — Quay lại RAG + Open WebUI · thực hành (Slide 18–25)

### Slide 18 — Có LLM local rồi, còn thiếu gì nữa?  ·  ~3 phút  ·  [loại: ly thuyet]
- **Trên slide (nội dung chữ):**
  - Cho đến giờ: LLM chạy trên máy + đã **hiểu lý thuyết 6 bước RAG** (Phần B) → biết RAG hoạt động thế nào
  - Nhưng terminal KHÔNG phải thứ dân văn phòng, nghiên cứu dùng hằng ngày
  - Còn thiếu: một **GIAO DIỆN** để dùng thực tế
    - Có lịch sử hội thoại (không phải gõ lại từ đầu)
    - Kéo-thả tài liệu, đổi model bằng 1 cú click
    - Người không biết code cũng dùng được
  - Giải pháp: dùng **giao diện có sẵn** → Open WebUI — cài 1 lệnh, dùng ngay, ai cũng dùng được (không cần code)
- **Hình/diagram:** docs/diagrams/01_overall_architecture.png (sơ đồ tổng: User → Giao diện → Ollama local → RAG/VectorDB; dùng để chỉ "giao diện" là lớp còn thiếu phía trước LLM)
- **Giảng viên LÀM:** Chiếu slide. Chỉ vào sơ đồ 01, khoanh lớp "Giao diện" trước Ollama — nói "đây là lớp còn thiếu". Nhấn: ta dùng giao diện có sẵn Open WebUI để khỏi phải code.
- **Học viên LÀM:** Nghe và quan sát. KHÔNG gõ gì.
- **Lời giảng (nói gì):**
  - "Chúng ta đã hiểu RAG hoạt động thế nào. Giờ cần một chỗ để DÙNG nó — và phải là chỗ ai cũng dùng được, không phải cửa sổ đen terminal của dân code."
  - "Cái còn thiếu rất đời thường: một giao diện giống ChatGPT — có ô chat, có lịch sử, kéo-thả được file vào."
  - "Cách nhanh nhất: dùng một giao diện có sẵn — cài một lệnh là xong, đẹp như ChatGPT, ai cũng dùng được mà không cần viết dòng code nào."
  - "Và cái 'có sẵn' đó tên là Open WebUI."
- **Chuyển cảnh → Slide 19:** "Nhưng trước khi mở Open WebUI lên, tôi muốn các bạn thấy một điều quan trọng: Open WebUI KHÔNG phải phép màu — nó chỉ tự động hóa đúng 6 bước RAG mà các bạn vừa học ở phần lý thuyết."

---

### Slide 19 — Ánh xạ: 6 bước RAG (lý thuyết) ↔ thông số trong Open WebUI  ·  ~5 phút  ·  [loại: ly thuyet]
- **Trên slide (nội dung chữ):**
  - Thông điệp lớn (in đậm, cỡ to): **"Bạn vừa HỌC 6 bước RAG để hiểu cơ chế. Open WebUI TỰ ĐỘNG HÓA đúng 6 bước đó — bạn chỉ chỉnh thông số, không phải viết code."**
  - Bảng ánh xạ 2 cột:

    | 6 bước RAG (lý thuyết — Slide 8) | Trong Open WebUI bạn chỉ cần... |
    |---|---|
    | 1. Loader — đọc file | **Upload / kéo-thả tài liệu** |
    | 2. Chunker — cắt nhỏ (size ~500) | Chỉnh **Chunk Size** trong Settings |
    | 3. Embedder — biến chữ thành vector | Chọn **Embedding Model** (`nomic-embed-text`) |
    | 4. VectorDB — lưu vector | **Tự quản** — không phải đụng tay |
    | 5. Retriever — lấy top-k đoạn | Chỉnh **Top K** trong Settings |
    | 6. Generator — sinh câu trả lời | Chọn **model chat** ở góc trên cùng |
  - Lưu ý quan trọng (ô cảnh báo): Open WebUI có **engine RAG RIÊNG** của nó (lưu tài liệu trong volume trên máy bạn). Nó tự động hóa **đúng 6 bước** lý thuyết bạn vừa học — bạn chỉ chỉnh thông số.
- **Hình/diagram:** docs/diagrams/02_rag_pipeline.png (pipeline RAG 6 bước — chiếu cạnh bảng để mỗi dòng bảng soi vào 1 ô trong pipeline)
- **Giảng viên LÀM:** Chiếu slide với pipeline 02 ở một bên, bảng ánh xạ ở bên kia. Đọc từng dòng bảng, mỗi dòng chỉ tay vào ô tương ứng trong diagram 02. Nhấn mạnh dòng cảnh báo cuối.
- **Học viên LÀM:** Nghe, quan sát, đối chiếu bảng. KHÔNG gõ gì. (Có thể chụp ảnh slide này — đây là slide "bản đồ" họ sẽ tra lại khi tự làm ở nhà.)
- **Lời giảng (nói gì):**
  - "Đây là slide quan trọng nhất của cả phần thực hành, nên tôi sẽ nói chậm. Các bạn nhớ 6 bước lý thuyết nãy không: load, chunk, embed, store, retrieve, generate? Open WebUI làm đúng 6 việc đó — bạn không viết code, chỉ chỉnh thông số trên màn hình."
  - "Nhìn bảng: Loader chính là nút upload tài liệu. Chunker chính là ô Chunk Size. Embedder là chỗ chọn embedding model. VectorDB nó tự lo, bạn không thấy. Retriever là ô Top K. Generator là model chat bạn chọn ở trên cùng."
  - "Một điểm để khỏi hiểu lầm: Open WebUI có engine RAG riêng của nó, chạy ngầm bên trong. Nhưng nó đi đúng 6 bước các bạn vừa học. Cho nên phần lý thuyết nãy không hề thừa — nó cho bạn cái 'bản đồ' để biết mỗi cái nút trên Open WebUI thực chất đang làm gì."
  - "Khi một thông số chỉnh sai cho ra kết quả tệ, bạn sẽ biết ngay nó hỏng ở bước nào — vì bạn đã hiểu 6 bước đó."
- **Chuyển cảnh → Slide 20:** "Vậy Open WebUI cụ thể là cái gì, lấy ở đâu, có an toàn không? Ta xem nhanh trước khi cài."

---

### Slide 20 — Open WebUI là gì?  ·  ~3 phút  ·  [loại: cong cu]
- **Trên slide (nội dung chữ):**
  - **Open WebUI** = giao diện chat mã nguồn mở, **giống ChatGPT**, chạy ngay trên máy bạn
  - Có sẵn mọi thứ một giao diện chat cần:
    - Lịch sử hội thoại nhiều phiên
    - Đổi model bằng 1 cú click (qwen3:1.7b ↔ 4b ↔ 8b...)
    - Kéo-thả tài liệu → hỏi đáp RAG ngay
    - Quản trị thông số RAG bằng giao diện (không cần code)
  - Cài đặt: **1 lệnh Docker** → `docker compose up -d`
  - VẪN bảo mật local — KHÔNG mâu thuẫn thông điệp đầu buổi:
    - `WEBUI_AUTH=False` chỉ cho lab; production BẬT lại để có tài khoản/đăng nhập
    - Open WebUI nối tới **Ollama local** (`host.docker.internal:11434`) — không gọi cloud
    - Tài liệu + lịch sử chat lưu trong volume `open-webui-data` trên máy bạn → **dữ liệu không rời máy**
- **Hình/diagram:** docs/screenshots/open_webui_rag_real.png (ảnh giao diện Open WebUI thật — để học viên thấy ngay "à, giống ChatGPT")
- **Giảng viên LÀM:** Chiếu slide kèm ảnh `open_webui_rag_real.png`. Chỉ vào ô chat, vùng chọn model, khu vực tài liệu trên ảnh. Mở file `docker-compose.yml` trong editor, chỉ vào 3 dòng: `OLLAMA_BASE_URL=http://host.docker.internal:11434`, `WEBUI_AUTH=False`, và volume `open-webui-data` — gắn từng dòng với 1 ý bảo mật trên slide.
- **Học viên LÀM:** Nghe, quan sát ảnh giao diện. KHÔNG gõ gì.
- **Lời giảng (nói gì):**
  - "Open WebUI nhìn gần như y hệt ChatGPT — nhưng nó chạy trên máy bạn và nói chuyện với con LLM local mà ta đã pull về."
  - "Nó có sẵn tất cả những thứ ta cần mà không phải code: lịch sử chat, đổi model một click, kéo-thả file để hỏi đáp tài liệu."
  - "Cài nó chỉ một lệnh Docker, lát nữa tôi làm trực tiếp."
  - "Quan trọng cho bài toán bảo mật đầu buổi: tài liệu bạn nạp vào và lịch sử chat đều nằm trong một thư mục dữ liệu trên chính máy này, và nó gọi Ollama ở local chứ không gửi ra cloud. Riêng `WEBUI_AUTH=False` là tôi tắt đăng nhập cho lab cho nhanh — khi triển khai thật trong cơ quan thì BẬT lại để mỗi người có tài khoản riêng."
- **Chuyển cảnh → Slide 21:** "Nói đủ rồi — giờ mở nó lên. Theo tôi từng bước, ai có Docker thì làm theo luôn."

---

### Slide 21 — [LÀM THEO] Khởi động Open WebUI từng bước  ·  ~5 phút  ·  [loại: lam theo]
- **Trên slide (nội dung chữ):**
  - Checklist 4 bước (đánh số to, rõ):
    - **B1. Kiểm tra Ollama đang chạy** → `ollama list` (phải thấy `qwen3:1.7b` và `nomic-embed-text`)
    - **B2. Bật Open WebUI** → `docker compose up -d` (lần đầu tải image ~1 GB, đã pre-pull trước buổi)
    - **B3. Kiểm tra container** → `docker ps` (phải thấy dòng `open-webui`)
    - **B4. Mở trình duyệt** → `http://localhost:3000` → chọn model **qwen3:1.7b** ở góc trên
  - Ô FALLBACK (nếu Docker bị chặn / không cài được):
    - Cài Open WebUI trực tiếp bằng pip (không cần Docker): `pip install open-webui` → `open-webui serve` → mở `http://localhost:8080` *(lần đầu nặng ~2.5GB/~20')*
    - Hoặc xem giảng viên demo trên máy chính + ảnh chụp các slide tiếp theo
- **Hình/diagram:** CAN TAO: ảnh chụp 4 cửa sổ ghép — (1) terminal sau `ollama list`, (2) terminal sau `docker compose up -d`, (3) terminal sau `docker ps` thấy `open-webui`, (4) trình duyệt mở `localhost:3000` lần đầu. (Tạm thời có thể dùng open_webui_rag_real.png cho ô (4).)
- **Giảng viên LÀM:**
  - Mở terminal, gõ `ollama list` → đọc to ra "có qwen3:1.7b, có nomic-embed-text, đủ".
  - Gõ `docker compose up -d` ngay tại thư mục gốc repo. Nói rõ: "image đã được tải sẵn trước buổi nên lệnh này chạy vài giây; nếu chưa pre-pull thì lần đầu mất 5–10 phút tải ~1 GB."
  - Gõ `docker ps`, chỉ vào dòng `open-webui`, cột STATUS là `Up`.
  - Mở trình duyệt vào `http://localhost:3000`, click ô chọn model góc trên, chọn `qwen3:1.7b`.
  - Nếu lớp có người báo Docker bị chặn: chỉ vào ô fallback, hướng dẫn cài `pip install open-webui` (nếu kịp) hoặc xem chung máy giảng viên.
- **Học viên LÀM:** Ai có Docker: GÕ THEO 4 lệnh, dừng lại ở màn `localhost:3000`. Ai không có Docker/không code: quan sát giảng viên, đánh dấu mình sẽ dùng fallback hoặc xem ở nhà.
- **Lời giảng (nói gì):**
  - "Trước tiên kiểm tra Ollama còn sống không: `ollama list`. Phải thấy hai cái — con LLM qwen3 1.7b và con embedding nomic. Thiếu cái nào thì pull lại như phần trước."
  - "Giờ bật giao diện: `docker compose up -d`. Chữ `-d` nghĩa là chạy nền. Image tôi đã tải trước buổi nên nó lên trong vài giây."
  - "`docker ps` để chắc chắn nó đang chạy — thấy dòng open-webui, STATUS Up là ngon."
  - "Mở trình duyệt, gõ localhost cổng 3000. Cấu hình mẫu để WEBUI_AUTH=False nên vào thẳng giao diện, KHÔNG phải tạo tài khoản — dữ liệu chỉ nằm trên máy. Xong chọn model qwen3:1.7b ở trên cùng."
  - "Bạn nào máy công ty chặn Docker: đừng lo, có thể cài thẳng bằng pip — `pip install open-webui` rồi `open-webui serve`, vào cổng 8080; hoặc cứ xem tôi làm, các bước y hệt nhau."
- **Chuyển cảnh → Slide 22:** "Có giao diện rồi nhưng nó chưa biết gì về tài liệu của bạn cả. Việc tiếp theo: nạp tài liệu vào — và có tới 2 cách."

---

### Slide 22 — [HƯỚNG DẪN] Nạp tài liệu vào Open WebUI — 2 cách  ·  ~5 phút  ·  [loại: lam theo]
- **Trên slide (nội dung chữ):**
  - **Cách 1 — Kéo-thả nhanh vào 1 đoạn chat** (dùng 1 lần, hỏi nhanh):
    - Trong ô chat, bấm dấu **+** (hoặc kéo-thả thẳng file vào) → chọn tài liệu → đợi báo upload xong → hỏi
    - Phù hợp: hỏi nhanh 1 file, không cần dùng lại
  - **Cách 2 — Tạo Knowledge base trong Workspace** (tài liệu dùng lại nhiều lần):
    - Vào **Workspace → Knowledge** → tạo mới (vd "Quy chế ATTT") → upload nhiều file vào
    - Khi chat, gõ **`#`** → chọn knowledge base đó để gắn vào câu hỏi
    - Phù hợp: bộ tài liệu cơ quan, dùng đi dùng lại
  - Định dạng tệp hỗ trợ: `.md`, `.txt`, `.pdf`, `.docx` (buổi nay dùng `2_rag/data/*.md` hoặc `2_rag/sample_upload/so_tay_cong_ty_mau.md`)
  - Xác nhận upload thành công: thấy tên file đính kèm + icon ✓ / báo "processed"
  - Tài liệu lưu ở đâu: trong volume Docker `open-webui-data` trên máy bạn → **không rời máy**
- **Hình/diagram (ẢNH THẬT đã chụp):** `docs/screenshots/owui_22a_create_kb.png` (form tạo Knowledge base) · `owui_22b_kb_6files.png` (kho "Quy chế ATTT" sau khi nạp đủ 6 file `2_rag/data/`) · `owui_22c_hash_select.png` (gõ `#` trong ô chat → popup chọn Collection/Files). *(Cách 1 — bấm `+` upload thẳng trong chat: tùy chọn, chụp thêm nếu cần.)*
- **Giảng viên LÀM:**
  - Demo Cách 1 trước: trong ô chat bấm `+`, chọn `2_rag/data/03_quy_trinh_su_co.md`, chờ icon báo xong.
  - Demo Cách 2: vào Workspace → Knowledge → tạo base "Quy chế ATTT" → upload cả 6 file trong `2_rag/data/`. Quay lại chat, gõ `#`, chọn base vừa tạo.
  - Chỉ rõ dấu hiệu "đã xử lý xong" trên màn hình. Nói tài liệu lưu trong volume trên máy.
- **Học viên LÀM:** Ai đang chạy Open WebUI: làm theo Cách 1 với 1 file của họ (hoặc file mẫu trong `2_rag/data/`). Cách 2 làm cùng giảng viên. Ai chỉ xem: quan sát + ghi chú 2 cách.
- **Lời giảng (nói gì):**
  - "Có hai cách nạp tài liệu, chọn theo nhu cầu. Cách một: kéo thả thẳng một file vào ô chat, hoặc bấm dấu cộng. Nhanh, hợp khi bạn chỉ muốn hỏi một file một lần."
  - "Cách hai mạnh hơn cho cơ quan: vào Workspace, mục Knowledge, tạo một 'kho tri thức' tên là Quy chế ATTT chẳng hạn, rồi nhét cả bộ tài liệu vào đó. Sau này mỗi lần chat, gõ dấu thăng `#` là gọi cả kho ra dùng — không phải upload lại."
  - "Để ý dấu hiệu upload xong: Open WebUI cần vài giây 'tiêu hóa' file — nó đang chunk và embed đúng như bước 2, 3 trong lý thuyết. Khi thấy báo xong mới hỏi."
  - "File này nằm ở đâu? Trong volume dữ liệu của Open WebUI, tức là một thư mục trên chính máy này. Không có gì gửi đi đâu cả."
- **Chuyển cảnh → Slide 23:** "Nạp xong rồi, nhưng kết quả tốt hay tệ phụ thuộc vào các THÔNG SỐ phía sau. Giờ ta vào Settings — đây chính là chỗ lý thuyết RAG gặp thực hành."

---

### Slide 23 — [HƯỚNG DẪN] Chỉnh thông số RAG + cấu trúc Prompt  ·  ~5 phút  ·  [loại: lam theo]
- **Trên slide (nội dung chữ):**
  - Đường vào: **Admin Panel → Settings → Documents** (cấu hình RAG của Open WebUI)
  - 4 thông số cần chỉnh (và VÌ SAO):
    - **Embedding Model** → đặt về **`nomic-embed-text`** để 100% local (mặc định Open WebUI có thể dùng model tải từ HuggingFace — đổi sang Ollama/nomic cho khớp đầu buổi)
    - **Chunk Size** → ~500 (giống giá trị nêu trong lý thuyết Slide 10; nhỏ quá thì vụn ý, lớn quá thì loãng)
    - **Top K** → 3 (số đoạn lấy ra cho mỗi câu hỏi)
    - **Hybrid Search** (BM25 + vector) → bật khi câu hỏi chứa mã/từ khóa hiếm (vd "P1", "QĐ-AN-001")
  - **Bảng "vàng": thông số Open WebUI ↔ bước RAG**

    | Thông số trong Open WebUI | = bước RAG nào (lý thuyết — Slide 8) | Chỉnh để làm gì |
    |---|---|---|
    | Upload / Knowledge | Bước 1 — Loader | Đưa tài liệu vào |
    | Chunk Size | Bước 2 — Chunk | To/nhỏ đoạn cắt |
    | Embedding Model | Bước 3 — Embed | Chất lượng vector (local) |
    | (tự quản) | Bước 4 — VectorDB | — |
    | Top K | Bước 5 — Retrieve | Lấy bao nhiêu đoạn |
    | Model chat + System Prompt | Bước 6 — Generate | Cách LLM trả lời |
  - **Cấu trúc System Prompt cho RAG** (dán vào ô System Prompt):
    > "Chỉ trả lời dựa vào tài liệu được cung cấp. Nếu tài liệu không đủ thông tin, nói rõ 'Tài liệu không đề cập'. Trích nguồn (tên file) sau mỗi ý."
- **Hình/diagram (ẢNH THẬT đã chụp):** `docs/screenshots/owui_23a_settings.png` (Admin → Settings → Documents: thấy Chunk Size 1000/Overlap 100, **Embedding Model mặc định = `all-MiniLM` — KHÔNG phải Ollama**, Top K 3, RAG Template) · `owui_23b_embedding_nomic.png` (sau khi đổi Embedding Engine = Ollama, model = `nomic-embed-text`). *(Khi lên slide: khoanh đỏ 4 ô Embedding/Chunk/Top-K/Hybrid.)*
- **Giảng viên LÀM:**
  - Vào Admin Panel → Settings → Documents. Chỉ và đổi **Embedding Model** về `nomic-embed-text` (giải thích vì sao: 100% local).
  - Chỉ ô Chunk Size (đặt ~500), Top K (đặt 3), bật/giải thích Hybrid Search.
  - Chiếu bảng "vàng", đọc từng dòng, mỗi dòng đối chiếu lại Slide 19 và diagram 02.
  - Dán đoạn System Prompt RAG (mẫu) vào ô System Prompt.
- **Học viên LÀM:** Ai chạy Open WebUI: chỉnh theo 4 thông số, dán system prompt. Ai xem: ghi lại bảng "vàng" (đây là bảng tra cứu họ giữ lại). KHÔNG ai phải nhớ thuộc — chụp ảnh slide.
- **Lời giảng (nói gì):**
  - "Đây là slide 'lý thuyết gặp thực hành'. Mỗi cái nút trong cái Settings này chính là một bước RAG trong lý thuyết — tôi sẽ chỉ từng cái."
  - "Việc đầu tiên và quan trọng nhất cho bảo mật: đổi Embedding Model về nomic-embed-text — con embedding local của ta. Mặc định Open WebUI có thể kéo một model embedding từ internet về; ta không muốn vậy, ta muốn 100% trên máy."
  - "Chunk Size để khoảng 500 như trong lý thuyết. Top K để 3 — tức mỗi câu hỏi lấy 3 đoạn liên quan nhất. Đây đúng là con số top-k = 3 ta nói ở Slide 10."
  - "Hybrid Search: bật khi tài liệu nhiều mã, ký hiệu ngắn — nhớ ví dụ 'P1' lúc nãy embedding bị trượt không? Hybrid thêm tìm theo từ khóa nên cứu được mấy ca đó."
  - "Cuối cùng là System Prompt — đây là chữ G, Generate. Tôi dán một prompt mẫu: chỉ trả lời theo tài liệu, không biết thì nói không biết, và phải trích nguồn. Chính ba câu này làm chatbot bớt bịa và kiểm chứng được."
- **Chuyển cảnh → Slide 24:** "Chỉnh xong rồi — giờ thử thật. Hỏi một câu trên đúng bộ tài liệu của ta và xem nó trích nguồn thế nào."

---

### Slide 24 — [DEMO] Hỏi đáp RAG trên tài liệu của bạn + trích nguồn  ·  ~4 phút  ·  [loại: demo]
- **Trên slide (nội dung chữ):**
  - Demo trực tiếp trên Open WebUI với knowledge base vừa nạp (`2_rag/data/`)
  - Câu hỏi demo (chạy CHẮC trên data mẫu):
    - "Quy trình xử lý sự cố ATTT gồm những bước nào?"
  - Điều cần nhìn trong câu trả lời:
    - Trả lời bám theo tài liệu (6 bước quy trình)
    - **Trích nguồn**: hiện tên file `03_quy_trinh_su_co.md` (bấm vào citation xem được đoạn gốc)
  - LƯU Ý: trên CPU, model "im lặng" vài giây trước khi chữ chạy ra — **bình thường, không phải treo**
- **Hình/diagram (ẢNH THẬT đã chụp):** `docs/screenshots/owui_24a_answer_vi.png` (qwen3:1.7b trả lời **tiếng Việt**, trích nguồn inline `03_quy_trinh_su_co.md` + nút "2 Sources") — **ảnh chính** · `owui_24b_answer_en.png` (bản tiếng Anh, bám 6 bước sát hơn — dự phòng) · `owui_24c_retrieved.png` (mở "Retrieved sources": thấy truy vấn tự sinh + đoạn nguồn). *(Còn có `open_webui_rag_real.png` = chat thường.)*
- **Giảng viên LÀM:**
  - Trong ô chat (đã gắn knowledge base bằng `#`), gõ: "Quy trình xử lý sự cố ATTT gồm những bước nào?" → Enter.
  - TRONG LÚC CHỜ (CPU im lặng ~10–20s): nói chuyện lấp khoảng lặng (xem lời giảng), chỉ vào slide nhắc "đây là lúc nó đang retrieve + generate".
  - Khi có câu trả lời: bấm vào phần trích nguồn (citation) để mở đoạn tài liệu gốc, chứng minh "nó không bịa".
  - Nếu live lỗi/quá chậm: chuyển sang `open_webui_rag_real.png` và giảng trên ảnh.
- **Học viên LÀM:** Quan sát. Ai đang chạy Open WebUI: gõ cùng câu hỏi trên máy mình, chú ý phần trích nguồn. Chưa hỏi câu của riêng mình ở slide này (để qua Slide 25).
- **Lời giảng (nói gì):**
  - "Tôi gõ câu hỏi thật: quy trình xử lý sự cố gồm những bước nào. Để ý: trên CPU nó sẽ im vài giây — đó là lúc nó đang chunk-hoá câu hỏi, đi tìm 3 đoạn liên quan, rồi mới sinh trả lời. Im lặng là bình thường, đừng tưởng treo máy."
  - (khi đang chờ) "Trong lúc chờ: chính cái độ trễ này là cái giá của 'chạy local, miễn phí, dữ liệu không rời máy'. Production thì người ta đẩy lên GPU cho nhanh, nhưng cơ chế y hệt."
  - (khi có kết quả) "Nó liệt kê đúng các bước. Quan trọng nhất: thấy phần trích nguồn không — file 03_quy_trinh_su_co. Tôi bấm vào đây… đây là đoạn gốc nó dựa vào. Đây là điểm khác biệt sống còn với ChatGPT thường: bạn KIỂM CHỨNG được."
- **Chuyển cảnh → Slide 25:** "Tới lượt các bạn. Tôi cho vài câu để các bạn tự gõ — và cảm nhận điều thú vị: bạn đang ĐIỀU KHIỂN được một con chatbot RAG chạy hoàn toàn trên máy mình."

---

### Slide 25 — [VÍ DỤ THỬ] Tự tay điều khiển chatbot RAG local  ·  ~4 phút  ·  [loại: demo]
- **Trên slide (nội dung chữ):**
  - Tự gõ thử (các câu chạy CHẮC trên data mẫu):
    - "USB cá nhân có được dùng không?"
    - "Có được forward email công vụ sang gmail?"
    - "Quy định mật khẩu của đơn vị?"
    - "Khi xảy ra rò rỉ dữ liệu cá nhân phải báo cáo ai?"
  - **Thử 1 câu NGOÀI tài liệu** (vd "Lương trung bình ngành CNTT 2026?") → xem nó nói *"Tài liệu không đề cập"* thay vì bịa — đó là RAG ĐÚNG (đúng thí nghiệm đã hứa ở Slide 12).
  - Thử cảm giác "điều khiển được":
    - Đổi **Top K** 3 → 5, hỏi lại → câu trả lời đầy đặn hơn (nhưng chậm hơn)
    - Đổi **model chat** 1.7b → 4b (nếu đã pull) → trả lời mạch lạc hơn, chậm hơn
  - Mẹo: hỏi bằng **từ tự nhiên**, tránh mã ngắn ("P1", "MFA") — embedding dễ trượt với mã/ký hiệu
  - Kết: tài liệu của BẠN + model của BẠN + thông số do BẠN chỉnh = chatbot RAG **của riêng bạn**, **local**
- **Hình/diagram:** docs/screenshots/open_webui_rag_real.png (tái dùng — minh họa kết quả mong đợi cho người chỉ quan sát)
- **Giảng viên LÀM:**
  - Cho 2–3 phút để học viên tự gõ các câu trên. Đi quanh hỗ trợ (hoặc mời 1 học viên đọc to câu trả lời máy họ).
  - Demo nhanh "điều khiển": đổi Top K 3→5 ngay trong Settings, hỏi lại 1 câu, cho thấy khác biệt; nếu có qwen3:4b thì đổi model cho thấy chất lượng tăng.
  - Nhắc lại mẹo "hỏi bằng từ tự nhiên" — liên hệ lại ví dụ "P1" bị trượt.
- **Học viên LÀM:** GÕ trực tiếp các câu hỏi trên máy mình (ai có Open WebUI). Thử đổi Top K hoặc model nếu kịp. Ai chỉ quan sát: chọn 1 câu, đoán trước câu trả lời rồi đối chiếu với máy giảng viên.
- **Lời giảng (nói gì):**
  - "Giờ là của các bạn. Gõ thử mấy câu này — đều chạy chắc trên bộ quy chế mẫu. Để ý mỗi câu đều có trích nguồn."
  - "Muốn cảm giác mình điều khiển được nó? Vào Settings đổi Top K từ 3 lên 5, hỏi lại — câu trả lời sẽ đầy đặn hơn vì lấy nhiều đoạn hơn, đổi lại chậm hơn. Hoặc đổi model lên 4b nếu máy bạn pull rồi — mạch lạc hơn hẳn. Bạn vừa chỉnh đúng những thông số trong 6 bước RAG — chỉ bằng vài cú click."
  - "Một mẹo thực chiến: hỏi bằng câu tự nhiên, đừng hỏi cộc lốc bằng mã như 'P1' hay 'MFA' — embedding không hiểu mấy ký hiệu ngắn đó, dễ trượt. Cái này đúng cho mọi hệ RAG."
  - "Và thử cố tình hỏi một câu KHÔNG có trong tài liệu — như lương trung bình ngành CNTT. Để ý: nó trả lời 'Tài liệu không đề cập' chứ không bịa. Đó là dấu hiệu một hệ RAG tốt — nhờ cái System Prompt ta dán ở Slide 23."
  - "Và đây là điều tôi muốn các bạn mang về: cái chatbot này — tài liệu của bạn, model của bạn, thông số do bạn chỉnh, chạy trên máy bạn, không gửi đi đâu. Bạn không 'xài' AI của người khác nữa — bạn LÀM CHỦ một con AI riêng."
- **Chuyển cảnh → Slide 26:** "RAG tới đây là trọn vẹn — bạn đã có một trợ lý đọc tài liệu của chính mình, chạy offline, có trích nguồn. Giờ ta tổng kết lại những gì đã làm được."

# Phần E — Kết bài (Slide 26–28)

### Slide 26 — Tong ket: ban da lam duoc gi  ·  ~3 phut  ·  [loai: ket bai]
- **Tren slide (noi dung chu):**
  - Tieu de: "Sau 2 gio, ban da co the…"
  - Checklist 2 dong (co dau tick):
    - ✅ Chay **LLM hoan toan offline** tren may — du lieu khong ra khoi may
    - ✅ Xay **RAG local doc tai lieu CUA MINH**, tra loi **co trich nguon** — hoan toan qua Open WebUI, khong code
  - Cau chot lon (in dam, giua duoi): **"Xay duoc 1 he thong RAG local — nhanh va hieu qua."**
  - Dong nho: "Quan trong nhat: lam chu du lieu, bao mat noi bo."
- **Hinh/diagram:** Tan dung `docs/diagrams/01_overall_architecture.png` (kien truc tong the — nhac lai toan canh: LLM local + RAG + giao dien) lam nen mo phia sau hoac ben phai. (Dung o day rat hop de "khep lai" buc tranh tong the.)
- **Giang vien LAM:**
  - Chieu slide, doc luot 2 muc checklist, voi moi muc lui lai nhac slide tuong ung da hoc (LLM o phan Ollama, RAG o phan Open WebUI).
  - Chi vao diagram `01_overall_architecture` neu dung: "Toan bo nhung manh ghep nay ghep lai thanh buc tranh nay."
- **Hoc vien LAM:** Nghe, nhin lai. Co the tu danh dau muc nao minh da lam theo duoc. KHONG go lenh.
- **Loi giang (noi gi):**
  - "Ta tong ket nhanh. Bat dau buoi sang cac thay co co the chua tung chay LLM offline. Bay gio thi: mot — cac thay co da chay duoc LLM ngay tren may, khong gui gi len mang."
  - "Hai — va day la trong tam buoi hom nay — cac thay co da xay duoc RAG local: nap tai lieu cua chinh minh vao, dat cau hoi, va nhan cau tra loi co trich dan nguon. Tat ca lam qua giao dien Open WebUI, khong can viet mot dong code."
  - "Neu chi nho mot cau ve buoi hom nay, hay nho: **ta co the tu xay mot he thong RAG local, nhanh va hieu qua, ma du lieu khong bao gio roi khoi to chuc.**"
- **Chuyen canh → Slide 27:** "Cau hoi cuoi cung va thuc te nhat: lam duoc roi, gio ap dung vao to chuc, doanh nghiep cua minh nhu the nao cho dung va an toan?"

### Slide 27 — Ap dung trong to chuc/doanh nghiep  ·  ~6 phut  ·  [loai: ly thuyet]
- **Tren slide (noi dung chu):**
  - Tieu de: "Dua ve to chuc: chon dung, trien khai an toan"
  - **Ma tran quyet dinh Local vs Cloud** (bang 2x2, truc do nhay du lieu × muc dich):
    - Du lieu NHAY (noi bo, PII, hop dong) + tra cuu noi bo → **LOCAL** (bat buoc)
    - Du lieu NHAY + tac vu phuc tap → **LOCAL**, dung model lon hon (4b/8b) hoac GPU server
    - Du lieu CONG KHAI + can chat luong toi da → Cloud API co the chap nhan
    - Du lieu CONG KHAI + thu nghiem nhanh → Cloud/Local deu duoc
    - Nguyen tac mot dong: **"Du lieu cang nhay → cang phai Local."**
  - **3-4 use case theo phong ban:**
    - HR: hoi dap noi quy, che do, quy trinh nghi phep tu so tay nhan su
    - Phap che: tra cuu hop dong, quy che, van ban quy pham
    - R&D: hoi dap tren tai lieu ky thuat/sang che noi bo
    - CSKH: tra loi tu kho FAQ/quy trinh san pham
  - **Checklist bao mat khi trien khai (4 muc):**
    - Phan loai tai lieu truoc khi nap (cong khai / noi bo / mat)
    - Redact PII (an thong tin ca nhan) truoc khi index
    - Phan quyen truy cap: production bat `WEBUI_AUTH`, moi nguoi 1 tai khoan; khong nap tai lieu MAT cho moi nguoi
    - Audit log (ghi lai ai hoi gi, truy van tai lieu nao)
- **Hinh/diagram:**
  - `docs/diagrams/07_production_scales.png` (3 muc do trien khai: Lab ca nhan ≤5 user → Noi bo phong/ban 10-100 user → Toan don vi 100-1000 user) — dung de tra loi "trien khai o quy mo nao".
  - `docs/diagrams/08_security_risks.png` (rui ro RAG) — dung de minh hoa khung checklist bao mat (RAG Poisoning, PII Leakage, Permission Bypass).
- **Giang vien LAM:**
  - Chieu slide, ve nhanh ma tran 2x2 len bang neu muon hoc vien tham gia (hoi: "tai liu hop dong cua phong phap che — local hay cloud?").
  - Chi vao `07_production_scales` giai thich 3 quy mo: nguoi khong code dung Open WebUI 1 may (Scale 1), phong ban dung Docker tren 1 server (Scale 2).
  - Chi vao `08_security_risks` doc qua tung rui ro, gan moi rui ro voi 1 muc trong checklist bao mat.
- **Hoc vien LAM:** Nghe, thao luan ngan (GV co the hoi truc tiep ve tinh huong phong ban cua tung nguoi). Khong go lenh.
- **Loi giang (noi gi):**
  - "Cau hoi quan trong nhat khi ve don vi: viec nay nen Local hay Cloud? Em de mot ma tran rat don gian — nhin theo hai truc: du lieu co NHAY khong, va muc dich la gi."
  - "Quy tac vang chi mot cau: **du lieu cang nhay thi cang phai Local.** Hop dong, ho so nhan su, sang che noi bo — nhung thu nay dut khoat khong nen gui len API ben thu ba."
  - "Ap dung cu the theo phong ban: HR lam tro ly tra cuu noi quy che do; phap che tra cuu hop dong va van ban; R&D hoi dap tren tai lieu ky thuat; cham soc khach hang tra loi tu kho FAQ. Mau so chung: moi phong deu co mot kho tai lieu rieng — do chinh la dat dien cho RAG local."
  - Chi vao `08_security_risks`: "Nhung truoc khi trien that, bon dieu bat buoc. Mot, phan loai tai lieu — khong nap nham tai lieu MAT cho moi nguoi truy van. Hai, che thong tin ca nhan truoc khi dua vao index. Ba, phan quyen — production bat dang nhap, moi nguoi mot tai khoan. Bon, ghi nhat ky — ai hoi gi, truy van tai lieu nao, deu phai luu lai de truy vet."
- **Chuyen canh → Slide 28:** "Den day la het phan noi dung. Em xin nhuong lai cho cau hoi cua cac thay co, va gui tai nguyen de moi nguoi tu di tiep."

### Slide 28 — Q&A + Tai nguyen + Cam on  ·  ~3 phut  ·  [loai: ket bai]
- **Tren slide (noi dung chu):**
  - Tieu de lon: "Q&A — va tai nguyen mang ve"
  - 3 muc tai nguyen (kem icon):
    - **Repo code** (toan bo demo: `0_setup/`, `1_ollama_basics/`, `2_rag/`, `docker-compose.yml`) — link/QR
    - **Handbook day du**: `TAI_LIEU_CHI_TIET.md` (huong dan tung buoc tu cai dat den RAG)
    - **Cheat-sheet**: lenh nhanh (cai Ollama, pull model qwen3:1.7b + nomic-embed-text, chay Open WebUI bang Docker `localhost:3000`)
  - 4 cau hoi RAG mau de tu thu o nha (in nho):
    - "Quy trinh xu ly su co ATTT gom nhung buoc nao?"
    - "USB ca nhan co duoc dung khong?"
    - "Co duoc forward email cong vu sang gmail?"
    - "Quy dinh mat khau?"
  - Dong cuoi (lon): "Cam on cac thay co! — PGS.TS. Le Anh Cuong"
  - **CAN TAO: anh QR code tro toi repo** (chua co trong repo — sinh QR tu URL repo va chen vao goc slide).
- **Hinh/diagram:**
  - `docs/screenshots/open_webui_rag_real.png` (anh giao dien Open WebUI tra loi co trich nguon) — dat lam anh nen/minh hoa "thanh qua", goi nho hoc vien ket qua dat duoc.
  - CAN TAO: QR code link repo (xem tren).
- **Giang vien LAM:**
  - Chieu slide, doc qua 3 nhom tai nguyen, chi vao QR (neu da tao) de hoc vien quet.
  - Nhac ro vi tri handbook: "File `TAI_LIEU_CHI_TIET.md` ngay trong repo, huong dan day du tung buoc."
  - Mo san terminal/Open WebUI o che do du phong de tra loi neu co cau hoi demo lai.
  - Moi cau hoi tu hoc vien.
- **Hoc vien LAM:** Dat cau hoi, quet QR / ghi lai link repo. Co the mo may chup man hinh slide tai nguyen.
- **Loi giang (noi gi):**
  - "Tat ca nhung gi minh lam hom nay deu nam trong repo nay — code demo, file Docker, va handbook `TAI_LIEU_CHI_TIET.md` huong dan tung buoc. Cac thay co quet QR hoac ghi lai link la co the tu dung lai o nha."
  - "Voi nhung ai chua quen code, chi can nho ba lenh trong cheat-sheet: cai Ollama, keo model qwen3:1.7b va nomic-embed-text, va chay Open WebUI bang Docker — vao trinh duyet o localhost:3000 la dung duoc ngay."
  - "Em de san bon cau hoi mau o day — cac thay co cu nap tai lieu cua minh roi thu hoi tuong tu."
  - "Xin cam on cac thay co da theo het buoi. Gio la phan cau hoi — moi nguoi cu thoai mai hoi a."
- **Chuyen canh → Slide N+1:** (Slide cuoi — ket thuc buoi hoc. Khong con chuyen canh.)

---

**Ghi chu asset cho nguoi dung slide (duong dan tuyet doi trong repo):**
- Da dung: `docs/diagrams/01_overall_architecture.png` (S26, tan dung diagram tong the); `docs/diagrams/07_production_scales.png` + `docs/diagrams/08_security_risks.png` (S27); `docs/screenshots/open_webui_rag_real.png` (S28).
- CAN TAO: QR code tro toi URL repo (chen o S28).

---

## Phụ lục A — Hình/asset CẦN TẠO (chưa có trong repo)

> ✅ **Slide 22, 23, 24 (Open WebUI) đã CHỤP ảnh THẬT** — xem Phụ lục B. Bảng dưới chỉ còn các hình thật sự cần tạo.

| Slide | Hình cần tạo |
|---|---|
| 1 | Ảnh bìa hero: gợi LLM → RAG, RAG là điểm nhấn trung tâm (tông xanh; "offline · private · open-source") |
| 2 | (tùy) Hình 3 checkbox HIỂU/XÂY/BIẾT + đích ngắm "thước đo thành công" |
| 4 | (tùy) Sơ đồ tầng: LLM local (nền) → RAG (nổi bật) |
| 9 | (tùy) Bảng trực quan embedding vẽ TĨNH trên slide: similarity("xe đạp","xe máy")=CAO vs ("xe máy","rau muống")=THẤP — không cần chạy code |

## Phụ lục B — Asset CÓ SẴN (dùng lại được)

- **Diagram** (`docs/diagrams/`): `02_rag_pipeline` (Slide 8), `04_embedding_space` (Slide 9), `01_overall_architecture` (Slide 6), `08_security_risks` (Slide 3 hoặc 12 — chọn 1).
- **Screenshot kết quả thật** (`docs/screenshots/`): `jupyter_m1.png` / `terminal_ollama_chat.png` (Slide 17), `open_webui_rag_real.png` (Slide 24).
- **Ảnh THẬT Open WebUI / Ollama — tự chụp bằng Playwright (`docs/screenshots/`), xếp theo LUỒNG từng bước:**
  - *Chọn LLM trên Ollama:* `ollama_01_library.png` (duyệt ollama.com/library) → `ollama_02_qwen3.png` (trang model qwen3: size/tag/pull)
  - *Kiểm tra kết nối Ollama:* `owui_30_connections.png` (Admin → Settings → **Connections**: Ollama API `:11434` bật xanh + nút verify)
  - *Nạp tài liệu (Slide 22):* `owui_31_knowledge_list.png` (danh sách Knowledge + nút **New Knowledge**) → `owui_22a_create_kb.png` (form tạo) → `owui_32_kb_add_content.png` (nút **+** thêm/upload file) → `owui_22b_kb_6files.png` (đã nạp 6 file) → `owui_22c_hash_select.png` (gõ `#` chọn kho)
  - *Thông số RAG (Slide 23):* `owui_23a_settings.png` (Documents settings) → `owui_23b_embedding_nomic.png` (đổi embedding = nomic)
  - *Hỏi đáp có trích nguồn (Slide 24):* `owui_24a_answer_vi.png` (chính) · `owui_24b_answer_en.png` · `owui_24c_retrieved.png`
  - *Trợ lý RAG chuyên dụng — khỏi gõ `#`:* tạo model → `owui_33_select_knowledge_picker.png` (gắn kho) → `owui_model_setup.png` (model đã gắn Knowledge) → `owui_34_model_picker.png` (chọn model trong chat) → `owui_model_chat.png` (hỏi bình thường, bám tài liệu)
- **Dữ liệu:** `2_rag/data/` (6 tài liệu mẫu) + `2_rag/sample_upload/`, `docker-compose.yml` (Open WebUI), handbook `TAI_LIEU_CHI_TIET.md`.
