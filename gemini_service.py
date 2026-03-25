"""
Gemini AI Service for Quiz Analysis
Handles communication with Google Generative AI API
Supports mock mode for development without API key
"""

import json
import re
import os
from typing import List, Dict, Optional


class GeminiService:
    """Service to analyze quiz questions with Google Gemini AI"""
    
    def __init__(self, api_key: str = None):
        """Initialize Gemini service with API key"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.use_mock = not self.api_key  # Use mock if no API key
        
        if not self.use_mock:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
            except Exception as e:
                print(f"Warning: Could not initialize Gemini: {e}. Using mock mode.")
                self.use_mock = True
    
    def format_questions_for_analysis(self, questions: List[Dict]) -> str:
        """Format questions into readable text for AI analysis"""
        quiz_text = ""
        
        for q in questions:
            quiz_text += f"\nCâu {q['question_number']}: {q['question_text']}\n"
            for ans in q['answers']:
                quiz_text += f"{ans['letter']}. {ans['content']}\n"
        
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
    
    def _generate_mock_predictions(self, questions: List[Dict]) -> Dict:
        """Generate mock predictions for testing without API key"""
        predictions = {}
        options = ['A', 'B', 'C', 'D']
        
        for q in questions:
            question_num = q['question_number']
            num_answers = len(q['answers'])
            # Simple mock: cycle through options based on question number
            answer_idx = (question_num - 1) % num_answers
            predictions[f"question_{question_num}"] = options[answer_idx]
        
        return predictions
    
    async def analyze_quiz(self, questions: List[Dict]) -> Dict:
        """
        Analyze quiz questions and predict correct answers
        
        Args:
            questions: List of question dicts with 'question_number', 'question_text', 'answers'
            
        Returns:
            Dict with predictions: {"question_1": "A", "question_2": "B", ...}
        """
        try:
            # Use mock if no API key
            if self.use_mock:
                print("⚠️  Mock mode: No Gemini API key configured. Using mock predictions.")
                predictions = self._generate_mock_predictions(questions)
                return predictions
            
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
            # Fallback to mock on error
            predictions = self._generate_mock_predictions(questions)
            print(f"⚠️  Falling back to mock predictions")
            return predictions


def create_gemini_service(api_key: str = None) -> GeminiService:
    """Factory function to create GeminiService instance"""
    return GeminiService(api_key)
