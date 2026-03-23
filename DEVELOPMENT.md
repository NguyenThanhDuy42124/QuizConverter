# Development Guide for Quiz Converter

## 🎯 Project Overview

Quiz Converter is a full-stack application that:
1. Parses HTML quiz questions from Moodle
2. Converts them to plain text and Word documents
3. Supports shuffling questions to create test variations
4. Stores conversion history in MySQL

## 📁 Project Structure

### Backend (`/backend`)
- **main.py**: FastAPI application with API routes
- **converter.py**: HTML parsing and document generation
- **combinatorics.py**: Quiz shuffling using combinatorics
- **models.py**: SQLAlchemy database models
- **schemas.py**: Pydantic validation models
- **database.py**: Database connection and session management
- **test_converter.py**: Unit tests
- **alembic/**: Database migration tools (optional)

### Frontend (`/frontend`)
- **src/App.js**: Main React component
- **src/api.js**: Axios HTTP client
- **src/components/**: React components
  - HtmlInputPanel.js: Form for HTML input
  - TextResultPanel.js: Display text output
  - WordExport.js: Download Word file button
- **src/styles/**: CSS stylesheets
- **public/index.html**: HTML template

## 🔧 Development Setup

### Prerequisites
- Python 3.10+
- Node.js 14+
- MySQL 8
- Git

### Backend Development

1. **Create virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database**:
   - Update `backend/.env` with MySQL credentials
   - Create database: `CREATE DATABASE quiz_converter;`

4. **Initialize database**:
   ```bash
   python
   >>> import asyncio
   >>> from database import init_db
   >>> asyncio.run(init_db())
   ```

5. **Run tests**:
   ```bash
   python test_converter.py
   ```

6. **Start development server**:
   ```bash
   python main.py
   # Server runs on http://localhost:8000
   # API docs: http://localhost:8000/docs
   ```

### Frontend Development

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**:
   ```bash
   npm start
   # App runs on http://localhost:3000
   ```

3. **Build for production**:
   ```bash
   npm run build
   ```

## 🚀 Key Features to Understand

### Phase 1: HTML Parser (converter.py)

The parser uses BeautifulSoup4 to extract:
- Questions from `<div class="que multichoice">`
- Question text from `<div class="qtext">`
- Answers from `<div class="answer">`
- Answer letters and content from nested elements

**Main Classes**:
- `QuizParser`: Extracts structured data from HTML
- `QuizConverter`: Generates text and Word outputs

### Phase 2: Math Engine (combinatorics.py)

Calculates possible quiz variations using:
- Question permutations: n!
- Answer permutations: ∏(m!)
- Total variations: n! × ∏(m!)

**Main Class**:
- `QuizShuffler`: Generates unique shuffled variations

### Phase 3: API (main.py)

RESTful endpoints:
- `POST /api/convert/`: Process HTML and generate outputs
- `GET /api/download/{file_id}`: Download Word file
- `GET /api/history/`: Retrieve conversion history

### Phase 4: Frontend (React)

Component hierarchy:
```
App
├── HtmlInputPanel (form)
├── TextResultPanel (output display)
└── WordExport (download button)
```

## 🔄 Data Flow

1. **User Input**: Paste HTML in HtmlInputPanel
2. **HTTP Request**: Frontend sends to `/api/convert/`
3. **Parsing**: Backend parses HTML to structured questions
4. **Generation**: Converter creates text and Word outputs
5. **Storage**: Saves to MySQL with unique file_id
6. **Response**: Returns text content and download URL
7. **Download**: User can download Word file from link

## 📊 Database Schema

**ConversionHistory Table**:
```sql
- id (Primary Key)
- created_at (Timestamp)
- question_count (Integer)
- html_input (Text) - Original HTML
- text_output (Text) - Generated plain text
- word_document_path (String) - File path on disk
- file_id (String) - Unique identifier
- is_shuffled (Integer) - Flag: shuffled or not
- shuffle_count (Integer) - Number of variations
- metadata_json (JSON) - Additional data
```

## 🧪 Testing

### Backend Unit Tests
```bash
python test_converter.py
```

Tests cover:
- HTML parsing (questions and answers)
- Text conversion
- Word document generation
- Combinatorics calculations
- End-to-end conversion

### Manual API Testing

Use FastAPI Swagger UI:
```
http://localhost:8000/docs
```

Or use cURL:
```bash
curl -X POST "http://localhost:8000/api/convert/" \
  -H "Content-Type: application/json" \
  -d '{"html_content": "...", "shuffle": false}'
```

## 🔐 Security Considerations

1. **Input Validation**: Pydantic validates all requests
2. **CORS**: Configured for frontend origin only
3. **File Handling**: Files stored in `temp/` folder
4. **Database**: Use strong credentials in production
5. **Environment Variables**: Keep `.env` out of version control

## 📝 Code Style

- **Python**: Follow PEP 8 with 4-space indentation
- **JavaScript**: Use ES6+ with arrow functions
- **Comments**: Document complex logic
- **Variable Names**: Use descriptive, snake_case in Python, camelCase in JS

## 🚨 Common Issues & Solutions

### Database Connection Error
```
Fix: Ensure MySQL is running and credentials in .env are correct
```

### Port Already in Use
```
Backend conflict: Change API_PORT in .env
Frontend conflict: Set PORT=3001 npm start
```

### CORS Error
```
Fix: Ensure CORS_ORIGINS in .env includes frontend URL
```

### HTML Not Parsing
```
Fix: Ensure HTML contains <div class="que multichoice">
```

## 📚 Additional Resources

- FastAPI docs: https://fastapi.tiangolo.com/
- React docs: https://react.dev/
- BeautifulSoup docs: https://www.crummy.com/software/BeautifulSoup/
- SQLAlchemy docs: https://docs.sqlalchemy.org/
- python-docx docs: https://python-docx.readthedocs.io/

## 🤝 Contributing

When adding features:
1. Write tests first
2. Follow existing code style
3. Update documentation
4. Test with sample HTML
5. Clean up temp files

---

**Last Updated**: 2024
