# HƯỚNG DẪN KẾT NỐI GOOGLE SHEETS (3 phút)

## Bước 1: Tạo Google Sheet
1. Vào https://sheets.google.com → Tạo **Bảng tính mới**
2. Đặt tên: **"Kết quả thi IELTS"**
3. Ở hàng 1, điền tiêu đề các cột:
   - A1: `Thời gian`
   - B1: `Họ tên`
   - C1: `Điểm`
   - D1: `Band`
   - E1: `Chi tiết đáp án`

## Bước 2: Tạo Apps Script
1. Trong Google Sheet, vào menu **Tiện ích mở rộng** → **Apps Script**
2. **Xóa hết** code mặc định trong file `Code.gs`
3. **Copy & Paste** đoạn code bên dưới vào:

```javascript
function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var data = JSON.parse(e.postData.contents);

    sheet.appendRow([
      new Date().toLocaleString('vi-VN', {timeZone: 'Asia/Ho_Chi_Minh'}),
      data.student_name,
      data.score + '/40',
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
   - Mô tả: `IELTS Result API`
   - Thực thi bằng: **Tôi (email của bạn)**
   - Ai có quyền truy cập: **Bất kỳ ai**
4. Bấm **Triển khai**
5. Bấm **Ủy quyền** → Chọn tài khoản Google → **Cho phép**
6. **SAO CHÉP URL** triển khai (dạng: `https://script.google.com/macros/s/xxx.../exec`)

## Bước 4: Dán URL vào file HTML
1. Mở file `ielts-reading-2.html`
2. Tìm dòng: `const GOOGLE_SHEET_URL = "PASTE_YOUR_URL_HERE";`
3. Thay `PASTE_YOUR_URL_HERE` bằng URL vừa copy

## ✅ XONG! 
- Khi học sinh nộp bài → kết quả tự động xuất hiện trong Google Sheet
- Anh mở Google Sheet bất cứ lúc nào để xem kết quả
