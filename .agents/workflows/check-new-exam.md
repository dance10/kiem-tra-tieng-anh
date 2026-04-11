---
description: Kiểm tra chất lượng file exam mới TRƯỚC khi push Github. Gọi sau /auto-add-exams, trước git push.
---
# QUY TRÌNH CHECK-NEW-EXAM

// turbo-all

> **Mục đích:** Kiểm tra toàn diện file exam vừa được thêm vào thư mục `Exam/` để đảm bảo không có lỗi gây gián đoạn khi học viên làm bài. Workflow này được gọi **sau** `/auto-add-exams` (sau bước 4) và **trước** khi `git push` (bước 5).

---

## Bước 1: Xác định file mới cần kiểm tra

- Chạy `git diff --name-only --cached` hoặc `git status` để xác định các file `.html` mới/sửa trong `Exam/`.
- Liệt kê danh sách file cần kiểm tra.
- Nếu không có file mới → **DỪNG** và thông báo "Không có file mới cần kiểm tra".

---

## Bước 2: Kiểm tra cấu trúc HTML

Với **từng file** mới, kiểm tra:

### 2a. DOCTYPE hợp lệ
- Dòng đầu tiên PHẢI là `<!DOCTYPE html>` (hoặc bắt đầu bằng `<!DOCTYPE`).
- **KHÔNG** được có text rác trước `<!DOCTYPE` (ví dụ: `IELTS READING TEST 5<!DOCTYPE html>`).
- Nếu phát hiện → **SỬA NGAY**: xoá text rác, chỉ giữ lại `<!DOCTYPE html>`.

### 2b. Thẻ đóng `</body>` và `</html>`
- File phải kết thúc đúng bằng `</body>` rồi `</html>`.

---

## Bước 3: Kiểm tra JavaScript Logic (QUAN TRỌNG NHẤT)

### 3a. Biến `answersSubmitted` — Khai báo + Gán giá trị
- Tìm `answersSubmitted` trong file.
- **PHẢI** có dòng khai báo: `let answersSubmitted = {};` hoặc `const answersSubmitted = {};`
- **PHẢI** có dòng gán giá trị trong vòng lặp: `answersSubmitted[...] = ...`
- **PHẢI** có dòng gửi trong fetch: `answers: answersSubmitted`
- Nếu **khai báo** nhưng **không gán** → Object rỗng `{}` gửi về Sheet → **SỬA NGAY**.
- Nếu **không khai báo** nhưng có **sử dụng** → `ReferenceError` crash → **SỬA NGAY**.

### 3b. Google Sheet URL
- PHẢI có biến `GOOGLE_SHEET_URL` chứa URL hợp lệ (bắt đầu bằng `https://script.google.com/macros/s/`).
- **KHÔNG** được là `PASTE_YOUR_URL_HERE`.

### 3c. Tên bài thi (`exam_type` / `exam`)
- Tìm field `exam_type` hoặc `exam` trong payload fetch.
- Giá trị PHẢI rõ ràng, có keyword category đúng:
  + `Starters` / `Movers` → category `young`
  + `KET` → category `ket`
  + `PET` / `Tuyển Sinh` → category `pet`
  + `TOEIC` → category `toeic`
  + `IELTS` → category `ielts`
- Tên **KHÔNG** được là mã code viết tắt (ví dụ: `IELTS-004`).

### 3d. Format payload fetch
- Payload gửi về Google Sheet PHẢI chứa đủ các trường:
  + `student_name` hoặc `name`
  + `exam_type` hoặc `exam`
  + `score`
  + `total`
  + `band`
  + `answers`

---

## Bước 4: Kiểm tra Redirect Path

### 4a. Redirect đến congratulations.html
- Tìm tất cả các dòng chứa `congratulations.html`.
- Vì file nằm trong `Exam/`, path PHẢI là `../congratulations.html` (có `../`).
- **KHÔNG** được là `congratulations.html` (thiếu `../`) → sẽ gây **404 Not Found**.
- Nếu sai → **SỬA NGAY**.

### 4b. Redirect KHÔNG có điều kiện
- Redirect **KHÔNG** được bọc trong `if (score >= x)`.
- Mọi học viên đều phải được redirect, bất kể điểm số.
- **KHÔNG** có `confirm()` dialog trước redirect.

---

## Bước 5: Kiểm tra Validation & Branding

### 5a. Validation tên học viên
- File PHẢI có input nhập tên.
- Hàm bắt đầu thi PHẢI kiểm tra `trim()` không rỗng.
- Nếu rỗng → phải `alert()` rồi `return`.
- **KHÔNG** được dùng `prompt()`.

### 5b. Branding
- PHẢI có nút 🏠 Trang Chủ trỏ về `../index.html`.
- Header PHẢI chứa: "Hoài An Nhiên", "Cô Thuý", MST.

### 5c. Script địa điểm + ngày thi
- Trước `</body>` PHẢI có đoạn script `dynamic-location-select`.

---

## Bước 6: Tổng hợp kết quả

Tạo bảng đánh giá cho từng file:

```
| File | Hạng mục | Trạng thái | Ghi chú |
|------|----------|------------|---------|
| xxx  | DOCTYPE  | ✅ PASS    |         |
| xxx  | answersSubmitted | ❌ FAIL | Chưa khai báo |
| ...  | ...      | ...        | ...     |
```

### Tổng kết:
- Nếu **tất cả PASS** → Thông báo "✅ File đã sẵn sàng để push lên Github!"
- Nếu **có FAIL** → Liệt kê lỗi đã tự động sửa và xác nhận lại.
- Sau khi sửa xong tất cả lỗi → Chạy lại kiểm tra nhanh để xác nhận.

---

## Bước 7: Chờ xác nhận push

- Hiển thị kết quả kiểm tra cho người dùng.
- Hỏi: "Tất cả file đã PASS. Tiến hành git push?"
- Nếu đồng ý → thực hiện:
  ```
  git add .
  git commit -m "Add [tên bài thi] - verified"
  git push
  ```

---

## DANH SÁCH LỖI PHỔ BIẾN (Tham khảo)

Các lỗi đã từng xảy ra trong hệ thống — luôn kiểm tra kỹ:

| # | Lỗi | File từng bị | Hậu quả |
|---|------|-------------|---------|
| 1 | Text rác trước `<!DOCTYPE>` | reading-5, reading-6 | Quirks Mode, render sai |
| 2 | `answersSubmitted` chưa khai báo | reading-4, reading-5 | JS crash khi submit |
| 3 | `answersSubmitted` khai báo nhưng không gán | reading-5 | Gửi object rỗng |
| 4 | Tên bài thi viết tắt (`IELTS-004`) | reading-4 | Dữ liệu Sheet lộn |
| 5 | Payload format cũ (`student_name`, `exam_type`) | reading-4 | Sheet không nhận đúng |
| 6 | Redirect thiếu `../` | reading-1, reading-2, ket-1, ket-2 | 404 Not Found |
| 7 | Redirect bọc trong `if (score >= x)` | (nhiều file cũ) | Điểm thấp không redirect |
