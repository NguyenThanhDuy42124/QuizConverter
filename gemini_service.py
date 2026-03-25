"""
Gemini AI Service for Quiz Analysis
Handles communication with Google Generative AI API
"""

import json
import re
from typing import List, Dict, Optional
import google.generativeai as genai


class GeminiService:
    """Service to analyze quiz questions with Google Gemini AI"""
    
    def __init__(self, api_key: str):
        """Initialize Gemini service with API key"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def format_questions_for_analysis(self, questions: List[Dict]) -> str:
        """Format questions into readable text for AI analysis"""
        quiz_text = ""
        
        for q in questions:
            quiz_text += f"\nCâu {q['number']}: {q['text']}\n"
            for ans in q['answers']:
                quiz_text += f"{ans['letter']}. {ans['text']}\n"
        
        return quiz_text
    
    def build_prompt(self, quiz_text: str) -> str:
        """Build precise prompt for Gemini AI"""
        prompt = f"""Bạn là một chuyên gia giải các bài trắc nghiệm tiếng Việt. 
Hãy phân tích các câu hỏi sau và chọn đáp án đúng nhất dựa trên kiến thức của bạn.

{quiz_text}

BẮTBUỘC: Trả về kết quả dưới dạng JSON THUẦN (chỉ JSON, không có text phía trước/sau):
{{
    "question_1": "A",
    "question_2": "B",
    "question_3": "C"
}}

Không giải thích gì thêm, chỉ trả về JSON."""
        return prompt
    
    async def analyze_quiz(self, questions: List[Dict]) -> Dict:
        """
        Analyze quiz questions and predict correct answers
        
        Args:
            questions: List of question dicts with 'number', 'text', 'answers'
            
        Returns:
            Dict with predictions: {"question_1": "A", "question_2": "B", ...}
        """
        try:
            # Format questions
            quiz_text = self.format_questions_for_analysis(questions)
            prompt = self.build_prompt(quiz_text)
            
            # Call Gemini API
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text
            json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
            
            if json_match:
                predictions = json.loads(json_match.group())
                return predictions
            else:
                raise ValueError("No valid JSON found in Gemini response")
        
        except Exception as e:
            print(f"Error analyzing quiz with Gemini: {str(e)}")
            raise


def create_gemini_service(api_key: str) -> Optional[GeminiService]:
    """Factory function to create GeminiService instance"""
    if not api_key:
        return None
    return GeminiService(api_key)
