"""
FastAPI application with API endpoints for quiz conversion.
Endpoints: POST /api/convert/ and GET /api/download/{file_id}
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

from fastapi import FastAPI, Depends, HTTPException, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import aiofiles
import uuid
from datetime import datetime
import asyncio
import json

from database import Base, engine, AsyncSessionLocal, init_db, dispose_engine
from models import ConversionHistory
from schemas import ConvertHTMLRequest, ConvertHTMLResponse, ConversionHistorySchema
from converter import parse_html_to_text_and_doc, QuizParser, export_marked_text, export_marked_docx, export_unmarked_docx
from combinatorics import shuffle_quiz
from gemini_service import analyze_quiz_with_ai


# Create FastAPI app
app = FastAPI(
    title="Quiz Converter API",
    description="Convert Moodle HTML quizzes to text and Word documents",
    version="1.0.0"
)

# Configure CORS with environment variable support
cors_origins = os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"]')
try:
    cors_origins_list = json.loads(cors_origins)
except (json.JSONDecodeError, TypeError):
    cors_origins_list = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp directory for files
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)


@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    try:
        await init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    await dispose_engine()


async def get_db():
    """Dependency for getting async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@app.post("/api/convert/", response_model=ConvertHTMLResponse)
async def convert_html(
    request: ConvertHTMLRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Convert HTML quiz to text and Word document.
    
    Args:
        request: HTML content and conversion parameters
        db: Database session
        
    Returns:
        JSON with success status, text output, and download URL
    """
    try:
        if not request.html_content.strip():
            raise HTTPException(status_code=400, detail="HTML content is empty")
        
        # Parse HTML
        text_output, doc_output, question_count = parse_html_to_text_and_doc(
            request.html_content
        )
        
        if question_count == 0:
            raise HTTPException(
                status_code=400,
                detail="No valid questions found in HTML"
            )
        
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        doc_filename = f"{file_id}.docx"
        doc_path = os.path.join(TEMP_DIR, doc_filename)
        
        # Save Word document
        doc_output.save(doc_path)
        
        # Handle shuffling if requested
        shuffle_count = 0
        if request.shuffle and request.shuffle_count > 0:
            # Parse questions for shuffling
            from converter import QuizParser
            parser = QuizParser()
            questions = parser.parse_questions(request.html_content)
            
            # Generate shuffled variations
            variations = shuffle_quiz(questions, request.shuffle_count)
            shuffle_count = len(variations)
        
        # Save to database
        history = ConversionHistory(
            html_input=request.html_content,
            text_output=text_output,
            word_document_path=doc_path,
            file_id=file_id,
            question_count=question_count,
            is_shuffled=1 if request.shuffle else 0,
            shuffle_count=shuffle_count
        )
        
        db.add(history)
        await db.commit()
        await db.refresh(history)
        
        return ConvertHTMLResponse(
            success=True,
            question_count=question_count,
            text_output=text_output,
            file_id=file_id,
            download_url=f"/api/download/{file_id}",
            conversion_history_id=history.id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in convert_html: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{file_id}")
async def download_document(
    file_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Download Word document by file ID.
    
    Args:
        file_id: Unique file identifier
        db: Database session
        
    Returns:
        Word document file
    """
    try:
        # Verify file exists in database
        result = await db.execute(
            select(ConversionHistory).where(
                ConversionHistory.file_id == file_id
            )
        )
        record = result.scalars().first()
        
        if not record:
            raise HTTPException(status_code=404, detail="File not found")
        
        doc_path = record.word_document_path
        
        # Verify file exists on disk
        if not os.path.exists(doc_path):
            raise HTTPException(status_code=404, detail="Document file not found")
        
        # Return file
        return FileResponse(
            path=doc_path,
            filename=f"quiz_{file_id[:8]}.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in download_document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/")
async def get_history(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Get recent conversion history.
    
    Args:
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of recent conversions
    """
    try:
        result = await db.execute(
            select(ConversionHistory)
            .order_by(ConversionHistory.created_at.desc())
            .limit(limit)
        )
        records = result.scalars().all()
        
        return [
            ConversionHistorySchema.model_validate(r) for r in records
        ]
    
    except Exception as e:
        print(f"Error in get_history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-with-ai/")
async def analyze_with_ai(request: ConvertHTMLRequest):
    """
    Analyze quiz with Google Gemini AI to predict correct answers.
    
    Args:
        request: ConvertHTMLRequest with html_content
        
    Returns:
        Dictionary with predictions and questions
    """
    try:
        if not request.html_content.strip():
            raise HTTPException(status_code=400, detail="HTML content is empty")
        
        # Parse questions from HTML
        parser = QuizParser()
        questions = parser.parse_questions(request.html_content)
        
        if not questions:
            raise HTTPException(status_code=400, detail="No questions found in HTML")
        
        # Analyze with AI
        predictions = analyze_quiz_with_ai(questions)
        
        # Prepare response
        result = {
            "total_questions": len(questions),
            "questions": []
        }
        
        for q in questions:
            q_num = q.get('question_number', q.get('number', 0))
            predicted = predictions.get(q_num, 'A')
            
            result["questions"].append({
                "question_number": q_num,
                "question_text": q.get('question_text', q.get('text', '')),
                "answers": q.get('answers', []),
                "predicted_answer": predicted
            })
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in analyze_with_ai: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export-marked-text/")
async def export_marked_text_endpoint(request: ConvertHTMLRequest):
    """
    Export quiz as text with AI-predicted answers marked.
    
    Args:
        request: ConvertHTMLRequest with html_content
        
    Returns:
        Text file with marked answers
    """
    try:
        if not request.html_content.strip():
            raise HTTPException(status_code=400, detail="HTML content is empty")
        
        # Parse questions
        parser = QuizParser()
        questions = parser.parse_questions(request.html_content)
        
        # Get AI predictions
        predictions = analyze_quiz_with_ai(questions)
        
        # Export as marked text
        text_content = export_marked_text(questions, predictions)
        
        # Return as text file
        from fastapi.responses import Response
        return Response(
            content=text_content,
            media_type="text/plain; charset=utf-8",
            headers={"Content-Disposition": "attachment; filename=quiz_marked.txt"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in export_marked_text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export-marked-docx/")
async def export_marked_docx_endpoint(request: ConvertHTMLRequest):
    """
    Export quiz as Word document with AI-predicted answers highlighted.
    
    Args:
        request: ConvertHTMLRequest with html_content
        
    Returns:
        Word document with marked answers
    """
    try:
        if not request.html_content.strip():
            raise HTTPException(status_code=400, detail="HTML content is empty")
        
        # Parse questions
        parser = QuizParser()
        questions = parser.parse_questions(request.html_content)
        
        # Get AI predictions
        predictions = analyze_quiz_with_ai(questions)
        
        # Export as marked docx
        doc = export_marked_docx(questions, predictions)
        
        # Save temporarily and return
        import io
        from docx import Document
        
        doc_io = io.BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)
        
        from fastapi.responses import Response
        return Response(
            content=doc_io.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=quiz_marked.docx"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in export_marked_docx: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export-unmarked-docx/")
async def export_unmarked_docx_endpoint(request: ConvertHTMLRequest):
    """
    Export quiz as Word document without answers shown.
    
    Args:
        request: ConvertHTMLRequest with html_content
        
    Returns:
        Word document without answers
    """
    try:
        if not request.html_content.strip():
            raise HTTPException(status_code=400, detail="HTML content is empty")
        
        # Parse and export without predictions
        text_output, doc_output, _ = parse_html_to_text_and_doc(request.html_content)
        
        # Save temporarily and return
        import io
        from docx import Document
        
        doc_io = io.BytesIO()
        doc_output.save(doc_io)
        doc_io.seek(0)
        
        from fastapi.responses import Response
        return Response(
            content=doc_io.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=quiz_unmarked.docx"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in export_unmarked_docx: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health/")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "quiz-converter-api"
    }


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Quiz Converter API",
        "version": "1.0.0",
        "endpoints": {
            "convert": "POST /api/convert/",
            "download": "GET /api/download/{file_id}",
            "history": "GET /api/history/",
            "health": "GET /api/health/"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
