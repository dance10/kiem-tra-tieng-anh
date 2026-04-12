function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var data = JSON.parse(e.postData.contents);

    // Xử lý tự động gom tên và địa điểm
    var studentName = data.student_name || data.name || data.studentName || 'Ẩn danh';
    var location = data.location || '';
    var examType = data.exam_type || data.exam || data.examType || 'Unknown';
    
    // Tự động phân giải điểm số chuẩn
    var totalQ = data.total || 40;
    var scoreStr = data.score;
    if (typeof scoreStr === 'number' || (typeof scoreStr === 'string' && scoreStr.indexOf('/') === -1)) {
        scoreStr = data.score + '/' + totalQ;
    }

    // Thêm các dữ liệu thời gian vào CUỐI cùng để Cột Answers cũ không bị xô lệch
    sheet.appendRow([
      new Date().toLocaleString('vi-VN', {timeZone: 'Asia/Ho_Chi_Minh'}),
      studentName,
      location,
      examType,
      scoreStr,
      data.band || '',
      data.answers ? JSON.stringify(data.answers) : '',  // Cột 7 (Cũ vẫn y nguyên)
      data.startTime || 'Dữ liệu cũ',                    // Cột 8 (Mới đính kèm sau)
      data.endTime || 'Dữ liệu cũ',                      // Cột 9
      data.timeTaken || 'Dữ liệu cũ'                     // Cột 10
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
  try {
    var action = (e && e.parameter && e.parameter.action) ? e.parameter.action : '';
    
    if (action === 'getResults') {
      var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
      var data = sheet.getDataRange().getValues();
      var results = [];
      
      // Bỏ qua dòng tiêu đề, đọc danh sách
      for (var i = 1; i < data.length; i++) {
        if (data[i][1]) { // Chỉ lọc dòng có tên
          results.push({
            time: data[i][0] || '',
            name: data[i][1] || '',
            location: data[i][2] || '', 
            exam: data[i][3] || '',     
            score: data[i][4] || '',
            band: data[i][5] || '',
            startTime: data[i][7] || 'Không có',
            endTime: data[i][8] || 'Không có',
            timeTaken: data[i][9] || 'Không có'
          });
        }
      }
      
      return ContentService.createTextOutput(
        JSON.stringify({ status: 'success', data: results })
      ).setMimeType(ContentService.MimeType.JSON);
    }
    
    return ContentService.createTextOutput(
      JSON.stringify({ status: 'success', message: 'API is running!' })
    ).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    return ContentService.createTextOutput(
      JSON.stringify({ status: 'error', message: error.toString() })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}