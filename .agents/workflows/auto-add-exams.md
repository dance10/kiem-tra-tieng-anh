---
description: Tự động quét file mới trong thư mục Fix, copy sang Exam, cấu hình Google Sheets và cập nhật index.html, auto-push Github
---
# QUY TRÌNH AUTO-ADD-EXAMS

// turbo-all

---

## KIẾN TRÚC HỆ THỐNG

```
BaiKiemTra/
├── Fix/                        ← File bài thi mới (chưa chuẩn hoá)
├── Exam/                       ← File bài thi CHÍNH THỨC (đã chuẩn hoá)
│   └── congratulations.html    ← Redirect → ../Congratulations/index.html
├── Template/                   ← 8 template giao diện chuẩn
│   ├── starters-template.html      (Pre-A1, Cambridge YLE)
│   ├── movers-template.html        (A1, Cambridge YLE)
│   ├── ket-template.html           (A2, Cambridge Key - React SPA)
│   ├── pet-template.html           (B1, Cambridge PET)
│   ├── ielts-reading-template.html (B2+, IELTS Academic Reading)
│   ├── ielts-writing-template.html (B2+, IELTS Academic Writing)
│   ├── toeic-reading-template.html (B1-B2, TOEIC Reading)
│   └── tuyensinh-template.html     (Tuyển Sinh lớp 10)
├── Congratulations/
│   └── index.html              ← Trang chúc mừng 4 cấp độ tự thích ứng
├── congratulations.html        ← Redirect → Congratulations/index.html
└── index.html                  ← Trang chủ portal
```

### Bảng phân loại Template

| Keyword trong tên file | Template sử dụng | Category trên Leaderboard |
|------------------------|-------------------|---------------------------|
| `starters` | `starters-template.html` | `young` (Thiếu nhi) |
| `movers` | `movers-template.html` | `young` (Thiếu nhi) |
| `ket` | `ket-template.html` | `ket` |
| `pet` | `pet-template.html` | `pet` |
| `tuyensinh` / `tuyển sinh` | `tuyensinh-template.html` | `pet` |
| `toeic` | `toeic-reading-template.html` | `toeic` |
| `ielts-reading` / `ielts reading` | `ielts-reading-template.html` | `ielts` |
| `ielts-writing` / `ielts writing` | `ielts-writing-template.html` | `ielts` |

---

## Bước 1: Quét Các File Mới
- So sánh các tệp `.html` trong `Fix/` chưa có ở `Exam/`.
- Nếu không có file mới → **DỪNG** và thông báo.
- Liệt kê danh sách file mới và xác định **loại bài thi** từ tên file.

## Bước 2: Chọn Template & Tạo Bản Sao

### 2a. Xác định Template phù hợp
- Dựa vào tên file và nội dung, chọn template **đúng cấp độ** (xem bảng phân loại trên).
- Nếu file gốc trong Fix/ đã có giao diện hoàn chỉnh → copy trực tiếp, KHÔNG cần dùng template.
- Nếu file gốc chỉ có câu hỏi thô → copy template, sau đó inject nội dung câu hỏi vào.

### 2b. Đổi tên chuẩn
- Quy tắc đặt tên: `{loại}-{số thứ tự}.html` — chữ thường, gạch ngang.
- Ví dụ: `ielts-reading-7.html`, `starters-2.html`, `toeic-reading-3.html`

### 2c. Sao chép
- Copy file sang thư mục `Exam/`.

## Bước 3: Cấu Hình Bài Thi (BẮT BUỘC cho mọi file)

Mở file HTML đã copy trong `Exam/` và đảm bảo ĐẦY ĐỦ tất cả các yêu cầu sau:

### 3a. Branding & Navigation
- Phải có nút 🏠 **Trang Chủ** quay về `../index.html`.
- Header phải chứa:
  ```
  CÔNG TY TNHH GIÁO DỤC VÀ ĐÀO TẠO HOÀI AN NHIÊN
  TRUNG TÂM TIẾNG ANH CÔ THUÝ
  MST: 0318842992
  CS1: 202/1 Nguyễn Thị Lắng, Củ Chi
  CS2: 61 Lê Đình Thám, Tân Phú
  CS3: 325/5T Nguyễn Thị Thảnh, Hóc Môn
  ```

### 3b. Google Sheets Integration
- Khai báo biến:
  ```javascript
  const GOOGLE_SHEET_URL = 'https://script.google.com/macros/s/AKfycbwrDJupIOU4PY92cMNRfafeQ-RH9Pra5EaHrnlELAnwsaVqaWiWzuIanPRY_BCM8Ohv/exec';
  ```
- Thêm element `#cloud-status` để hiển thị trạng thái kết nối.
- Thêm element `#save-status` để hiển thị trạng thái lưu kết quả.

