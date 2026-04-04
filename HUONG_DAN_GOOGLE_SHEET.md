# HƯỚNG DẪN KẾT NỐI GOOGLE SHEETS (3 phút)

## Bước 1: Tạo Google Sheet
1. Vào https://sheets.google.com → Tạo **Bảng tính mới**
2. Đặt tên: **"Kết quả thi Tiếng Anh"**
3. Ở hàng 1, điền tiêu đề các cột:
   - A1: `Thời gian`
   - B1: `Họ tên`
   - C1: `Bài thi`
   - D1: `Điểm`
   - E1: `Xếp loại/Band`
   - F1: `Chi tiết đáp án`

## Bước 2: Tạo Apps Script
1. Trong Google Sheet, vào menu **Tiện ích mở rộng** → **Apps Script**
2. **Xóa hết** code mặc định trong file `Code.gs`
3. **Copy & Paste** đoạn code bên dưới vào:

```javascript
function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var data = JSON.parse(e.postData.contents);

    var examType = data.exam_type || 'Unknown';
    var totalQ = data.total || 40;

    sheet.appendRow([
      new Date().toLocaleString('vi-VN', {timeZone: 'Asia/Ho_Chi_Minh'}),
      data.student_name,
      examType,
      data.score + '/' + totalQ,
      data.band,
      JSON.stringify(data.answers)
    ]);

    return ContentService.createTextOutput(
      JSON.stringify({ status: 'success' })
    ).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(
      JSON.stringify({ status: 'error', message: error.toString() })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput("API is running!");
}
```

4. Bấm **💾 Lưu** (hoặc Ctrl+S)

## Bước 3: Deploy (Triển khai)
1. Bấm nút **Triển khai** → **Triển khai mới**
2. Chọn loại: **Ứng dụng web**
3. Cài đặt:
   - Mô tả: `Exam Result API`
   - Thực thi bằng: **Tôi (email của bạn)**
   - Ai có quyền truy cập: **Bất kỳ ai**
4. Bấm **Triển khai**
5. Bấm **Ủy quyền** → Chọn tài khoản Google → **Cho phép**
6. **SAO CHÉP URL** triển khai (dạng: `https://script.google.com/macros/s/xxx.../exec`)

## Bước 4: Dán URL vào các file HTML
URL **đã được cấu hình sẵn** trong cả 3 file bài thi:
- `ielts-reading-1.html` → IELTS Reading Test 1
- `ielts-reading-2.html` → IELTS Reading Test 2
- `ket-a2-exam.html` → KET A2 Exam

**Nếu cần đổi URL**, tìm dòng `const GOOGLE_SHEET_URL = "..."` trong mỗi file và thay URL mới.

## ⚠️ CẬP NHẬT Apps Script (Nếu cần)
Nếu anh đã Deploy trước đó, cần **Deploy lại bản mới** để nhận thêm cột "Bài thi":
1. Vào Apps Script → Paste code mới ở trên
2. **Triển khai** → **Quản lý triển khai** → Bấm **✏️ (Chỉnh sửa)**
3. Chọn **Phiên bản mới** → Bấm **Triển khai**

## ✅ XONG! 
- Khi học sinh nộp bài (từ bất kỳ bài thi nào) → kết quả tự động ghi vào Google Sheet
- Google Sheet sẽ hiển thị: Thời gian, Họ tên, Loại bài thi, Điểm, Xếp loại/Band, Chi tiết đáp án
- Học viên đạt thành tích cao sẽ được chuyển đến trang **Chúc mừng** vinh danh 🏆
