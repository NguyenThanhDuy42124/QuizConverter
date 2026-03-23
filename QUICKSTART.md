# ⚡ Quick Start Guide

## 🚀 5-Minute Setup

### Windows Users
1. Double-click `setup.bat`
2. Wait for installation to complete
3. Update `backend/.env` with your MySQL credentials
4. Open two terminals:
   - Terminal 1: `cd backend && python main.py`
   - Terminal 2: `cd frontend && npm start`
5. Open http://localhost:3000 in browser

### Mac/Linux Users
1. Run `bash setup.sh`
2. Wait for installation to complete
3. Update `backend/.env` with your MySQL credentials
4. Open two terminals:
   - Terminal 1: `cd backend && python -m venv venv && source venv/bin/activate && python main.py`
   - Terminal 2: `cd frontend && npm start`
5. Open http://localhost:3000 in browser

## 📋 Manual Setup (if automated setup fails)

### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
# Update .env with your MySQL info
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## ✅ Verify Setup

**Backend Working**:
- Visit http://localhost:8000/docs
- Should see Swagger API documentation

**Frontend Working**:
- Visit http://localhost:3000
- Should see Quiz Converter interface

**Database Connected**:
- Check MySQL is running
- Try POST request to /api/convert/

## 📄 Sample HTML to Test

```html
<div class="que multichoice">
  <div class="content">
    <div class="qtext">
      <p>What is Python?</p>
    </div>
  </div>
  <div class="answer">
    <div>
      <span class="answernumber">A.</span>
      <div class="flex-fill">A programming language</div>
    </div>
    <div>
      <span class="answernumber">B.</span>
      <div class="flex-fill">A snake species</div>
    </div>
    <div>
      <span class="answernumber">C.</span>
      <div class="flex-fill">A software tool</div>
    </div>
  </div>
</div>
```

1. Copy the above HTML
2. Paste in HtmlInputPanel on http://localhost:3000
3. Click "Phân tích & Chuyển đổi"
4. See results and download Word file

## 🛠️ Common Issues

| Issue | Solution |
|-------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| "Connection refused" on backend | Ensure MySQL is running |
| Port 8000/3000 in use | Change port in .env or scripts |
| "npm not found" | Install Node.js from nodejs.org |
| "python not found" | Install Python 3.10+ |

## 📚 Full Documentation

- **README.md** - Project overview and API docs
- **DEVELOPMENT.md** - In-depth development guide

## 🎯 What to Do Next

1. **Test with real Moodle HTML**: Export quiz from Moodle and paste
2. **Create more test cases**: Add tests in `backend/test_converter.py`
3. **Deploy to production**: Set up environment and configure database
4. **Customize styling**: Modify CSS files in `frontend/src/styles/`
5. **Add features**: Database history view, batch processing, etc.

---

**Need Help?** Check DEVELOPMENT.md or README.md
