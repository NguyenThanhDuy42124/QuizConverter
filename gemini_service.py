"""
Google Gemini AI Service using HTTP API (not SDK).
Calls Gemini API directly via HTTP POST request using requests library.
Supports both real API mode and mock mode for development.
Uses the correct v1beta endpoint per Gemini's guidance.
"""

import os
import json
import logging
import requests
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for AI-powered quiz answer analysis using HTTP API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini service with API key from environment or parameter."""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.use_mock_mode = False
        
        # API endpoint - use v1beta (CRITICAL!)
        self.api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models"
        
        # Try models in order of preference (v1beta compatible only)
        self.models_to_try = [
            "gemini-1.5-flash",      # Latest, fast, reliable
            "gemini-1.5-pro",        # More powerful
            "gemini-2.0-flash",      # Newest model
        ]
        
        # System instruction to force single letter response
        self.system_instruction = """Bạn là một chuyên gia giải trắc nghiệm.
CHỈ trả về một chữ cái duy nhất là A, B, C, hoặc D.
TUYỆT ĐỐI không giải thích hay thêm từ ngữ khác.
Ví dụ: A"""
        
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set. Running in mock mode.")
            logger.info("To enable real API: create .env.local file with GEMINI_API_KEY")
            self.use_mock_mode = True
        else:
            logger.info(f"✅ Gemini API (HTTP) initialized. Trying models: {', '.join(self.models_to_try)}")
    
    async def analyze_quiz(self, questions: List[Dict]) -> Dict:
        """
        Analyze quiz questions and predict correct answers using AI.
        
        Args:
            questions: List of question dictionaries from parser
            
        Returns:
            Dictionary with predictions for each question
        """
        if self.use_mock_mode:
            return self._mock_analyze(questions)
        
        try:
            return self._real_analyze(questions)
        except Exception as e:
            logger.error(f"Error in real analysis: {e}. Falling back to mock mode.")
            return self._mock_analyze(questions)
    
    def _real_analyze(self, questions: List[Dict]) -> Dict:
        """Perform real analysis using Gemini HTTP API."""
        predictions = {}
        answers_options = ['A', 'B', 'C', 'D']
        all_failed = True
        
        for q in questions:
            try:
                question_num = q.get('question_number', q.get('number', 0))
                question_text = q.get('question_text', q.get('text', ''))
                answers = q.get('answers', [])
                
                # Format the question
                formatted_prompt = self._format_question(question_text, answers)
                
                response = None
                last_error = None
                
                # Try each model until one works
                for model_name in self.models_to_try:
                    try:
                        logger.debug(f"[Q{question_num}] Trying model: {model_name}")
                        
                        # Build URL - IMPORTANT: use v1beta!
                        url = f"{self.api_endpoint}/{model_name}:generateContent?key={self.api_key}"
                        
                        # Build request payload (Google's required format)
                        payload = {
                            "contents": [
                                {
                                    "parts": [
                                        {"text": formatted_prompt}
                                    ]
                                }
                            ],
                            "systemInstruction": {
                                "parts": [
                                    {"text": self.system_instruction}
                                ]
                            },
                            "generationConfig": {
                                "temperature": 0.1  # Low temperature for accuracy
                            }
                        }
                        
                        # Make HTTP POST request
                        headers = {"Content-Type": "application/json"}
                        logger.debug(f"[Q{question_num}] POST {url.replace(self.api_key, 'API_KEY_HIDDEN')}")
                        
                        http_response = requests.post(
                            url,
                            headers=headers,
                            json=payload,
                            timeout=10
                        )
                        
                        if http_response.status_code == 200:
                            response_data = http_response.json()
                            response = response_data
                            logger.info(f"✅ [Q{question_num}] Success with model: {model_name}")
                            all_failed = False
                            break
                        else:
                            error_msg = http_response.text[:200] if http_response.text else "No error details"
                            last_error = f"HTTP {http_response.status_code}: {error_msg}"
                            logger.debug(f"❌ [{model_name}] Q{question_num}: {last_error}")
                            continue
                    
                    except Exception as model_err:
                        last_error = str(model_err)
                        logger.debug(f"❌ [{model_name}] Q{question_num}: {last_error}")
                        continue
                
                # Process response
                if response:
                    try:
                        # Extract text from Google's nested response structure
                        answer_text = response["candidates"][0]["content"]["parts"][0]["text"].strip()
                        predicted_answer = self._parse_gemini_response(answer_text, answers_options)
                        
                        if predicted_answer:
                            predictions[question_num] = predicted_answer
                            logger.debug(f"Q{question_num}: Predicted answer = {predicted_answer}")
                        else:
                            predictions[question_num] = 'A'
                            logger.debug(f"Q{question_num}: No valid prediction, using 'A'")
                    except (KeyError, IndexError, TypeError) as e:
                        logger.warning(f"Q{question_num}: Failed to parse response: {e}")
                        predictions[question_num] = 'A'
                else:
                    predictions[question_num] = self._mock_single_question(question_num)
                    if last_error:
                        logger.warning(f"Q{question_num}: API failed ({last_error}), using mock")
            
            except Exception as e:
                question_num = q.get('question_number', q.get('number', 0))
                logger.error(f"Error analyzing question {question_num}: {e}")
                predictions[question_num] = self._mock_single_question(question_num)
        
        # If ALL models failed
        if all_failed and not self.use_mock_mode:
            logger.warning("⚠️  ALL AI models failed!")
            logger.warning(f"  - Models tried: {', '.join(self.models_to_try)}")
            logger.warning(f"  - API Key set: {bool(self.api_key)}")
            logger.warning(f"  - Endpoint: {self.api_endpoint}")
            logger.warning("  Check: API key validity, billing quota, network access, rate limits")
            self.use_mock_mode = True
        
        return predictions
    
    def _mock_single_question(self, question_num: int) -> str:
        """Generate mock prediction for a single question."""
        cycle = ['A', 'B', 'C', 'D']
        return cycle[(question_num - 1) % len(cycle)]
    
    def _mock_analyze(self, questions: List[Dict]) -> Dict:
        """Mock analysis for development without API key."""
        predictions = {}
        
        for i, q in enumerate(questions):
            question_num = q.get('question_number', q.get('number', i + 1))
            predictions[question_num] = self._mock_single_question(question_num)
            logger.debug(f"[MOCK] Q{question_num}: Predicted answer = {predictions[question_num]}")
        
        return predictions
    
    def _format_question(self, question_text: str, answers: List[Dict]) -> str:
        """Format question for Gemini API."""
        prompt = f"Câu hỏi: {question_text}\n\nCác đáp án:\n"
        for ans in answers:
            letter = ans.get('letter', '')
            content = ans.get('content', '')
            prompt += f"{letter}. {content}\n"
        
        return prompt
    
    def _parse_gemini_response(self, response_text: str, valid_options: List[str]) -> Optional[str]:
        """Parse Gemini response to extract answer letter."""
        # Clean response
        response_text = response_text.strip().upper()
        
        # Look for first valid letter
        for char in response_text:
            if char in valid_options:
                return char
        
        # If no valid letter found, return None
        return None


# Global service instance
_gemini_service = None


def get_gemini_service() -> GeminiService:
    """Get or create Gemini service instance."""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service


def analyze_quiz_with_ai(questions: List[Dict]) -> Dict:
    """Convenience function to analyze quiz."""
    service = get_gemini_service()
    return service.analyze_quiz(questions)
