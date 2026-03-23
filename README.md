# Quiz Converter Project

Ứng dụng chuyên chuyển đổi HTML quizzes từ Moodle sang định dạng Word (.docx) và Plain Text, kèm tính năng xáo trộn đề thi.

## 🎯 Tính năng

- **Phân tích HTML**: Tự động trích xuất câu hỏi và đáp án từ HTML Moodle
- **Xuất Word**: Tạo file Word (.docx) định dạng đẹp
- **Xuất Text**: Bản văn bản thuần của bài trắc nghiệm
- **Xáo trộn Đề**: Tạo nhiều phiên bản đề với xáo trộn câu hỏi và đáp án
- **Lưu trữ**: Lưu lịch sử chuyển đổi trong MySQL
- **API RESTful**: FastAPI backend với CORS hỗ trợ React frontend

## 📋 Cấu trúc Dự án

```
quiz-converter/
├── backend/                    # Python FastAPI Backend
│   ├── main.py                # FastAPI app + routes
│   ├── converter.py           # Parser HTML + Generator Word/Text
│   ├── combinatorics.py       # Math engine (xáo trộn)
│   ├── models.py              # SQLAlchemy ORM
│   ├── schemas.py             # Pydantic models
│   ├── database.py            # MySQL config
│   ├── requirements.txt       # Python dependencies
│   ├── test_converter.py      # Unit tests
│   └── alembic/              # Database migrations (optional)
│
└── frontend/                   # React 19 Frontend
    ├── src/
    │   ├── App.js             # Main component
    │   ├── api.js             # Axios API client
    │   ├── components/
    │   │   ├── HtmlInputPanel.js      # Nhập HTML
    │   │   ├── TextResultPanel.js     # Hiển thị kết quả
    │   │   └── WordExport.js          # Nút tải Word
    │   ├── styles/
    │   │   ├── App.css
    │   │   ├── HtmlInputPanel.css
    │   │   ├── TextResultPanel.css
    │   │   └── WordExport.css
    │   ├── index.js
    │   └── App.css
    ├── public/
    │   └── index.html
    ├── package.json
    ├── .env                   # Environment variables
    └── .gitignore
```

## 🚀 Hướng Dẫn Cài Đặt

### Backend Setup

1. **Cài đặt Python dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Cấu hình Database**:
   - Đảm bảo MySQL 8 đang chạy
   - Tạo database: `CREATE DATABASE quiz_converter;`
   - Cập nhật `.env` với thông tin kết nối

3. **Khởi tạo Database**:
```bash
python -c "import asyncio; from database import init_db; asyncio.run(init_db())"
```

4. **Chạy Backend**:
```bash
python main.py
```
API sẽ chạy tại `http://localhost:8000`

### Frontend Setup

1. **Cài đặt Node dependencies**:
```bash
cd frontend
npm install
```

2. **Cấu hình API URL**:
   - Cập nhật `.env` nếu backend không chạy trên `localhost:8000`

3. **Chạy Development Server**:
```bash
npm start
```
App sẽ mở tại `http://localhost:3000`

## 📚 API Endpoints

### POST `/api/convert/`
Chuyển đổi HTML sang Word + Text

**Request**:
```json
{
  "html_content": "<div class='que multichoice'>...</div>",
  "shuffle": false,
  "shuffle_count": 1
}
```

**Response**:
```json
{
  "success": true,
  "question_count": 5,
  "text_output": "Câu 1: ...\nA. ...",
  "file_id": "abc123def456",
  "download_url": "/api/download/abc123def456",
  "conversion_history_id": 1
}
```

### GET `/api/download/{file_id}`
Tải file Word

**Response**: Binary file (.docx)

### GET `/api/history/?limit=10`
Lấy lịch sử chuyển đổi

### GET `/api/health/`
Kiểm tra trạng thái API

## 💻 Công nghệ Sử Dụng

**Backend**:
- Python 3.10+
- FastAPI - Web framework
- SQLAlchemy - ORM
- BeautifulSoup4 - HTML parsing
- python-docx - Word document generation
- MySQL 8 - Database

**Frontend**:
- React 19
- Axios - HTTP client
- CSS3 - Styling

## 🧪 Testing

```bash
cd backend
python test_converter.py
```

## 📝 Lưu Ý

- Module `converter.py` hỗ trợ DOM HTML từ Moodle với class `que multichoice`
- Hỗ trợ tối đa 100 mã đề được xáo trộn
- File Word sẽ được lưu trong thư mục `temp/`
- Dữ liệu được lưu trữ trong MySQL cho mục đích lịch sử

## 🔐 Bảo Mật

- Không lưu HTML gốc nhạy cảm lâu dài
- Frontend sử dụng CORS để kiểm soát quyền truy cập
- .env không được commit
- Mật khẩu MySQL nên được thay đổi trước khi deploy

## 📧 Support

Nếu gặp vấn đề, vui lòng kiểm tra:
1. MySQL đang chạy
2. Python 3.10+ đã cài đặt
3. Node.js 14+ đã cài đặt
4. Port 8000 (backend) và 3000 (frontend) không bị chiếm

---

**Version**: 1.0.0  
**License**: MIT