### 3c. Validation Tên Học Viên (BẮT BUỘC)
- File phải có input nhập tên (id phổ biến: `student-name`, `overlay-name`, `candidateName`, `cand-name`, `ket-student-name`, `studentName`).
- Hàm `startTest()` hoặc nút "Bắt đầu" phải kiểm tra `name.trim()` không được trống.
- Nếu trống → `alert('Vui lòng nhập họ và tên để bắt đầu làm bài!')` rồi `return`.
- **KHÔNG** được dùng `prompt()` để hỏi tên sau khi nộp bài — tên phải nhập TRƯỚC khi thi.

### 3d. Thu Thập Chi Tiết Đáp Án (BẮT BUỘC)
- Trong hàm `submitTest()` hoặc hàm chấm điểm, PHẢI khai báo `const answersSubmitted = {};`.
- Trong vòng lặp chấm từng câu, gán `answersSubmitted[i] = input.value` để lưu câu trả lời.
- Payload fetch gửi lên Google Sheets phải đúng format chuẩn:
  ```javascript
  body: JSON.stringify({
      student_name: window.studentName,
      exam_type: 'TÊN_BÀI_THI',     // VD: 'IELTS-007', 'Starters Test 2'
      score: score,
      total: TOTAL_QUESTIONS,
      band: bandText,                 // VD: '7.0', '4 Shields', 'Grade B'
      answers: answersSubmitted
  })
  ```

### 3e. Redirect đến trang Congratulations (BẮT BUỘC)
> **QUAN TRỌNG:** Redirect PHẢI **luôn luôn** xảy ra cho MỌI mức điểm, KHÔNG được bọc trong `if (score >= x)`.

- Trang `Congratulations/index.html` sẽ tự động xử lý 4 cấp độ dựa vào % điểm:
  - ≥85%: Tuyên dương hoành tráng (vàng gold, confetti)
  - 70-84%: Chúc mừng tích cực (xanh dương, ngôi sao)
  - 50-69%: Động viên + lời khuyên (xanh lá, 4 tips)
  - <50%: Khuyến khích + hướng dẫn chi tiết (cam ấm, 6 tips + SĐT)

- **KHÔNG dùng `confirm()` dialog** — redirect trực tiếp sau 2-3 giây.

- Format redirect chuẩn (nằm NGOÀI `if`, sau khi lưu Google Sheets xong):
  ```javascript
  // Redirect to Congratulations page
  setTimeout(() => {
      window.location.href = `../congratulations.html?name=${encodeURIComponent(studentName)}&score=${score}&total=${total}&band=${bandText}&exam=${encodeURIComponent(examName)}`;
  }, 3000);
  ```

- **Lưu ý path:**
  - File trong `Exam/` dùng: `../congratulations.html` (sẽ tự redirect → `Congratulations/index.html`)
  - HOẶC trỏ thẳng: `../Congratulations/index.html`

### 3f. Chèn Script Địa Điểm + Ngày Thi Tự Động (BẮT BUỘC)
Ngay trước thẻ `</body>`, PHẢI chèn đoạn script sau. Script này tự động:
1. Tìm ô nhập tên học viên và chèn dropdown chọn địa điểm (Củ Chi / Tân Phú / Hóc Môn / Online).
2. Hook vào `fetch()` để gắn trường `location` vào payload Google Sheets.
3. Tự động điền ngày hiện tại (múi giờ Việt Nam) vào ô `input[type="date"]` nếu trống.

```html
<script>
document.addEventListener('DOMContentLoaded', () => {
    const possibleIds = ['overlay-name', 'student-name', 'studentName', 'ket-student-name', 'cand-name', 'candidateName'];
    let nameInput = null;
    for (let id of possibleIds) {
        if (document.getElementById(id)) {
            nameInput = document.getElementById(id);
            break;
        }
    }

    // Fallback: tìm theo placeholder chứa chữ "tên"
    if (!nameInput) {
        const inputs = document.querySelectorAll('input[type="text"]');
        for (let input of inputs) {
            if (input.placeholder && input.placeholder.toLowerCase().includes('tên')) {
                nameInput = input;
                break;
            }
        }
    }

    if (nameInput && !document.getElementById('dynamic-location-select')) {
        const select = document.createElement('select');
        select.id = 'dynamic-location-select';
        select.innerHTML = '<option value="Củ Chi">Củ Chi</option><option value="Tân Phú">Tân Phú</option><option value="Hóc Môn">Hóc Môn</option><option value="Online">Online</option>';
        select.className = nameInput.className;
        select.style.marginTop = '10px';
        select.style.marginBottom = '10px';
        nameInput.parentNode.insertBefore(select, nameInput.nextSibling);

        const originalFetch = window.fetch;
        window.fetch = function() {
            if (arguments[0] && arguments[0].includes('script.google.com')) {
                try {
                    let opts = arguments[1];
                    let bodyObj = JSON.parse(opts.body);
                    bodyObj['location'] = select.value;
                    opts.body = JSON.stringify(bodyObj);
                } catch(e) { console.error(e); }
            }
            return originalFetch.apply(this, arguments);
        };
    }

    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            const vnTime = new Date(new Date().getTime() + 7 * 3600 * 1000);
            input.value = vnTime.toISOString().split('T')[0];
        }
    });
});
</script>
</body>
```

