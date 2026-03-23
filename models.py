"""
SQLAlchemy ORM models for storing conversion history.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from datetime import datetime
from database import Base


class ConversionHistory(Base):
    """Model for storing quiz conversion history."""
    
    __tablename__ = "conversion_history"

    id = Column(Integer, primary_key=True, index=True)
    
    # Metadata
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    
    # Content information
    question_count = Column(Integer, default=0, nullable=False)
    
    # Original input
    html_input = Column(Text, nullable=False)
    
    # Generated outputs
    text_output = Column(Text, nullable=True)
    word_document_path = Column(String(255), nullable=True)
    
    # Additional metadata
    file_id = Column(String(100), unique=True, index=True, nullable=True)
    is_shuffled = Column(Integer, default=0)  # 0: No, 1: Yes
    shuffle_count = Column(Integer, default=0)  # Number of variation versions created
    
    # Extended info stored as JSON
    metadata_json = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<ConversionHistory(id={self.id}, question_count={self.question_count}, created_at={self.created_at})>"
