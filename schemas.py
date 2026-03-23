"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class QuestionAnswer(BaseModel):
    """Schema for a single quiz question and its answers."""
    question_number: int
    question_text: str
    answers: List[dict] = Field(
        ...,
        description="List of answer options with letter and content"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "question_number": 1,
                "question_text": "What is Python?",
                "answers": [
                    {"letter": "A", "content": "A programming language"},
                    {"letter": "B", "content": "A snake"},
                    {"letter": "C", "content": "A tool"}
                ]
            }
        }


class ConvertHTMLRequest(BaseModel):
    """Request model for HTML conversion endpoint."""
    html_content: str = Field(..., description="HTML content from Moodle quiz")
    shuffle: bool = Field(default=False, description="Whether to shuffle questions")
    shuffle_count: int = Field(
        default=1,
        ge=1,
        le=100,
        description="Number of shuffled variations to generate"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "html_content": "<div class='que multichoice'>...</div>",
                "shuffle": False,
                "shuffle_count": 1
            }
        }


class ConvertHTMLResponse(BaseModel):
    """Response model for conversion endpoint."""
    success: bool
    message: Optional[str] = None
    question_count: int
    text_output: str = Field(..., description="Plain text version of quiz")
    file_id: str = Field(..., description="Unique ID for Word document file")
    download_url: str = Field(..., description="URL to download Word document")
    conversion_history_id: int = Field(..., description="Database record ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "question_count": 5,
                "text_output": "Câu 1: ...\nA. ...\nB. ...",
                "file_id": "abc123def456",
                "download_url": "/api/download/abc123def456",
                "conversion_history_id": 1
            }
        }


class ConversionHistorySchema(BaseModel):
    """Schema for database record."""
    id: int
    created_at: datetime
    question_count: int
    file_id: Optional[str]
    is_shuffled: int
    shuffle_count: int
    
    class Config:
        from_attributes = True


class DownloadResponse(BaseModel):
    """Response for download endpoint metadata."""
    file_id: str
    created_at: datetime
    question_count: int
    
    class Config:
        from_attributes = True