> **LƯU Ý:** Nếu file gốc từ Fix/ đã có sẵn thẻ `</body>`, hãy thay thế nó bằng đoạn script trên (đoạn script đã bao gồm `</body>` ở cuối). Nếu ID input tên trong file mới khác với danh sách `possibleIds`, hãy thêm ID đó vào mảng.

## Bước 4: Cập Nhật Trang Chủ index.html

### 4a. Tăng Counter
- Cập nhật số tổng `#stat-exam-count` (tổng số bài thi).

### 4b. Thêm Exam Card
- Chèn block `div.exam-card` vào `#cards-grid`, xếp theo cấp độ A2→B1→B2.
- Card phải chứa: tên bài thi, số câu hỏi, thời gian, nút làm bài.

### 4c. Leaderboard Category
- Bảng xếp hạng dùng kiến trúc **2 tầng tự động**: Tầng 1 là category (Thiếu nhi, KET, PET/TS10, TOEIC, IELTS) — **KHÔNG cần sửa**. Tầng 2 (sub-tabs) tự động sinh từ data.
- Chỉ cần đảm bảo `exam_type` trong payload fetch trong file HTML chứa keyword đúng:
  + Starters / Movers → category `young`
  + KET → category `ket`
  + PET / Tuyển Sinh → category `pet`
  + TOEIC → category `toeic`
  + IELTS → category `ielts`

## Bước 5: Kiểm Tra Chất Lượng File Mới (BẮT BUỘC)

> **QUAN TRỌNG:** Bước này PHẢI chạy trước khi push lên Github.

- Gọi workflow `/check-new-exam` để kiểm tra toàn diện file vừa thêm.
- Workflow sẽ tự động kiểm tra: DOCTYPE, biến `answersSubmitted`, redirect path, tên bài thi, format payload, branding, validation...
- Nếu phát hiện lỗi → workflow sẽ **tự sửa** và báo cáo.
- Chỉ khi **tất cả PASS** mới chuyển sang Bước 6.

## Bước 6: Auto Git Push
- `git add .`
- `git commit -m "Add [tên bài thi mới] - verified"`
- `git push`

---

## CHECKLIST KIỂM TRA TRƯỚC KHI PUSH

Trước khi chạy `git push` ở Bước 5, kiểm chứng file mới trong `Exam/` phải đáp ứng:

- [ ] Có nút 🏠 Trang Chủ (`href="../index.html"`)
- [ ] Có branding "Hoài An Nhiên" + "Cô Thuý" + MST + 3 cơ sở
- [ ] Có biến `GOOGLE_SHEET_URL` đúng endpoint
- [ ] Có `#cloud-status` hiển thị trạng thái kết nối
- [ ] Có validation tên học viên (không cho phép bỏ trống, dùng `alert`, KHÔNG dùng `prompt`)
- [ ] Có object `answersSubmitted` thu thập đáp án chi tiết
- [ ] Payload fetch có trường `answers: answersSubmitted`
- [ ] `exam_type` trong payload chứa keyword đúng category
- [ ] Redirect đến `../congratulations.html` **KHÔNG có điều kiện if** (luôn redirect)
- [ ] **KHÔNG** có `confirm()` dialog trước redirect
- [ ] Có đoạn script Địa Điểm + Ngày Thi tự động (trước `</body>`)
- [ ] index.html đã cập nhật exam card và counter

---

## LƯU Ý QUAN TRỌNG

### ❌ KHÔNG được làm
- KHÔNG bọc redirect trong `if (score >= x)` — mọi học viên đều phải được redirect
- KHÔNG dùng `confirm()` trước redirect — dùng `setTimeout` trực tiếp
- KHÔNG dùng `prompt()` để hỏi tên — tên luôn nhập trước khi thi
- KHÔNG sửa file template gốc trong `Template/` — chỉ copy sang `Exam/`

### ✅ NÊN làm
- Dùng template phù hợp cấp độ để đảm bảo giao diện thống nhất
- Giữ nguyên đoạn script location select y hệt (đã tích hợp sẵn trong template)
- Đảm bảo redirect hoạt động cho cả điểm cao LẪN điểm thấp
- Kiểm tra file bằng workflow `/check-all-exams` sau khi thêm
